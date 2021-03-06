from VLSI_project import *
from convert_nand import *
from string_extractor import *
from nltk import word_tokenize	

list_of_alphabets = list(map(chr, range(97, 123)))

output1 = input_from_text_file("inp_file.txt")

output2 = nand_2_inputs_circuit(output1)

output2_list = word_tokenize(output2)

present_input_list = []

for element in output2_list:
	if element in list_of_alphabets:
		present_input_list.append(element)

present_input_list = list(set(present_input_list))
present_input_list = sorted(present_input_list)

user_static_input_list = []
user_output_list = [] 

for i in present_input_list:
	temp = input("Enter coordinates of the input:", str(i))
	user_static_input_list.append(eval(temp))
	
temp = input("Enter coordinates of the final output pin:")
user_output_list.append(temp)

user_forbidden_list = []
while True:


	temp = input("Enter the forbidden coordinates, enter X if you want to stop the process:")
	
	if(temp == 'X'):
		break
		
	else:
		user_forbidden_list.append(eval(temp))
		
print("I am at line 45 in top_level")	
string_extractor(output2,user_static_input_list,user_output_list,user_forbidden_list)


