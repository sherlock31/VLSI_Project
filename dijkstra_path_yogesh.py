# Title : Digkstra Path 
# Written by : Yogesh Mahajan (y.mahajan456@gmail.com)
# Description : dijkstra_lens function takes n*m grid, start point and returns matrix dis_mat such that dis_mat[i][j] = length of shortest path from source 
#                to point[i][j] 
#
# Every point is given by touple(x,y)
# grid[i][j] == 0 if point is forbidden else 1

from copy import deepcopy

def dijkstra_lens(start,grid):
    
    X = len(grid[0])        # n grid dimentsions
    Y = len(grid)           # m
    
    max_dis = X*Y
    
    current  = start        # current touple
    visited = [[False for i in j] for j in grid]    # all elements are unvisited at start
    dis_mat = [[max_dis for i in j] for j in grid] # distance of all point is set to max_dis
    
    dis_mat[start[0]][start[1]] = 1         # distance of starting point = 1 (include point)
    
    while(True):
        
        visited[current[0]][current[1]] = True
	
        neighbours = [(current[0]+1,current[1]),(current[0]-1,current[1]),(current[0],current[1]+1),(current[0],current[1]-1)]
        
        neighbours_copy = [tuple(i for i in j) for j in neighbours]
		    
        for i in neighbours_copy:               # remove invalid cases
            if (i[0] == -1 or i[1] == -1 or i[0]>=X or i[1] >=Y or not(grid[i[0]][i[1]])):      # boundry conditions
                neighbours.remove(i)
        del neighbours_copy   
		
        for point in neighbours:
            dis_mat[point[0]][point[1]] = min(dis_mat[point[0]][point[1]],1+dis_mat[current[0]][current[1]])
		    
        tmp_dis = max_dis
        next_node = (-1,-1)     
        
        for i in range(Y):
            for j in range(X):
                if (not(visited[i][j])):
                    if dis_mat[i][j]<tmp_dis:
                        tmp_dis = dis_mat[i][j]
                        next_node = (i,j)
						
        if(tmp_dis == max_dis):
            break
		    
        current = next_node
	
    for i in range(Y):
        for j in range(X):
            if(dis_mat[i][j] == max_dis):
                dis_mat[i][j] = None
    return dis_mat
        
            
        
        
    
