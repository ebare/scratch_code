#!/home/evan/anaconda3/bin/python

from daemon import DaemonContext
import os
import time
import sys
import argparse
import fnmatch
import signal
import subprocess

PID_DIR = '/home/evan/daemon_pids'

class TestApp(object):

    def __init__(self):
        pass

    def run(self):
        self.pid = str(os.getpid())
        with open(os.path.join(PID_DIR, str(self.pid) + '.pid'), 'w') as pidfile:
            pidfile.write(self.pid)
        while True:
            print('Running process ID: {0}'.format(self.pid))
            time.sleep(3)

class DaemonRunner(object):

    def __init__(self, app, outpath=None):
        self.daemon_context = DaemonContext()
        self.app = app
        if outpath:
            self.daemon_context.stdout = open(outpath, 'a')

    def start(self):
        self.daemon_context.open()
        self.app.run()
        status()

def pid_exists(pid):
    pid = int(pid)
    try:
        os.kill(pid, 0)
    except:
        return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['start', 'stop', 'status'])
    parser.add_argument('-n', type=int, dest='num_daemons', default=1)
    args = parser.parse_args()

    if args.cmd == 'start':
        start(args.num_daemons)
    if args.cmd == 'stop':
        stop()
    if args.cmd == 'status':
        status()

def start(num_daemons=1):
    print('Starting {0} daemons'.format(num_daemons))
    for i in range(num_daemons):
        subprocess.call('/home/evan/code/daemon_starter.py')
    while count_active() != num_daemons:
        time.sleep(0.1)
    status()

def stop():
    pid_files = get_pid_files()
    if len(pid_files) == 0:
        print('No running daemons')
        return
    for pidfile in pid_files:
        pid = pidfile.split('.')[0]
        if pid_exists(pid):
            os.kill(int(pid), signal.SIGTERM)
            print('Process terminated: ' + str(pid))
        else:
            print('Cleaning up stale process: ' + str(pid))
        os.remove(os.path.join(PID_DIR, pidfile))

def count_active():
    active = 0
    for pid in get_pid_files():
        if pid_exists(pid.split('.')[0]):
            active = active + 1
    return active

def status():
    pid_files = get_pid_files()
    if len(pid_files) == 0:
        print('No running daemons')
        return
    for pidfile in pid_files:
        pid = pidfile.split('.')[0]
        if pid_exists(pid):
            print('Running : ' + str(pid))
        else:
            print('Stale process: ' + str(pid))

def get_pid_files():
    return [f for f in filter(lambda x: fnmatch.fnmatch(x, '*.pid'), os.listdir(PID_DIR))]

if __name__ == '__main__':
    main()