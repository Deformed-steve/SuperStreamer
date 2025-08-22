import sys, urllib.parse, xbmcplugin, xbmcgui
import requests

# Kodi addon handle
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

# API key and base URLs
TMDB_API_KEY = 'a63b70ca6288b339b0b556535449d1b9'  # replace with your TMDb key
TMDB_MOVIE_POPULAR = 'https://api.themoviedb.org/3/movie/popular?api_key={}&page={}'
TMDB_TV_POPULAR = 'https://api.themoviedb.org/3/tv/popular?api_key={}&page={}'

# Default state
current_page = 1
current_type = 'movie'  # 'movie' or 'tv'
current_query = None

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def list_items(reset=False):
    global current_page
    if current_query:
        url = f'https://api.themoviedb.org/3/search/{current_type}?api_key={TMDB_API_KEY}&query={urllib.parse.quote(current_query)}&page={current_page}'
    else:
        if current_type == 'movie':
            url = TMDB_MOVIE_POPULAR.format(TMDB_API_KEY, current_page)
        else:
            url = TMDB_TV_POPULAR.format(TMDB_API_KEY, current_page)

    res = requests.get(url).json()
    if reset:
        xbmcplugin.endOfDirectory(addon_handle, succeeded=True)

    for item in res['results']:
        title = item.get('title') if current_type == 'movie' else item.get('name')
        poster = 'https://image.tmdb.org/t/p/w300' + item['poster_path'] if item.get('poster_path') else ''
        url = build_url({'action': 'play', 'id': item['id']})
        li = xbmcgui.ListItem(title)
        li.setArt({'icon': poster, 'thumb': poster})
        xbmcplugin.addDirectoryItem(addon_handle, url, li, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)

def play_item(item_id):
    # VidSrc embed URL
    stream_url = f'https://vidsrc.cc/v2/embed/{current_type}/{item_id}'
    li = xbmcgui.ListItem(path=stream_url)
    xbmcplugin.setResolvedUrl(addon_handle, True, li)

# Parse arguments
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

if params.get('action') == 'play':
    play_item(params['id'])
else:
    list_items()

