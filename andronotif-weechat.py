import requests
import serial
import time

# script variables
SCRIPT_NAME = "andronotify"
SCRIPT_AUTHOR = "ptoohill"
SCRIPT_VERSION = "0.0.1"
SCRIPT_LICENSE = "GPL"
SCRIPT_DESC = "Send signal to Teensy to light up Android figurine " \
              "when hilighted or private message."

HOST="70.121.140.185"
PORT="9001"

# make sure we're run under weechat.
import_ok = True
try:
    import weechat
except ImportError:
    print "This script must be run under WeeChat."
    print "Get WeeChat now at: http://www.weechat.org/"
    import_ok = False

# script options
settings = {
}

state = 'N'


# Functions
def disable_led(data, signal, signal_data):
    global state
    if state != 'N':
        weechat.prnt("Disabling LED: ", "Disable LED...")
        send_rest_message('N')
        state = 'N'
    return weechat.WEECHAT_RC_OK


def enable_led(data, bufferp, uber_empty, tagsn, isdisplayed, ishilight,
               prefix, message):
    global state
    mynick = weechat.buffer_get_string(bufferp,"localvar_nick")
    # Verify it was a private message and we are not the sender.
    if state == 'N':
        if weechat.buffer_get_string(bufferp,
               "localvar_type") == "private" and weechat.buffer_get_string(
                bufferp, "localvar_nick") != prefix:
            send_rest_message('Y')
            state = 'Y'
        if int(ishilight):
            (weechat.buffer_get_string(bufferp, "short_name") or
                    weechat.buffer_get_string(bufferp, "name"))
            send_rest_message('Y')
            state = 'Y'
    else:
        weechat.prnt("", "LED is already active, ignoring...")
    return weechat.WEECHAT_RC_OK


def send_serial_message(data):
    try:
        weechat.prnt("", "Trying to connect to serial... ")
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        arduino.write(data)
        weechat.prnt("", arduino.readline())
    except Exception as e:
        weechat.prnt("", 'Failed to communicate via serial')
        weechat.prnt("", e)


def send_rest_message(data):
    try:
        weechat.prnt("Connecting:", "Trying to connect to endpoint... ")
        option = 'enable' if data == 'Y' else 'disable'
        r = requests.get("http://{host}:{port}/{option}".format(
            host=HOST, port=PORT, option=option))
        weechat.prnt("Sent request for {data}, status: ".format(data=data),
                     str(r.status_code))
    except Exception as e:
        weechat.prnt("", 'Failed to communicate via rest endpoint')
        weechat.prnt("", e)

if __name__ == "__main__":
    if import_ok and weechat.register(
            SCRIPT_NAME, SCRIPT_AUTHOR,SCRIPT_VERSION, SCRIPT_LICENSE,
            SCRIPT_DESC, "", ""):
        # Init everything
        for option, default_value in settings.items():
            if weechat.config_get_plugin(option) == "":
                weechat.config_set_plugin(option, default_value)
        # Hook privmsg
        weechat.hook_print("", "irc_privmsg", "", 1, "enable_led", "")
        # Hook signal, this tells us user responded to weechat
        hook = weechat.hook_signal("input_text_changed", "disable_led", "")
