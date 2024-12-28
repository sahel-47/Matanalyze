import jinja2 
import os
from helper import generate_dense_matrix_with_sparsity
import numpy as np
from scipy.sparse import coo_matrix
import math as m


def find_min_var(N, constraint):
    target = m.floor(N / constraint) 
    if(N/constraint) ==  m.floor(N / constraint) :
        return constraint
     # Compute the target floor value
    for var in range(1, constraint):  # Iterate from 1 to constraint - 1
        if m.floor(N / var) == target:
            return var     
    return constraint 

row_length_sparse = int(input("ENTER THE SPARSE ROW LENGTH: "))
print()
column_length_sparse = int(input("ENTER THE SPARSE COLUMN LENGTH: "))
print()
row_length_dense = int(input("ENTER THE DENSE ROW LENGTH: "))
print()
column_length_dense = int(input("ENTER THE DENSE COLUMN LENGTH: "))
print()
sparsity_sparse = float(input("ENTER THE SPARSITY OF THE SPARSE MATRIX: "))
print()
sparsity_dense = float(input("ENTER THE SPARSITY OF THE DENSE MATRIX: "))

sparse_matrix = generate_dense_matrix_with_sparsity(
                row_length_sparse, column_length_sparse, sparsity_sparse
            )

coo_form = coo_matrix(sparse_matrix)

dense_matrix = generate_dense_matrix_with_sparsity(
                row_length_dense, column_length_dense, sparsity_dense
            )

NNZ = np.count_nonzero(sparse_matrix)
spar = (row_length_sparse  * column_length_sparse - NNZ) * 100 / (row_length_sparse  * column_length_sparse)

print()
print("-----------------*********HLS-GENERATOR*********-----------------")
print()
multiplier_constraint = int(input("ENTER THE MAXIMUM NUMBER OF MULTIPLIERS TO BE GENERATED: "))
print()
onchip_row_size = int(input("ENTER THE NUMBER OF ROWS OF B THAT MUST BE LOADED ONCHIP VIA FIFO: "))
print()
onchip_out_size = int(input("ENTER THE NUMBER OF ROWS THAT THAT MUST BE OFF LOADED FROM ONCHIP TO OFCHIP VIA FIFO: "))
print()
question = input("Do you want to keep the default minimum number of array partitions or increase it? (Y/N): ")
print()


optimal_multipliers = find_min_var(column_length_dense, multiplier_constraint)

if(question == 'y' or question == 'Y'):
    array_partition = int(input("ENTER THE PARTITION FACTOR: "))
    print()
    while(array_partition < optimal_multipliers):
        print("THE ARRAY FACTOR MUST BE GREATER THAN",optimal_multipliers)
        array_partition = int(input("PLEASE ENTER THE VALUE AGAIN: "))
        print()

else:
    array_partition = optimal_multipliers


print("NUMBER OF OPTIMAL MULTIPLIERS WITHIN THE CONSTRAINT :",optimal_multipliers)

variables = {
    "M" : row_length_sparse,
    "K" : column_length_sparse,
    "N" : column_length_dense,
    "NNZ" : NNZ,
    "MULTIPLIERS" : optimal_multipliers,
    "ROW_CHUNK_LOAD_SIZE" : onchip_row_size,
    "OUTPUT_CHUNK_SIZE" : onchip_out_size,
    "PARTITION_FACTOR" : array_partition
}
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template('rowHardware.jinja')

rendered_file = template.render(variables)
output_directory = 'HLS_DESIGN'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
print()
HLSfile = input("Enter the name of the file: ")
HLSfile += ".cpp"

HLSfinal = os.path.join(output_directory,HLSfile)

with open(HLSfinal, 'w') as f:
    f.write(rendered_file)

print()
print("DESIGN COMPLETED..............")