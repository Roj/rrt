import random
import math
import pyglet #1.2alpha1



vertices = [(0,0)]
edges = []

def cFreeRandom():
    return (random.random() * 10, random.random() * 10)
def distance(pointA,pointB):
    #euclidean distance
    #fuck efficiency
    return math.sqrt( (pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2 )

def getClosestVertex(vertices,point):
    minDistance = distance(vertices[0],point)
    minID = 0
    for i in range(1,len(vertices)):
        currentDist = distance(vertices[i],point)
        if(currentDist < minDistance):
            minDistance = currentDist
            minID = i
    return vertices[minID]
def findPointInLine(pointA,pointB,maxDistance):
    #we need to find a point in the line that is maxDistance of dist
    #so we use the versor from A to B, multiplied by maxDistance
    #i dont know operable arrays/matrix in python - fix this later
    versorX = pointB[0]-pointA[0]
    versorY = pointB[1]-pointA[1]
    modulus = distance((0,0),(versorX,versorY))
    #modulus will always be float, so this division is right
    versorX = versorX / modulus
    versorY = versorY / modulus
    pointB = (versorX * maxDistance + pointA[0], versorY * maxDistance + pointB[0])
    return pointB
def getVertexID(vertex,vertices):
    found = False
    i=0
    while (not found) and (i<=len(vertices)):
        if vertices[i] == vertex:
            found = True
        else: i=i+1
    return i
def getParentVertex(vertex,edges):
    found = False
    i=0
    while (not found) and (i <= len(edges)):
        if edges[i][1] == vertex:
           found = True
        else: i=i+1
    return i
def getClosestConfig(pointA,pointB,edges,vertices):
    #our robot can not turn immediately
    #so the deviation angle cant be more than 30deg
    maxDeviation = 30*math.pi/180
    maxDistance = sqrt(2) #arbitrary as fuck

    #computation of deviation
    #variables renamed here for ease of understanding
    start = vertices[getParentVertex(getVertexID(pointA,vertices),edges)]
    middle = pointA
    end = pointB
    deviation = math.atan2(end[0] - middle[0],end[1] - middle[1]) - math.atan2(middle[0] - start[0],middle[1] - start[1])
    
    if maxDistance < distance(pointA,pointB):
        pointB = findPointInLine(pointA,pointB,maxDistance)
    #now we need to check for deviation, this one's a little harder
    if abs(deviation) > maxDeviation:
        direction = (1, math.tan(deviation))
        pointB = findPointInLine(pointA,direction, distance(pointA,pointB))
    return pointB    

def lineCollides(pointA,pointB):
    return False # lel, there are no obstacles for now

for i in range(1,10):
    randPoint = cFreeRandom()
    closestVertex = getClosestVertex(vertices,randPoint)
    closestConfig = getClosestConfig(closestVertex,randPoint,edges,vertices)

    if not lineCollides(closestVertex,closestConfig):
        vertices.append(closestConfig)
        edges.append(makeEdge(closestVertex,closestConfig))
