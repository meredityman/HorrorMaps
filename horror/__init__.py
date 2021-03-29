import json
import os

ROOT = os.path.dirname(__file__)

cue_sheet         = json.load(open(os.path.join(ROOT, "config/cues.json"    ), "r"))
network_settings  = json.load(open(os.path.join(ROOT, "config/devices.json" ), "r"))

from .regex_helper import RegexCounter
from .cuemanager   import send_cue, test_all_cues
