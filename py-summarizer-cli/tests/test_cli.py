import os
import unittest
import subprocess
import sys
from pathlib import Path

class TestCLI(unittest.TestCase):
    def test_cli_runs(self):
        proj_root = Path(__file__).resolve().parents[1]
        sample = proj_root / "tests" / "fixtures" / "sample.txt"
        outdir = proj_root / "out_test"
        if outdir.exists():
            for p in outdir.iterdir():
                p.unlink()
            outdir.rmdir()

        cmd = [sys.executable, str(proj_root / "src" / "cli_tool" / "main.py"),
               "--input", str(sample), "--outdir", str(outdir)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue((outdir / "sample_summary.json").exists())
        self.assertTrue((outdir / "sample_insights.csv").exists())

if __name__ == "__main__":
    unittest.main()
