# AWSAD2CLI
Problem (either/or):
- You have SAML federation with MS AAD (myapps), Authenticator based MFA for console access but getting the SAMLResponse is too time consuming and expires every hour.
- You have a console login but you want to be able to use the AWS CLI. You are a Cloud Administrator and you have configured AWS Managed AD for console logins but your developers need CLI access. You don't want to create IAM users with access keys as this negates the reason to have AD based logins. There is no easy method to create AWS keys for a console based Managed AD user!

This tool automated console login and extraction of AWS keys using AWS cloud console. AWSAD2CLI converts AWS AD and MS AAD console logins to CLI credentials.
For AWS AD access CloudShell is used to assume an additional CLI role. AWS CLI SSO mode uses IAM identity center to login using a IDC based account.

Different to some tools AWSAD2CLI uses Selenium which is capable of a more stable user experience in case of changes to the login process.

### Pre requisites
- Chrome has to be installed on the local machine (see below)
- For AWS AD SSO you need the ARN of a role to assume.
- You need the login URL for your console based access (i.e. myapp.awsapps.com/console)

### Installing Chome (if needed) on RHEL / Amazon Linux
Use apt for Debian based systems.
```
cd /tmp
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install ./google-chrome-stable_current_x86_64.rpm
sudo ln -s /usr/bin/google-chrome-stable /usr/bin/chromium
```

## Installation
AWSAD2CLI can be installed from Pypi (pip) or by cloning this repository.

### Pip installation
```
pip install awsad2cli
```
### Running from a cloned repository
```
cd AWSAD2CLI
python setup.py install
```

## Usage
```
$ awsad2cli --help
usage: awsad2cli [-h] [-o OUTPUT] -u URL [-r ROLE] [--ad] [-U USERNAME] [-p PROFILE] [-s SECONDS] [-v] [--cache-location CACHE_LOC] [--no-cache]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT             Output format - json [default], profile
  -u URL                Login URL ('https://myapp.awsapps.com/console/
  -r ROLE               ARN of role to assume
  --ad
  -U USERNAME           Username (will be cached in $PWD/.username) - delete this if needed
  -p PROFILE            AWS Config profile to create / update, defaults to the username
  -s SECONDS            Role duration in seconds (limited by the max session duration (not checked): default 3600
  -v                    Show browser window and debug info for selenium.
  --cache-location CACHE_LOC
                        Location of cached chrome data (NOTE: will contain AAD cookies. Disabling this option will require re-authentication each usage)
  --no-cache            Disable Caching of chrome data..

```
