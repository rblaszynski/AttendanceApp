from __future__ import print_function
from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString

for reader in readers():
    try:
        connection = reader.createConnection()
        connection.connect()
        print(reader, toHexString(connection.getATR()))
    except NoCardException:
        print(reader, 'no card inserted')

import sys
if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)