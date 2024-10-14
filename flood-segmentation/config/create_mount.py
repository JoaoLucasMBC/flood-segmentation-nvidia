import json
import os
from dotenv import load_dotenv

load_dotenv()

mounts_file = os.path.expanduser("~/.tao_mounts.json")

drive_map = {
    "Mounts": [
            # Mapping the data directory
            {
                "source": os.path.join(os.environ["LOCAL_PROJECT_DIR"], f"v{os.environ['VERSION']}"),
                "destination": "/workspace/tao-experiments"
            },
            # Mapping the specs directory.
            {
                "source": os.path.join(os.environ["LOCAL_SPECS_DIR"], f"v{os.environ['VERSION']}"),
                "destination": os.environ["TAO_SPECS_DIR"]
            },
            # Mapping the data directory.
            {
                "source": os.path.join(os.environ["LOCAL_DATA_DIR"], f"v{os.environ['VERSION']}"),
                "destination": os.environ["TAO_DATA_DIR"]
            },
        ],
    "DockerOptions": {
        "user": "{}:{}".format(os.getuid(), os.getgid())
    }
}

# writing the mounts file
with open(mounts_file, "w") as mfile:
    json.dump(drive_map, mfile, indent=4)
