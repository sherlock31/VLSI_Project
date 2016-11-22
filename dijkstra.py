from copy import deepcopy

#Find Shortest Path using Dijkstra's Algorithm  
def dijkstra_path(start, end, blocked):
	
    X = len(blocked[0])				# of columns
    Y = len(blocked)				# of rows
    max_cost = X*Y					#Maximum possible cose
    
    current = start					#Starting node
    visited = blocked				#Set all blocked nodes as visited
    cost = [[X*Y for i in range(X)]
            for j in range(Y)]		#Initialize cost matrix
    cost[start[0]][start[1]] = 1	#Set start node cost to 1
    
    while(True):
        visited[current[0]][current[1]] = True	#Current node has been visited

        nearby = [(current[0]+1,current[1]),
                  (current[0]-1,current[1]),
                  (current[0],current[1]+1),
                  (current[0],current[1]-1)] 	#Possible nearby blocks
		    
		#Calulate the cost of the allowed nearby blocks
        for i in nearby:
            if not (i[0] == -1 or i[1] == -1 or i[0]>= X or i[1] >= Y
                or blocked[i[0]][i[1]]):
                cost[i[0]][i[1]] = min(cost[i[0]][i[1]],1+
                                   cost[current[0]][current[1]])
			
		#Calculate the minumum cost node among the unvisited
        min_cost = max_cost
        min_node = ()
        for i in range(len(visited)):
            for j in range(len(visited[i])):
                if (not(visited[i][j])):
                    if cost[i][j]<min_cost:
                        min_cost = cost[i][j]
                        min_node = (i,j)
					
        current = tuple(min_node)	#Set that node to be the next node
        #Occurs when all blocks have been visited or graph is disconnected
        if(min_cost == max_cost):
            break	   
    
	#Extract the necessary node costs
    length = [cost[i[0]][i[1]] if cost[i[0]][i[1]] < X*Y
              else None for i in end]	#Set disconnected node lengths to None
            
    return length
	

blocked = [[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
           [1,1,1,0,1,1,0,0,1,1,1,0,0,0,1,0],
           [0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0],
           [0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0],
           [0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,1,1,0,0,1,1,0,0],
           [0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,0],
           [0,1,1,0,0,0,0,1,0,1,0,0,1,0,1,0],
           [0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0],
           [0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0],
           [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,0,1,0,0,1,1,0,0],
           [0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0],
           [0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]]		#Signifies the disallowed blocks
blocked = [[i == 1 for i in j] for j in blocked] 	#Convert to Boolean Matrix

points = [(0,0), (0,6), (1,12), (2,10), (3,15), (4,2),
          (8,3), (8,7), (8,13), (10,1), (13,7), (13,13), (15,3) ]	#Nodes
len_V = 13
length=[[] for i in points]

for i in range(len_V):
    temp_length= dijkstra_path(points[i],points[0:i],deepcopy(blocked))
    length[i] = temp_length
    print(length[i])
