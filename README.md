# AWSAD2CLI
Problem? You have a console login but you want to be able to use the AWS CLI. You are a Cloud Administrator and you have configured AWS Managed AD for console logins but your developers need CLI access. You don't want to create IAM users with access keys as this negates the reason to have AD based logins. There is no easy method to create AWS keys for a console based Managed AD user!

Solution! AWSAD2CLI - automated console login and extraction of AWS keys using AWS cloud console. AWSAD2CLI converts AWS AD based login to an assumed CLI role using the AWS Console Cloud Shell and selenium. AWS CLI SSO mode uses IAM identity center to login using a IDC based account. SAML based logins.

### Pre requisites
- Chrome has to be installed on the local machine (see below)
- You need the ARN of a role to assume
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
awsad2cli -h
usage: awsad2cli [-h] [-o OUTPUT] -u URL -r ROLE [-U USERNAME] [-p PROFILE] [-v]

optional arguments:
  -h, --help   show this help message and exit
  -o OUTPUT    Output format - json [default], profile
  -u URL       Login URL ('https://myapp.awsapps.com/console/
  -r ROLE      ARN of role to assume
  -U USERNAME  Username (will be cached in $PWD/.username) - delete this if needed
  -p PROFILE   AWS Config profile to create / update, defaults to the username
  -v           Show browser window and debug info for selenium.

export AWS_PROFILE <your_profile_name>
aws sts get-caller-identity
```
