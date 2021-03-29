from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
import time
import uuid
import json
import os

from . import cue_sheet

osc_channels = {}
osc_startup()

def send_cue(req_cue):
    if req_cue not in cue_sheet["cues"]:
        print(f"Cue '{req_cue}' not found.")

    for target in cue_sheet["targets"].values():
        ip   = target["ip"]
        cues = target["cues"]

        if req_cue in cues:
            cue = cues[req_cue]

            if not cue: 
                continue

            port = cue["port"]

            if (ip, port) not in osc_channels:
                client_uuid = str(uuid.uuid4())
                osc_udp_client(ip, port, client_uuid)
            else:
                client_uuid = osc_channels[(ip, port)]

            addr = cue["addr"]
            data = cue["data"]

            msg = oscbuildparse.OSCMessage(addr, None, data)
            print(msg)
            osc_send(msg, client_uuid)

    osc_process()


def test_all_cues():
    for cue in cue_sheet["cues"]:
        input(f"Press enter to send '{cue}'")
        send_cue(cue)