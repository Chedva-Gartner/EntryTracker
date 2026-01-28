import sys
import re
from pathlib import Path
import subprocess

version_file = Path("VERSION")

with open(version_file, "r") as f:
    major, minor, patch = map(int, f.read().strip().split("."))


def get_version_type():
    result = subprocess.run(["git", "log", "-1", "--pretty=%B"], capture_output=True, text=True)
    message = result.stdout.lower()

    if "breaking change" in message:
        return "major"
    elif "feat" in message:
        return "minor"
    elif "fix" in message:
        return "patch"
    else:
        return "patch" 

version_type = get_version_type()

if version_type == "major":
    major += 1
    minor = 0
    patch = 0
elif version_type == "minor":
    minor += 1
    patch = 0
elif version_type == "patch":
    patch += 1

new_version = f"{major}.{minor}.{patch}"

with open(version_file, "w") as f:
    f.write(new_version)

print(f"Bumped version: {new_version}")
