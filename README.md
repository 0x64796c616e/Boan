# Boan
Boan is an HTTP(s) proxy that allows for the modification of requests to aid in manual web application penetration testing

## Usage

Clone the github repo. The only dependencies are the QT bindings for Python 3, which are installed by default on OSX. On Linux they can beinstalled with:
```
 $ sudo apt-get install python3-pyqt5
```
Just run as a script:
```
 $ python boan.py
```
or
```
 $ chmod +x boan.py
 $ ./boan.py
```
The above command runs the proxy on tcp/8080. To use another port, specify the port number in settings. Also in settings, you can black list filetypes or white list in-scope hosts.

Set your default network manager to use the proxy on the specified port. On Linux: Network --> Network Proxy --> Manual

![netowrk instalation](http://i63.tinypic.com/2i1321f.png)

## Enable HTTPS intercept

To intercept HTTPS connections, generate private keys and a private CA certificate:

 $ ./setup_https_intercept.sh

With the proxy running, browse to http://boan.cert/ and install the CA certificate in the browsers.





