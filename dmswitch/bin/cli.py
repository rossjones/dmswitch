import ConfigParser
import os
import argparse
import sys

from dmswitch.switch import (Switch, Check, build_template)

def main():
    """ Entry point for the console app """
    parser = argparse.ArgumentParser()
    parser.add_argument("--switch", type=str, help="Trigger the switch NAME!")
    parser.add_argument("--check", type=int,
        help="Check the switches that haven't run in last CHECK hours")
    args = parser.parse_args()

    if not args.switch and not args.check:
        print "One of --switch or --check are required"
        sys.exit(1)

    # If we have a config file, we should load it.  If we haven't, then
    # we can't work out who to send the email to. If we can't send the
    # email .. well, you get the idea.
    config_path = os.path.expanduser("~/dms.ini")
    if not os.path.exists(config_path):
        print "Unable to find config at {}".format(config_path)
        sys.exit(1)

    config = ConfigParser.ConfigParser()
    config.read(config_path)

    notify = [n.strip() for n in config.get('dms', 'notify').split(',')]
    template = config.get('dms', 'template')

    if args.switch:
        switch = Switch(args.switch)
        switch.process()

    if args.check:
        fails = []
        check = Check(args.check)
        for (name, when) in check.process():
            fails.append((name, when,))

        if fails:
            print "Notifying {}".format(notify)
            print build_template(template, fails, args.check)