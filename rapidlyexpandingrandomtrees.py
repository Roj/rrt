import random
import math
import pyglet #1.2alpha1

start = (0,0)
goal = (9,7)

space = (10,9)
vertices = [start]
edges = []
obstacles = []

wWidth = 640
wHeight = 480

iterations = 100

def pointCollides(point):
	global obstacles
	#todo later
	return False
def cFreeRandom():
	global space
	point = (random.random() * space[0], random.random() * space[1])
	collides = pointCollides(point)
	#boobies
	while collides:
		point = (random.random() * space[0], random.random() * space[1]	)
		collides = pointCollides(point)
	print(point)
	return point
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
def findPointInLine(pointA,pointB,dist):
	#we need to find a point in the line that is maxDistance of dist
	#so we use the versor from A to B, multiplied by maxDistance
	#i dont know operable arrays/matrix in python - fix this later
	versorX = pointB[0]-pointA[0]
	versorY = pointB[1]-pointA[1]
	modulus = distance((0,0),(versorX,versorY))
	#modulus will always be float, so this division is right
	versorX = versorX / modulus
	versorY = versorY / modulus

	#print((versorX,versorY))
	pointB = (versorX * dist + pointA[0], versorY * dist + pointA[1])
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
	while (not found) and (i < len(edges)):
		if edges[i][1] == vertex:
		   found = True
		else: i=i+1
	return i
def getClosestConfig(pointA,pointB,edges,vertices):
	#our robot can not turn immediately
	#so the deviation angle cant be more than 30deg
	maxDeviation = 90*math.pi/180
	maxDistance = 1 #arbitrary as fuck
	#computation of deviation
	#variables renamed here for ease of understanding
	start = vertices[getParentVertex(getVertexID(pointA,vertices),edges)]
	middle = pointA
	end = pointB
	DeltaX1 = end[0] - middle[0]
	DeltaY1 = end[1] - middle[1]

	DeltaX0 = middle[0] - start[0]
	DeltaY0 = middle[1] - start[1]
	deviation = math.atan2(DeltaX1,DeltaY1) - math.atan2(DeltaX0,DeltaY0)
	
	if maxDistance < distance(pointA,pointB):
		pointB = findPointInLine(pointA,pointB,maxDistance)
	#now we need to check for deviation, this one's a little harder

	if abs(deviation) > maxDeviation:
		deviation = abs(deviation)/deviation * maxDeviation # sgn(deviation) * mD
		if(DeltaX0 != 0):
			direction = (1, math.tan(deviation) + DeltaY0/DeltaX0 )
		else:
			direction = (1, math.tan(deviation))
		pointB = findPointInLine(pointA,direction + pointA, distance(pointA,pointB))
	return pointB    

def lineCollides(pointA,pointB):
	return False # lel, there are no obstacles for now
def makeEdge(pointA,pointB,vertices):
	idA = getVertexID(pointA,vertices)
	idB = getVertexID(pointB,vertices)
	return (idA,idB)

print
for i in range(1,iterations):
	randPoint = cFreeRandom()
	closestVertex = getClosestVertex(vertices,randPoint)
	closestConfig = getClosestConfig(closestVertex,randPoint,edges,vertices)

	if not lineCollides(closestVertex,closestConfig):
		vertices.append(closestConfig)
		edges.append(makeEdge(closestVertex,closestConfig,vertices))

window = pyglet.window.Window(wWidth,wHeight)
label = pyglet.text.Label('Rapidly-expanding random trees test (RRT)',
	font_name='Arial',
	font_size=12,
	x=window.width//2,
	y=window.height-30,
	anchor_x='center',
	anchor_y='center')
allPoints = ()
allEdges = []
for j in range(0,len(vertices)):
	allPoints = allPoints + (int(vertices[j][0] * 64),int(vertices[j][1] * 48))	
for j in range(0,len(edges)):
	allEdges = allEdges + [edges[j][0],edges[j][1]]
print(allEdges)

@window.event
def on_draw():
	global allPoints, allEdges, edges, vertices
	window.clear()
	label.draw()
	
	pyglet.graphics.draw(len(vertices),pyglet.gl.GL_POINTS,('v2i',allPoints))
	pyglet.graphics.draw_indexed(len(vertices),pyglet.gl.GL_LINES,allEdges,('v2i',allPoints))



pyglet.app.run()


#for i in range(0,len(edges)):
	#print(edges[i])
#now we are pretty sure that we got to the goal
#endPoint = getGoalPoint(goal,vertex)
#bestPath = [endPoint]
#currentPoint = getVertexId(endPoint)
#i=len(edges)-1
#while currentPoint != 0:
	#if currentPoint==edges[i][1]:
		#bestPath.append(currentPoint)
		#currentPoint=edges[i][0]
#		i=i-1
#bestPath=bestPath[::-1]

