import serial.tools.list_ports

from flask import Flask
app = Flask(__name__)


@app.route("/enable")
def enable():
    ser = serial.Serial('COM8', 9600, timeout=0)
    ser.write("Y")
    ser.close()
    return "enabled"

@app.route("/disable")
def disable():
    ser = serial.Serial('COM8', 9600, timeout=0)
    ser.write("N")
    ser.close()
    return "disabled"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9045, debug=False)