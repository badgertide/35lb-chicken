import subprocess
import shutil

def run(cmd):
    print(">", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)

def run_capture(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout

def time_to_seconds(t: str) -> float:
    """converts 0:01:00.500 to 60.5."""
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

def check_dependency(name):
    """Checks if an executable exists on the system."""
    path = shutil.which(name)
    if path is None:
        print(f"Error: '{name}' is not installed or not in PATH.")
        return False
    return True