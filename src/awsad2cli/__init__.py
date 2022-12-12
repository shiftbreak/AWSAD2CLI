import argparse
import configparser
import os

from .aws_login import do_aws_login


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', dest='output', type=str, default="json", help="Output format - json [default], profile")
    parser.add_argument('-u', dest='url', required=True, type=str,
                        help="Login URL ('https://myapp.awsapps.com/console/")
    parser.add_argument('-r', dest='role', required=True, type=str, help="ARN of role to assume")
    parser.add_argument('-U', dest='username', type=str,
                        help="Username (will be cached in $PWD/.username) - delete this if needed")
    parser.add_argument('-p', dest='profile', type=str,
                        help="AWS Config profile to create / update, defaults to the username")
    parser.add_argument('-s', dest='seconds', type=int, default=3600, required=False,
                        help="Role duration in seconds (limited by the max session duration (not checked): default 3600")
    parser.add_argument('-v', dest='verbose', action="store_true",
                        help="Show browser window and debug info for selenium.")
    args = parser.parse_args()

    url = args.url
    role = args.role

    key_id, key_secret, session_token, username = do_aws_login(
        url,
        role,
        username=args.username,
        verbose=args.verbose,
        seconds=args.seconds
    )
    print("Captured temporary credentials, attempting to assume role")
    Config = configparser.ConfigParser()
    creds_file = os.path.expanduser('~/.aws/credentials')
    Config.read(creds_file)

    if args.profile is None or args.profile == "":
        profile = username
    else:
        profile = args.profile

    if not Config.has_section(profile):
        Config.add_section(profile)
    Config.set(profile, 'aws_access_key_id', key_id)
    Config.set(profile, 'aws_secret_access_key', key_secret)
    Config.set(profile, 'aws_session_token', session_token)
    with open(creds_file, 'w') as configfile:
        Config.write(configfile)

    print(
        f"Created profile in {creds_file} with name: {profile}\n"
        f"To use it run 'export AWS_PROFILE={profile}' in a terminal window")


if __name__ == "__main__.py":
    main()
