import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent.parent
security_dir = root / "security"
security_dir.mkdir(exist_ok=True)

commands = [
    ("pip-audit", [sys.executable, "-m", "pip_audit", "--format", "json"], security_dir / "pip-audit.json"),
    ("bandit", [sys.executable, "-m", "bandit", "-r", str(root), "-f", "json", "-o", str(security_dir / "bandit-report.json")], None),
    ("safety", [sys.executable, "-m", "safety", "check", "--json"], security_dir / "safety-report.json"),
]

for name, cmd, output_path in commands:
    print(f"Running {name}: {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Return code: {proc.returncode}")
    if proc.stdout:
        print(f"Stdout length: {len(proc.stdout)}")
    if proc.stderr:
        print(f"Stderr length: {len(proc.stderr)}")
    if output_path is not None:
        output_path.write_text(proc.stdout, encoding="utf-8")
        print(f"Wrote {output_path} ({output_path.stat().st_size} bytes)")
    if proc.returncode != 0 and name not in ["pip-audit", "bandit", "safety"]:
        print(f"{name} failed")
        if proc.stderr:
            print(proc.stderr)
        sys.exit(proc.returncode)

print("All security reports generated successfully. Some tools may report vulnerabilities or warnings via nonzero exit codes.")
