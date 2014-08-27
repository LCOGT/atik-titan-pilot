import artemishsc
from artemishsc import *

from time import sleep

from sys import exit

DEFAULT_DEVICE = -1

try:
    dll_loaded = ArtemisLoadDLL('shared\ArtemisHSC.dll')
    print 'DLL loaded: ' + str(dll_loaded)
    if not dll_loaded:
        exit(1)

    print 'Artemis API Version: ' + str(ArtemisAPIVersion())
    print

    titan = ArtemisConnect(DEFAULT_DEVICE)

    try:
        connected = ArtemisIsConnected(titan)
        print 'Connected: ' + str(connected)

        if not connected:
            exit(1)

        print 'Starting exposure'

        ArtemisStartExposure(titan, 2)
        while not ArtemisImageReady(titan):
            sleep(0.5)
    
        print 'Exposure complete'

        i, x, y, w, h, bin_x, bin_y = ArtemisGetImageData(titan)
        print "[%d] Fetched imaged data - x=%d/y=%d w=%d/h=%d bin: x=%d/y=%d" % (i, x, y, w, h, bin_x, bin_y)

        image_buffer = ArtemisImageBuffer(titan)
        for buffer_y in xrange(y, y + h):
            for buffer_x in xrange(x, x + w):
                pass


    finally:
        ArtemisDisconnect(titan)


finally:
    ArtemisUnLoadDLL()
    print
    print "Done."
    print
