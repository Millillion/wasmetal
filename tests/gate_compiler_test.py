"""A changed compiler configuration must never reuse stale model objects."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build_gate_sim


class CompilerRebuild(unittest.TestCase):
    def test_portable_model_does_not_require_the_build_workers_cpu(self):
        portable = build_gate_sim.compilation(True,portable=True)
        self.assertTrue(portable['portable'])
        self.assertNotIn('-march=native',portable['cflags'])
        self.assertIn('-O3',portable['cflags'])
        self.assertIn('-march=native',build_gate_sim.compilation(True)['cflags'])

    def test_changed_flags_change_the_executable_without_a_source_edit(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            objects = directory / "obj"
            objects.mkdir()
            source = objects / "model.cpp"
            source.write_text("#include <cstdio>\nint main(){std::printf(\"%d\\n\",MODEL_VALUE);}\n")
            original = source.read_bytes()
            (objects / "Vwasmetal_core.mk").write_text(
                "Vwasmetal_core: model.o\n"
                "\t$(LINK) model.o -o $@\n"
                "model.o: model.cpp\n"
                "\t$(CXX) $(VM_USER_CFLAGS) -c model.cpp -o $@\n"
            )
            for expected in (41, 42):
                options = build_gate_sim.compilation(False)
                options["cflags"] += f" -DMODEL_VALUE={expected}"
                build_gate_sim.compile_model(directory, options, 1, True)
                actual = subprocess.check_output([str(objects / "Vwasmetal_core")], text=True).strip()
                self.assertEqual(actual, str(expected))
                self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
