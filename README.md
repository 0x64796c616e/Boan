# Boan
Boan is an HTTP(s) proxy that allows for the modification of requests to aid in manual web application penetration testing

## Installation

Clone the github repo. The only dependency is the PyQt5 bindings for Python 3, which is installed by default on OSX. On Linux they can be installed with:
```
 $ sudo apt-get install python3-pyqt5
```
See https://wiki.qt.io/Language_Bindings for other help.

## Usage
Just run as a script:
```
 $ python boan.py
```
or
```
 $ chmod +x boan.py
 $ ./boan.py
```
The above command runs the proxy on tcp/8080 by default. To use another port, specify the port number in settings. Also in settings, you can black list filetypes or white list in-scope hosts.

Set your default network manager to use the proxy on the specified port. On Linux: Network --> Network Proxy --> Manual

![netowrk instalation](http://i63.tinypic.com/2i1321f.png)

... and proxy away! Feel free to try my demonstration web form at http://demofire.000webhostapp.com/ or test your penetration testing skills on http://testfire.net/.

![boan running](http://i67.tinypic.com/2nh1fn6.png)

## Enable HTTPS intercept

To intercept HTTPS connections, generate private keys and a private CA certificate:

 $ ./setup_https_intercept.sh

With the proxy running, browse to http://boan.cert/ and install the CA certificate in the browsers.

![cert example](http://i65.tinypic.com/vr8rc4.png)




