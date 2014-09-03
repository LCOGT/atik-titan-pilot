import time
import datetime
import sys
import getpass
import warnings
import os
import pprint

import numpy
import pyfits

from artemishsc import *


EXPOSURE_TIME = 1.0
DEVICE_NUMBER = 0
GET_TEMPERATURE_SENSOR_COUNT = 0
FITS_FILENAME = 'titan.fits'
DTYPE_PIXEL = numpy.uint16
DIVIDER = '-' * 40

pp = pprint.PrettyPrinter()


def formatted_file_size_kilobytes(input_file):
    size_in_bytes = os.path.getsize(input_file)
    size_in_kilobytes = int(size_in_bytes / 1024)
    formatted_string = format(size_in_kilobytes, ',d') + ' KB'
    return formatted_string


dll_loaded = ArtemisLoadDLL('shared\ArtemisHSC.dll')
print 'DLL loaded: ', dll_loaded
if not dll_loaded:
    sys.exit(1)
print

titan = ArtemisConnect(DEVICE_NUMBER)

device_name = ArtemisDeviceName_pythonString(DEVICE_NUMBER)
device_serial_number = ArtemisDeviceSerial_pythonString(DEVICE_NUMBER)
device_api_version = ArtemisAPIVersion()
_, camera_serial_number_flags, camera_serial_number = ArtemisCameraSerial(titan)
camera_type = '4021' if bool(camera_serial_number_flags & int('01', 2)) else '1102'
print 'General Properties'
print DIVIDER
print 'Artemis API Version: ', device_api_version
print 'Device Name: ', device_name
print 'Device Serial Number: ', device_serial_number
print 'Camera Serial Number: ', camera_serial_number
print 'Camera Type: ', camera_type

print 'Cooling Properties'
print DIVIDER
_, flags, level, minlvl, maxlvl, setpoint = ArtemisCoolingInfo(titan)
cooling_exists = bool(flags & int('00000001', 2))
cooling_on_off_power_control = bool(flags & int('00000010', 2))
cooling_on_off_cooling_control = bool(flags & int('00000100', 2))
cooling_selectable_power_levels = bool(flags & int('00001000', 2))
cooling_set_point_cooling = bool(flags & int('00010000', 2))
cooling_warming_up = bool(flags & int('00100000', 2))
cooling_on = bool(flags & int('01000000', 2))
cooling_set_point_control = bool(flags & int('10000000', 2))
print 'Cooling exists: ', cooling_exists
if cooling_exists:
    _, sensor_count = ArtemisTemperatureSensorInfo(titan, GET_TEMPERATURE_SENSOR_COUNT)
    print 'Temperature Sensor count: ', sensor_count
    for sensor_number in range(1, sensor_count):
        _, temperature = ArtemisTemperatureSensorInfo(titan, sensor_number)
        print 'Temperature Sensor[%d] reading (Celsius): %.2f' % (sensor_number, temperature / 100.0)
    print 'Cooling on/off power control: ', cooling_on_off_power_control
    print 'Cooling on/off cooling control: ', cooling_on_off_cooling_control
    print 'Cooling selectable power levels: ', cooling_selectable_power_levels
    print 'Cooling set-point cooling: ', cooling_set_point_cooling
    print 'Cooling warming up: ', cooling_warming_up
    print 'Cooling cooling on: ', cooling_on
    print 'Cooling set-point control: ', cooling_set_point_control
    print 'Cooling current/minimum/maximum power level: %d/%d/%d' % (level, minlvl, maxlvl)
    print 'Cooling set point: %.2f (Celsius):' % (setpoint / 100.0,)
print

_, colour_type, normal_offset_x, normal_offset_y, preview_offset_x, preview_offset_y = ArtemisColourProperties(titan)
print "Colour Properties"
print DIVIDER
print 'Colour Type: ', colour_type
print 'Normal Offset X: ', normal_offset_x
print 'Normal Offset Y: ', normal_offset_y
print 'Preview Offset X: ', preview_offset_x
print 'Preview Offset Y: ', preview_offset_y
print

print 'Initialization & Settings'
print DIVIDER

# print 'Bin Data: ', ArtemisGetBin(titan)

connected = ArtemisIsConnected(titan)
print 'Connected: ', connected
if not connected:
    raise Exception('device is not connected')

camera_properties = ArtemisProperties_pythonDictionary(titan)
print 'Camera Properties: ', pp.pprint(camera_properties)
print

print 'Exposure'
print DIVIDER

print 'Exposure time: ', EXPOSURE_TIME

ArtemisStartExposure(titan, EXPOSURE_TIME)
time.sleep(EXPOSURE_TIME)
while not ArtemisImageReady(titan):
    time.sleep(0.5)

now = datetime.date.today()
observation_timestamp = datetime.datetime.fromtimestamp(time.time()).isoformat()
print 'Observation timestamp: ', observation_timestamp

percent_done = 0
print 'Download % completed: ', percent_done
while percent_done < 100:
    percent_done = ArtemisDownloadPercent(titan)
    print 'Download % completed: ', percent_done

_, x, y, w, h, bin_x, bin_y = ArtemisGetImageData(titan)
print 'Fetched imaged data - x=%d/y=%d w=%d/h=%d bin: x=%d/y=%d' % (x, y, w, h, bin_x, bin_y)
print

print 'FITS File Generation'
print DIVIDER
image_buffer = ArtemisImageBuffer_pythonList(titan)
image_array = numpy.asarray(numpy.reshape(image_buffer, (w, h)), dtype=DTYPE_PIXEL, order='C')

user = getpass.getuser()

header_primary = pyfits.Header()
header_primary['SIMPLE'] = 'T'
header_primary['BITPIX'] = 16
# header_primary['BYTEORDR'] = 'BIG_ENDIAN'
header_primary['NAXIS'] = 2
header_primary['NAXIS1'] = h
header_primary['NAXIS2'] = w
header_primary['EXTEND'] = 'T'
#header_primary['DATATYPE'] = 'INTEGER*2'
header_primary['TELESCOP'] = 'N/A'
header_primary['INSTRUME'] = format('%s [%d]' % (device_name, device_api_version))
header_primary['OBJECT'] = 'N/A'
header_primary['OBJECT2'] = '_'
header_primary['ORIGIN'] = 'Las Cumbres Observatory'
#header_primary['FEXPTIME'] = int(EXPOSURE_TIME * 1000)
header_primary['DATE'] = observation_timestamp
header_primary['DATE-OBS'] = observation_timestamp
header_primary['BSCALE'] = 1
header_primary['BUNIT'] = 'DN'
header_primary['BZERO'] = 0.0
header_primary['EXPTIME'] = int(EXPOSURE_TIME * 1000)
header_primary['CRPIX1'] = 100.0
header_primary['CRPIX2'] = 100.0
header_primary['CRVAL1'] = 0.0
header_primary['CRVAL2'] = 0.0
header_primary['CRTYPE1'] = 'RA--TAN'
header_primary['CRTYPE2'] = 'DEC--TAN'
header_primary['PSCALE1'] = 1.0
header_primary['PSCALE2'] = 1.0
header_primary['ASTRPROG'] = __file__
header_primary['ASTRVER'] = '1.0'
header_primary['AUTHOR'] = user
header_primary['OBSERVER'] = user

header_primary.add_comment(format('Generated by %s' % ( __file__)))

hdu_primary = pyfits.PrimaryHDU(header=header_primary, data=image_array, uint=True)

print 'Headers:'
for key, value in header_primary.iteritems():
    print '\t%-8s: %s' % (key, value)
print

with warnings.catch_warnings([UserWarning]):
    hdu_primary.writeto(name=FITS_FILENAME, clobber=True, output_verify='fix', checksum=False)

print 'File Size: ', formatted_file_size_kilobytes(FITS_FILENAME)
print

hdu_list = pyfits.open(FITS_FILENAME)
try:
    hdu_list.info()
finally:
    hdu_list.close()
print

ArtemisDisconnectAll()
ArtemisUnLoadDLL()

print DIVIDER
print 'Done.'
