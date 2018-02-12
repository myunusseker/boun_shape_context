import numpy as np
import math
import pickle
import random
import matplotlib.pyplot as plt
import csv
from pprint import pprint

shapes_root = 'ShapeForceExperiment'

shapeCount = 100
expCount = 5

supsup = 0;

training_features = []
training_labels = []
for i in range(1,shapeCount+1):
    shf = open(shapes_root + '/shape' + str(i) + '/shape' + str(i) + '.txt' ,'r')
    cf = open(shapes_root + '/shape' + str(i) + '/corners.txt','r')
    N = int(cf.readline())
    shapeMultiplier = 3 * random.random() + 1
    corners = [[0 for xx in range(2)] for yy in range(N)]
    for c in range(N):
        cornerLine = cf.readline().split()

        corners[c][0] = shapeMultiplier * float(cornerLine[0])
        corners[c][1] = shapeMultiplier * float(cornerLine[1])
    for j in range(N):

        for e in range(expCount):

            expFile = open(shapes_root + '/shape' + str(i) + '/output-'+str(i)+'-'+str(j)+'-'+str(e)+'.txt', 'r')
            forceLine = expFile.readline().split()
            f = [0,0]
            f[0] = shapeMultiplier * float(forceLine[0])
            f[1] = shapeMultiplier * float(forceLine[1])
            #f.append(1)

            supCount = int(expFile.readline())

            if(supCount != 2 ):
                supsup +=1
                continue

            supPointIds = [0 for xx in range(N)]

            for k in range(supCount):
                sid = int(expFile.readline().split()[0])
                supPointIds[sid] = 1

            for c in range(N):

                nc = (c-1)%N

                train_sample = []
                train_sample.extend([i, N , j, e])

                #Find rotation
                rotAngle = -(math.atan2(corners[nc][1] - corners[c][1], corners[nc][0] - corners[c][0])-math.pi/2)
                transVec = np.array([-corners[c][0],-corners[c][1]])

                #f = [3,3]
                #rotAngle = -math.pi/4;
                #transVec = np.array([-1, -1])

                Rot_mat = np.array([[math.cos(rotAngle),-math.sin(rotAngle)],[math.sin(rotAngle),math.cos(rotAngle)]])

                F_hom = (np.array([f]) + transVec).transpose()

                F_rel = np.matmul(Rot_mat,F_hom)
                #print 'M is ', Rot_mat
                #print 'F is ', F_hom
                #print 'Translated F', F_rel
                #plt.scatter([corners[c][0], corners[nc][0]], [corners[c][1], corners[nc][1]])
                #plt.hold()
                #plt.scatter([F_hom[0]],[F_hom[1]])

                train_sample.extend([float(F_rel[0]),float(F_rel[1])])
                #train_sample.extend( [corners[c][0], corners[c][1]] )

                fp = open(shapes_root + '/shape' + str(i) + '/shapeContext' + str(c) + '.txt','r')
                shape_context = pickle.load(fp)
                flat_shape_context = sum(shape_context, [])
                train_sample.extend(flat_shape_context)
                training_features.append(train_sample)
                training_labels.append(supPointIds[c])


#pprint(training_features)
#pprint(training_labels)



print len(training_labels)
print len(training_features[0])

with open("shape_data_FORCE_Multiplied.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(training_features)




with open("shape_labels_FORCE_Multiplied.csv", "wb") as f:
    for c in training_labels:
        f.write(str(c) + "\n")
    f.close()

print supsup