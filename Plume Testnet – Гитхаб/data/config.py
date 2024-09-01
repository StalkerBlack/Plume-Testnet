import os
import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, 'abis')

CHECK_IN_ABI = os.path.join(ABIS_DIR, 'check_in.json')

FAUCET = os.path.join(ABIS_DIR, 'faucet.json')

VOTE = os.path.join(ABIS_DIR, 'vote.json')

CULTURED = os.path.join(ABIS_DIR, 'cultured.json')








