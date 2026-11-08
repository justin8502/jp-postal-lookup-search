import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCE = os.path.join(ROOT, "json")
DESTINATION = os.path.join(
    ROOT, "packages", "python", "src", "jp_postal_lookup_search", "data"
)

files = [
  "postal_code_lookup.json",
  "address_lookup.json",
]

os.makedirs(DESTINATION, exist_ok=True)

for filename in files:
  source_file = os.path.join(SOURCE, filename)
  destination_file = os.path.join(DESTINATION, filename)

  with open(source_file, "rb") as src:
    with open(destination_file, "wb") as dst:
      dst.write(src.read())

PYTHON_PACKAGE = os.path.join(ROOT, "packages", "python")

subprocess.run(
    [sys.executable, "-m", "build", "-v"],
    cwd=PYTHON_PACKAGE,
    check=True,
)