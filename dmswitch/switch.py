from datetime import datetime, timedelta
import os
from string import Template
import time

FOLDER = "~/.dms"

def ensure_config_folder():
    folder = os.path.expanduser(FOLDER)
    if not os.path.exists(folder):
        os.mkdir(folder)

def now_to_timestamp():
    return time.mktime( datetime.now().timetuple() )

def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

def build_template(template, fails, hours):
    jobs = [""]
    for what, when in fails:
        jobs.append( "\t'{}' - last ran {}".format(what, when))

    jobstring = "\n ".join(jobs)

    result = Template(template).substitute({'hours': hours, 'jobs': jobstring})
    return "".join([result, "\n\n"])

class Switch(object):

    def __init__(self, name):
        self.name = name
        ensure_config_folder()

    def process(self):
        data = now_to_timestamp()
        path = os.path.expanduser(os.path.join(FOLDER, self.name))
        with open(path, "w") as f:
            f.write(str(data))

class Check(object):

    def __init__(self, hours):
        self.hours = hours
        self.seconds = self.hours * 60 * 60
        ensure_config_folder()

    def process(self):
        full_path = os.path.expanduser(FOLDER)
        filenames = os.listdir(full_path)
        now = datetime.now()

        for filename in filenames:
            path = os.path.join(full_path, filename)
            with open(path, 'r') as f:
                try:
                    timestamp = float(f.read())
                    the_time_was = timestamp_to_datetime(timestamp)
                    delta = now - the_time_was
                    if delta.total_seconds() > self.seconds:
                        yield (filename, the_time_was)
                except Exception, e:
                    # TODO: Do something with malformed file. Perhaps log it
                    # and delete it?
                    continue
