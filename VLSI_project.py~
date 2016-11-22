from pyeda.inter import *

#### Classes for OR_Block and AND_Block defined in terms of NAND2 gates as stated in documentation

class AND_Block:
	def __init__ (self, name, index, inp1, inp2) :
		self.m_name = name
		self.m_index = index
		self.m_inp1 = inp1
		self.m_inp2 = inp2
		
	def __str__(self) : 
		str_temp = "AND_Block(" + self.m_inp1.__str__() + "," + self.m_inp2.__str__() + ")"
		return str_temp
		
class OR_Block:
	def __init__ (self, name, index, inp1, inp2) :
		self.m_name = name
		self.m_index = index
		self.m_inp1 = inp1
		self.m_inp2 = inp2
		
	def __str__(self) : 
		str_temp = "OR_Block(" + self.m_inp1.__str__() + "," + self.m_inp2.__str__() + ")"
		return str_temp
		
#### Classes for logical expression which have child classes AND gate and OR gate

class LogicalOperation  :
  def __init__ ( self, name, type, inp ) :
    self.m_name = name
    self.m_type = type
    self.m_inp = inp
    
  def __str__ ( self ) :
  	str_temp = ""
  	for i in range(len(self.m_inp)) :
  	  	str_temp = str_temp + self.m_inp[i].__str__() + "," 
  	str_temp = str_temp[:-1]
  	return self.m_type + "( " + str_temp + " )"
  	
  def setNextPin(self,source):
        self.m_inp.append(source)

class Input  :
  def __init__ ( self, name ) :
    self.m_name = name
    self.m_type = "Input"
    self.m_value = None
  def __str__ ( self ) :
    return self.m_name

class AndGate(LogicalOperation):

    def __init__(self,name,inp):
        LogicalOperation.__init__(self,name,"AND",inp)

    def performGateLogic(self):

        for i in range(len(self.m_inp)):
        	if  isinstance(self.m_inp[i], Input):
        	      	a = self.m_inp[i].m_value
        	else:
        			a = self.m_inp[i].performGateLogic()
        	if a==False:
        		return False
        return True
        
class OrGate(LogicalOperation):

    def __init__(self,name,inp):
        LogicalOperation.__init__(self,name,"OR",inp)

    def performGateLogic(self):

        for i in range(len(self.m_inp)):
        	if isinstance(self.m_inp[i], Input):
        	      	a = self.m_inp[i].m_value
        	else:
        			a = self.m_inp[i].performGateLogic()
        	if a==True:
        		return True
        return False
        
class NotGate(LogicalOperation):

    def __init__(self,name,inp):
        LogicalOperation.__init__(self,name,"NOT",inp)

    def performGateLogic(self):

        if isinstance(self.m_inp[0], Input):
        	      	a = self.m_inp[0].m_value
        else:
        			a = self.m_inp[0].performGateLogic()
        if a == True:
        	return False
        return True
    

class Connector:

    def __init__(self, fgate, tgate):
        self.fromgate = fgate
        self.togate = tgate

        tgate.setNextPin(fgate)

    def getFrom(self):
        return self.fromgate

    def getTo(self):
        return self.togate

### Recursive function to convert multiple input AND gate into NAND2 gates
def multiple_input_and_to_and_block ( multiple_input_and, index ) : #takes input and gate with multiple inputs
	#should give output as final AND block ie and block of min index which is at top of tree
	no_of_inp = len(multiple_input_and.m_inp)
	if (no_of_inp == 2):
		tmp = AND_Block(multiple_input_and.m_name+"block",index,multiple_input_and.m_inp[0],multiple_input_and.m_inp[1])
		#print (tmp)
		return tmp
	else :
		tmp = AndGate (multiple_input_and.m_name, multiple_input_and.m_inp[:-1])
		tmp1 = multiple_input_and_to_and_block(tmp, index+1)
		return AND_Block("AND_Block",index,tmp1,multiple_input_and.m_inp[len(multiple_input_and.m_inp)-1])

### Recursive function to convert multiple input OR gate into NAND2 gates	
def multiple_input_or_to_or_block ( multiple_input_or, index ) : #takes input and gate with multiple inputs
	#should give output as final OR block ie or block of min index which is at top of tree
	no_of_inp = len(multiple_input_or.m_inp)
	if (no_of_inp == 2):
		tmp = OR_Block(multiple_input_or.m_name+"block",index,multiple_input_or.m_inp[0],multiple_input_or.m_inp[1])
		return tmp
	else :
		tmp = OrGate (multiple_input_or.m_name, multiple_input_or.m_inp[:-1])
		tmp1 = multiple_input_or_to_or_block(tmp, index+1)
		return OR_Block("OR_Block",index,tmp1,multiple_input_or.m_inp[len(multiple_input_or.m_inp)-1])

a, b, c, d = map(exprvar, "abcd")

############### The expression to be converted to NAND2 form written here ################
f1 = Or(~a & ~b & ~c, ~a & ~b & c, a & ~b & c, a & b & c, a & b & ~c)

f1m = espresso_exprs(f1)
f_str = str(f1m)
f_str = f_str.replace(" ", "")

nd_a = Input( "a" )
nd_b = Input( "b" )
nd_c = Input( "c" )
nd_d = Input( "d" )

not_a = NotGate( "~a", [nd_a])
not_b = NotGate( "~b", [nd_b])
not_c = NotGate( "~c", [nd_c])
not_d = NotGate( "~d", [nd_d])

gate_dict = { 'a' : nd_a , 'b' : nd_b , 'c' : nd_c , 'd' : nd_d , '~a' : not_a ,'~b' : not_b ,'~c' : not_c ,'~d' : not_d  }

sub = f_str.split("And")
sub.pop(0)
and_gate_no = 0
and_gates = []
and_blocks = []         

for i in sub:
	i = i.replace("),","")
	i = i.replace(")","")
	i = i.replace("(","")
	and_inp = i.split(",")
	g = AndGate("a_gate"+str(and_gate_no),[])
	for sig in and_inp:
		g.m_inp.append(gate_dict[sig])
	and_gates.append(g)	
	and_blocks.append(multiple_input_and_to_and_block(g,0)) 
	and_gate_no = and_gate_no + 1

or_gate = OrGate("or_gate",[])
for i in and_gates:
	or_gate.m_inp.append(i)

print("")
print("Final expression in terms of AND and OR")
print(or_gate)

or_gate_with_blocks = OrGate ("or_gate",[])
for i in and_blocks:
	or_gate_with_blocks.m_inp.append(i)

final_OR_block = multiple_input_or_to_or_block(or_gate_with_blocks,0)
print("")
print("Final NAND2 expression in terms of AND_Block and OR_Block")
print(final_OR_block)





