# VLSI_Project


FOR THE CODE VLSI_Project.py which is responsible for defining the classes and conversion into SOP expression

Code input:

Input to the code from the file inp_file.txt
This file should contain the minterms of the Boolean function to be minimized.

Code functionality:

The code takes input as minterms of the boolean expression.
It converts this to a boolean expression in terms of And and Or
This is then converted to DNF expression and passed onto espresso_exprs for minimization.
The minimized expression obtained is then parsed, and stored in terms of user defined classes.

Classes are defined for AndGate and OrGate which take as input the minimized SOP expression 
and implement object oriented functionality. 
This is then converted to NAND2 gates, in tree structure.
Implemented in terms of AndBlock and OrBlock for NAND2 implementation of AND and OR.

Code Requirements:

External library PyEDA used for the espresso minimization.
Python3.4 minimum required for the code to run.

Example:

Input file:
000
001
101
111
110

Converted to Boolean form:
Or(Or(Or(Or(Or(And(And(~a, ~b), ~c), 0), And(And(~a, ~b), c)), And(And(a, ~b), c)), And(And(a, b), c)), And(And(a, b), ~c))

Converted to DNF form:
Or(And(~a, ~b, ~c), And(~a, ~b, c), And(a, ~b, c), And(a, b, c), And(a, b, ~c))

Minimized SOP espresso_exprs output:
(Or(And(~b, c), And(~a, ~b), And(a, b)),)

Implemented in terms of user defined classes:
OR( AND( NOT( b ),c ),AND( NOT( a ),NOT( b ) ),AND( a,b ) )

Implemented in terms of NAND2 gates tree form:
OR_Block(OR_Block(AND_Block(NOT( b ),c),AND_Block(NOT( a ),NOT( b ))),AND_Block(a,b))


For the code string_extractor.py which is responsible for assigning optimized 2d placement for an input boolean expression in a 17x17 grid:

	1.We require NLTK library, which was used to tokenize the input expression and matplotlib library to plot the cost 
	2.Code can be tested by uncommenting the code written at the bottom for various types of possible boolean expressions
	3.This code can be fed in with input from Sudipto's code whose result is an optimized nand2 expression
	4.Number of iterations can be changed to get better results 
