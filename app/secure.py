"""Runtime secrets are generated per installation; never handed to the learner."""
import os
from pathlib import Path

def secret(name):
    directory=os.environ.get('LAB_SECRET_DIR')
    if directory:
        return (Path(directory)/(name+'.key')).read_text().strip()
    return os.environ.get('LAB_CONTROL_KEY','synthetic-control-key-not-for-production')
