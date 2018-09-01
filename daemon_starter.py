#!/home/evan/anaconda3/bin/python
from daemon_test import DaemonRunner, TestApp
import os

def _start_one():
    dr = DaemonRunner(TestApp(), '/home/evan/daemon_out/outfile.log')
    dr.start()

if __name__ == '__main__':
    _start_one()