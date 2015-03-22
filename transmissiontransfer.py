import os
import argparse
import logging

import transmissionrpc

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def transmission_add_argparse_arguments(parser, name):
    parser.add_argument('{}_host'.format(name))
    parser.add_argument('--{}-port'.format(name), default=9091, type=int, metavar="port")

def main():
    parser = argparse.ArgumentParser(description='Move torrent between Transmission instances')
    
    transmission_add_argparse_arguments(parser, "source")
    transmission_add_argparse_arguments(parser, "destination")
    parser.add_argument('--equivalent-path', required=True, nargs=2, metavar=("sourcepath", "destinationpath"), action='append')
    
    args = parser.parse_args()
    
    logger.debug("Connecting to source")
    source = transmissionrpc.Client(args.source_host, port=args.source_port)
    logger.debug("Connecting to destination")
    destination = transmissionrpc.Client(args.destination_host, port=args.destination_port)
    
    directory_mapping = dict(args.equivalent_path)
    def get_remote_directory(torrent):
        for source_directory, destination_directory in directory_mapping.items():
            if torrent.downloadDir.startswith(source_directory):
                return torrent.downloadDir.replace(source_directory, destination_directory)
        return None
    
    source_torrents = source.get_torrents()
    source_torrents = filter(get_remote_directory, source_torrents)
    logger.info("Found {} candidate torrents".format(len(source_torrents)))
    
    destination_torrents = destination.get_torrents()
    existing_hashes = {torrent.hashString for torrent in destination_torrents}
    
    for torrent in source_torrents:
        if torrent.hashString not in existing_hashes:
            with open(torrent.torrentFile, "rb") as torrent_file:
                data = torrent_file.read()
            logger.info("Adding {}".format(torrent))
            new_torrent = destination.add(data.encode("base64"), download_dir=get_remote_directory(torrent), paused=True)
            new_torrent = new_torrent.values()[0]
            new_torrent.update()
            logger.debug("Added {}".format(new_torrent))
        else:
            new_torrent = [nt for nt in destination_torrents if nt.hashString == torrent.hashString][0]
            if new_torrent.progress == 100.0:
                if new_torrent.status == 'stopped':
                    logger.info("Starting {}".format(new_torrent))
                    new_torrent.start()
                if torrent.status != 'stopped':
                    logger.info("Stopping {}".format(torrent))
                    torrent.stop()
                continue
        
        if new_torrent.name != torrent.name:
            logger.info("Renaming {} to {}".format(new_torrent.name, torrent.name))
            destination.rename_torrent_path(new_torrent.id, new_torrent.name, torrent.name)
            new_torrent.update()
        
        old_files = torrent.files()
        new_files = new_torrent.files()
        for file_id in old_files:
            old_file = old_files[file_id]
            new_file = new_files[file_id]
            if old_file['name'] != new_file['name']:
                correct_path = os.path.split(old_file['name'])[-1]
                logger.info("Renaming {} to {}".format(new_file['name'], correct_path))
                destination.rename_torrent_path(new_torrent.id, new_file['name'], correct_path)
        new_torrent.update()
        destination.verify_torrent(new_torrent.id)

if __name__ == '__main__':
    main()