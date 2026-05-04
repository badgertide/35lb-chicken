import subprocess
import shutil
import base64
import json5

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

def replace_element_with_list(source, insert, index):
    """replace an element in a source list with a list
    used for breaking up one element into many elements"""
    return source[:index] + insert + source[index+1:]

def print_to_log(log, obj=None):
    print(log)
    if obj:
        base64str = json5.dumps(obj, separators=(',', ':')).encode()
        print(f"b64: {base64.b64encode(base64str).decode()}")