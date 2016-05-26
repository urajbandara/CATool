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
	
class social_network(object):
        def __init__( self,num):
                self.n = []
                self.number = num
        def get_network_opinion( self, g):
                opsum =0.0
                #rnd.randint(0,high=10)
                #x=0.0
                #print(self.number)
                if self.number == 1:
                        f=open('net1.txt','r')
                        tarray = []
                        for line in f:
                                tarray.append([int(x) for x in line.split()])
                        rows = len(tarray)
                        cols = len(tarray[0])
                        self.n=numpy.zeros(shape=(rows,cols),dtype=numpy.int)
                        for r in range(len(tarray)):
                                for c in range(len(tarray[0])):
                                        self.n[r][c] = tarray[r][c]
                                q = tarray[r][0]
                                y = tarray[r][1]
                                type(q)
                                opsum += g.get_neighbour_state(q,y)
                                #print(type(opsum))
                                #print(type(x))
                                #x += opsum
                elif self.number == 0:
                        f=open('net2.txt','r')
                        tarray = []
                        for line in f:
                                tarray.append([int(x) for x in line.split()])
                        rows = len(tarray)
                        cols = len(tarray[0])
                        self.n=numpy.zeros(shape=(rows,cols),dtype=numpy.int)
                        for r in range(len(tarray)):
                                for c in range(len(tarray[0])):
                                        self.n[r][c] = tarray[r][c]
                                q = tarray[r][0]
                                y = tarray[r][1]
                                type(q)
                                opsum += g.get_neighbour_state(q,y)
                elif self.number == 2:
                        f=open('net3.txt','r')
                        tarray = []
                        for line in f:
                                tarray.append([int(x) for x in line.split()])
                        rows = len(tarray)
                        cols = len(tarray[0])
                        self.n=numpy.zeros(shape=(rows,cols),dtype=numpy.int)
                        for r in range(len(tarray)):
                                for c in range(len(tarray[0])):
                                        self.n[r][c] = tarray[r][c]
                                q = tarray[r][0]
                                y = tarray[r][1]
                                type(q)
                                opsum += g.get_neighbour_state(q,y)
                return opsum
        def get_netsize(self):
                return len(self.n)

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
					#if rule in self.ruleset:
					if opinionsum < 0.1:
						g.m[i][j] = 0
					elif opinionsum >= 0.1 and opinionsum < 0.2:
                                                g.m[i][j] = 0.11
                                        elif opinionsum >= 0.2 and opinionsum < 0.3:
                                                g.m[i][j] = 0.22
                                        elif opinionsum >= 0.3 and opinionsum < 0.4:
                                                g.m[i][j] = 0.33
                                        elif opinionsum >= 0.4 and opinionsum < 0.5:
                                                g.m[i][j] = 0.44
                                        elif opinionsum >= 0.5 and opinionsum < 0.6:
                                                g.m[i][j] = 0.55
                                        elif opinionsum >= 0.6 and opinionsum < 0.7:
                                                g.m[i][j] = 0.66
                                        elif opinionsum >= 0.7 and opinionsum < 0.8:
                                                g.m[i][j] = 0.77
                                        elif opinionsum >= 0.8 and opinionsum < 0.9:
                                                g.m[i][j] = 0.88
					else:
						g.m[i][j] = 0.99
					#g.m[i][j] = 1 - g.m[i][j]
class game_of_life(object):
	def __init__ ( self, rule_set ):
		self.ruleset = set(rule_set)

	def apply ( self, g, n=1 ):
		for t in range(0,n):
                        #print(n)
			time.sleep(1)
			for i in xrange( 0, g.rows):
				for j in xrange( 0, g.columns):
					#rule = g.get_neighbour_rule(i,j)
					neighbourlife = g.get_neighbour_life(i,j)
					#if rule in self.ruleset:
					if neighbourlife == 3:
						g.m[i][j] = 1
					elif neighbourlife == 2:
						g.m[i][j] = g.m[i][j]
					else:
						g.m[i][j] = 0
					#g.m[i][j] = 1 - g.m[i][j]
class cellular_automata_with_cyber_sn(object):
	def __init__ (self, rule_set,time_metrix,network_metrix):
		self.ruleset = set(rule_set)
		self.tmetrix = list(time_metrix)
		self.network = list(network_metrix)

	def apply(self,g,n=1):
                impact = 0
		for t in range(0,n):
                        #print(t)
			time.sleep(1)
			for i in xrange( 0, g.rows):
				for j in xrange( 0, g.columns):
					timespent= int(self.tmetrix[i][j])
					networkno = self.network[i][j]
					opinionsum = g.get_neighbour_opinion_sum(i,j)
					net1 = social_network(networkno)
					sn_op = net1.get_network_opinion(g)
					netsz = net1.get_netsize()
					gdensity = g.get_neighbour_opinion_density(i,j)
					if netsz >0:
                                                impact = float(sn_op)/float(netsz)
                                                #print(type(sn_op))
                                                #print(type(netsz))
					#if rule in self.ruleset:
					#impact = timespent*network
                                        #print(impact)
                                        #print(str(netsz) + " " + str(sn_op) + " " + str(impact))
                                       
                                        if gdensity > 6:
                                                #print(gdensity)
                                                if opinionsum > 0.5:
                                                        if impact < 0.4:
                                                                g.m[i][j] = 0
                                                        else:
                                                                g.m[i][j] = 1
                                                elif opinionsum <= 0.5:
                                                        if impact >= 0.6:
                                                                g.m[i][j] = 1
                                                        else:
                                                                g.m[i][j] = 0
                                                else:
                                                        g.m[i][j] = 0

                                        else:
                                                if opinionsum > 0.5:
                                                        g.m[i][j] = 1
                                                else:
                                                        g.m[i][j] = 0
                                                
						#g.m[i][j] = 0

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
if life:
        ca = game_of_life(ruleset)
elif sn:
        timemetrix= rnd.randint(24,size=(sz,sz))
        networks = rnd.randint(0,3,size=(sz,sz))
        ca = cellular_automata_with_cyber_sn(ruleset,timemetrix,networks)
else:
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
			if state[i][j] < 0.1 :
				glColor3f(1.0,0,0)
			elif state[i][j] >= 0.1 and state[i][j] < 0.2:
				glColor3f(1.0,1.0,0)
			elif state[i][j] >= 0.2 and state[i][j] < 0.3:
				glColor3f(1.0,0,1.0)
			elif state[i][j] >= 0.3 and state[i][j] < 0.4:
				glColor3f(0,1.0,1.0)
			elif state[i][j] >= 0.4 and state[i][j] < 0.5:
				glColor3f(0,1.0,0.5)
			elif state[i][j] >= 0.5 and state[i][j] < 0.6:
				glColor3f(1.0,0.5,0)
			elif state[i][j] >= 0.6 and state[i][j] < 0.7:
				glColor3f(0.5,0,1.0)
			elif state[i][j] >= 0.7 and state[i][j] < 0.8:
				glColor3f(1.0,0,0.5)
			elif state[i][j] >= 0.8 and state[i][j] < 0.9:
				glColor3f(1.0,0.5,0.5)
			else:
                                #print(state[i][j])
				glColor3f(0,1.0,0)                      
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
