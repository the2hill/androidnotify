This set of scripts creates a blinking notification for weechat.

A Teensy/Arduino board controls LEDs (in this case installed in an Android figurine) and listens on the hosts computer comport. Utilizing the andronoitif.py and the setup.py a Windows based application can be created. This application host the Flask webserver waiting for notification updates from the weechat client. 

The andronotif-weechat file must be installed in the .weechat/python/autoload directory. The weechat code can also do serial communication directly with an update to enable/disable led methods. This way you can run locally and not via Windows. 

http://www.py2exe.org/

python setup.py py2exe
