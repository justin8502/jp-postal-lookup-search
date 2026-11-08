import json
from importlib.resources import files

postal_code_map = json.loads(
  files(__package__).joinpath("data/postal_code_lookup.json").read_text(encoding="utf-8")
)

address_map = json.loads(
  files(__package__).joinpath("data/address_lookup.json").read_text(encoding="utf-8")
)
