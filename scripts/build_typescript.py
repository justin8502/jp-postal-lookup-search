import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "json")
DESTINATION = os.path.join(
  ROOT, "packages", "typescript", "src", "data"
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

TYPESCRIPT_PACKAGE = os.path.join(ROOT, "packages", "typescript")

is_windows = os.name == "nt"
npm = "npm.cmd" if is_windows else "npm"

# Clean previous build
if is_windows:
  subprocess.run(
    ["cmd", "/c", "if exist dist rmdir /s /q dist"],
    cwd=TYPESCRIPT_PACKAGE,
    check=True,
  )
else:
  subprocess.run(
    ["rm", "-rf", "dist"],
    cwd=TYPESCRIPT_PACKAGE,
    check=True,
  )

# Build npm package
subprocess.run(
  [npm, "run", "build"],
  cwd=TYPESCRIPT_PACKAGE,
  check=True,
  shell=is_windows,
)

# Pack npm package
subprocess.run(
  [npm, "pack"],
  cwd=TYPESCRIPT_PACKAGE,
  check=True,
  shell=is_windows,
)
