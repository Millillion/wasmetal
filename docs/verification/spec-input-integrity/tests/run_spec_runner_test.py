"""Check that a slow or silent simulator cannot turn a timeout into a pass."""
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import run_spec


class RunnerTimeout(unittest.TestCase):
    def test_invalid_timeout_does_not_launch_a_simulator(self):
        for timeout in (0, -1):
            with self.subTest(timeout=timeout), patch.object(run_spec.subprocess, "Popen") as launch:
                with self.assertRaises(ValueError):
                    run_spec.RTL(response_timeout=timeout)
                launch.assert_not_called()

    def test_silent_simulator_is_terminated_and_reported_as_execution_error(self):
        with tempfile.TemporaryDirectory() as directory:
            simulator = Path(directory) / "silent-simulator"
            simulator.write_text(f"#!{sys.executable}\nimport time\ntime.sleep(30)\n")
            simulator.chmod(0o755)
            real_popen = subprocess.Popen
            processes = []

            def launch(*args, **kwargs):
                process = real_popen(*args, **kwargs)
                processes.append(process)
                return process

            started = time.monotonic()
            try:
                with patch.object(run_spec.subprocess, "Popen", side_effect=launch):
                    with self.assertRaisesRegex(run_spec.ExecutionError, "TIMEOUT.*1 seconds"):
                        run_spec.RTL(simulator=simulator, response_timeout=1)
                self.assertEqual(len(processes), 1)
                self.assertIsNotNone(processes[0].poll())
                self.assertLess(time.monotonic() - started, 10)
            finally:
                for process in processes:
                    if process.poll() is None:
                        process.kill()
                        process.wait()
                    process.stdin.close()
                    process.stdout.close()


if __name__ == "__main__":
    unittest.main()
