%module artemishsc

%{
#include "ArtemisHscAPI.h"
#include <oleauto.h>
%}

%include "carrays.i"
%include "typemaps.i"
%include "cpointer.i"
%include "exception.i"

//
// General
//
%array_class(unsigned short, shortArray);
%array_class(VARIANT, variantArray);


//
// Misc
//
%apply int *OUTPUT { int *x, int *y, int *w, int *h, int *binx, int *biny };
int ArtemisGetImageData(ArtemisHandle hCam, int *x, int *y, int *w, int *h, int *binx, int *biny);

%apply int *OUTPUT { int *x, int *y, int *w, int *h };
int ArtemisGetSubframe(ArtemisHandle hCam, int *x, int *y, int *w, int *h);

%apply int *OUTPUT { int *x, int *y };
int ArtemisGetBin(ArtemisHandle hCam, int *x, int *y);

%apply bool *OUTPUT { char *pName };
bool ArtemisDeviceName(int device, char *pName);
bool ArtemisDeviceSerial(int device, char *pName);

%apply int *OUTPUT { ARTEMISCOLOURTYPE *colourType, int *normalOffsetX, int *normalOffsetY, int *previewOffsetX, int *previewOffsetY };
int ArtemisColourProperties(ArtemisHandle hCam, ARTEMISCOLOURTYPE *colourType, int *normalOffsetX, int *normalOffsetY, int *previewOffsetX, int *previewOffsetY);


//
// ArtemisProperties
//
%inline %{

    PyObject *ArtemisProperties_pythonDictionary(ArtemisHandle hCam) {
        struct ARTEMISPROPERTIES pProp;
        int result = ArtemisProperties(hCam, &pProp);
        if (result != ARTEMIS_OK) {
            return NULL;
        }
        
        PyObject *dict = PyDict_New();
        PyDict_SetItem(dict, PyString_FromString("protcol"), PyInt_FromLong((long) pProp.Protocol));
        PyDict_SetItem(dict, PyString_FromString("pixel_count_x"), PyInt_FromLong((long) pProp.nPixelsX));
        PyDict_SetItem(dict, PyString_FromString("pixel_count_y"), PyInt_FromLong((long) pProp.nPixelsY));
        PyDict_SetItem(dict, PyString_FromString("pixel_microns_x"), PyFloat_FromDouble((double) pProp.PixelMicronsX));
        PyDict_SetItem(dict, PyString_FromString("pixel_microns_y"), PyFloat_FromDouble((double) pProp.PixelMicronsY));
        PyDict_SetItem(dict, PyString_FromString("ccd_flags"), PyInt_FromLong((long) pProp.ccdflags));
        PyDict_SetItem(dict, PyString_FromString("camera_flags"), PyInt_FromLong((long) pProp.cameraflags));
        PyDict_SetItem(dict, PyString_FromString("description"), PyString_FromString(pProp.Description));
        PyDict_SetItem(dict, PyString_FromString("manufacturer"), PyString_FromString(pProp.Manufacturer));

        return dict;
    }
%}


//
// Image Data
//
%inline %{

    PyObject *unsignedShortArrayToPythonList(unsigned short *array, int array_length) {
        PyObject *list = PyList_New(array_length);

        for (int i = 0; i < array_length; i++) {
            PyObject *value = PyInt_FromLong((long) array[i]);
            PyList_SetItem(list, i, value);
        }

        return list;
    }

    unsigned short *ArtemisImageBuffer_unsignedShort(ArtemisHandle hCam) {
        return (unsigned short *) ArtemisImageBuffer(hCam);
    }

    PyObject *ArtemisImageBuffer_pythonList(ArtemisHandle hCam) {
        int x, y, w, h, binx, biny;
        ArtemisGetImageData(hCam, &x, &y, &w, &h, &binx, &biny);
        int pixels = w * h;
        printf("ArtemisGetImageArray_unsignedShort: pixel count = %d\n", pixels);
        return unsignedShortArrayToPythonList(ArtemisImageBuffer_unsignedShort(hCam), pixels);
    }

%}

%include "ArtemisHscAPI.h"
