%module artemishsc

%{
#include "ArtemisHscAPI.h"
#include <oleauto.h>
%}

%include "carrays.i"
%include "typemaps.i"
%include "cpointer.i"

%apply int *OUTPUT { int *x, int *y, int *w, int *h, int *binx, int *biny };
int ArtemisGetImageData(ArtemisHandle hCam, int *x, int *y, int *w, int *h, int *binx, int *biny);

%array_class(unsigned short, shortArray);
%array_class(VARIANT, variantArray);

%inline %{

    unsigned short *ArtemisImageBuffer_unsignedShort(ArtemisHandle hCam) {
        return (unsigned short *) ArtemisImageBuffer(hCam);
    }

    unsigned short *ArtemisGetImageArray_unsignedShort(ArtemisHandle hCam) {
        int x, y, w, h, binx, biny;
        ArtemisGetImageData(hCam, &x, &y, &w, &h, &binx, &biny);
        int pixels = w * h;
        printf("ArtemisGetImageArray_unsignedShort: pixel count = %d\n", pixels);

        VARIANT *imageArray = (VARIANT *)malloc(sizeof(VARIANT) * pixels);
        for (int pixel = 0; pixel < pixels; pixel++) {
            VariantInit(&imageArray[pixel]);
        }
        printf("ArtemisGetImageArray_unsignedShort: initialized imageArray\n");

        ArtemisGetImageArray(hCam, imageArray);
        printf("ArtemisGetImageArray_unsignedShort: got image array\n");

        unsigned short *uiImageArray = (unsigned short *)malloc(sizeof(unsigned short) * pixels);
        printf("ArtemisGetImageArray_unsignedShort: uiImageArray allocated\n");

        for (int pixel = 0; pixel < pixels; pixel++) {
#ifdef DEBUG
            printf("at pixel [%06d]: ui[%p]/ia[%p]: %hd\n", pixel, &uiImageArray[pixel], &imageArray[pixel], imageArray[pixel].uiVal);
#endif
            uiImageArray[pixel] = imageArray[pixel].uiVal;
        }
        printf("ArtemisGetImageArray_unsignedShort: pixels converted\n");

        return uiImageArray;
    }

    PyObject *ArtemisGetImageArray_pythonList(ArtemisHandle hCam) {
        int x, y, w, h, binx, biny;
        ArtemisGetImageData(hCam, &x, &y, &w, &h, &binx, &biny);
        int pixels = w * h;
        printf("ArtemisGetImageArray_pythonList: pixel count = %d\n", pixels);

        unsigned short *uiImageArray = ArtemisGetImageArray_unsignedShort(hCam);
        PyObject *listImageArray = PyList_New(pixels);
        printf("ArtemisGetImageArray_pythonList: created list\n");

        for (int pixel = 0; pixel < pixels; pixel++) {
            PyObject *value = PyInt_FromLong((long) uiImageArray[pixel]);
            PyList_SetItem(listImageArray, pixel, value);
        }
        printf("ArtemisGetImageArray_pythonList: populated list\n");

        free(uiImageArray);
        printf("ArtemisGetImageArray_pythonList: deallocated uiImageArray\n");

        return listImageArray;
    }

%}

%include "ArtemisHscAPI.h"
