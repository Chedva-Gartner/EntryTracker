import sys
import subprocess
from pathlib import Path

version_file = Path("VERSION")

if not version_file.exists():
    print(f"::error::File not found: {version_file}. Please ensure it exists in the root directory.")
    sys.exit(1)

try:
    content = version_file.read_text().strip()
    if not content:
        raise ValueError("VERSION file is empty")
    
    major, minor, patch = map(int, content.split("."))

except (ValueError, IndexError) as e:
    print(f"::error::Invalid version format in {version_file}. Expected x.y.z (e.g., 1.0.0). Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"::error::An unexpected error occurred while reading {version_file}: {e}")
    sys.exit(1)

def get_version_type():
    try:
        result = subprocess.run(["git", "log", "-1", "--pretty=%B"], capture_output=True, text=True, check=True)
        message = result.stdout.lower()

        if "breaking change" in message:
            return "major"
        elif "feat" in message:
            return "minor"
        elif "fix" in message:
            return "patch"
        else:
            return "patch"
    except subprocess.CalledProcessError:
        print("::warning::Could not get git log. Defaulting to patch bump.")
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

try:
    version_file.write_text(new_version)
    print(f"Bumped version: {new_version}")
except Exception as e:
    print(f"::error::Could not write to {version_file}: {e}")
    sys.exit(1)
