# Sparse Matrix Calculator
This project implements a sparse matrix calculator that can perform addition, subtraction, and multiplication operations on large sparse matrices.

## Features
- Load sparse matrices from text files
- Perform matrix operations:
  - Addition
  - Subtraction
  - Multiplication
- Save results with operation-specific filenames
## File Format
Input matrices should be in the following format:

```
rows=3
cols=3
(0, 0, 1)
(1, 1, 2)
(2, 2, 3)
```
## Usage
1. Place your matrix files in the sample_inputs folder
2. Run the program: python main.py
3. Select an operation (1-3)
4. Choose the input matrices
5. View the results
## Results Storage
The program stores results in result.txt
## Implementation Details
- Uses a custom sparse matrix implementation for memory efficiency
- Handles large matrices with minimal memory usage
- Validates matrix dimensions before operations
- Skips out-of-bounds indices in input files

## Requirements
- Python 3.6+
- No external dependencies required
