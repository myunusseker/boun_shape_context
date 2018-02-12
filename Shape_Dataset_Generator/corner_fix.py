shapeCount = 100
shapes_root = 'ShapeForceExperiment'

for i in range(1,shapeCount+1):
    shf = open(shapes_root + '/shape' + str(i) + '/shape' + str(i) + '.txt' ,'r')
    cf = open(shapes_root + '/shape' + str(i) + '/corners.txt','w')
    expFile = open(shapes_root + '/shape' + str(i) + '/output-' + str(i) + '-' + str(0) + '-' + str(0) + '.txt', 'r')

    shape_id = int(shf.readline())
    N = int(shf.readline())

    corners = [[0 for x in range(2)] for y in range(N)]

    for j in range(N):

        cornersText = shf.readline().split()
        corners[j][0] = float(cornersText[0])
        corners[j][1] = float(cornersText[1])

    forceLine = expFile.readline().split()
    noktalar = expFile.readline().split()

    supCount = int(noktalar[0])
    if supCount == 0:
        print 'No support for shape ' + str(i)
        continue

    cornerLine = expFile.readline().split()

    c_id = int(cornerLine[0])
    corner_pts = [float(cornerLine[1]),float(cornerLine[2]) ]

    corner_diff_x = corner_pts[0] - corners[c_id][0];
    corner_diff_y = corner_pts[1] - corners[c_id][1];

    cf.write(str(N) + '\n')
    for j in range(N):

        corners[j][0] += corner_diff_x
        corners[j][1] += corner_diff_y

        cf.write(str(corners[j][0]) + ' ' + str(corners[j][1]) + '\n')

    cf.close()
    shf.close()
    expFile.close()