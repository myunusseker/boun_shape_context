import math
import sys
import signal
import random
import matplotlib.pyplot as plt
import numpy as np
import time
from shutil import copyfile
import copy
from pprint import pprint
import pickle

shapes_root = 'ShapeForceExperiment'

shapeCount = 100
sampleCount = 200

rings = 10
wedges = 20

def getShapeContextOfPoint(x,y,nextX,nextY):
    global samplePoints,sampleCount,rings,wedges,centerX,centerY

    centerAngle = math.degrees(math.atan2(nextY-y,nextX-x))
    #print centerX-x , centerY-y
    if centerAngle < 0:
        centerAngle+=360

    #print "Center Angle  is:",centerAngle

    maxDist = math.sqrt(2)

    shapeContext = [[0 for m in range(wedges)] for n in range(rings)]



    for i in range(sampleCount):
        vector = [samplePoints[i][0]-x,samplePoints[i][1]-y]
        dist = math.sqrt(vector[0]**2+vector[1]**2)
        #if dist == 0:
        #    continue
        angle = math.degrees(math.atan2(vector[1],vector[0]))

        if angle < 0:
            angle+=360
        #print "angle:",angle
        angle = angle - centerAngle
        if angle < 0:
            angle+=360
        r= int(math.log(dist+1)/(math.log(maxDist+1)/rings))
        w= int(angle/(360.0/wedges))

        if w == wedges:
            w = 0
        #print "VECTOR:",vector
        #print "\tangle: ",angle,"\t#wedgeBin:",w,"\tdist:",dist,"\tlogDist:",math.log(math.sqrt(vector[0]**2+vector[1]**2)+1),"\t#ringBin",r
        shapeContext[r][w] += 1

        ####





    return shapeContext


def dist2(p1,p2):
    return math.sqrt( (p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def sign(c1,c2):
    return 1 if c2[0]-c1[0] > 0 else -1

for i in range(1,shapeCount+1):
    print 'Sekil ID', i
    shf = open(shapes_root + '/shape' + str(i) + '/shape' + str(i) + '.txt' ,'r')
    cf = open(shapes_root + '/shape' + str(i) + '/corners.txt','r')

    N = int(cf.readline())

    corners = [[0 for x in range(2)] for y in range(N)]

    for j in range(N):

        cornersText = cf.readline().split()
        corners[j][0] = float(cornersText[0])
        corners[j][1] = float(cornersText[1])

    #print "Corners " , corners
    maxX = max(corners, key=lambda e: e[0])[0]
    maxY = max(corners, key=lambda e: e[1])[1]

    minX = min(corners, key=lambda e: e[0])[0]
    minY = min(corners, key=lambda e: e[1])[1]

    #print maxX, maxY ,minX , minY

    res_Y = 1.0
    res_X = 1.0

    shape_Y = (maxY-minY);
    shape_X = (maxX-minX)

    if shape_X/ shape_Y > 1.0:
        res_Y = shape_Y/shape_X
    else:
        res_X = shape_X/shape_Y

    #print res_X, res_Y

    centerY = - minY/shape_Y*res_Y
    centerX = - minX/shape_X*res_X

    #print "Window of this image is:", res_X, res_Y
    #print "Center of the image (y,x) will go to:", centerY, centerX

    for ii in range(N):
        corners[ii][1] = corners[ii][1] / shape_Y * res_Y - minY / shape_Y * res_Y
        corners[ii][0] = corners[ii][0] / shape_X * res_X - minX / shape_X * res_X

    edgeTotal = 0
    for j in range(N):
        edgeTotal += dist2(corners[j], corners[(j + 1) % N])
########################
    binSize = edgeTotal/sampleCount

    currentPoint = copy.deepcopy(corners[0])
    currentEdge = 0

    edgeDir = [0,0]
    edgeDir[1] = -(corners[0][1] - corners[1][1])
    edgeDir[0] = -(corners[0][0] - corners[1][0])

    enorm = math.sqrt(edgeDir[0]**2 + edgeDir[1]**2)

    edgeDir[1] *= binSize/enorm
    edgeDir[0] *= binSize/enorm
    currentEdgeLen = dist2(corners[0],corners[1])
    
    samplePoints = [[0 for x in range(2)] for y in range(sampleCount)]


    for j in range(sampleCount):
        currentEdgeLen -= binSize
        samplePoints[j] = copy.deepcopy(currentPoint)
        #print 'CUR:', j, samplePoints[j],

        nextPoint =  [ currentPoint[0] + edgeDir[0] , currentPoint[1] + edgeDir[1] ]
        #print 'NEXT?',nextPoint,


        if(currentEdgeLen < 0):
            #print 'DONMEK ISTEDI edgeLEN:', currentEdgeLen, j ,
            currentEdge = (currentEdge + 1) % N
            edgeDir[1] = -(corners[currentEdge][1] - corners[(currentEdge+1)%N][1])
            edgeDir[0] = -(corners[currentEdge][0] - corners[(currentEdge+1)%N][0])
            enorm = math.sqrt(edgeDir[0] ** 2 + edgeDir[1] ** 2)

            offset = [0,0]
            offset[0] =  edgeDir[0] * (-currentEdgeLen/enorm)
            offset[1] =  edgeDir[1] * (-currentEdgeLen/enorm)
            #print 'OFFSET',offset,

            edgeDir[1] *= binSize / enorm
            edgeDir[0] *= binSize / enorm


            currentEdgeLen = dist2(corners[currentEdge],corners[(currentEdge+1)%N]) + currentEdgeLen
            currentPoint[0] = corners[currentEdge][0] + offset[0]
            currentPoint[1] = corners[currentEdge][1] + offset[1]
            #print 'EKLEDI BU CIKTI:', currentPoint
        else:
            #print 'DONMUYOR', nextPoint
            currentPoint = copy.deepcopy(nextPoint)



    #for kk in range(sampleCount):
    #    print kk,samplePoints[kk],samplePoints[(kk+1)%sampleCount], dist2(samplePoints[kk], samplePoints[(kk+1)%sampleCount])


    
    """
    smp = np.array(samplePoints)
    crn = np.array(corners + [corners[0]])
    cx, cy = crn.T
    xx, yy = smp.T
    plt.axis('equal')
    plt.plot(cx, cy)
    plt.scatter(xx, yy)
    plt.scatter([0,0,1,1],[0,1,0,1])
    plt.scatter([centerX],[centerY])
    
    for i in range(rings+1):
        rad = i*math.log(math.sqrt(2)+1)/rings
        print math.e**rad-1
        circle3 = plt.Circle((corners[1][0], corners[1][1]), math.e**rad-1, color='g', fill=False)

        ax = plt.gca()
        # (or if you have an existing figure)
        # fig = plt.gcf()
        # ax = fig.gca(
        ax.add_artist(circle3)
    """
    for ix,c in enumerate(corners):

        sc = getShapeContextOfPoint(c[0], c[1],corners[(ix-1)%N][0],corners[(ix-1)%N][1])

        with open(shapes_root + '/shape' + str(i) + '/shapeContext'+ str(ix) + '.txt','wb') as fp:
            pickle.dump(sc,fp)

        pprint(sc)
        #plt.show()

        #with open('shapeContext' + str(ix) + '.txt', 'r') as fp2:
        #    asd = pickle.load(fp2)
        #    print "Picle"
        #    pprint(asd)

