import sys, xbmcplugin, xbmcgui

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'videos')

li = xbmcgui.ListItem("Test Video")
li.setPath("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")
xbmcplugin.addDirectoryItem(addon_handle, "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", li, False)

xbmcplugin.endOfDirectory(addon_handle)
