import requests
from bgg_tools import Game
from xml.etree import ElementTree as ET

base_url = 'http://boardgamegeek.com/xmlapi/collection/'

class Collection:
    data = None
    downloaded = False

    games = None

    def __init__(self, username):
        self.username = username
    
    def download_collection(self):
        download_error = False
        try:
            attempt = get_user_collection(self.username)
        except:
            download_error = True
        if not download_error:
             if attempt['success']:
                self.data = attempt['payload']
                self.downloaded = True
     
    def get_game_ids(self):
        print(get_game_ids(self.data))

def get_user_collection(username):

    request_url = base_url + username

    print('Downloading', username, "from", request_url)

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

def get_game_ids(data_tree):
    return([Game(node.attrib['objectid']) for node in data_tree.findall('item') if node.attrib['subtype'] == 'boardgame'])

