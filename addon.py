# -*- coding: utf-8 -*
# Auther: Theunderbird2086
# Module: addon
"""
   OpenVPN profile downloader for Kodi
"""

import os

import xbmcaddon
import xbmcgui

from resources.lib.const import FILTER_COUNTRY, FILTER_SPEED, STORAGE_PATH
import resources.lib.downloader as downloader

_ADDON = xbmcaddon.Addon()
_ADDONNAME = _ADDON.getAddonInfo('name')


if __name__ == '__main__':

    FILTERS_FROM_CONFIG = {
        FILTER_COUNTRY: _ADDON.getSetting(FILTER_COUNTRY),
        FILTER_SPEED: _ADDON.getSettingInt(FILTER_SPEED)
    }

    PROFILE_PATH = _ADDON.getSetting(STORAGE_PATH)
    if PROFILE_PATH == "home://VPN":
        PROFILE_PATH = os.path.join(os.path.expanduser('~'), 'VPN')
        _ADDON.setSetting(STORAGE_PATH, PROFILE_PATH)

    NO_OF_FILES = downloader.get(FILTERS_FROM_CONFIG, PROFILE_PATH)

    MSG = "Downloaded {} profiles.".format(NO_OF_FILES)

    xbmcgui.Dialog().notification(_ADDONNAME, MSG)
