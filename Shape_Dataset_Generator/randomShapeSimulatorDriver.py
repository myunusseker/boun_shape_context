import math
import sys
import signal
import random
import matplotlib.pyplot as plt
import numpy as np
import rospy
import time
from shutil import copyfile
from std_msgs.msg import Int32
from std_msgs.msg import Bool

def callback(data):
	global simulationState
	simulationState = data.data

def dist2(a,b,c,d):
	return math.sqrt((a-c)**2+(b-d)**2)


def createRandomShape(iterationTime):
	global N,points
	N = random.randint(3,10)
	r = 0.1
	threshold = 0.3/N
	points=np.zeros((N,3))
	for i in range(N):
		flag = True
		while flag:
			x = random.random()*2*r-r
			y = math.sqrt(r**2 - x**2)
			if random.random() > 0.5:
				y*=-1
			flag = False
			for j in range(i):
				if dist2(x,y,points[j][0],points[j][1]) < threshold:
					flag = True
					break
		points[i][0] = x
		points[i][1] = y
		points[i][2]=math.atan2(points[i][1],points[i][0])/math.pi*180

	points = points[points[:,2].argsort()]
	f = open('shape.txt','w')
	f.write(str(iterationTime+1)+"\n")
	f.write(str(N)+"\n")
	for i in range(N):
		f.write(str(points[i][0])+" "+str(points[i][1])+"\n")
	for i in range(N-2):
		f.write(str(0)+" "+str(i+1)+" "+str(i+2)+"\n")
	for i in range(N-2):
		f.write(str(N)+" "+str(i+N+2)+" "+str(i+N+1)+"\n")
	for i in range(N-1):
		f.write(str(i)+" "+str(i+N)+" "+str(i+1+N)+"\n")
		f.write(str(i)+" "+str(i+1+N)+" "+str(i+1)+"\n")
	f.write(str(N-1)+" "+str(2*N-1)+" "+str(N)+"\n")
	f.write(str(N-1)+" "+str(N)+" "+str(0)+"\n")
	f.close()
	copyfile('shape.txt','ShapeForceExperiment/shape'+str(iterationTime+1)+'/shape'+str(iterationTime+1)+'.txt')

def startSimulation():
	global start,rate,true
	for i in range(5):
		start.publish(true)
		rate.sleep()


def stopSimulation():
	global stop,rate,true
	stop.publish(true)
	rate.sleep()

def sigint_handler(signal, frame):
	print 'INTERRUPTED'
	stopSimulation()
	sys.exit(0)


N = 0 
points = 0
true = Bool()
true.data = True
simulationState = -1
iterationTime = 5
shapeNumber = 100
start = rospy.Publisher('/startSimulation', Bool, queue_size=10)
stop = rospy.Publisher('/stopSimulation', Bool, queue_size=10)
rospy.init_node('shapeExperimentPython')
rate = rospy.Rate(10)
rospy.Subscriber("/simulationState", Int32, callback)



signal.signal(signal.SIGINT, sigint_handler)
stopSimulation()

for i in range(shapeNumber):
	createRandomShape(i);
	for j in range(N):
		x1 = points[j][0]
		y1 = points[j][1]
		x2 = points[(j+1)%N][0] 
		y2 = points[(j+1)%N][1]
		for k in range(iterationTime):
			rX = random.random()*(x2-x1)+x1
			rY = ((y2-y1)/(x2-x1))*(rX-x1)+y1
			ff = open("force.txt","w");
			ff.write(str(j)+" "+str(k)+"\n"+str(rX)+" "+str(rY)+"\n")
			ff.close()
			while(simulationState != 0):
				i=i
			startSimulation()
			while(simulationState != 2):
				i=i
			stopSimulation()





