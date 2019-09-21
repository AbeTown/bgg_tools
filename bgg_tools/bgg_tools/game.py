import requests

base_url = 'http://www.boardgamegeek.com/xmlapi/'

class Game:
    data = None
    downloaded = False

    def __init__(self, id):
        self.id = id
    
    def download_data(self, **kwargs):
        self.data = get_game_data(self.id, **kwargs)
        self.downloaded = True


def get_game_data(id, comments=None, stats=None, historical=None, h_begin=None, h_end=None):
    
    if type(id) is int:
        id = str(id)

    request_url = base_url + 'boardgame/' + id

    # Add any optional argumetns to the url
    if any(arg is not None for arg in [comments, stats, historical]):
        request_url += '?'
    if comments is not None:
        print("comments present!")
        request_url += 'comments=1&'
    if stats is not None:
        request_url += 'stats=1&'
    if historical is not None:
        request_url += 'historical=1&'
        if h_begin is not None:
            request_url += 'from=' + h_begin + '&'
        if h_end is not None:
            request_url += 'end=' + h_end + '&'
    
    print('Downloading', id, "from", request_url)
    response = requests.get(request_url)
    response


