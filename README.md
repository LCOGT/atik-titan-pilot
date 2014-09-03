atik-titan-pilot
================

Summary
-------
This project contains all the components for performing an LCOGT pilot test of the Atik Titan camera.

The goals is to wrap the C/C++ Artik/Artemis code in Python.

To build:

    c:\<project-dir>\build.bat
    

To run test program:

    c:\<project-dir>\artemis.bat
![](docs\atik-titan-pilot-overview.png)
    
Special Functions
-----------------
In general the Artemis SDK functions work as explained in the Artemis SDK documentation.

##### Argument Return Values
Functions that take pointers for use as return values have been modified.

<table>
    <tr>
        <th>Function Name</th>
        <th>Example</th>
    </tr>
    <tr>
        <td><code>ArtemisGetImageData</code></td>
        <td>
            <code>
                return_code, x, y, w, h, bin_x, bin_y = ArtemisGetImageData(device_handle)
            </code>
        </td>
    </tr>
    <tr>
        <td><code>ArtemisGetSubframe</code></td>
        <td>
            <code>
                return_code, x, y, w, h = ArtemisGetSubframe(device_handle)
            </code>
        </td>
    </tr>
    <tr>
        <td><code>ArtemisGetBin</code></td>
        <td>
            <code>
                return_code, x, y = ArtemisBin(device_handle)
            </code>
        </td>
    </tr>
    <tr>
        <td><code>ArtemisColourProperties</code></td>
        <td>
            <code>
                return_code, colour_type, normal_offset_x, normal_offset_y,
                preview_offset_x, preview_offset_y = 
                ArtemisColourProperties(device_handle)
            </code>
        </td>
    </tr>
</table>

##### Type Conversion
Functions  whose return types are not inherently compatible with Python now have similarly-named wrapper functions.
<table>
    <tr>
        <th>Name/Source</th>
        <th>Return&nbsp;Type</th>
        <th>Example</th>
    </tr>
    <tr>
        <td>
            <code>
                <div>ArtemisDeviceName_pythonString</div>
                <div>ArtemisDeviceName</div>
            </code>
        </td>                
        <td><code>PyString</code></td>
        <td>
            <code>
                device_name = ArtemisDeviceName_pythonString(device_number)
            </code>
        </td>
    </tr>
    <tr>
        <td>
            <code>
                <div>ArtemisDeviceSerial_pythonString</div>
                <div>ArtemisDeviceSerial</div>
            </code>
        </td>                
        <td><code>PyString</code></td>
        <td>
            <code>
                device_serial = ArtemisDeviceSerial_pythonString(device_number)
            </code>
        </td>
    </tr>
    <tr>
        <td>
            <code>
                <div>ArtemisProperties_pythonDictionary</div>
                <div>ArtemisProperties</div>
            </code>
        </td>                
        <td><code>PyDict</code></td>
        <td>
            <code>
                device_properties = ArtemisProperties_pythonDictionary(device_handle)
            </code>
        </td>
    </tr>
    <tr>
        <td>
            <code>
                <div>ArtemisImageBuffer_pythonList</div>
                <div>ArtemisImageBuffer</div>
            </code>
        </td>                
        <td><code>PyList</code></td>
        <td>
            <code>
                device_serial = ArtemisImageBuffer_pythonList(device_handle)
            </code>
        </td>
    </tr>
<table>

##### Problematic Functions
The following functions are unimplemented, or not recommended.
<table>
    <tr>
        <th>Name</th>
        <th>Reason</th>
    </tr>
    <tr><td><code>ArtemisFTName</code></td><td>Deprecated</td></tr>
    <tr><td><code>ArtemisFTSerial</code></td><td>Deprecated</td></tr>
    <tr><td><code>ArtemisGetImageArray</code></td><td>Unknown behavior. Replaced by <code>ArtemisImageBuffer_pythonList</code></td></tr>
    <tr><td><code>ArtemisSendPeripheralMessage</code></td><td>Diagnostic method: currently unnecessary</code></td></tr>
    <tr><td><code>ArtemisIsLicensed</code></td><td>Diagnostic method: currently unnecessary</code></td></tr>
</table>
All of these methods may be implemented by modifying the <code>artemishsc.i</code>. For example, given <code>int example(float *response)</code>:
<div>
    <code>        
        <div>%apply int *OUTPUT { float *response};</div>
        <div>int example(float *response);</div>
    </code>
</div>

Files
-----
<table>
    <tr>
        <th>Filename</th>
        <th>Description</th>
    </tr>
    
    <tr><td><code>artemis.bat</code></td><td>Wrapper to execute <code>artemis.py<code></td></tr>
    <tr><td><code>artemis.py</code></td><td>Example Python script exercising the Artemis API (outputs <code>titan.fits</code>)</td></tr>
    <tr><td><code>artemishsc.i</code></td><td>The <a href="http://www.swig.org/">SWIG</a> interface file</td></tr>
    <tr><td><code>artemishsc.py</code></td><td>yyy</td></tr>
    <tr><td><code>artemishsc.pyc</code></td><td><i>Auto-generated by SWIG</i></td></tr>
    <tr><td><code>artemishsc_wrap.c</code></td><td><i>Auto-generated by SWIG</i></td></tr>
    <tr><td><code>ArtemisHscAPI.cpp</code></td><td>The Artemis SDK code (vendor provided)</td></tr>
    <tr><td><code>ArtemisHscAPI.h</code></td><td>The Artemis SDK header (vendor provided)</td></tr>
    <tr><td><code>build.bat</code></td><td>Builds the <code>lib/artemishsc.pyc</code> SWIG-generated Python library</td></tr>
    <tr><td><code>lib/</code></td><td>Output directory for the Python library build process</td></tr>
    <tr><td><code>README.md</code></td><td>Source for this document</td></tr>
    <tr><td><code>setup.py</code></td><td>Python setup script for the Python library build</td></tr>
    <tr><td><code>shared/</code></td><td>A collection of libraries required by the Artemis SDK</td></tr>
    <tr><td><code>stdafx.h</code></td><td>Placeholder for unneeded (but included) C header file</td></tr>
</table>

- - -

Reference
---------

+ [Atik Titan](http://www.atik-cameras.com/products/info/atik-titan)
+ [SWIG Home](http://www.swig.org/)
+ [Atik Cameras Downloads](http://www.atik-cameras.com/support/downloads)
+ [Artemis SDK C API](http://www.cypress.com/?docID=45181)
+ [Python 2.7](https://www.python.org/download/releases/2.7.7/)
+ [Minimalist GNU for Windows (MinGW)](http://www.mingw.org/)
+ [DS9 FITS Image Viewer](http://ds9.si.edu/site/Home.html)
+ [Anaconda Python (scipy/pyfits)](http://continuum.io/downloads)