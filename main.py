
from flask import Flask, render_template, Response,jsonify
from camera import VideoCamera
import RPi.GPIO as GPIO
import serial,time ,random
import json
app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM1',115200,timeout=4)
GPIO.setmode(GPIO.BCM)


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
    GPIO.setup(5,GPIO.IN,GPIO.PUD_DOWN)
    global lat,long,temparature,humidity,prevhu,prevt,prevlat,prevlong,prevcpm,prevnSv,nSv,prevstatus,status 
    time.sleep(2)
    status= False
    if (GPIO.input(5)==GPIO.HIGH):
         status=True
         print("yes")
    else:
         status=False 
         
    if ser.in_waiting > 0:
        global jsonData
        
        jsonString = ser.readline().decode('utf-8').rstrip()

        try:
            jsonData = json.loads(jsonString)
        except json.decoder.JSONDecodeError:
                print("Failed to parse JSON")
        humidity = jsonData["humidity"]
        temparature = jsonData["temperature"]
        lat=jsonData["lat"]
        long=jsonData["long"]
        cpm=jsonData["cpm"]
        nSv=jsonData["nSv"]
        avg_h2s=jsonData["h2sppm"]
        avg_co=jsonData["coppm"]
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
        return jsonify({'humidity':humidity,'temparature':temparature,'lat':lat,'long':long,'cpm':cpm,'nSv':nSv,'avg_h2s':avg_h2s,'avg_co':avg_co,'alt':alt,'status':status})
    else:
        print(f"humidity::{prevhu},temparature:{prevt},lat:{prevlat},long:{prevlong}")
        return jsonify({'humidity':prevhu,'temparature':prevt,'lat':prevlat,'long':prevlong,'cpm':prevcpm,'nSv':prevnSv,'avg_h2s':0,'avg_co':0,'alt':0,'status':status})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000',debug=True)
