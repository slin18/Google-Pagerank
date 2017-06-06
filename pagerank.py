import numpy as np
from numpy.linalg import inv

#this dictionary will represent our simple directed graph 
graph = {'A': ['B', 'C'],
         'B': ['C', 'D'],
         'C': ['D'],
         'D': ['C'],
         'E': ['F'],
         'F': ['C']}
#some other inputs you can try
'''
graph = {'1': ['2'],
	     '2': ['1','3','4'],
	     '3': ['2','1'],
	     '4': ['3','4']}
'''
'''graph = {'Kevin': ['Mark', 'Katie'],
		 'Katie': ['Kevin', 'Mark', 'Jieun'],
		 'Jay': ['Jieun', 'Alex'],
		 'Mark': ['Kevin', 'Katie'],
		 'Jieun': ['Katie', 'Mark', 'Jay'], 
		 'Alex': ['Jay']}
'''
''' 
	 Pretty print graph
'''
def pprint(graph): 
	print("\nGraph:")
	for x in graph.keys(): 
		print("%s: " %x, end ='')
		for y in range(0, len(graph[x])):
			if y == len(graph[x])-1:
				print("%s" %(graph[x])[y])
			else:
				print("%s, " %(graph[x])[y], end = '')
	print("")

pprint(graph)

#place the out_degree into an array
def out_degree(graph):
	a = [] 
	for x in graph.keys():
		a.append(len(graph[x]))
	return a
print("Outdegree: %s" %out_degree(graph))

#place the in_degree into an array
def in_degree(graph): 
	a = [] #place in degrees here
	for x in graph.keys():
		z = 0
		for y in graph.keys():
			for h in range(0, len(graph[y])):
				if x in (graph[y])[h]:
					z += 1
		a.append(z)
	return a
print("\nIndegree: %s" %in_degree(graph))

'''
	Look_up references the keys as integer values from 0 to len(graph)
	This is to ensure all non-integer key values are compatible with
	numpy matrix
'''
def look_up():
	lookUp = {}
	i = 0
	for x in graph.keys():
		lookUp[x] = i
		i+=1
	return lookUp

#print(look_up())

'''
	A_ij = { if there is an edge from j to i, 1 
		   { else 0
	ex: B to A -> 1,2 = 1; A->A -> 1,1 = 1
	Note: can use in-degree to check matrix
		  number of 1s for row of key corresponds to 
	      number of 1s for matrix
'''
def convert_matrix():
	matrixA = np.zeros((len(graph), len(graph)))
	lookUpGraph = look_up()
	for x in graph.keys(): 
		i = lookUpGraph[x]
		for y in graph.keys():
			for h in range(0, len(graph[y])):
				if x == (graph[y])[h]:
					j=lookUpGraph[y]
					matrixA[i][j] = 1 
	return matrixA


print("\nA\n%s" %convert_matrix())

'''Whoops: this converted the matrix incorrectly 
	 What it did: if the j is in i, mark 1 vs
	 What its supposed to do: if there exists an edge from j to i
def convert_matrix(): 
	matrixA = np.zeros((len(graph), len(graph)))
	lookUpGraph = look_up()
	for x in graph.keys(): 
		i = lookUpGraph[x] 
		for h in range(0, len(graph[x])):
			if graph[x][h] in lookUpGraph.keys():
				j=lookUpGraph[graph[x][h]]
				#print("i: %s, j: %s " %(i, j))
				matrixA[i][j] = 1
	return matrixA
'''

'''
	A_ij = { max(out_degree, 1)
		   { 0 if i != j
'''
def diag_matrix():
	out_degreeList = out_degree(graph)
	x=np.identity(len(graph))
	matrixBound = len(graph)-1
	for z in range(matrixBound,-1,-1): #decrement = -1, doens't include -1
		#print(z)
		popV = out_degreeList.pop() #so that you don't call pop twice 
		if(popV >  x[z][z]): #out_degree bigger than the diagonal 
			x[z][z] = popV
	return(x)

print("D\n%s"%diag_matrix())

'''
	column vector
'''
def one_matrix(): 
	x = np.ones((len(graph), 1))
	return(x)

print("1\n%s"%one_matrix())

'''
	D*(D-0.85*A)^-1 *1
'''
def pageRank(): 
	one = one_matrix()
	diag = diag_matrix()
	matrixA = convert_matrix()
	solution=np.matmul(np.matmul(diag,inv(np.subtract(diag,0.85*matrixA))), one) 
	return solution

print("\nPagerank is D*(D-0.85*A)^-1 * 1\n%s" %pageRank())
