import os
import json

from subprocess import getoutput


_METADATA_PATH = os.path.join(os.path.dirname(__file__), "metadata.json")
_METADATA_FILE_HASH = \
    "942a1e5cb78e0b299198b567041b257c8a6e6e9ab21a07d34f3898af6a0b5aa6"

current_metadata_file_hash = getoutput(f"sha256sum {_METADATA_PATH}").split()
if current_metadata_file_hash[0] != _METADATA_FILE_HASH:
    raise FileNotFoundError(f"`{_METADATA_PATH}` is not valid!")

with open(_METADATA_PATH, "r") as file:
    metadata = json.load(file)
