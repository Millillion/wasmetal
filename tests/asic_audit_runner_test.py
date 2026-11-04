#!/usr/bin/env python3
"""An aborted audit must not publish a previous run's success."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import audit_asic


class AuditFailure(unittest.TestCase):
    def test_failed_setup_invalidates_only_the_requested_report(self):
        for loadable in [False,True]:
            with self.subTest(loadable=loadable),tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);(root/'reports').mkdir()
                names=['asic-audit.json','asic-loadable-audit.json']
                for name in names:(root/'reports'/name).write_text('{"status":"elaborated_and_audited"}\n')
                selected=root/'reports'/names[int(loadable)]
                other=root/'reports'/names[1-int(loadable)]
                previous=other.read_bytes()
                with patch.object(audit_asic,'ROOT',root),patch.object(audit_asic,'load_profile',side_effect=ValueError('invalid profile')),patch.object(sys,'argv',['audit_asic.py']+(['--loadable'] if loadable else [])):
                    with self.assertRaisesRegex(ValueError,'invalid profile'):audit_asic.main()
                self.assertFalse(selected.exists())
                self.assertEqual(other.read_bytes(),previous)


if __name__=='__main__':unittest.main()
