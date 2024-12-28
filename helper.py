import numpy as np


def save_as_mtx(array, filename):
    #Converts a 2D array to Matrix Market format and saves it to a file.

    rows, cols = len(array), len(array[0])  # Get dimensions
    nnz = 0  # Count non-zero elements (optional for MM format)

    # Calculate number of non-zero elements (optional for MM format)
    for row in array:
        nnz += len([val for val in row if val != 0])

    with open(filename, "w") as f:
        # Write header line
        f.write(f"%%MatrixMarket matrix coordinate pattern \n")
        f.write(f"{rows} {cols} {rows}\n")
        # Write data lines
        for i, row in enumerate(array):
            for j, value in enumerate(row):
                if value != 0:  # Write only non-zero elements (optional for MM format)
                    f.write(f"{i} {j} {value}\n")


def generate_dense_matrix(rows, cols):
    non_zero_values = np.random.uniform(1.0, 100.0, size=(rows, cols))

    return non_zero_values


def generate_dense_matrix_with_sparsity(rows, cols, p_zero=0.0):
    """
    Generates a dense matrix with a specified percentage of zeros.

    Returns:
       A dense matrix with the specified dimensions and percentage of zeros.
    """

    if p_zero < 0 or p_zero > 1:
        raise ValueError("p_zero must be between 0 and 1")


    num_zeros = int(rows * cols * p_zero)


    dense_matrix = np.random.randint(1.0, 100.0, size=(rows, cols),dtype=np.int32) #remove int32

    # Randomly set the desired number of elements to zero
    zero_indices = np.random.choice(rows * cols, num_zeros, replace=False)
    dense_matrix.flat[zero_indices] = 0

    return dense_matrix
