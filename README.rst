transmissiontransfer
====================

This script connects to two instances of transmission using the RPC interface
and moves torrents from one to the other.

Example usage:

    transmissiontransfer localhost mybooklive.fritz.box --equivalent-path /Volumes/Kiff /shares/Kiff

This will add to the instance running on `mybooklive` any torrent that is on
`localhost` *and* that is being saved to `/Volumes/Kiff`. The resultant
torrents will be saved to `/shares/Kiff`. This allows files stored on an
external drive to be migrated to another machine for managing longer term
seeding.

For many files, simply re-adding the torrent to the new machine would be
enough, however this script also ensures that all files and directories are
correctly named, so if a file was renamed in the original torrent client (for
example, to fit a local naming convention without breaking seeding) these names
will be carried across.

The initial run of this will add any torrents and rename them as appropriate,
before triggering a verification run. If it comes across any duplicate torrents
that have been successfully verified it will stop them in source and start them
in destination.
