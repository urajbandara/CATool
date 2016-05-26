from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
import random
import numpy
import time
from numpy import random as rnd
from array import array


class Grid(object):
	ref = [[64,32,16], [128,256,8], [1,2,4]]
	def __init__( self, m ):
		self.m = m
		self.rows = len(m)
		self.columns = len(m[0])
                #print(self.rows)
                #print(self.columns)
	def get_neighbour_rule ( self, i, j ):
		'''
			treats the grid as a torus... so the neighbours of the pixels at the edges are the ones on the opposite edges
		'''
		x = 0
		for r in range(-1,2):
			for s in range(-1,2):
				row = i + r 
				if row >= self.rows:
					row = row - self.rows
				column = j + s
				if column >= self.columns:
					column = column - self.columns
				if self.m[row][column] != 0:
					x += Grid.ref[r+1][s+1]
		return x
	
	def get_neighbour_opinion_sum ( self, i, j):
		x=0
		y=0
		#print("i-" + str(i) + "j-" + str(j))
		if i < self.rows - 1:
			x += self.m[i+1][j]
			y += 1
		x += self.m[i-1][j]
		y += 1
		if j < self.columns - 1:
			x += self.m[i][j+1]
			y += 1
		x += self.m[i][j-1]
		y += 1
		x += self.m[i][j]
		y += 1
		#for r in range(-1,2):
			#for s in range(-1,2):
				#row = i + r
				#if row < self.rows:
					#row = i
					#column = j + s
					#if column < self.columns:
						#column = j
						#x += self.m[row][column]
				#print(self.m[row][column])
		x=x/y
		return x
	def get_neighbour_opinion_density ( self, i, j):
		x=0
		status = self.m[i][j]
		#print("i-" + str(i) + "j-" + str(j))
		if i < self.rows - 1 and j < self.columns - 1:
                         for r in range(-1,2):
                                for s in range(-1,2):
                                        if r != 0 or s != 0:
                                                y = self.m[i+r][j+s]
                                                if y == status:
                                                        x += y
		return x
	
	def get_neighbour_life( self, i, j):
		x=0
		#print("i-" + str(i) + "j-" + str(j))
		if i < self.rows - 1 and j < self.columns - 1:
			x += self.m[i-1][j+1]
			x += self.m[i][j+1]
			x += self.m[i+1][j+1]
			x += self.m[i-1][j]
			#x += self.m[i][j]
			x += self.m[i+1][j]
			x += self.m[i-1][j-1]
			x += self.m[i][j-1]
			x += self.m[i+1][j+1]
		#x += self.m[i][j]
		#for r in range(-1,2):
			#for s in range(-1,2):
				#row = i + r
				#if row < self.rows:
					#row = i
					#column = j + s
					#if column < self.columns:
						#column = j
						#x += self.m[row][column]
				#print(self.m[row][column])
		return x
        def get_neighbour_state(self,i,j):
                return self.m[i][j]
        
	def __getitem__( self, i ):
		return self.m[i+1][1:self.m.shape[1]-1]
	
	def __str__(self):
		return g.m.__str__()
	
class cellular_automata(object):
	def __init__ ( self, rule_set ):
		self.ruleset = set(rule_set)

	def apply ( self, g, n=1 ):
		for t in range(0,n):
                        #print(n)
			time.sleep(1)
			for i in xrange( 0, g.rows):
				for j in xrange( 0, g.columns):
					#rule = g.get_neighbour_rule(i,j)
					opinionsum = g.get_neighbour_opinion_sum(i,j)
					if opinionsum < 0.33:
						g.m[i][j] = 0
                                        elif opinionsum >= 0.33 and opinionsum < 0.66:
                                                g.m[i][j] = 0.5
                                        elif opinionsum >= 0.66:
                                                g.m[i][j] = 1
					

args = set(sys.argv)
print('Initializing ...')

if ( "-h" in args ):
	print ('Usage:')
	print ('\t%s [options]'%(sys.argv[0]))
	print ('\n\tOPTIONS:')
	print ('\n\t\t-d\t\tDefault initialization of rules')
	print ('\n\t\t-h\t\tDisplays this message')
	print ('\n\t\t-a\t\tAnimates the evolution')
	print ('\n\t\t-l\t\tGame of life')
	print ('\n\t\t-sn\t\tcyber sn effect')
	print ('\n\t\t-f\t\tload initial configuration from file')
	sys.exit()

if "-d" in args :
	sz = 50
	ruleset = [random.randint(0,511) for x in range(30)]
	print('Rules are:', ruleset)
	args.remove("-d")
else:
	print('Enter size of grid:')
	try:
		sz = int(raw_input())
	except:
		sz = 50

	print('Enter Rules:(integers all < 512) ')
	s = raw_input()

	try:
		ruleset = [ int(x) for x in s.split() ]
		if len(ruleset) == 0:
			ruleset = [random.randint(0,511) for x in range(30)]
			print('Rules are:', ruleset)
	except:
		print('Wrong format seperate integers with single space...')
		ruleset = [random.randint(0,511) for x in range(30)]
		print('Rules are:', ruleset)

auto = False
life = False
sn = False
generation = 0
if "-a" in args:
	#auto mode
	auto = True
if "-l" in args:
        life =True
elif "-sn" in args:
        sn = True

f=open('init.txt','r')
tarray = []
for line in f:
        tarray.append([int(x) for x in line.split()])
sz = len(tarray)
state=numpy.zeros(shape=(sz,sz))
if "-f" in args:
        for r in range(len(tarray)):
                for c in range(len(tarray[0])):
                        state[r][c] = tarray[r][c]
else:
        state = rnd.rand(sz,sz)
        bstate=numpy.zeros(shape=(sz,sz))
        #for r in range(0,sz):
                #for s in range(0,sz):
                        #if bstate[r][s] < 0.33333333:
                                #state[r][s] = 0
                        #elif bstate[r][s] >= 0.33333333 and bstate[r][s] < 0.66666666:
                                #state[r][s] = 0.5
                        #else:
                        #state[r][s] = bstate[r][s]
        
        
#state = [ map(int,line) for line in f]
#print(tstate[0][3])
#print(tstate)
#bstate = rnd.rand(sz,sz)>0.5
#state=numpy.zeros(shape=(sz,sz))
#for r in range(0,sz):
#        for s in range(0,sz):
#                if bstate[r][s]>0.5:
#                        state[r][s] = 1
#                else:
#                        state[r][s] = 0
                #print(state[r][s])

#the code below is not working atleast on my computer...
#state = [[False]*sz]*sz
#for i in range(0,sz):
#	for j in range(0,sz):
#		if random.randint(0,1) == 1 :
#			state[i][j] = True
#		else:
#			state[i][j] = False

g = Grid(state)
ca = cellular_automata(ruleset)

def display_state():
	xstart = 0.2
	ystart = 0.2
	delta = 0.6/(sz-1)
	glPointSize(5)
	glColor3f(0,0,0)
	glBegin(GL_POINTS)
	#print(state)
	for i in range(0,sz):
		for j in range(0,sz):                   
			if state[i][j] < 0.33 :
				glColor3f(0,1.0,0)
			elif state[i][j] >= 0.33 and state[i][j] < 0.66:
				glColor3f(1.0,1.0,0)
			elif state[i][j] >= 0.66:
				glColor3f(1.0,0,0)                      
			glVertex2d(xstart + i*delta, ystart + j*delta)
	glEnd()
#	glFlush()

def next_state():
	ca.apply(g)
        #generation +=1
        #print(generation)
        
def display(*args):
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)
	display_state()
	glFlush()
	

def idleFunc(*args):
        global generation
        generation += 1
        glutSetWindowTitle('Cellular Automata (Generation-' + str(generation)+ ')')
	next_state()
	display()
	

def mouse(button,state,x,y):
        if (state == GLUT_UP):
                global generation
                generation += 1
                #print(generation)
                glutSetWindowTitle('Cellular Automata (Generation-' + str(generation)+ ')')
                next_state()
                display()
                print(state)
	#generation +=1

def setup_viewport():
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)

def reshape(w,h):
	glViewport(0,0,w,h)
	setup_viewport()

def key(*args):
	print('Bye! :)')
	sys.exit()

def main():
        
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGB)
	glutInitWindowSize(500,500)
	glutCreateWindow('Cellular Automata')
	setup_viewport()
	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	if auto:
		glutIdleFunc(idleFunc)
	glutKeyboardFunc(key)
	glutMouseFunc(mouse)
	glutMainLoop()

main()
