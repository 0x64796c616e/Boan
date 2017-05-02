# Boan
Boan is an HTTP(s) proxy that allows for the modification of requests to aid in manual web application penetration testing


## Usage

Just run as a script:

$ python boan.py

or

$ chmod +x boan.py
$ ./boan.py

Above command runs the proxy on tcp/8080. To use another port, specify the port number in settings. Also in settings, you can black list filetypes or white list in-scope hosts.

## Enable HTTPS intercept

To intercept HTTPS connections, generate private keys and a private CA certificate:

$ ./setup_https_intercept.sh

With the proxy running, browse to http://boan.cert/ nd install the CA certificate in the browsers.



