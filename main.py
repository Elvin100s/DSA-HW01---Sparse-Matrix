#!/usr/bin/env python3
"""
SPARSE MATRIX CALCULATOR
"""
import os
import sys
import datetime
import json
import time
from typing import Optional
from matrix_io import parse_matrix_file, write_matrix_to_file, write_matrix_to_json
from operations import add, subtract, multiply

# Configuration
SAMPLE_FOLDER = "sample_inputs"
OUTPUT_FILE = "result.json"  # Change to "result.txt" for text format
OPERATIONS = {
    '1': ('Add', add),
    '2': ('Subtract', subtract),
    '3': ('Multiply', multiply)
}

def select_file(folder: str) -> Optional[str]:
    """Interactive file selection"""
    try:
        # Get list of available matrix files (.txt) in the specified folder
        files = [f for f in os.listdir(folder) 
                if f.endswith('.txt') and os.path.isfile(os.path.join(folder, f))]
        
        # Handle case where no matrix files are found
        if not files:
            print(f"No matrix files found in {folder}")
            return None
            
        # Display available matrices for selection
        print("\nAvailable matrices:")
        for i, f in enumerate(files, 1):
            print(f"{i}: {f}")
            
        # Get user selection with validation
        while True:
            choice = input(f"Select (1-{len(files)} or 'q'): ").strip().lower()
            if choice == 'q':
                return None
            if choice.isdigit() and 1 <= int(choice) <= len(files):
                return os.path.join(folder, files[int(choice)-1])
            print("Invalid selection")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def save_result_with_summary(result, operation, matrix1_path, matrix2_path, m1, m2, sample_folder):
    """Save result with summary information"""
    # Generate timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create the result.json file with summary information
    summary_path = os.path.join(sample_folder, OUTPUT_FILE)
    
    # Create summary data
    summary = {
        "operation_info": {
            "timestamp": timestamp,
            "operation_type": operation,
            "input_files": {
                "matrix1": os.path.basename(matrix1_path),
                "matrix2": os.path.basename(matrix2_path)
            }
        },
        "input_matrices": {
            "matrix1": {
                "dimensions": f"{m1.rows}x{m1.cols}",
                "non_zero_elements": len(list(m1.items()))
            },
            "matrix2": {
                "dimensions": f"{m2.rows}x{m2.cols}",
                "non_zero_elements": len(list(m2.items()))
            }
        },
        "result": {
            "dimensions": f"{result.rows}x{result.cols}",
            "non_zero_elements": len(list(result.items())),
            "sample_entries": [
                {"row": row, "col": col, "value": val}
                for (row, col), val in list(result.items())[:5]  # Include up to 5 sample entries
            ]
        }
    }
    
    # Write the summary to result.json
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary_path

def main():
    print("\n=== Sparse Matrix Calculator ===")
    
    # Select operation (add, subtract, or multiply)
    while True:
        print("\nOperations:")
        for k, (name, _) in OPERATIONS.items():
            print(f"{k}: {name}")
        choice = input("Select operation (1-3/q): ").strip().lower()
        if choice == 'q':
            return
        if choice in OPERATIONS:
            op_name, op_func = OPERATIONS[choice]
            break
        print("Invalid choice")

    # Create sample folder if it doesn't exist
    os.makedirs(SAMPLE_FOLDER, exist_ok=True)
    
    # Select first matrix file
    print("\nSelect first matrix:")
    path1 = select_file(SAMPLE_FOLDER)
    if not path1: return
    
    # Select second matrix file
    print("\nSelect second matrix:")
    path2 = select_file(SAMPLE_FOLDER)
    if not path2: return

    try:
        # Load matrices
        print("\nLoading matrices...")
        start_time = time.time()
        m1 = parse_matrix_file(path1)
        m2 = parse_matrix_file(path2)
        load_time = time.time() - start_time
        
        print(f"Matrices loaded in {load_time:.4f} seconds")
        print(f"Matrix 1: {m1.rows}x{m1.cols} with {len(list(m1.items()))} non-zero elements")
        print(f"Matrix 2: {m2.rows}x{m2.cols} with {len(list(m2.items()))} non-zero elements")
        
        # Validate operation
        if choice in ('1', '2') and (m1.rows != m2.rows or m1.cols != m2.cols):
            raise ValueError("Dimension mismatch for addition/subtraction")
        if choice == '3' and m1.cols != m2.rows:
            raise ValueError("Columns of first must match rows of second for multiplication")
    
        # Perform operation with timing
        print(f"\nPerforming {op_name}...")
        start_time = time.time()
        result = op_func(m1, m2)
        op_time = time.time() - start_time
        
        print(f"Operation completed in {op_time:.4f} seconds")
        print(f"Result: {result.rows}x{result.cols} with {len(list(result.items()))} non-zero elements")
        
        # Save the result with summary information
        summary_path = save_result_with_summary(result, op_name, path1, path2, m1, m2, SAMPLE_FOLDER)
        print(f"\n✅ Success! Summarized result saved to:\n{os.path.abspath(summary_path)}")
        print(f"The summary includes operation details, input matrices information, and result overview.")
        
    except Exception as e:
        # Handle and display any errors that occur during processing
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()