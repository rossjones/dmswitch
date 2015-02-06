# dmswitch

dmswitch is a very simple program for checking that cron jobs run. You can append it to the crontab line as follows and it will record the time that the process finished.

```
10 0 * * * some-task && dmswitch --switch sometask
```

As a separate task, and to find all processes that didn't run in the last 24 hours you can do

```
0 0 * * * dmswitch --check 24 
```

Any tasks that haven't run (or rather completed) in the last 24 hours will be sent in an email to the configured email addresses.

## Installation

1. Create a virtualenv and activate it
2. ```git clone git@github.com:rossjones/dmswitch.git```
3. python setup.py install
4. Create a dms.ini file in the home directory of the user which dmswitch will run as. It should look  
   like the one below.

## Config

1. Copy the dms.ini.sample file to the home directory of the user who will run the switch, as dms.ini
2. Change the email addresses (comma-separated) who will receive an email on failures.
3. Change the smtp settings to point to your SMTP server.

