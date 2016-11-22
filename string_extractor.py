from nltk import word_tokenize	
from copy import deepcopy
import random 
import math

alpha_values = {chr(i): (i - 97) for i in range(ord("a"), ord("a") + 26)} 		#for relation between alphabets and numbers
list_of_alphabets = list(map(chr, range(97, 123)))


#CODE IN THIS FILE, gives an initial placement to gates of an input boolean expression (this part is working correctly), it then tries to find the optimum placement by using an algorithm somewhat similar to simulated annealing(there are some issues in wire_length calculation which we will resolve today
#Approach is right according to our understading

#PLEASE NOTE THAT THERE IS SOME ISSUE WITH minimum_wire_length calculation, string extracter is working perfectly, we hope to resolve all the issues by tomorrow

#for a given index in the copy list it iterates throught the boolean expression and returns the index after the brackets have been balanced and also the number of nand gates it encountered during the iteration

def bracket_equaliser(current_index):
	
	global copy_list
	
	braket_equal = 1				# expression like NAND(NAND(a,b), c), we want to reach c by using this function, equalizing internal brackets

	iterating_index = current_index + 1			#index of the first bracket i.e. the bracket after the second NAND in the above example expression
	nand_count = 0
	
	while(braket_equal != 0):			#till all the brackets are not equal
		
		iterating_index = iterating_index + 1 	#
		
		if(copy_list[iterating_index] == "("):
			braket_equal = braket_equal + 1
			
		elif(copy_list[iterating_index] == ")"):
			braket_equal = braket_equal - 1
		
		elif(copy_list[iterating_index] == "NAND"):
			nand_count = nand_count + 1
		
	return (iterating_index + 1, nand_count) 		#index of the element after brackets has been matched		

def nand_assigner(nand_index):			#Assigns inputs and output to a NAND gate which was found at nand_index in copy_list
	
	global current_gate_number 			#this should in some sense correspond to the gate number on which we are operating currently
	global static_input_list			#list of coordinates of static inputs a,b,c,d,e....
	global alpha_values					#Dictionary that relates alphabets and numbers 0,1... i.e a = 0, b = 1, ...
	global copy_list					#copied list of boolean expression	
	global output_list	
	global gate_input_found_list
	global gate_input_list
	global list_of_alphabets
	global output_pin
		
	if((copy_list[nand_index + 2] in list_of_alphabets) and (copy_list[nand_index + 3] in list_of_alphabets)):  	#that is both are pure inputs
		
		temp_inp1 = static_input_list[alpha_values[copy_list[nand_index + 2]]]	#extracting coordinates of the input from static_input_list
		temp_inp2 = static_input_list[alpha_values[copy_list[nand_index + 3]]]
		
		gate_input_found_list[current_gate_number] = 2							#both the inputs are found
		
		gate_input_list.append([temp_inp1,temp_inp2])		#inputs are specified for the current gate 

		#index_of_output = 0
		
		#for i in range(current_gate_number, -1, -1):		#index_of_output will be the latest NAND gate without both the inputs 
		#	if((gate_input_found_list[i] == 0) or (gate_input_found_list[i] == 1) ):
		#		index_of_output = i
		#		break
		
		#output_list[current_gate_number] = Gate_list[index_of_output]		#output of the current gate is the most immediate gate without both the inputs
		
		#if(current_gate_number == 0):
		#	output_list[current_gate_number] = output_pin
		
		#gate_input_found_list[index_of_output] = gate_input_found_list[index_of_output] + 1		#that gate now has an input which is our current gate 
		
		
	elif((copy_list[nand_index + 2] in list_of_alphabets) and (copy_list[nand_index + 3] == "NAND")):	#first pure input and second is output from NAND
		
		temp_inp1 = static_input_list[alpha_values[copy_list[nand_index + 2]]]			#getting the coordinates of the pure input 
		gate_input_found_list[current_gate_number] = gate_input_found_list[current_gate_number] + 1		
		
		temp_inp2 = Gate_list[current_gate_number + 1]									#Its input is output of next nand gate

		gate_input_list.append([temp_inp1,temp_inp2])						#inputs are appended in the input list

		#index_of_output = 0
		
		#for i in range(current_gate_number, -1, -1):
		#	if((gate_input_found_list[i] == 0) or (gate_input_found_list[i] == 1) ):
		#		index_of_output = i
		#		break
		
		
		#output_list[current_gate_number] = Gate_list[index_of_output] 
		#if(current_gate_number == 0):
		#	output_list[current_gate_number] = output_pin
		
		            
		#gate_input_found_list[index_of_output] = gate_input_found_list[index_of_output] + 1	
			
	elif((copy_list[nand_index + 2] == "NAND") ):
		
		temp_inp1 = Gate_list[current_gate_number + 1]							#the first input is the next immediate gate after the current NAND gate 
		
		(second_input_index,nand_count) = bracket_equaliser(nand_index + 2)	 #after equalizing the brackets it will give the index of the next input of the 
																				#current gate 						
		
		if(copy_list[second_input_index] in list_of_alphabets):      #if the second input is a pure input 
			
			temp_inp2 = static_input_list[alpha_values[copy_list[second_input_index]]]	
			gate_input_found_list[current_gate_number] = gate_input_found_list[current_gate_number] + 1
				
			gate_input_list.append([temp_inp1,temp_inp2])			
			
			
		elif(copy_list[second_input_index] == "NAND"):					#if the second input is a NAND gate 
			
			#temp_inp2 = #???? this will be the number of current gate + input gate1 + number of gates seen in that gate + 1
			temp_inp2 = Gate_list[current_gate_number + 1 + nand_count + 1]
			gate_input_list.append([temp_inp1,temp_inp2])			
		
		
		#for i in range(current_gate_number, -1, -1):
		#	if((gate_input_found_list[i] == 0) or (gate_input_found_list[i] == 1) ):
		#		index_of_output = i
		#		break
		
		
		#output_list[current_gate_number] = Gate_list[index_of_output]      
		#if(current_gate_number == 0):
		#	output_list[current_gate_number] = output_pin
		
		
		#gate_input_found_list[index_of_output] = gate_input_found_list[index_of_output] + 1	
	
	
def string_extracter(string_temp, input_coordinates, output, forbidden_coordinates ):	#inputs: operation string, coordinates of the inputs
																						#coordinates of the output, coordinates of the forbidden locations	
	
	temp_list = word_tokenize(string_temp)
	temp_list = [x for x in temp_list if x != ',']				#temp_list will be list of "NAND", operands like a,b,c... and "(", ")" to show indentation 
	
	
	global copy_list 
	copy_list = deepcopy(temp_list)						#deepcopy
	
	global total_gates 
	total_gates = 0 											#total number of gates in the expression
	
	for ele in temp_list:
		if ele == "NAND":
			total_gates = total_gates + 1						#total number of gates will be computed
	
	print("total_gates are", total_gates)		
	
	global Gate_list
	Gate_list = [0,0]*total_gates										#Gate_list will be a list of coordinates of gates i.e. [[Gx1,Gy1],[Gx2,Gy2],...]
	
	global forbidden_list 
	forbidden_list = forbidden_coordinates				#list of forbidden coordinates
	
	global static_input_list
	static_input_list = input_coordinates				#list of coordinates of inputs like a,b,c,d...
	
	global gate_input_list 
	gate_input_list = []			#list of coordinates of inputs to gates i.e. [[[g1_inpx1,g1_inpy1],[g1_inpx2,g1_inpy2]],[[..
	
	global output_list
	output_list = [0]*total_gates										#list of coordinates of outputs of gates [[ox1,oy1],[ox2,oy2]...]
	
	global output_pin
	output_pin = output									#coordinates of output_pin
	
	global gate_input_found_list
	gate_input_found_list = [0]*total_gates							#ith element will denote number of inputs found for the gate i.e 0,1 or 2
	
	global wire_length
	wire_length = 0	
	
	
	#output_list[0] = (output_pin)				#the topmost gate's output will be the output_pin specified by the user	
		
	possible_coordinates = [[x, y] for x in range(17) for y in range(17)]
	
	for element in forbidden_list:
	
		while element in possible_coordinates: possible_coordinates.remove(element)  	
	
	Gate_list = random.sample(possible_coordinates, total_gates)  	#all the gates are assigned random positions
	
	global current_gate_number 				
	current_gate_number = -1	
	
	for index, element in enumerate(copy_list):				#iterating through the list
		
		if element == "NAND":								#NAND gate found
			global current_gate_number
			current_gate_number = current_gate_number + 1	#first gate should be counted as 0 as we are using it to index stuff somewhere 
			
			#print("current_index at line 187 is", current_gate_number)
			
			nand_assigner(index)							#calling NAND assigner to determine inputs and outputs of the currently found NAND gate

	print("Gate_list is", Gate_list)
	print("Gate_inputs are", gate_input_list)
	#print("Gate_outputs are", output_list)
	print("static inputs are", static_input_list)
	print("final output pin is", output_pin)
	
	
#We are assuming a grid of 17 x 17, the function calculates minimum_wire_length between 2 points

def dijkstra_path(start, end, blocked):
	
    X = len(blocked[0])				# of columns
    Y = len(blocked)				# of rows
    max_cost = X*Y					#Maximum possible cose
    
    current = start					#Starting node
    visited = blocked				#Set all blocked nodes as visited
    cost = [[X*Y for i in range(X)]
            for j in range(Y)]		#Initialize cost matrix
    cost[start[0]][start[1]] = 1	#Set start node cost to 1
    
    #print("current is", current)
    #print("type of current is", type(current))
    #print("end is", end)
    #print("type of end is", type(end))
    #print("blocked is", blocked)
    
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
    
    length = [cost[i[0]][i[1]] if cost[i[0]][i[1]] < X*Y
              else None for i in end]	#Set disconnected node lengths to None
    
    
    
    #print("cost is", cost)
   # length = [0]
    #print("length is", length)        
    #length = [0]
    
    return length
	



#this function returns wirelength for a given configuration of gates, inputs and forbidden points in the grid
 	
def wire_length_calculator(gate_input_list, gate_coordinate_list, output_node, forbidden_coordinates_list ):

	total_wire_length = 0
	
	blocked = [[None]*17]*17
	
	for i in range(17):
		for j in range(17):
			if([i,j] in forbidden_coordinates_list):
				blocked[i][j] = 1
				
			else:
				blocked[i][j] = 0
	
	blocked = [[i == 1 for i in j] for j in blocked] 
	
	for gate_number_index, gate_element in enumerate(gate_input_list):
		
		
		start_coordinates = tuple(gate_input_list[gate_number_index][0])	#starting value of the distance finding problem is input to the gate
		
		arbit_temp = tuple(gate_coordinate_list[gate_number_index])
		
		destination_coordinates = []						#destination is the gate 
		destination_coordinates.append(arbit_temp)
		
		single_wire_length_1 = dijkstra_path(deepcopy(start_coordinates),deepcopy(destination_coordinates),deepcopy(blocked))	
			
		start_coordinates = tuple(gate_input_list[gate_number_index][1])	#starting value of the distance finding problem is input to the gate
		arbit_temp = tuple(gate_coordinate_list[gate_number_index])
		
		destination_coordinates = []						#destination is the gate 
		destination_coordinates.append(arbit_temp)
		
		single_wire_length_2 = dijkstra_path(deepcopy(start_coordinates),deepcopy(destination_coordinates),deepcopy(blocked))	
			
		total_wire_length = total_wire_length + int(single_wire_length_1[0]) + int(single_wire_length_2[0])
		
	
	output_location = tuple(output_node)
	output_list_temp = []
	output_list_temp.append(output_location)
	
	start_coordinates = tuple(gate_coordinate_list[0])
	
	#print("start_coordinates at 316 are", start_coordinates)
	#print("end_coordinates at 317 are", output_list_temp)
	
	final_output_length = dijkstra_path(deepcopy(start_coordinates), deepcopy(output_list_temp), deepcopy(blocked))
		
	total_wire_length = total_wire_length + int(final_output_length[0])

	return total_wire_length



def optimizer(gate_input_list, gate_coordinate_list, output_node, forbidden_coordinates_list):

	print("Gate Input List received in optimizer:", gate_input_list)
	print("Gate coordinates in optimizer:", gate_coordinate_list)



	for iteration in range(1000):		#unsure about number of iterations that will be required, search for a smarter approach here 
	
		
		copy_gate_input_list = deepcopy(gate_input_list)
		copy_gate_coordinate_list = deepcopy(gate_coordinate_list)
		
		second_copy_of_gate_coordinate_list = deepcopy(copy_gate_coordinate_list)
		
		#total length of wires in correct 
		old_length = wire_length_calculator(copy_gate_input_list,copy_gate_coordinate_list, output_node, forbidden_coordinates_list)	
		
		
		for gate_index, gate in enumerate(second_copy_of_gate_coordinate_list):
			
			number_of_possible_moves = 4		#this is the max possible moves, we will check for the restrictions and reduce it whenever move is blocked
			
			illegal_moves = [] 
			
			if(gate[0] == 0): 		#gate is at x wala boundary
				
				number_of_possible_moves = number_of_possible_moves - 1
				illegal_moves.append([gate[0] -1, gate[1]])
				
			if(gate[0] == 16): 		#gate is at second x wala boundary
			
				number_of_possible_moves = number_of_possible_moves - 1
				illegal_moves.append([gate[0] + 1, gate[1]])
				
			if(gate[1] == 0):		#y boundary 1
				
				number_of_possible_moves = number_of_possible_moves - 1
				illegal_moves.append([gate[0], gate[1] - 1])
				
			
			if(gate[1] == 16):
			
				number_of_possible_moves = number_of_possible_moves - 1
				illegal_moves.append([gate[0], gate[1] + 1])
			
			#checking whether there is a blocked area or not at the future location 	
			if(([gate[0] - 1, gate[1]] in forbidden_coordinates_list) or (([gate[0] - 1, gate[1]] in copy_gate_coordinate_list))):
			
				number_of_possible_moves = number_of_possible_moves - 1
				illegal_moves.append([gate[0] - 1, gate[1] ])
				
				
			if(([gate[0] + 1, gate[1]] in forbidden_coordinates_list) or (([gate[0] + 1, gate[1]] in copy_gate_coordinate_list))):
			
				number_of_possible_moves = number_of_possible_moves - 1
				illegal_moves.append([gate[0] + 1, gate[1] ])
			
			if(([gate[0], gate[1] - 1] in forbidden_coordinates_list) or (([gate[0], gate[1] - 1] in copy_gate_coordinate_list))):
			
				number_of_possible_moves = number_of_possible_moves - 1
				illegal_moves.append([gate[0], gate[1] - 1])
				
			if(([gate[0], gate[1] + 1] in forbidden_coordinates_list) or (([gate[0], gate[1] + 1] in copy_gate_coordinate_list))):
			
				number_of_possible_moves = number_of_possible_moves - 1
				illegal_moves.append([gate[0], gate[1] + 1])
			
			if(number_of_possible_moves > 0):
				random_selection_bit = random.randrange(number_of_possible_moves)	#to select one of the possible moves 
			
				all_possible_moves = [[gate[0] - 1, gate[1]],[gate[0] + 1, gate[1]], [gate[0], gate[1] - 1], [gate[0], gate[1] + 1]]
				#print("all_possible_moves are", all_possible_moves)
				
				
				for element in illegal_moves:	#removing the illegal_moves moves from all poossible moves 
	
					while element in all_possible_moves: all_possible_moves.remove(element)  	
				
				#this should be a single list element which is not the case right now 
						
				new_move = random.choice(all_possible_moves)  	#selecting one of the legal moves 
				#print("new_move is ", new_move)
			
			copy_of_copy_of_gate_input_list = deepcopy(copy_gate_input_list)
			
			#updating the input list also for the current move, that is if some gate has our current gate as input then the changed position of  
			#current gate should be reflected there
			
			for index_1,k in enumerate(copy_of_copy_of_gate_input_list):
				for index_2,l in enumerate(k):
					if(l == gate):
						copy_gate_input_list[index_1][index_2] = new_move
						
				 
				 
			copy_gate_coordinate_list[gate_index] = new_move		 		#MISTAKE hai yaha, wrong dimension of list 
			
			#print("copy_gate_input_list at 420:",copy_gate_input_list)
			#print("copy_gate_coordinate_list:" ,copy_gate_coordinate_list)
			
			new_length = wire_length_calculator(copy_gate_input_list, copy_gate_coordinate_list, output_node, forbidden_coordinates_list)	
				
				
			if(new_length <= old_length):
				#accept the changes, lists are updated
				gate_coordinate_list = deepcopy(copy_gate_coordinate_list)
				gate_input_list = deepcopy(copy_gate_input_list)
					
			else:
				#do the probabilistic acceptance thing 
				
				cost_difference = new_length - old_length
				probability_of_acceptance = math.exp(-cost_difference)
				
				if(random.random() <= probability_of_acceptance):
					
					gate_coordinate_list = deepcopy(copy_gate_coordinate_list)
					gate_input_list = deepcopy(copy_gate_input_list)
		
				
				
					
	return gate_coordinate_list		#final coordinates of the gates after everything				
				
string_extracter("NAND(a,b)",[[0,1],[0,3]], [10,0],[[2,0],[9,9]])	
#string_extracter("NAND(a,NAND(b,c)",[[0,1],[0,3],[0,9]],[10,0],[[3,3],[4,4]]) #different expressions can be commented out to see the output and  initial 
																			   #placement							
#string_extracter("NAND(NAND(b,c),a)",[[0,1],[0,3],[0,9]],[10,0],[[3,3],[4,4]])
#string_extracter("NAND(NAND(a,b),NAND(c,d))",[[0,1],[0,3],[0,9],[0,11]],[10,0],[[3,3],[4,4]])

#string_extracter("NAND(NAND(a,NAND(b,c)),NAND(d,e))",[[0,1],[0,3],[0,9],[0,11],[5,0]],[10,0],[[3,3],[4,4]])
global gate_input_list	
global Gate_list
global output_pin
global output_pin
global forbidden_list 




optimized_gate_coordinate_list = optimizer(gate_input_list, Gate_list, output_pin, forbidden_list)
print("optimized gate list is", optimized_gate_coordinate_list)


 


