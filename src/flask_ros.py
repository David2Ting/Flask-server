#! /usr/bin/env python

import os
import rospy
import threading

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from std_msgs.msg import UInt32
from std_msgs.msg import Int32
def ros_callback(msg):
    print(msg)

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')
threading.Thread(target=lambda: rospy.init_node('example_node', disable_signals=True)).start() #Used to create a node in a non-interfering way
rospy.Subscriber('/listener', Int32, ros_callback) #Create subscriber
pub = rospy.Publisher('/talker', Int32, queue_size=10) #Create publisher

app = Flask(__name__,template_folder=template_path) #Create app and specify template 
socketio = SocketIO(app)  #Establish socket-io server

#Listens for driveEvent signal across socket io
@socketio.on('driveEvent')
def drive_cmd(message):
    print(message['RPM'])
    msg = Int32()
    msg.data = message['RPM'] #Publishes RPM key of the message dictionary
    pub.publish(msg)


@app.route('/') #Routes the home director to 
def home():

    return render_template('index.html') #Uses the pre-made frontend


if __name__ == '__main__':
    app.run(port=5000)
