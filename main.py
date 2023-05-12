
from flask import Flask, render_template, Response,jsonify
from camera import VideoCamera
import RPi.GPIO as GPIO
import serial,time ,random
import json
app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0',115200,timeout=4)
value1=0
value2=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN)
@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/data',methods=['POST','GET'])
def data():
    time.sleep(2)
    led= False
    if GPIO.input(5)==GPIO.HIGH:
        led=True
    else:
            led=False 
    global lat,long,temparature,humidity,prevhu,prevt,prevlat,prevlong,prevcpm,prevnSv,nSv        
    if ser.in_waiting > 0:
        global jsonData
        
        jsonString = ser.readline().decode('utf-8').rstrip()

        try:
            jsonData = json.loads(jsonString)
        except json.decoder.JSONDecodeError:
                print("Failed to parse JSON")
        humidity = jsonData["humidity"]
        temparature = jsonData["temparature"]
        lat=jsonData["lat"]
        long=jsonData["long"]
        cpm=jsonData["cpm"]
        nSv=jsonData["nSv"]
        avg_h2s=jsonData["average_of_h2s"]
        avg_co=jsonData[" average_of_co "]
        alt=jsonData["alt"]
        prevlat =lat
        prevlong=long
        prevhu= humidity
        prevt= temparature
        prevcpm=cpm
        prevnSv=nSv
    # store the variable and process it further as needed
        print(f"humidity: { humidity}, temparature: {temparature},lat:{lat},long:{long}")
        print (temparature) 
        return jsonify({'humidity':humidity,'temparature':temparature,'lat':lat,'long':long,'cpm':cpm,'nSv':nSv,'avg_h2s':avg_h2s,'avg_co':avg_co,'alt':alt,'status':led})
    else:
        print(f"humidity::{prevhu},temparature:{prevt},lat:{prevlat},long:{prevlong}")
        return jsonify({'humidity':prevhu,'temparature':prevt,'lat':prevlat,'long':prevlong,'cpm':prevcpm,'nSv':prevnSv,'avg_h2s':0,'avg_co':0,'alt':0,'status':'false'})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000',debug=True)
