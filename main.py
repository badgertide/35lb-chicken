import shutil
import sys
import os

def checkDependency(name):
    path = shutil.which(name)
    if path is None:
        print(f"Error: '{name}' is not installed or not in PATH.")
        return False
    return True

def getTargetDir():
    if len(sys.argv) == 1: #no args
        return os.getcwd()
    elif len(sys.argv) == 2: #one arg
        return os.path.abspath(sys.argv[1])
    else:
        print("Usage: py main.py [DIRECTORY]")

def main():
    # check for dependencies
    has_ffmpeg = checkDependency("ffmpeg")
    has_ffprobe = checkDependency("ffprobe")
    if not (has_ffmpeg and has_ffprobe):
        sys.exit(1)

    target_dir = getTargetDir()
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory")
        sys.exit(1)

    example_file = os.path.join(target_dir, "example.txt")
    print(example_file)

if __name__ == "__main__":
    main()