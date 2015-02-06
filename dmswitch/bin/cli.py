import ConfigParser
import os
import argparse
import smtplib
import sys

from dmswitch.switch import (Switch, Check, build_template)

def _get_smtp_connection(config):
    server = config.get('smtp', 'server', 'localhost')
    port = config.getint('smtp', 'port') or 25
    username = config.get('smtp', 'username')
    password = config.get('smtp', 'password')
    use_ssl =  config.getboolean('smtp', 'ssl')

    if use_ssl:
        conn = smtplib.SMTP_SSL(server, port)
    else:
        conn = smtplib.SMTP(server, port)

    return conn

def send_email(notify, config, msg):
    from_address = config.get('dms', 'from')
    subject = config.get('dms', 'subject')

    try:
        conn = _get_smtp_connection(config)
        conn.sendmail(from_address, notify, msg)
        conn.quit()
    except Exception, e:
        print e


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
            content = build_template(template, fails, args.check)

            print "Notifying {}".format(notify)
            print content

            send_email(notify, config, content)
