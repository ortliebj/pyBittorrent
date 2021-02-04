from Torrent import Torrent
from Tracker import Tracker


if __name__ == '__main__':
    # create Torrent object to hold .torrent info
    torrent = Torrent('test/2021-01-11-raspios-buster-armhf-lite.zip.torrent')

    # read the file and decode metadata
    torrent.read_file()
    print('metadata: ', torrent.metadata)

    # create the info_hash
    torrent.create_info_hash()
    print('info_hash length: ', len(torrent.info_hash))
    print('info_hash: ', torrent.info_hash)

    # print metadata stuff
    print('announce: ', torrent.metadata['announce'])
    print('created by: ', torrent.metadata['created by'])
    print('creation date: ', torrent.metadata['creation date'])
    print('encoding: ', torrent.metadata['encoding'])
    print('info: ', torrent.metadata['info'])
    print('length: ', torrent.metadata['info']['length'])
    print('name: ', torrent.metadata['info']['name'])
    print('piece length: ', torrent.metadata['info']['piece length'])
    print('pieces: ', torrent.metadata['info']['pieces'])
    print('private: ', torrent.metadata['info']['private'])

    # --------- Tracker stuff ------------- #
    tracker = Tracker(torrent)
    print('---------TRACKER---------')

    print('tracker.peer_id: ', tracker.params['peer_id'])
    print('tracker.peer_id length: ', len(tracker.params['peer_id']))

    print('request params: ', tracker.params)

    response = tracker.make_request_to_tracker()
    print('tracker response: ', response.response)

    response.extract_peers()
    print('number of peers: ', len(response.peers))
    print('list of peers:', response.peers)
