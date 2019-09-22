import requests
from xml.etree import ElementTree as ET

base_url = 'http://www.boardgamegeek.com/xmlapi/'

class Game:
    data = None
    downloaded = False
    ratings = None
    name = None

    def __init__(self, id):
        self.id = id
    
    def download_data(self, **kwargs):
        attempt = get_game_data(self.id, **kwargs)
        if attempt['success']:
            self.data = attempt['payload']
            self.name = get_game_name(self.data)
            self.downloaded = True
    
    def get_ratings(self):
        if self.ratings is None:
            self.ratings = get_ratings(self.data, self.id)
            return(self.ratings)
        else:
            return(self.ratings)

    # def export_info(self):
    #     pass
    




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
    if response.status_code == 200:
        return({
            'success': True,
            'payload': ET.fromstring(response.content)
        })
    else:
        return({
            'success': False,
            'payload': None
        }
        )

    return(response)


def get_game_name(data_tree):
    for child in data_tree.iter('name'):
        if 'primary' in child.attrib:
            if child.attrib['primary'] == 'true':
                return(child.text)

def get_ratings(data_tree, id):
    ratings = [[id,child.attrib['username'],child.attrib['rating']] for child in data_tree.iter('comment') if child.attrib['rating'] != "N/A"]
    return(ratings)