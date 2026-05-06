import subprocess
import webbrowser
import sys
from pathlib import Path

result = subprocess.run([sys.executable, "-m", "coverage", "html"])

if result.returncode == 0:
    subprocess.run([sys.executable, "-m", "coverage", "report", "--show-missing"])
    report = Path("htmlcov/index.html").resolve()
    webbrowser.open(report.as_uri())