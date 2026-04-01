import os
import xlwt
from datetime import datetime
import os
import re

def extract_base_dir_from_batch():
    """Extract BASE_DIR from run_IOP.bat file"""
    try:
        # Path to run_IOP.bat (2 folders up from current script)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        batch_file_path = os.path.join(current_dir, '..', '..', '..', 'run_IOP.bat')
        batch_file_path = os.path.normpath(batch_file_path)
        
        if not os.path.exists(batch_file_path):
            # print(f"Warning: run_IOP.bat not found at {batch_file_path}, using default D:/traget/IDCevo/IOP_configuration")
            return 'D:/traget/IDCevo/IOP_configuration'
        
        with open(batch_file_path, 'r') as file:
            content = file.read()
            
        # Look for the BASE_DIR pattern
        match = re.search(r'set\s+"BASE_DIR=([^"]+)"', content)
        if match:
            base_dir = match.group(1)
            # Convert backslashes to forward slashes for consistency
            base_dir = base_dir.replace('\\', '/')
            # print(f"Extracted BASE_DIR from run_IOP.bat: {base_dir}")
            return base_dir
        else:
            # print("Warning: BASE_DIR not found in run_IOP.bat, using default D:/traget/IDCevo/IOP_configuration")
            return 'D:/traget/IDCevo/IOP_configuration'
            
    except Exception as e:
        # print(f"Warning: Error reading run_IOP.bat: {e}, using default D:/traget/IDCevo/IOP_configuration")
        return 'D:/traget/IDCevo/IOP_configuration'
    
# HTML version with color display - this is now the main logging function
def save_to_notepad(stdout="", stderr="", header=None, color=None):
    # Create HTML version with proper colors
    base_dir = extract_base_dir_from_batch()
    html_path = f"{base_dir}/Test_results/IOP_logs.html".replace('/', '\\')
    folder = os.path.dirname(html_path)
    
    # Create the main folder
    if folder:
        os.makedirs(folder, exist_ok=True)
    
    # Create Screenshots folder in the same location
    screenshots_folder = os.path.join(folder, "Screenshots")
    if not os.path.exists(screenshots_folder):
        try:
            os.makedirs(screenshots_folder, exist_ok=True)
        except OSError as e:
            print(f"Warning: Could not create Screenshots folder: {e}")
    
    # Check if HTML file exists, if not create with HTML structure
    if not os.path.exists(html_path):
        with open(html_path, "w", encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Test Results</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #f5f5f5; padding: 20px; }
        .passed { color: green; font-weight: bold; }
        .failed { color: red; font-weight: bold; }
        .skipped { color: orange; font-weight: bold; }
        .header { font-weight: bold; }
        pre { background-color: white; padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
    </style>
</head>
<body>
<pre>
""")

    with open(html_path, "a", encoding='utf-8') as f:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if header is not None:
            if color == "green":
                f.write(f'\n[{timestamp}] === <span class="passed">{header}</span> ===\n')
            elif color == "red":
                f.write(f'\n[{timestamp}] === <span class="failed">{header}</span> ===\n')
            elif color == "orange":
                f.write(f'\n[{timestamp}] === <span class="skipped">{header}</span> ===\n')
            else:
                f.write(f"\n[{timestamp}] === {header} ===\n")
        if stdout:
            f.write(f"[{timestamp}] {stdout}\n")
        if stderr:
            f.write(f"[{timestamp}] {stderr}\n")

# Keep this as an alias for backward compatibility
def save_to_notepad_html(stdout="", stderr="", header=None, color=None):
    save_to_notepad(stdout, stderr, header, color)

# Function to save test results to Excel
def save_to_excel(test_name, result, comment):
    base_dir = extract_base_dir_from_batch()
    excel_path = f"{base_dir}/Test_results/IOP_results.xls".replace('/', '\\')
    folder = os.path.dirname(excel_path)
    
    # Create the main folder if it doesn't exist
    if folder:
        os.makedirs(folder, exist_ok=True)
    
    # Read existing data if file exists
    existing_data = []
    if os.path.exists(excel_path):
        try:
            # Use xlrd to read existing data
            import xlrd
            old_workbook = xlrd.open_workbook(excel_path)
            old_sheet = old_workbook.sheet_by_index(0)
            
            # Read all existing data (skip header row)
            for row_num in range(1, old_sheet.nrows):
                row_data = [
                    old_sheet.cell_value(row_num, 0),  # Test Name
                    old_sheet.cell_value(row_num, 1),  # Result
                    old_sheet.cell_value(row_num, 2)   # Comment
                ]
                existing_data.append(row_data)
        except Exception as e:
            print(f"Error reading existing Excel file: {e}")
            # If can't read existing file, start fresh
            existing_data = []
    
    # Create new workbook
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Test Results')
    
    # Add headers with yellow background
    header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_colour yellow')
    sheet.write(0, 0, 'Test Name', header_style)
    sheet.write(0, 1, 'Result', header_style)
    sheet.write(0, 2, 'Comment', header_style)
    
    # Set styles for results
    pass_style = xlwt.easyxf('font: color green')
    fail_style = xlwt.easyxf('font: color red')
    skip_style = xlwt.easyxf('font: color orange')
    
    # Write existing data back
    current_row = 1
    for row_data in existing_data:
        sheet.write(current_row, 0, row_data[0])  # Test Name
        result_str = str(row_data[1]).lower()
        if result_str == "passed":
            sheet.write(current_row, 1, row_data[1], pass_style)  # Result with green
        elif result_str == "skipped":
            sheet.write(current_row, 1, row_data[1], skip_style)  # Result with orange
        else:
            sheet.write(current_row, 1, row_data[1], fail_style)  # Result with red
        sheet.write(current_row, 2, row_data[2])  # Comment
        current_row += 1
    
    # Add the new test result
    if result.lower() == "passed":
        sheet.write(current_row, 0, test_name)
        sheet.write(current_row, 1, result, pass_style)
        sheet.write(current_row, 2, comment)
    elif result.lower() == "skipped":
        sheet.write(current_row, 0, test_name)
        sheet.write(current_row, 1, result, skip_style)
        sheet.write(current_row, 2, comment)
    else:  # Failed
        sheet.write(current_row, 0, test_name)
        sheet.write(current_row, 1, result, fail_style)
        sheet.write(current_row, 2, comment)
    
    # Save the workbook
    workbook.save(excel_path)
    return excel_path
