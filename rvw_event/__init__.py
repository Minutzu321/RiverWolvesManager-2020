from .general import RVWGeneral
from .particip import RVWPartikip_Sedinta, RVWNuPartikip_Sedinta, RVWPrezent
from .event import RVWEvent

events = []

def init():
    events.append(RVWGeneral())
    events.append(RVWPartikip_Sedinta())
    events.append(RVWNuPartikip_Sedinta())
    events.append(RVWPrezent())

def execute(cmd, args = []):
    if len(events) == 0:
        init()
    for event in events:
        if event.cmd.lower() == cmd.lower():
            return event.execute(args)
    return None
