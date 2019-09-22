import requests
from xml.etree import ElementTree as ET

base_url = 'http://www.boardgamegeek.com/xmlapi/'

class Game:
    data = None
    page = 1
    downloaded = False

    name = None
    year_published = None

    ratings = None

    mechanic = None
    category = None
    publisher = None
    honor = None
    podcastepisode = None
    version = None
    family = None
    artist = None
    designer = None  

    def __init__(self, id):
        self.id = id
    
    def download_data(self, **kwargs):
        attempt = get_game_data(self.id, **kwargs)
        if attempt['success']:
            self.data = attempt['payload']
            self.downloaded = True
            self.name = get_game_name(self.data)

            self.mechanic = get_descriptor('mechanic', self.data, self.id)
            self.category = get_descriptor('category', self.data, self.id)
            self.publisher = get_descriptor('publisher', self.data, self.id)
            self.honor = get_descriptor('publisher', self.data, self.id)
            self.podcastepisode = get_descriptor('podcastepisode', self.data, self.id)
            self.version = get_descriptor('version', self.data, self.id)
            self.family = get_descriptor('family', self.data, self.id)
            self.artist = get_descriptor('artist', self.data, self.id)
            self.designer = get_descriptor('designer', self.data, self.id)

            self.year_published = get_year_published(self.data)
    
    def get_ratings(self):
        if self.ratings is None:
            ratings = []
            more_ratings = True
            data = self.data
            while(more_ratings):
                new_ratings = get_ratings(data, self.id)
                more_ratings = new_ratings['more']
                if more_ratings:
                    ratings += new_ratings['payload']
                    self.page += 1
                    attempt = get_game_data(self.id, comments=True, page=self.page)
                    if attempt['success']:
                        data = attempt['payload']
                    else:
                        more_ratings = False 
            self.ratings = ratings
            return(self.ratings)
        else:
            return(self.ratings)

def get_game_data(id, comments=None, stats=None, historical=None, h_begin=None, h_end=None, page=1):
    
    if type(id) is int:
        id = str(id)

    request_url = base_url + 'boardgame/' + id

    # Add any optional argumetns to the url
    if any(arg is not None for arg in [comments, stats, historical]):
        request_url += '?'
    if comments is not None:
        print("comments present!")
        request_url += 'comments=1&page=' + str(page) + '&'
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


def get_comments(data_tree):
    return(data_tree[0].findall("comment"))


def get_game_name(data_tree):
    for child in data_tree.iter('name'):
        if 'primary' in child.attrib:
            if child.attrib['primary'] == 'true':
                return(child.text)

def get_ratings(data_tree, id):
    comments = get_comments(data_tree)
    if len(comments) == 0:
        return({
            'more': False,
            'payload': None
        })
    ratings = [[id,child.attrib['username'],child.attrib['rating']] for child in comments if child.attrib['rating'] != "N/A"]
    return({
        'more': True,
        'payload': ratings
        })

def get_year_published(data_tree):
    node = data_tree[0].find('yearpublished')
    if node is not None:
        return(node.text)
    return(None)

def get_descriptor(descriptor, data_tree, id):
    nodes = data_tree[0].findall('boardgame' + descriptor)
    if len(nodes) > 0:
        return([[id, node.attrib['objectid'], node.text] for node in nodes])