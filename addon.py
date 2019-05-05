# -*- coding: utf-8 -*
# Auther: Theunderbird2086
# Module: default

import xbmcaddon
import xbmcgui
 
import downloader

_ADDON       = xbmcaddon.Addon()
_ADDONNAME   = addon.getAddonInfo('name')
 
_DEFAULT_FILTER = ['KR', 'US']


if __name__ == '__main__':
    _no_of_files = downloader.get(_DEFAULT_FILTER)

    msg = "Downloaded {} profiles.".format(_no_of_files)
 
    xbmcgui.Dialog().ok(_ADDONNAME, msg)
