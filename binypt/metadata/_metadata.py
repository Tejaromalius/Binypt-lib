import os
import json

from subprocess import getoutput


_METADATA_PATH = os.path.join(os.path.dirname(__file__), "metadata.json")
_METADATA_FILE_HASH = \
    "521232f528eca6fab4916d7b317b951d46a48101ff1febcf0be312564d3fd372"

current_metadata_file_hash = getoutput(f"sha256sum {_METADATA_PATH}").split()
if current_metadata_file_hash[0] != _METADATA_FILE_HASH:
    raise FileNotFoundError(f"`{_METADATA_PATH}` is not valid!")

with open(_METADATA_PATH, "r") as file:
    metadata = json.load(file)
