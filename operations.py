from matrix_core import SparseMatrix

def check_dimensions(a, b, operation):
    # Validate matrix dimensions for the requested operation
    # Addition/subtraction require matching dimensions
    # Multiplication requires inner dimensions to match (cols of A = rows of B)
    if operation in ('add', 'subtract'):
        if a.rows != b.rows or a.cols != b.cols:
            raise ValueError("Matrix dimensions must match for addition or subtraction.")
    elif operation == 'multiply':
        if a.cols != b.rows:
            raise ValueError("Matrix A columns must equal Matrix B rows for multiplication.")
    else:
        raise ValueError("Unknown operation.")

def add(a, b):
    # Add two sparse matrices
    # First validates dimensions match
    # Creates a new result matrix with same dimensions
    # Efficiently handles sparse matrices by only processing non-zero elements
    check_dimensions(a, b, 'add')
    result = SparseMatrix(a.rows, a.cols)
    for (i, j), val in a.items():
        result.set(i, j, val)
    for (i, j), val in b.items():
        result.set(i, j, result.get(i, j) + val)
    return result

def subtract(a, b):
    # Subtract matrix b from matrix a
    # First validates dimensions match
    # Creates a new result matrix with same dimensions
    # Efficiently handles sparse matrices by only processing non-zero elements
    check_dimensions(a, b, 'subtract')
    result = SparseMatrix(a.rows, a.cols)
    for (i, j), val in a.items():
        result.set(i, j, val)
    for (i, j), val in b.items():
        result.set(i, j, result.get(i, j) - val)
    return result

def multiply(a, b):
    # Optimize multiplication for sparse matrices
    check_dimensions(a, b, 'multiply')
    result = SparseMatrix(a.rows, b.cols)
    
    # Create column-indexed structure for matrix B to avoid scanning all columns
    b_cols = {}
    for (row, col), val in b.items():
        if row not in b_cols:
            b_cols[row] = {}
        b_cols[row][col] = val
    
    # Perform multiplication using the optimized structure
    for (i, k), val_a in a.items():
        if k in b_cols:  # Only process if row k in B has non-zero elements
            for j, val_b in b_cols[k].items():
                result.set(i, j, result.get(i, j) + val_a * val_b)
    
    return result
