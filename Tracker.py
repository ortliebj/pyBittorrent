# handle tracker HTTP requests and responses
import bencodepy
import requests
from random import randint
from struct import unpack

import utils


class Tracker:
    def __init__(self, torrent):
        self.torrent = torrent
        # self.announce = announce  # url of tracker in the form of http://tracker.com:6969/announce
        # self.peer_id = ''      # 20 byte string used as a personal identifier
        # self.port = 6881       # the port number the client is listed on. usually 6881-6889
        # self.uploaded = 0      # total number of bytes uploaded since the client sent the ‘started’ event to the tracker
        # self.downloaded = 0    # total number pf bytes downloaded since the client sent the ‘started’ event to the tracker
        # self.left = 0          # the number of bytes the client still has to download, in base ten ASCII
        # self.compact = 1       # 1 means peer list will be 6 byte chunks, 0 for a dictionary
        # self.event = ''        # optional
        # self.ip = ''           # optional
        # self.numwant = 50      # optional, number of peers wanted. usually defaults to 50
        # self.key = ''          # optional
        # self.tracker_id = ''   # optional
        self.params = {          # parameters to be included in the request to tracker
            "info_hash": self.torrent.info_hash,
            "peer_id": self.generate_peer_id('PY', '0001'),
            'port': 6881,
            'uploaded': 0,
            'downloaded': 0,
            'left': 0,
            'compact': 1
        }
        self.response = {}      # content of decoded response

    def generate_peer_id(self, client_id, client_version):
        """
        Generate a peer_id
        :param client_id: A two letter client id
        :param client_version: A four digit client version
        :return: peer id
        """
        # This is using the Azureus style e.g. '-AZ2060-...', where AZ is the client id,
        # and the next four numbers are the version number
        # it's 20 bytes so we need 12 random characters
        # only generate once when client is opened
        peer_id = f'-{client_id}{client_version}-'
        for _ in range(0, 12):
            peer_id += str(randint(0, 9))
        return peer_id

    def make_request_to_tracker(self):
        """
        Makes the GET request to the tracker
        :return: TrackerResponse object
        """
        raw_response = requests.get(self.torrent.metadata['announce'], params=self.params)
        print('status code: ', raw_response.status_code)
        if raw_response.status_code != 200:
            raise ConnectionError(f'Couldn\'t connect to tracker: {raw_response.status_code}')
        return TrackerResponse(bencodepy.decode(raw_response.content))


class TrackerResponse:
    def __init__(self, response):
        self.response = utils.dict_to_utf8(response)
        # the below variables are all part of response. just here for the info
        self.peers = []                # peers in format (ip, port)
        # self.complete = 0            # number of seeders with the complete file
        # self.incomplete = 0          # number of leechers
        # self.downloaded = 0          # number of times the file has been downloaded
        # self.interval = 60 * 30      # interval (in seconds) the client should wait between regular requests to tracker
        # self.min_interval = 60 * 15  # (optional) minimum announce interval. don't reannounce more frequently than this

    def extract_peers(self):
        """
        Takes the peers byte list from response and creates a list of peers
        :return: list of peers in the form [(ip, port), ...]
        """
        # the peers dict in the response is in 6 byte chunks
        # the first 4 bytes are the ip address, last 2 bytes are port
        # all big endian
        raw = self.response['peers']
        # split byte string into list of 6 byte chunks
        peers_chunks = [raw[i:i+6] for i in range(0, len(raw), 6)]
        # '!' is network byte order, 'I' is an unsigned int, 'H' is an unsigned short
        self.peers = [unpack('!IH', peer) for peer in peers_chunks]
        return self.peers
