from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
import random
import numpy
import time
import elementtree.ElementTree as ET
from numpy import random as rnd
from array import array


class Grid(object):
	ref = [[64,32,16], [128,256,8], [1,2,4]]
	def __init__( self, m ):
		self.m = m
		self.rows = len(m)
		self.columns = len(m[0])
 
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
                '''
                        This method will return mean of opinion sum for particular cell
                '''
		x=0
		y=0
		
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
		x=x/y
		return x
	def get_neighbour_opinion_density ( self, i, j):
		x=0
		status = self.m[i][j]
		if i < self.rows - 1 and j < self.columns - 1:
                         for r in range(-1,2):
                                for s in range(-1,2):
                                        if r != 0 or s != 0:
                                                y = self.m[i+r][j+s]
                                                if y == status:
                                                        x += 1
		return x
	
	def get_neighbour_life( self, i, j):
		x=0
		if i < self.rows - 1 and j < self.columns - 1:
			x += self.m[i-1][j+1]
			x += self.m[i][j+1]
			x += self.m[i+1][j+1]
			x += self.m[i-1][j]
			x += self.m[i+1][j]
			x += self.m[i-1][j-1]
			x += self.m[i][j-1]
			x += self.m[i+1][j+1]
		return x
        def get_neighbour_state(self,i,j):
                return self.m[i][j]
        
	def __getitem__( self, i ):
		return self.m[i+1][1:self.m.shape[1]-1]
	
	def __str__(self):
		return g.m.__str__()
	
class network(object):
        def __init__(self,filename):     
                self.n = []
                self.file = filename
                self.size = 0
                self.hubs = []
        def loadnetwork(self):
                f = open(self.file)
                tarray = []
                for line in f:
                        tarray.append([int(x1) for x1 in line.split()])
                        rows = len(tarray)
                        cols = len(tarray[0])
                        self.n=numpy.zeros(shape=(rows,cols),dtype=numpy.int)
                        for r in range(len(tarray)):
                                for c in range(len(tarray[0])):
                                        self.n[r][c] = tarray[r][c]
                f.close()
                self.initialize_hubs()
                self.size = len(self.n)
                return self
        def initialize_hubs(self):
                numofhubs = random.randint(1,5)
                self.hubs=numpy.zeros(shape=(numofhubs,2),dtype=numpy.int)
                for r in range(0,numofhubs):
                        hubx = random.randint(0,50)
                        huby = random.randint(0,50)
                        self.hubs[r][0] = hubx
                        self.hubs[r][1] = huby
                        print('adding hub ' + str(hubx) + ',' + str(huby))

        def get_numberof_hubs(self):
                return len(self.hubs)
                        
                
class social_network(object):
        def __init__( self):
                self.networks = []
                self.count = 0
        def add_network(self,filename):
                nw = network(filename)
                print(self.count)
                self.networks.append(nw.loadnetwork())
                self.count += 1
        def get_network_opinion( self, g,i,j,number,compro):
                opsum =0.0
                nwork = self.networks[number]
                if compro:
                        for r in range(len(nwork.n)):
                                q = nwork.n[r][0]
                                y = nwork.n[r][1]
                                nstate = g.get_neighbour_state(q,y)
                                cstate = g.get_neighbour_state(i,j)
                                if nstate == cstate:
                                        opsum += nstate
                else:
                        for r in range(len(nwork.n)):
                                q = nwork.n[r][0]
                                y = nwork.n[r][1]
                                nstate = g.get_neighbour_state(q,y)
                                cstate = g.get_neighbour_state(i,j)
                                opsum += nstate
                return opsum
        
        def get_hubs_opinion(self,g,i,j,netnumber):
                ntw = self.networks[netnumber]
                hubop = 0
                noofhubs = ntw.get_numberof_hubs()
                for r in range(noofhubs):
                        xx = ntw.hubs[r][0]
                        yy = ntw.hubs[r][1]
                        if xx!= i and yy!= j:
                                hubop = g.get_neighbour_state(xx,yy)
                                break
                return hubop                        
                                
                
        def get_netsize(self,i,j,number):
                netsz = 0
                nwork = self.networks[number]
                for r in range(len(nwork.n)):
                        if nwork.n[r][0] == i and nwork.n[r][1]==j:
                                netsz= len(nwork.n)
                                break
                        else:
                                netsz= 0
                return netsz
        def is_member(self,i,j):
                for r in range(len(self.n)):
                        if self.n[r][0] == i and self.n[r][1]==j:
                                print(self.n[r][0])
                                print(self.n[r][1])
                                return 1
                        else:
                                return 0

class cellular_automata(object):
	def __init__ ( self, rule_set ):
		self.ruleset = set(rule_set)

	def apply ( self, g, n=1 ):
		for t in range(0,n):
                        time.sleep(1)
			for i in xrange( 0, g.rows):
				for j in xrange( 0, g.columns):
					opinionsum = g.get_neighbour_opinion_sum(i,j)
					if opinionsum > 0.5:
						g.m[i][j] = 1
					else:
						g.m[i][j] = 0
						
class game_of_life(object):
	def __init__ ( self, rule_set ):
		self.ruleset = set(rule_set)

	def apply ( self, g, n=1 ):
		for t in range(0,n):
			time.sleep(1)
			for i in xrange( 0, g.rows):
				for j in xrange( 0, g.columns):
					neighbourlife = g.get_neighbour_life(i,j)
					if neighbourlife == 3:
						g.m[i][j] = 1
					elif neighbourlife == 2:
						g.m[i][j] = g.m[i][j]
					else:
						g.m[i][j] = 0

class cellular_automata_with_cyber_sn(object):
	def __init__ (self, rule_set,time_metrix,network_metrix,sn,compro):
		self.ruleset = set(rule_set)
		self.tmetrix = list(time_metrix)
		self.network = list(network_metrix)
		self.snet = sn
                self.comprouser = compro
	def apply(self,g,n=1):
                impact = 0
                try:
                        for t in range(0,n):
                                print(t)
                                time.sleep(1)
                                fw = open('init3.txt','w')
                                for i in xrange( 0, g.rows):
                                        for j in xrange( 0, g.columns):
                                                timespent= int(self.tmetrix[i][j])
                                                networkno = self.network[i][j]
                                                opinionsum = g.get_neighbour_opinion_sum(i,j)
                                                netsz = self.snet.get_netsize(i,j,networkno)
                                                gdensity = g.get_neighbour_opinion_density(i,j)
                                                sn_op = self.snet.get_network_opinion(g,i,j,networkno,self.comprouser)
                                                hub_op = self.snet.get_hubs_opinion(g,i,j,networkno)
                                                if netsz > 0:
                                                        impact = float(sn_op)/float(netsz)
                                                if gdensity > 4 and netsz > 0:
                                                        print("i-" + str(i) + "  j-" + str(j) + " netsz-" + str(netsz) +" " + str(sn_op)+ " " + str(impact))
                                                        if opinionsum > 0.5:
                                                                if impact < 0.5 or hub_op < 0.5:
                                                                        g.m[i][j] = 0.05
                                                                else:
                                                                        g.m[i][j] = 0.95
                                                        elif opinionsum <= 0.5:
                                                                if impact >= 0.5 or hub_op >= 0.5:
                                                                        g.m[i][j] = 0.95
                                                                else:
                                                                        g.m[i][j] = 0.05
                                                        else:
                                                                g.m[i][j] = 0

                                                else:
                                                        if opinionsum > 0.5:
                                                                g.m[i][j] = 1
                                                        else:
                                                                g.m[i][j] = 0
                                fw.close()

                except ValueError as v:
                        print("value")
                except Exception as t:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(sys.exc_info())
args = set(sys.argv)

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
	try:
                sz = 50
	except:
		sz = 50

	s= None

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
	auto = True
if "-l" in args:
        life =True
elif "-sn" in args:
        sn = True
f = None
state = None
ca = None
g = None
def setInitialState():
        global f,state,ca,g,args,sz,sn
        snetwork = None
        snnetcount = 0
        compro = False
        state=numpy.zeros(shape=(sz,sz))
        if "-f" in args:
                print('Enter Config File Name:')
                fname = raw_input()
                while True:
                        if len(fname) == 0:
                                print('Enter Config File Name:')
                                fname = raw_input()
                        else:
                                break
                tree = ET.parse(fname)
                root = tree.getroot()
                initfile = root.find('init')
                type = initfile.get('type')
                srcfile = None
                if type == 'f':
                       srcfiletag = initfile.find('file')
                       srcfile= srcfiletag.get('src')
                f=open(srcfile,'r')
                tarray = []
                for line in f:
                        tarray.append([int(x) for x in line.split()])
                sz = len(tarray)
                for r in range(len(tarray)):
                        for c in range(len(tarray[0])):
                                state[r][c] = tarray[r][c]

                sntag = root.find('socialnetwork')
                sninclude = sntag.get('include')
                comprostr = sntag.get('usertype')
                if comprostr == '1':
                        compro = True
                if sninclude == 'true':
                        sn = True
                        snetwork = social_network()
                if snetwork != None:
                        for networktag in sntag.findall('network'):
                                snfiletag = networktag.find('file')
                                snfile = snfiletag.get('src')
                                print(snfile)
                                snetwork.add_network(snfile)
                                snnetcount += 1
        else:
                bstate = rnd.rand(sz,sz)
                state=numpy.zeros(shape=(sz,sz))
                for r in range(0,sz):
                        for s in range(0,sz):
                                if bstate[r][s]>0.5:
                                        state[r][s] = 1
                                else:
                                        state[r][s] = 0
        g = Grid(state)
        if life:
                ca = game_of_life(ruleset)
        elif sn:
                timemetrix= rnd.randint(24,size=(sz,sz))
                networks = rnd.randint(1,snnetcount,size=(sz,sz))
                ca = cellular_automata_with_cyber_sn(ruleset,timemetrix,networks,snetwork,compro)
        else:
                ca = cellular_automata(ruleset)
        
def setAuto(pauto):
        auto=pauto

def display_state():
	xstart = 0.2
	ystart = 0.2
	delta = 0.6/(sz-1)
	glPointSize(5)
	glColor3f(0,0,0)
	glBegin(GL_POINTS)
	for i in range(0,sz):
		for j in range(0,sz):                   
			if state[i][j] ==1 :
				glColor3f(1.0,0,0)
			elif state[i][j] == .95:
				glColor3f(0,0,1.0)
			elif state[i][j] == .05:
                                glColor3f(1.0,1.0,0)
			else:
				glColor3f(0,1.0,0)                      
			glVertex2d(xstart + i*delta, ystart + j*delta)
	glEnd()

def next_state():
	ca.apply(g)
        
def display(*args):
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)
	display_state()
	glFlush()
	

def idleFunc(*args):
        global generation
        generation += 1
        glutSetWindowTitle('Cellular Automata (Generation-' + str(generation)+ ')')
	display()
	next_state()
	

def mouse(button,state,x,y):
        if state == GLUT_UP:
                global generation
                generation += 1
                glutSetWindowTitle('Cellular Automata (Generation-' + str(generation)+ ')')
                next_state()
                display()

def setup_viewport():
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)

def reshape(w,h):
	glViewport(0,0,w,h)
	setup_viewport()
def closemethod():
        glutDestroyWindow(glutGetWindow())

def key(*args):
	print('Bye! :)')
	sys.exit()

def main():
        global generation
        setInitialState()
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGB)
	glutInitWindowSize(500,500)
	glutCreateWindow('Cellular Automata (Generation-' + str(generation)+ ')')
	setup_viewport()
	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	glutCloseFunc(closemethod)
	if auto:
		glutIdleFunc(idleFunc)
	glutKeyboardFunc(key)
	glutMouseFunc(mouse)
	glutMainLoop()

main()
