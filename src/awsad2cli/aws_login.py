
import time
from getpass import getpass
from json import JSONDecodeError
from os.path import exists
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import keyring

def get_username() -> str:
    username = keyring.get_password('awsad2cli', 'current_username')
    if username is not None:
        return username

    username = input("Username: ")
    keyring.set_password('awsad2cli', 'current_username', username)

    return username


def get_creds(username: str, add_mfa: bool = False) -> Tuple[str, str]:

    password = keyring.get_password('awsad2cli', username)

    if password is None:
        password = getpass(f"Password for {username}: ")
        keyring.set_password('awsad2cli', username, password)
    mfa = None
    if add_mfa:
        mfa = getpass(f"MFA code for {username}: ")
    return password, mfa


def do_aws_login(final_url: str, role_arn: str, username: Optional[str] = None, verbose: bool = False, seconds: int = 3600) -> Tuple[
    str, str, str, str]:
    chrome_options = Options()

    if seconds > 3600:
        print("Cannot assume role greater than 1 hour due to role chaining restriction.")
        exit(1)

    if username is None:
        username = get_username()
        print(f"Logging in with username: {username}")
    else:
        print(f"Storing default username {username} in system keyring")
        keyring.set_password('awsad2cli', 'current_username', username)

    if not verbose:
        # Run in headless mode - allows tool to run on the CLI
        chrome_options.add_argument("--headless")

        # Disable verbose debug logging
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                "like Gecko) Chrome/107.0.5304.107 Safari/537.36")

    # noinspection PyArgumentList
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(final_url)

    USERNAME_FIELD = (By.ID, "wdc_username")
    PASSWORDFIELD = (By.ID, "wdc_password")
    NEXTBUTTON = (By.ID, "wdc_login_button")
    MFANUM = (By.ID, "wdc_mfa")

    # Do automated login
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(USERNAME_FIELD)).send_keys(username)

    try:
        driver.find_element(By.ID, 'wdc_mfa')
        add_mfa = True
    except NoSuchElementException:
        add_mfa = False

    password, mfa = get_creds(username, add_mfa=add_mfa)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(password)
    if mfa is not None:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(MFANUM)).send_keys(mfa)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
    print("Attempting login with supplied credentials")
    try:
        WebDriverWait(driver, 20).until(EC.url_contains("/console/home"))
    except TimeoutException:
        print("Login mail have failed - check your credentails or run in verbose mode")
        exit(1)
    print("Opening cloud shell")
    domain = urlparse(driver.current_url).netloc
    cloudshell_url = f"https://{domain}/cloudshell/home"
    driver.get(cloudshell_url)

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "ace_text-input")))
    print("CloudShell loaded")
    a = driver.find_element(by=By.CLASS_NAME, value='ace_text-input')
    actionChains = ActionChains(driver)
    actionChains.move_to_element(a)

    blinking = False
    while not blinking:
        for e in driver.find_elements(by=By.CLASS_NAME, value='ace_line'):
            try:
                if "cloudshell-user" in e.text:
                    blinking = True
            except:
                pass

    time.sleep(5)
    role_cmd = f"aws sts assume-role --role-session-name {username} --role-arn {role_arn} --duration-seconds {seconds}"
    a.send_keys(role_cmd)
    a.send_keys(Keys.ENTER)
    time.sleep(5)
    text = []
    started = False
    ended = False
    unformatted_text = ""
    for e in driver.find_elements(by=By.CLASS_NAME, value='ace_line'):
        if e.text is not None:
            t = e.text.strip()
            unformatted_text += t + "\n"
            if t.startswith("{"):
                started = True

            if t.startswith("[cloud") and started:
                ended = True
            if started and not ended:
                text.append(t)
    if verbose:
        input("Press Enter to continue...")
    tt = "".join(text).strip()
    try:
        creds = json.loads(tt)
        c = creds['Credentials']
        key_id = c['AccessKeyId']
        key_secret = c['SecretAccessKey']
        session_token = c['SessionToken']
        exp = c['Expiration']
        exp_str = datetime.fromisoformat(exp).astimezone().isoformat()
        print(f"Creds expire at {exp_str}")

        return key_id, key_secret, session_token, username
    except JSONDecodeError:
        print(f"Error thrown when assumeing role with command: {role_cmd}")
        print(f"Here is the console output: \n{unformatted_text}")
        exit(1)
