#!/usr/bin/env python3
"""Prove the startup-system runner retires children on exit, failure and timeout."""
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from check_memory_startup_system import ROOT,owned_run

CHILD='''import signal,time,sys
from pathlib import Path
signal.signal(signal.SIGINT,signal.SIG_IGN)
signal.signal(signal.SIGTERM,signal.SIG_IGN)
heartbeat=Path(sys.argv[1])
while True:
    heartbeat.write_text(str(time.monotonic_ns()))
    time.sleep(0.01)
'''
PARENT='''import os,signal,subprocess,sys,time
from pathlib import Path
signal.signal(signal.SIGINT,signal.SIG_IGN)
signal.signal(signal.SIGTERM,signal.SIG_IGN)
Path(sys.argv[1]).write_text(str(os.getpid()))
child=subprocess.Popen([sys.executable,'-c',sys.argv[3],sys.argv[2]])
deadline=time.monotonic()+10
while not Path(sys.argv[2]).exists():
    if time.monotonic()>deadline:raise RuntimeError('child did not start')
    time.sleep(0.01)
if sys.argv[4]=='timeout':time.sleep(60)
else:sys.exit(int(sys.argv[4]))
'''

class StartupRunner(unittest.TestCase):
    def exercise(self,mode):
        with tempfile.TemporaryDirectory(prefix='startup-runner-',dir=ROOT/'build') as temporary:
            directory=Path(temporary);pidfile=directory/'parent.pid';heartbeat=directory/'heartbeat'
            command=[sys.executable,'-c',PARENT,str(pidfile),str(heartbeat),CHILD,mode]
            try:
                with (directory/'log').open('w') as log:
                    if mode=='timeout':
                        with self.assertRaises(subprocess.TimeoutExpired):owned_run(command,log,1)
                    else:self.assertEqual(owned_run(command,log,10).returncode,int(mode))
                self.assertTrue(heartbeat.exists(),'descendant never ran')
                before=heartbeat.read_bytes();time.sleep(0.2)
                self.assertEqual(heartbeat.read_bytes(),before,'descendant survived runner retirement')
            finally:
                if pidfile.exists():
                    try:
                        import os
                        os.killpg(int(pidfile.read_text()),signal.SIGKILL)
                    except ProcessLookupError:pass
    def test_success_retires_descendant(self):self.exercise('0')
    def test_failure_retires_descendant(self):self.exercise('7')
    def test_timeout_retires_descendant(self):self.exercise('timeout')

if __name__=='__main__':unittest.main()
