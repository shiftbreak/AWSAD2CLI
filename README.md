# AWSAD2CLI
A tool to convert AWS AD based login to an assumed CLI role using the AWS Console Cloud Shell and selenium

This tool can be run from the CLI however Chrome has to be installed on the local machine.

Usage:
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
```
