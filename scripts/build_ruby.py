import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "json")
DESTINATION = os.path.join(
  ROOT, "packages", "ruby", "lib", "jp_postal_lookup_search", "data"
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
