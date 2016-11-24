#Convert logical expression to equivalent 2-input NAND gate logical expression
#Sample logical expression :- and(a,or(b,c,d),c,and(d,and(g,h)))
#We assume that the logical expression contains only multiple input AND and OR gate
from copy import deepcopy

#Currently working on 4 and more inputs AND and OR gate
#2 and 3 inputs AND and OR gate working completely fine
#The function get_nand_exp converts multiple input AND and OR to a table representing the circuits tree

#Converts a logical expression to a tabular form repressenting a table
#The first column contains the gate names and variable input names
#The second column contains the index of where the corresponding variable is connected to
def exp_to_tree(exp):
	exp = exp.replace('(',' ( ')
	exp = exp.replace(')',' ) ')
	exp = exp.replace(',',' , ')
	exp = exp.split(' ')
	exp = [j for i,j in enumerate(exp) if j != ',']
	exp = [j for i,j in enumerate(exp) if j != '']		#Contains list of gates and variables with necessary brackets
	l = len(exp)
	while exp:											#Here is the necessary algorithm 
		if(len(exp) == l):
			table = [[exp[0], None, 1]]
			index = 1
			stack = [(len(table) - 1)]
			exp = exp[2:len(exp)]
		else:
			if((exp[0] == 'and') or (exp[0] == 'or') or (exp[0] == 'nand')):
				table.append([exp[0], stack[-1], len(stack)+1])
				stack.extend([len(table) - 1])
				exp = exp[2:len(exp)]
			elif(exp[0] == ')'):
				stack = stack[0:len(stack)-1]
				exp = exp[1:len(exp)]
			else:
				table.append([exp[0], stack[-1], None])
				exp = exp[1:len(exp)]
	return table

def table_to_nand_exp(table):							#From the tree table, we find the equivalent 2-input NAND gate circuit for all the multiple input AND
														#and OR gate included in the logical expression
	indices = []
	fcol = [row[0] for row in table] 
	indices.extend([i for i, x in enumerate(fcol) if x == 'and'])
	indices.extend([i for i, x in enumerate(fcol) if x == 'or'])
	indices.extend([i for i, x in enumerate(fcol) if x == 'nand'])
	indices = sorted(indices, key=int)					#Gets index of gates in table
	copy1 = table
	L = len(copy1)
	
	while(len(copy1) != 1):
		m = max(indices)
		indices = indices[0:len(indices)-1]
		
		fcol = [row[0] for row in copy1]				#First column
		scol = [row[1] for row in copy1]				#Second column
		
		out = [i for i, j in enumerate(scol) if j == m]
		inputs = [fcol[i] for i in out]	
		gate = fcol[m]										#Getting which gate it is that we want to get the equivalent 2-input NAND gate expression
		
		nand_exp = get_nand_exp(inputs,gate)			#We get necessary NAND gate expression
		if(len(copy1) == L):
			temp1 = nand_exp
		else:
			temp2 = nand_exp.replace('temp',temp1)
			temp1 = temp2
		
		copy2 = []
		for j in copy1:
			if j[1] != m:
				copy2.append(j)
		copy1 = copy2
		copy1[m][0] = 'temp'							#Itratively, we store already computed NAND gate expression and use that as input for others

	copy1[0][0] = temp1
	return copy1[0][0]									#The necessary NAND gate expression

def nand_table_to_nand_exp(table):							#From the tree table, we find the equivalent 2-input NAND gate circuit for all the multiple input AND
														#and OR gate included in the logical expression
	indices = []
	fcol = [row[0] for row in table] 
	indices.extend([i for i, x in enumerate(fcol) if x == 'nand'])
	indices = sorted(indices, key=int)					#Gets index of gates in table
	copy1 = table
	while(len(copy1) != 1):
		m = max(indices)
		indices = indices[0:len(indices)-1]
		
		fcol = [row[0] for row in copy1]				#First column
		scol = [row[1] for row in copy1]				#Second column
		
		out = [i for i, j in enumerate(scol) if j == m]
		inputs = [fcol[i] for i in out]					#Getting inputs for a AND or OR gate 
		gate = fcol[m]									#Getting which gate it is that we want to get the equivalent 2-input NAND gate expression
		
		nand_exp = 'nand'+'('+str(inputs[0])+','+str(inputs[1])+')'			#We get necessary NAND gate expression
		
		copy2 = []
		for j in copy1:
			if j[1] != m:
				copy2.append(j)
		copy1 = copy2
		copy1[m][0] = nand_exp							#Itratively, we store already computed NAND gate expression and use that as input for others

	return copy1[0][0]									#The necessary NAND gate expression

def get_nand_exp(inputs,gate):
	n = len(inputs)
	if(n == 2):
		inputs2 = inputs
		if(gate == 'and'):
			inputs2 = inputs
			copy_and = deepcopy([['nand', None],['nand', 0],[inputs2[0], 1, None],[inputs2[1], 1, None],['nand', 0],[inputs2[0], 4, None],[inputs2[1], 4, None]])
			copy_and[0].append(1)
			copy_and[1].append(2)
			copy_and[4].append(2)
			return nand_table_to_nand_exp(copy_and)
		elif(gate == 'or'):
			inputs2 = inputs
			copy_or = [['nand', None],['nand', 0],[inputs2[0], 1, None],[inputs2[0], 1, None],['nand', 0],[inputs2[1], 4, None],[inputs2[1], 4, None]]
			copy_or[0].append(1)
			copy_or[1].append(2)
			copy_or[4].append(2)
			return nand_table_to_nand_exp(copy_or)
		else:
			copy_nand = nand_unit
			return nand_table_to_nand_exp(copy_nand)
	else:
			expr = get_nand_exp(inputs[0:len(inputs)-1],gate)
			table1 = exp_to_tree(expr)
			if(len(inputs) == 4): table1 = [['nand', None, 1]] + table1[3:len(table1)]
			fcol1 = [row[0] for row in table1]
			scol1 = [row[1] for row in table1]
			tcol1 = [row[2] for row in table1]
			rankList = []
			out1 = [i for i, j in enumerate(fcol1) if j == 'nand']	#index of gates
			ind = 1
			for k in out1:
				out2 = [i for i, j in enumerate(scol1) if j == k]
				
				if(fcol1[out2[0]] == 'nand' and fcol1[out2[1]] != 'nand'):
					ind = 0
					[out,input] = deepcopy([k,out2])							#contains the index of gate (which has impure inputs) and its input indices 
					rank = tcol1[k]
					break
				elif(fcol1[out2[0]] != 'nand' and fcol1[out2[1]] == 'nand'):
					ind = 0
					[out,input] = deepcopy([k,out2])
					rank = tcol1[k]
					break
			
			if(ind):
				for run in table1:
					if run[0] == 'nand':
						rankList.append(run[2])
				for r in rankList:
					if(r%2 == 0):
						index_rankList = [k for k,j in enumerate(tcol1) if j == r]			#indices of ranks given to nand gates
						
						for count in index_rankList:
							temp = [m for m, n in enumerate(scol1) if n == count]			#gives the index of inputs whose output is at the same row of the minimum even rank
							if(fcol1[temp[0]] != 'nand' and fcol1[temp[1]] != 'nand'):
								indx = count			#Contains Y+1
								out2 = temp
								i = r					#Contains I+1
								break
						break
				
				inputs2 = [inputs[len(inputs)-1], inputs[len(inputs)-2]]
				index1 = out2[1]
				Y = indx-1
				i = i-1
				for i in range(3): table1 = table1[0:index1-2] + table1[index1:-1]					
				if(gate == 'and'):
					copy = [['nand', Y, i],
							[inputs[len(inputs)-3], Y+1, None],
							['nand', Y+1, i+1],
							['nand', Y+3, i+2],
							[inputs2[1], Y+4, None],
							[inputs2[0], Y+4, None],
							['nand', Y+3, i+2],
							[inputs2[1], Y+7, None],
							[inputs2[0], Y+7, None],
							['nand', Y, i],
							[inputs[len(inputs)-3], Y+10, None],
							['nand', Y+10, i+1],
							['nand', Y+12, i+2],
							[inputs2[1], Y+13, None],
							[inputs2[0], Y+13, None],
							['nand', Y+12, i+2],
							[inputs2[1], Y+16, None],
							[inputs2[0], Y+16, None]]
							
					
					for ins in copy:
						table1.insert(index1,ins)
						index1 = index1 + 1
				elif(gate == 'or'):
					copy = [['nand', Y, i],
							[inputs[len(inputs)-3], Y+1, None],
							['nand', Y+1, i+1],
							['nand', Y+3, i+2],
							[inputs2[0], Y+4, None],
							[inputs2[0], Y+4, None],
							['nand', Y+3, i+2],
							[inputs2[1], Y+7, None],
							[inputs2[1], Y+7, None],
							['nand', Y, i],
							[inputs[len(inputs)-3], Y+10, None],
							['nand', Y+10, i+1],
							['nand', Y+12, i+2],
							[inputs2[0], Y+13, None],
							[inputs2[0], Y+13, None],
							['nand', Y+12, i+2],
							[inputs2[1], Y+16, None],
							[inputs2[1], Y+16, None]]
					for ins in copy:
						table1.insert(index1,ins)
						index1 = index1 + 1
			else:
				if(fcol1[input[0]] == 'nand'):
					index1 = input[1]
					inputs2[0] = fcol1[input[1]]
					inputs2[1] = inputs[len(inputs)-1]
				else:
					index1 = input[0]
					inputs2[0] = fcol1[input[0]]
					inputs2[1] = inputs[len(inputs)-1]
				Y = out
				Y = Y-1
				i = rank
				i = i-1
				for i in range(17):
					temp = table1[Y+1]
					table1 = [x for x in table1 if x != temp]
				
				if(gate == 'and'):
					copy = [['nand', Y, i+1],
							['nand', Y+1, i+2],
							['nand', Y+2, i+3],
							[inputs2[0], Y+3, None],
							[inputs2[1], Y+3, None],
							['nand', Y+2, i+3],
							[inputs2[0], Y+6, None],
							[inputs2[1], Y+6, None],
							['nand', Y+1, i+2],
							['nand', Y+9, i+3],
							[inputs[len(inputs)-2], Y+10, None],
							[inputs[len(inputs)-3], Y+10, None],
							['nand', Y+9, i+3],
							[inputs[len(inputs)-2], Y+13, None],
							[inputs[len(inputs)-3], Y+13, None],
							['nand', Y, i+1],
							['nand', Y+16, i+2],
							['nand', Y+17, i+3],
							[inputs2[0], Y+18, None],
							[inputs2[1], Y+18, None],
							['nand', Y+17, i+3],
							[inputs2[0], Y+20, None],
							[inputs2[1], Y+20, None],
							['nand', Y+16, i+2],
							['nand', Y+24, i+3],
							[inputs[len(inputs)-2], Y+25, None],
							[inputs[len(inputs)-3], Y+25, None],
							['nand', Y+24, i+3],
							[inputs[len(inputs)-2], Y+28, None],
							[inputs[len(inputs)-3], Y+28, None]]
							
					for ins in copy:
						table1.insert(index1,ins)
						index1 = index1 + 1
				elif(gate == 'or'):
					copy = [['nand', Y, i+1],
							['nand', Y+1, i+2],
							['nand', Y+2, i+3],
							[inputs2[0], Y+3, None],
							[inputs2[0], Y+3, None],
							['nand', Y+2, i+3],
							[inputs2[1], Y+6, None],
							[inputs2[1], Y+6, None],
							['nand', Y+1, i+2],
							['nand', Y+9, i+3],
							[inputs[len(inputs)-3], Y+10, None],
							[inputs[len(inputs)-3], Y+10, None],
							['nand', Y+9, i+3],
							[inputs[len(inputs)-2], Y+13, None],
							[inputs[len(inputs)-2], Y+13, None],
							['nand', Y, i+1],
							['nand', Y+16, i+2],
							['nand', Y+17, i+3],
							[inputs2[0], Y+18, None],
							[inputs2[0], Y+18, None],
							['nand', Y+17, i+3],
							[inputs2[1], Y+20, None],
							[inputs2[1], Y+20, None],
							['nand', Y+16, i+2],
							['nand', Y+24, i+3],
							[inputs[len(inputs)-3], Y+25, None],
							[inputs[len(inputs)-3], Y+25, None],
							['nand', Y+24, i+3],
							[inputs[len(inputs)-2], Y+28, None],
							[inputs[len(inputs)-2], Y+28, None]]
							
					for ins in copy:
						table1.insert(index1,ins)
						index1 = index1 + 1
	expr_nand = nand_table_to_nand_exp(table1)					
	return expr_nand

expr = 'and(a,or(b,c))'
table = exp_to_tree(expr)
expr1 = table_to_nand_exp(table)
print(expr1)
#inputs = ['g','h','k']
#gate = 'and'
#exp_nand = get_nand_exp(inputs,gate)
#for run in table2:
#        print(run)
#exp_nand = nand_table_to_nand_exp(table2)
#print(exp_nand)


