%module artemishsc
%{
#include "ArtemisHscAPI.h"
%}

%include "carrays.i"
%include "typemaps.i"

%array_class(VARIANT, variantArray);

%apply int *OUTPUT { int *x, int *y, int *w, int *h, int *binx, int *biny };
%apply unsigned short *OUTPUT { void *imageBufferHandler };

int ArtemisGetImageData(ArtemisHandle hCam, int *x, int *y, int *w, int *h, int *binx, int *biny);
void* ArtemisImageBuffer(ArtemisHandle hCam);

%include "ArtemisHscAPI.h"
