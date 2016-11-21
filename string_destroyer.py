from nltk import word_tokenize	
from copy import deepcopy
import random 


alpha_values = {chr(i): (i - 97) for i in range(ord("a"), ord("a") + 26)} 		#for relation between alphabets and numbers

list_of_alphabets = list(map(chr, range(97, 123)))


#RECHECK EVERYTHING

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


#there is some pain in indexing of gate 0 vs 1 se shuru hone wala pain, also 

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
		
		#print("current_gate_number = ", current_gate_number)
		gate_input_found_list[current_gate_number] = 2							#both the inputs are found
		
		gate_input_list.append([temp_inp1,temp_inp2])		#inputs are specified for the current gate 

		index_of_output = 0
		
		for i in range(current_gate_number, -1, -1):		#index_of_output will be the latest NAND gate without both the inputs 
			if((gate_input_found_list[i] == 0) or (gate_input_found_list[i] == 1) ):
				index_of_output = i
				break
		
		output_list[current_gate_number] = Gate_list[index_of_output]		#output of the current gate is the most immediate gate without both the inputs
		
		if(current_gate_number == 0):
			output_list[current_gate_number] = output_pin
		
		gate_input_found_list[index_of_output] = gate_input_found_list[index_of_output] + 1		#that gate now has an input which is our current gate 
		
		
	elif((copy_list[nand_index + 2] in list_of_alphabets) and (copy_list[nand_index + 3] == "NAND")):	#first pure input and second is output from NAND
		
		temp_inp1 = static_input_list[alpha_values[copy_list[nand_index + 2]]]			#getting the coordinates of the pure input 
		gate_input_found_list[current_gate_number] = gate_input_found_list[current_gate_number] + 1		
		
		temp_inp2 = Gate_list[current_gate_number + 1]									#Its input is output of next nand gate

		gate_input_list.append([temp_inp1,temp_inp2])						#inputs are appended in the input list

		index_of_output = 0
		
		for i in range(current_gate_number, -1, -1):
			if((gate_input_found_list[i] == 0) or (gate_input_found_list[i] == 1) ):
				index_of_output = i
				break
		
		
		output_list[current_gate_number] = Gate_list[index_of_output]             
		gate_input_found_list[index_of_output] = gate_input_found_list[index_of_output] + 1	
			
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
		
		
		for i in range(current_gate_number, -1, -1):
			if((gate_input_found_list[i] == 0) or (gate_input_found_list[i] == 1) ):
				index_of_output = i
				break
		
		
		output_list[current_gate_number] = Gate_list[index_of_output]      
		gate_input_found_list[index_of_output] = gate_input_found_list[index_of_output] + 1	
	
	
def string_destroyer(string_temp, input_coordinates, output, forbidden_coordinates ):	#inputs: operation string, coordinates of the inputs
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
	gate_input_list = [[[0,0],[0,0]]]*total_gates				#list of coordinates of inputs to gates i.e. [[[g1_inpx1,g1_inpy1],[g1_inpx2,g1_inpy2]],[[..
	
	global output_list
	output_list = [0]*total_gates										#list of coordinates of outputs of gates [[ox1,oy1],[ox2,oy2]...]
	
	global output_pin
	output_pin = output									#coordinates of output_pin
	
	global gate_input_found_list
	gate_input_found_list = [0]*total_gates							#ith element will denote number of inputs found for the gate i.e 0,1 or 2
	
	global wire_length
	wire_length = 0	
	
	
	output_list.append(output_pin)				#the topmost gate's output will be the output_pin specified by the user	
		
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
	print("Gate_outputs are", output_list)
	print("static inputs are", static_input_list)
	print("final output pin is", output_pin)
	
	
	
#string_destroyer("NAND(a,b)",[[0,1],[0,3]], [4,0],[[2,0],[9,9]])	
		
string_destroyer("NAND(a,NAND(b,c)",[[0,1],[0,3],[0,9]],[10,0],[[3,3],[4,4]])







#this function returns wirelength for a given configuration of gates, inputs and forbidden points in the grid
 	
#def wire_length_calculator(gate_input_list, gate_coordinate_list, output_node, forbidden_coordinates_list ):

#	wire_length = 0
	
#	for gate_number_index, gate_element in enumerate(gate_input_list):
			
			




#def change_the_configuration





	

#	print(temp_list)
	
#string_destroyer("NAND(a,NAND(b,c))")
	



