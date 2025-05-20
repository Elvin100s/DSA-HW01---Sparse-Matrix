class SparseMatrix:
    def __init__(self, rows, cols):
        # Initialize a sparse matrix with specified dimensions
        # Only non-zero elements will be stored in the data dictionary
        self.rows = rows
        self.cols = cols
        self.data = {}

    def set(self, row, col, value):
        # Set a value at the specified position
        # Validates indices are within bounds
        # Only stores non-zero values to save memory
        # Removes entries when set to zero
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            raise IndexError("Index out of bounds.")
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def get(self, row, col):
        # Retrieve value at specified position
        # Returns 0 for positions not explicitly set (sparse matrix default)
        return self.data.get((row, col), 0)

    def items(self):
        # Return all non-zero elements as (position, value) pairs
        # Used for efficient iteration over non-zero elements
        return self.data.items()
