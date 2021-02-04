# torrent file info

import os
import bencodepy
from hashlib import sha1

import utils


class Torrent:
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = {}
        self.info_hash = b''                # 20 byte sha1 hash of info dictionary
        # self.announce = ''
        # self.announce_list = []           # optional
        # self.info = {}
        # self.length = 0                   # length of file in bytes
        # self.name = ''
        # self.creation_date = 0            # optional
        # self.encoding = ''                # optional
        # self.comment = ''                 # optional
        # self.created_by = ''              # optional
        # self.private = 0                  # optional, private = 1, public = 0
        # self.piece_length = 0             # number of bytes in each piece
        # self.pieces = b''                 # concatenation 20 byte sha1 hashes of pieces

    def read_file(self):
        """
        Read a .torrent file and decodes metadata.
        :return: None
        """
        app_root = os.path.dirname(__file__)
        torrent_path = os.path.join(app_root, self.file_path)
        with open(torrent_path, 'rb') as f:
            self.metadata = bencodepy.decode(f.read())
        self.metadata = utils.dict_to_utf8(self.metadata)

    def create_info_hash(self):
        """
        Bencode the info dict and hash it with SHA1
        :param meta_data: decoded meta data from .torrent file
        :return: hashlib digest
        """
        self.info_hash = sha1()
        self.info_hash.update(bencodepy.encode(self.metadata['info']))
        self.info_hash = self.info_hash.digest()
        return self.info_hash

