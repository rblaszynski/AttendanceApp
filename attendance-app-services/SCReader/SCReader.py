from __future__ import print_function
from smartcard.Exceptions import NoCardException
from smartcard.ATR import ATR
from smartcard.System import readers
from smartcard.util import toHexString

def toHex(s):
    lst = []
    for ch in s:
        hv = int(ch, 16)
        lst.append(hv)

    return lst

for reader in readers():
    try:
        connection = reader.createConnection()
        connection.connect()
        atr = toHexString(connection.getATR())
        atr1 = atr.split(' ', 18)
        atr2 = toHex(atr1)
        atr3 = ATR(atr2)
        print(reader, ': ', toHexString(connection.getATR()))
        print('Historical bytes: ', toHexString(atr3.getHistoricalBytes()))
        #print('checksum: ', "0x%X" % atr3.getChecksum())
        #print('checksum OK: ', atr3.checksumOK)
        #print('T0  supported: ', atr3.isT0Supported())
        #print('T1  supported: ', atr3.isT1Supported())
        #print('T15 supported: ', atr3.isT15Supported())
    except NoCardException:
        print(reader, 'no card inserted')

import sys
if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)