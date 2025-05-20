import os
import json
from typing import Dict, Tuple
from matrix_core import SparseMatrix

def parse_matrix_file(file_path: str) -> SparseMatrix:
    """Parse matrix file with enhanced validation and error reporting"""
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

    # Validate header format
    if len(lines) < 2 or not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
        raise ValueError("Invalid file format: missing rows/cols declaration")

    # Extract matrix dimensions
    rows = int(lines[0].split("=")[1])
    cols = int(lines[1].split("=")[1])
    matrix = SparseMatrix(rows, cols)
    
    # Track statistics for reporting
    total_entries = 0
    skipped_entries = 0
    out_of_bounds_indices = {}
    
    # Parse each entry line
    for line_num, line in enumerate(lines[2:], start=3):
        if not (line.startswith('(') and line.endswith(')')):
            raise ValueError(f"Invalid format in line {line_num}: {line}")
        
        parts = line[1:-1].replace(" ", "").split(',')
        if len(parts) != 3:
            raise ValueError(f"Expected 3 values in line {line_num}: {line}")
        
        try:
            row, col = int(parts[0]), int(parts[1])
            val = float(parts[2])
            total_entries += 1
            
            if not (0 <= row < rows) or not (0 <= col < cols):
                skipped_entries += 1
                # Store pattern of out-of-bounds indices
                key = f"({row}, {col})"
                out_of_bounds_indices[key] = out_of_bounds_indices.get(key, 0) + 1
                
                print(f"⚠️ Skipping out-of-bounds index at line {line_num}: ({row}, {col}) - valid range is (0-{rows-1}, 0-{cols-1})")
                continue
                
            matrix.set(row, col, val)
        except ValueError:
            raise ValueError(f"Non-numeric value in line {line_num}: {line}")

    # Report summary of skipped entries
    if skipped_entries > 0:
        print(f"\nSummary of skipped entries:")
        print(f"Total entries processed: {total_entries}")
        print(f"Entries skipped due to out-of-bounds indices: {skipped_entries} ({skipped_entries/total_entries*100:.2f}%)")
        
        # Report most common out-of-bounds patterns
        print("\nMost common out-of-bounds patterns:")
        for pattern, count in sorted(out_of_bounds_indices.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {pattern}: {count} occurrences")
            
        # Suggest possible fixes
        if any(f"({row}, {cols})" in out_of_bounds_indices for row in range(rows)):
            print("\nSuggestion: Some indices appear to use 1-based indexing for columns.")
            print("Consider adjusting column indices by subtracting 1 from each column value.")

    return matrix

def write_matrix_to_file(matrix: SparseMatrix, file_path: str):
    """Write matrix in text format"""
    # Write matrix to file in the standard format
    # First writes dimensions, then each non-zero entry
    with open(file_path, 'w') as f:
        f.write(f"rows={matrix.rows}\ncols={matrix.cols}\n")
        for (row, col), val in sorted(matrix.items()):
            f.write(f"({row}, {col}, {val})\n")

def write_matrix_to_json(matrix, file_path):
    """
    Writes a sparse matrix to a JSON file.
    
    Args:
        matrix: The sparse matrix object
        file_path: Path to save the JSON file
    """
    import json
    
    # Create a dictionary representation of the matrix
    # Includes dimensions and all non-zero entries
    data = {
        "rows": matrix.rows,
        "cols": matrix.cols,
        "entries": [
            {"row": row, "col": col, "value": val}
            for (row, col), val in matrix.items()
        ]
    }
    
    # Write the JSON data to the specified file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)