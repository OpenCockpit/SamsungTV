# Copyright (C) 2026 by xcentaurix

import os

from Components.config import config, ConfigSelection
from Components.Harddisk import harddiskmanager

from .Variables import USER_AGENT


# --- Data folder management -----------------------------------------------

_data_folder = ""


def getDataFolder():
    return _data_folder


def _getMountChoices():
    choices = []
    for p in harddiskmanager.getMountedPartitions():
        if os.path.exists(p.mountpoint):
            d = os.path.normpath(p.mountpoint)
            if p.mountpoint != "/":
                choices.append((p.mountpoint, d))
    choices.sort()
    return choices


def _getMountDefault(choices):
    choices = {x[1]: x[0] for x in choices}
    return choices.get("/media/hdd") or choices.get("/media/usb") or ""


def _onPartitionChange(*_args, **_kwargs):
    choices = _getMountChoices()
    config.plugins.samsungtv.datalocation.setChoices(choices=choices, default=_getMountDefault(choices))
    updateDataFolder()


def updateDataFolder(*_args, **_kwargs):
    global _data_folder
    _data_folder = ""
    if v := config.plugins.samsungtv.datalocation.value:
        if os.path.exists(v):
            _data_folder = os.path.join(v, "SamsungTV")
            os.makedirs(_data_folder, exist_ok=True)


def initMountChoices():
    choices = _getMountChoices()
    config.plugins.samsungtv.datalocation = ConfigSelection(choices=choices, default=_getMountDefault(choices))
    harddiskmanager.on_partition_list_change.append(_onPartitionChange)
    config.plugins.samsungtv.datalocation.addNotifier(updateDataFolder, immediate_feedback=False)


initMountChoices()
