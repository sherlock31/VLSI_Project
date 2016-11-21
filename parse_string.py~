from nltk import word_tokenize				#importing nltk's word tokenizer

class Stack:						#Stack Class
	def __init__(self):
		self.items = []
	
	def isEmpty(self):
		return self.items == []
	
	def push(self, item):
		self.items.insert(0,item)
	
	def pop(self):
		return self.items.pop(0)
	
	def peek(self):
		return self.items[0]
	
	def size(self):
		return len(self.items)

	def print_stack(self):
		index = len(self.items) - 1 
		for ele in self.items:
			print(index, ele)
			index = index - 1
	#def __str__(self):
			
	
	
complete_stack = Stack()			#Stack that will store all the operands and operations
operand_stack = Stack()#Stack that will only store operands, it can be useful when we only want to make input blocks at the beginning of graphical window 
data_list = [] 
	
def extract_data(input_string):		#function that parses the string and pushes content into respective stacks
	
	print("Your input string is", input_string)
	data_list = word_tokenize(input_string)			#tokenizing the string to extract out 
	
	for element in data_list:
		
		if(not (element == ")" or element == "(")):
			complete_stack.push(element)
			
			if(not(element == "nand")):					#case of duplicate operands will be handled in the display function
				operand_stack.push(element)
		
		
extract_data("((x nand y) nand z)")

complete_stack.print_stack()	
	
	
