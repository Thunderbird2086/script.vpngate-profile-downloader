# -*- coding: utf-8 -*
# Auther: Theunderbird2086
# Module: addon

import xbmcaddon
import xbmcgui
 
from resources.lib.const import FILTER_COUNTRY, FILTER_SPEED
import resources.lib.downloader as downloader

_ADDON       = xbmcaddon.Addon()
_ADDONNAME   = _ADDON.getAddonInfo('name')
 


if __name__ == '__main__':
    
    filters = {
      FILTER_COUNTRY: _ADDON.getSetting(FILTER_COUNTRY),
      FILTER_SPEED: int(_ADDON.getSetting(FILTER_SPEED))
    }
            
    no_of_files = downloader.get(filters)

    msg = "Downloaded {} profiles.".format(no_of_files)
 
    xbmcgui.Dialog().ok(_ADDONNAME, msg)
