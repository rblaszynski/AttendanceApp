from __future__ import print_function

from smartcard import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.CardType import ATRCardType, AnyCardType
from smartcard.Exceptions import NoCardException
from smartcard.ATR import ATR
from smartcard.System import readers
from smartcard.util import toHexString, toBytes
import sys

def toHex(s):
    lst = []
    for ch in s:
        hv = int(ch, 16)
        lst.append(hv)

    return lst

f=open("data.txt", "a+")
for reader in readers():
    try:
        connection = reader.createConnection()
        connection.connect()
        atr = toHexString(connection.getATR())
        atr1 = atr.split(' ', 18)
        atr2 = toHex(atr1)
        atr3 = ATR(atr2)
        cardtype = AnyCardType()
        cardrequest = CardRequest(timeout=10, cardType=cardtype)
        cardservice = cardrequest.waitforcard()
        cardservice.connection.connect()
        READ = [0x00, 0xCA, 0x00, 0x00, 0x00]
        apdu = READ
        print(reader, ': ', toHexString(connection.getATR()))
        print('Historical bytes: ', toHexString(atr3.getHistoricalBytes()))
        f.write(toHexString(connection.getATR()))
        f.write("\n")
        print('Sending ', toHexString(apdu), '...')
        response, status1, status2 = cardservice.connection.transmit(apdu)
        print('Response: ', response, ' |  status: ', "%x %x" % (status1, status2))
        uid = toHexString(response).replace(' ', '')
        print('UID: ', uid)

        if 'win32' == sys.platform:
            print('press Enter to continue')
            sys.stdin.read(1)

    except NoCardException:
        print(reader, ': ', 'no card inserted')
        if 'win32' == sys.platform:
            print('press Enter to continue')
            sys.stdin.read(1)