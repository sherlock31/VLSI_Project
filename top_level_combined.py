from VLSI_Project import *
from convert_nand import *
from string_extractor import *

output1 = input_from_text_file("inp_file.txt")

output2 = nand_2_inputs_circuit(output1)

string_extractor(output2)


