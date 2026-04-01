from flask import Flask, render_template, request, jsonify
import pandas as pd
import xml.etree.ElementTree as ET
import os
import sys
import traceback
from datetime import datetime
import re

def extract_base_dir_from_batch():
    """Extract BASE_DIR from base_dir.txt file"""
    try:
        # Path to base_dir.txt (same folder as demo_app.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        batch_file_path = os.path.join(current_dir, 'base_dir.txt')
        batch_file_path = os.path.normpath(batch_file_path)
        
        if not os.path.exists(batch_file_path):
            print(f"Warning: base_dir.txt not found at {batch_file_path}, using default D:/traget/IDCevo")
            return 'D:/traget/IDCevo'
        
        with open(batch_file_path, 'r') as file:
            content = file.read()
            
        # Look for the BASE_DIR pattern
        match = re.search(r'set\s+"BASE_DIR=([^"]+)"', content)
        if match:
            base_dir = match.group(1)
            # Convert backslashes to forward slashes for consistency
            base_dir = base_dir.replace('\\', '/')
            print(f"Extracted BASE_DIR from base_dir.txt: {base_dir}")
            return base_dir
        else:
            print("Warning: BASE_DIR not found in base_dir.txt, using default D:/traget/IDCevo")
            return 'D:/traget/IDCevo'
            
    except Exception as e:
        print(f"Warning: Error reading base_dir.txt: {e}, using default D:/traget/IDCevo")
        return 'D:/traget/IDCevo'

def debug_log(message):
    """Simple debug function that writes to both console and file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    
    # Print to console with error handling
    try:
        print(log_message, flush=True)
        sys.stdout.flush()
    except Exception as e:
        # If console writing fails, try without flush
        try:
            print(log_message)
        except:
            pass  # If all console writing fails, continue silently
    
    # Also write to file for debugging with better error handling
    try:
        # Use absolute path to ensure file is created in the right location
        log_file_path = os.path.join(os.path.dirname(__file__), "debug.log")
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
            f.flush()  # Ensure data is written to disk
    except Exception as e:
        # If file writing fails, try to write to a temp location
        try:
            import tempfile
            temp_log = os.path.join(tempfile.gettempdir(), "demo_app_debug.log")
            with open(temp_log, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
        except:
            pass  # If all file writing fails, continue silently

# Test LiteLLM import
try:
    import litellm
    debug_log("SUCCESS: LiteLLM imported successfully")
    debug_log(f"LiteLLM version: {getattr(litellm, '__version__', 'unknown')}")
except Exception as e:
    debug_log(f"ERROR: Failed to import LiteLLM: {str(e)}")
    litellm = None

app = Flask(__name__)

# Extract base directory from run_IOP.bat and construct paths
base_dir = extract_base_dir_from_batch()
CSV_PATH = f"{base_dir}/BMW_IDCevo_IOP_Test_script_generator/BMW_IDCevo_IOP.csv"
XML_PATH = f"{base_dir}/BMW_IDCevo_IOP_Test_script_generator/BMW_IDCevo_IOP_Validation.xml"

# Log when Flask app starts
debug_log("Flask application initialized successfully")
debug_log(f"CSV_PATH: {CSV_PATH}")
debug_log(f"XML_PATH: {XML_PATH}")

# Add request logging middleware with error handling
@app.before_request
def log_request():
    try:
        # Safely get request attributes with fallbacks
        method = getattr(request, 'method', 'UNKNOWN')
        path = getattr(request, 'path', 'UNKNOWN')
        remote_addr = getattr(request, 'remote_addr', 'UNKNOWN')
        
        debug_log(f"REQUEST: {method} {path} from {remote_addr}")
        
        # Safely check for JSON content
        if hasattr(request, 'is_json') and request.is_json:
            try:
                json_data = request.get_json()
                debug_log(f"REQUEST JSON: {json_data}")
            except Exception as json_error:
                debug_log(f"REQUEST JSON: Failed to parse - {str(json_error)}")
                
    except Exception as e:
        # If all request logging fails, log the error and continue
        try:
            debug_log(f"ERROR in log_request: {str(e)}")
        except:
            pass  # If even error logging fails, continue silently

############################################
# helper: extract clean test name
############################################
def extract_test_name(full_name):
   # example:
   # CEC-40: Terminate outgoing call
   if ":" in full_name:
       name = full_name.split(":")[1].strip()
   else:
       name = full_name.strip()
   # convert to python friendly format - replace spaces and special characters with underscores
   name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
   return name

############################################
# upload XML and return list of test cases
############################################
@app.route("/upload_xml", methods=["POST"])
def upload_xml():
   debug_log("ENDPOINT CALLED: /upload_xml")
   file = request.files["file"]
   file.save(XML_PATH)
   tree = ET.parse(XML_PATH)
   root = tree.getroot()
   tests = []
   for tc in root.findall(".//TestCase"):
       # Get TestCase id attribute for display, but use Test_Case_Item_ID for selection
       testcase_id = tc.get("id")  # This is the actual TestCase id attribute from XML
       test_item_id = tc.findtext("Test_Case_Item_ID")  # This is used for selection
       name = tc.findtext("Test_Case_Name")
       tests.append({
           "id": test_item_id,  # Frontend uses this for selection
           "testcase_id": testcase_id,  # Store the actual TestCase id for reference
           "name": extract_test_name(name)
       })
   return jsonify(tests)

############################################
# import selected tests into existing CSV
############################################
@app.route("/import_tests", methods=["POST"])
def import_tests():
   selected = request.json["selected"]
   tree = ET.parse(XML_PATH)
   root = tree.getroot()
   rows = []
   for tc in root.findall(".//TestCase"):
       # Check Test_Case_Item_ID for frontend selection matching
       test_item_id = tc.findtext("Test_Case_Item_ID")
       if test_item_id in selected:
           # Use Test_Case_Item_ID as the primary Test Case ID (not the TestCase id attribute)
           # This ensures we use the actual Test Case Item ID (like 173001) instead of TestCase id (like 37)
           
           full_name = tc.findtext("Test_Case_Name")
           rows.append({
               "Test Case ID": test_item_id,  # Use Test_Case_Item_ID for consistency
               "Test Name": extract_test_name(full_name),
               "Test Case Precondition":
                   tc.findtext("Test_Case_Precondition"),
               "Test Case Description":
                   tc.findtext("Test_Case_Description"),
               "Test Case Expected Result":
                   tc.findtext("Test_Case_Expected_Result"),
               "Test Script Description": ""
           })
   xml_df = pd.DataFrame(rows)
   if os.path.exists(CSV_PATH):
       csv_df = pd.read_csv(CSV_PATH)
       merged = pd.concat([csv_df, xml_df], ignore_index=True)
       merged = merged.drop_duplicates(
           subset=["Test Name"],
           keep="last"
       )
   else:
       merged = xml_df
   merged.to_csv(CSV_PATH, index=False)
   return "ok"

############################################
# return CSV to frontend
############################################
@app.route("/get_csv")
def get_csv():
   if not os.path.exists(CSV_PATH):
       return jsonify([])
   df = pd.read_csv(CSV_PATH)
   # Sort by Test Case ID in descending order if the column exists
   if 'Test Case ID' in df.columns:
       df['Test Case ID'] = pd.to_numeric(df['Test Case ID'], errors='coerce')
       df = df.sort_values('Test Case ID', ascending=False)
   return jsonify(df.fillna("").to_dict(orient="records"))

############################################
# Clean AI response to remove unwanted formatting and headers
############################################
def clean_ai_response(response_text):
    """Clean AI response to remove unwanted headers, markdown, and formatting"""
    
    if not response_text or not response_text.strip():
        return ""
    
    cleaned_text = response_text.strip()
    
    # Remove common unwanted headers/introductions
    unwanted_headers = [
        "Based on the existing test script descriptions",
        "Here is the Test Script Description",
        "The Test Script Description for",
        "Test Script Description:",
        "# AI-Generated Test Script Description:",
        "Based on",
        "Here is",
        "The following is",
        "Below is",
    ]
    
    for header in unwanted_headers:
        if cleaned_text.lower().startswith(header.lower()):
            # Find the end of the line and remove everything up to there
            lines = cleaned_text.split('\n')
            # Remove first line if it contains unwanted header
            if len(lines) > 1:
                cleaned_text = '\n'.join(lines[1:]).strip()
            break
    
    # Remove markdown code block markers
    if cleaned_text.startswith('```'):
        lines = cleaned_text.split('\n')
        # Remove first line with ```
        if len(lines) > 1:
            lines = lines[1:]
        # Remove last line if it's just ```
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        cleaned_text = '\n'.join(lines).strip()
    
    # Remove trailing ``` if present
    if cleaned_text.endswith('```'):
        cleaned_text = cleaned_text[:-3].strip()
    
    # Remove any lines that are just colons or similar formatting
    lines = cleaned_text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped_line = line.strip()
        # Skip empty lines at the beginning
        if not cleaned_lines and not stripped_line:
            continue
        # Skip lines that are just formatting characters
        if stripped_line in [':', '```', '---', '===']:
            continue
        # Skip lines that look like headers we want to remove
        if any(header.lower() in stripped_line.lower() for header in unwanted_headers):
            continue
        cleaned_lines.append(line)
    
    # Join back and clean up extra whitespace
    result = '\n'.join(cleaned_lines).strip()
    
    # Remove any remaining unwanted patterns at the start
    while result:
        first_line = result.split('\n')[0].strip()
        if (not first_line or 
            first_line.startswith('Based on') or 
            first_line.startswith('Here is') or
            first_line.startswith('The Test Script') or
            'test case information' in first_line.lower() or
            first_line == '```'):
            # Remove this line
            lines = result.split('\n')
            if len(lines) > 1:
                result = '\n'.join(lines[1:]).strip()
            else:
                result = ""
                break
        else:
            break
    
    return result

############################################
# Auto-generate descriptions for missing tests
############################################
def analyze_existing_patterns(df):
   """Analyze existing test script descriptions to find common patterns"""
   existing_descriptions = df[df['Test Script Description'].notna() & (df['Test Script Description'].str.strip() != '')]['Test Script Description'].tolist()
   
   if not existing_descriptions:
       return {
           'common_setup': [],
           'common_cleanup': [],
           'common_patterns': [],
           'bluetooth_patterns': [],
           'call_patterns': [],
           'pairing_patterns': []
       }
   
   # Extract common setup steps
   common_setup = []
   common_cleanup = []
   bluetooth_patterns = []
   call_patterns = []
   pairing_patterns = []
   
   for desc in existing_descriptions:
       lines = desc.split('\n')
       
       # Common setup patterns
       for line in lines:
           if 'USB_Matrix_Status()' in line:
               common_setup.append(line.strip())
           elif 'get_serial_number()' in line:
               common_setup.append(line.strip())
           elif 'create_recordings_folder()' in line:
               common_setup.append(line.strip())
           elif 'start_screen_recording' in line:
               common_setup.append(line.strip())
           elif 'bluetooth_name' in line and 'adb shell settings get secure' in line:
               common_setup.append(line.strip())
           elif 'create_device' in line:
               common_setup.append(line.strip())
               
           # Common cleanup patterns
           elif 'screenshot' in line and 'save it on the path' in line:
               common_cleanup.append(line.strip())
           elif 'save in Excel' in line:
               common_cleanup.append(line.strip())
           elif 'adb shell input keyevent 3' in line:
               common_cleanup.append(line.strip())
           elif 'stop_screen_recording' in line:
               common_cleanup.append(line.strip())
               
           # Bluetooth-specific patterns
           elif 'Bluetooth' in line or 'bluetooth' in line:
               bluetooth_patterns.append(line.strip())
               
           # Call-specific patterns
           elif ('call' in line.lower() or 'dial' in line.lower() or 
                 'answer' in line.lower() or 'end_call' in line.lower()):
               call_patterns.append(line.strip())
               
           # Pairing-specific patterns
           elif ('pair' in line.lower() or 'connect' in line.lower() or 
                 'pairing' in line.lower()):
               pairing_patterns.append(line.strip())
   
   return {
       'common_setup': list(set(common_setup)),
       'common_cleanup': list(set(common_cleanup)),
       'bluetooth_patterns': list(set(bluetooth_patterns)),
       'call_patterns': list(set(call_patterns)),
       'pairing_patterns': list(set(pairing_patterns))
   }

@app.route("/generate_descriptions", methods=["POST"])
def generate_descriptions():
   """AI-powered generation of Test Script Descriptions with progress tracking"""
   debug_log("=== STARTING GENERATE_DESCRIPTIONS ENDPOINT ===")
   
   if litellm is None:
       debug_log("ERROR: LiteLLM is not available!")
       return jsonify({"success": False, "message": "LiteLLM is not available"})
   
   if not os.path.exists(CSV_PATH):
       return jsonify({"success": False, "message": "CSV file not found"})
   
   df = pd.read_csv(CSV_PATH)
   debug_log(f"Loaded CSV with {len(df)} rows")
   
   # Count tests that need descriptions
   empty_descriptions = df[df['Test Script Description'].isna() | (df['Test Script Description'].str.strip() == '')].index.tolist()
   debug_log(f"Found {len(empty_descriptions)} tests needing descriptions")
   
   if not empty_descriptions:
       return jsonify({"success": True, "message": "All test cases already have descriptions!"})

   # Analyze existing patterns from the CSV data
   existing_descriptions = df[df['Test Script Description'].notna() & (df['Test Script Description'].str.strip() != '')]['Test Script Description'].tolist()
   
   # Extract common patterns from existing descriptions
   common_patterns = analyze_existing_patterns(df)
   
   updated_count = 0
   failed_count = 0
   total_to_process = len(empty_descriptions)
   failed_tests = []
   
   for i, idx in enumerate(empty_descriptions):
       row = df.iloc[idx]
       test_name = row['Test Name']
       precondition = str(row.get('Test Case Precondition', '')).strip()
       description = str(row.get('Test Case Description', '')).strip() 
       expected_result = str(row.get('Test Case Expected Result', '')).strip()
       
       debug_log(f"--- Processing test {i+1}/{total_to_process}: {test_name} ---")
       
       try:
           # Generate contextual description using LiteLLM API
           script_description = generate_contextual_description(
               test_name, precondition, description, expected_result, existing_descriptions
           )
           
           if script_description and script_description.strip():
               df.at[idx, 'Test Script Description'] = script_description
               updated_count += 1
               debug_log(f"SUCCESS: Generated description for {test_name}")
           else:
               debug_log(f"WARNING: Empty description returned for {test_name}")
               failed_count += 1
               failed_tests.append(test_name)
               
       except Exception as e:
           debug_log(f"FAILED: Error generating description for {test_name}: {str(e)}")
           debug_log(f"Exception traceback: {traceback.format_exc()}")
           failed_count += 1
           failed_tests.append(test_name)
       
       # Calculate progress
       progress = int((i + 1) / total_to_process * 100)
       debug_log(f"Progress: {progress}% - Processed {test_name}")
   
   # Save the updated CSV
   df.to_csv(CSV_PATH, index=False)
   debug_log(f"CSV saved with {updated_count} updated descriptions")
   
   message = f"Generated descriptions for {updated_count} test cases!"
   if failed_count > 0:
       message += f" {failed_count} failed: {', '.join(failed_tests)}"
   
   debug_log("=== COMPLETED GENERATE_DESCRIPTIONS ENDPOINT ===")
   
   return jsonify({
       "success": True, 
       "message": message,
       "updated_count": updated_count,
       "failed_count": failed_count,
       "total_processed": total_to_process
   })

def generate_contextual_description(test_name, precondition, description, expected_result, existing_descriptions):
    """Generate contextual test script description using LiteLLM API and extract CSV data into lists"""
    
    debug_log(f"=== STARTING GENERATION FOR: {test_name} ===")
    
    # Extract all information from CSV file into lists
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        debug_log(f"Loaded CSV with {len(df)} rows")
        
        # Extract data into lists as requested
        test_names = df['Test Name'].fillna('').tolist()
        preconditions = df['Test Case Precondition'].fillna('').tolist()
        descriptions = df['Test Case Description'].fillna('').tolist()
        expected_results = df['Test Case Expected Result'].fillna('').tolist()
        existing_descriptions_list = df['Test Script Description'].fillna('').tolist()
        
        debug_log(f"Extracted {len(test_names)} test names")
        debug_log(f"Extracted {len(preconditions)} preconditions") 
        debug_log(f"Extracted {len(descriptions)} descriptions")
        debug_log(f"Extracted {len(expected_results)} expected results")
        debug_log(f"Extracted {len(existing_descriptions_list)} existing descriptions")
        
    else:
        debug_log("WARNING: CSV file not found, using empty lists")
        test_names = []
        preconditions = []
        descriptions = []
        expected_results = []
        existing_descriptions_list = []
    
    if litellm is None:
        debug_log("ERROR: LiteLLM is not available!")
        raise Exception("LiteLLM is not available")
    
    # Configure LiteLLM with working settings from test
    litellm.api_base = "https://brllm.harman.com"
    litellm.api_key = "sk-WZrmCvrdiCijVsm9XLVFbw"  # Valid Harman LiteLLM key
    litellm.set_verbose = True
    
    debug_log(f"LiteLLM API base: {litellm.api_base}")
    debug_log(f"LiteLLM API key set: {litellm.api_key}")
    debug_log(f"LiteLLM verbose: {litellm.set_verbose}")
    
    # Prepare a comprehensive prompt with all extracted data
    prompt = f"""You must generate ONLY the Test Script Description content for the test case "{test_name}" based on existing test script descriptions. 

CRITICAL INSTRUCTIONS:
- Return ONLY the raw test script steps, no introductory text
- Do NOT include any headers like "Based on..." or "Here is..."
- Do NOT wrap the response in markdown code blocks (```), quotes, or any formatting
- Start directly with the first step like "check USB Matrix status..."
- End with the last step, no closing remarks

Current test case information:
- Test Name: {test_name}
- Precondition: {precondition}
- Description: {description}
- Expected Result: {expected_result}

All available test data from CSV:
Test Names: {test_names}
Preconditions: {preconditions}
Test Descriptions: {descriptions}
Expected Results: {expected_results}
Existing Test Script Descriptions: {existing_descriptions_list}

Generate ONLY the test script steps, starting directly with the first step:"""
    
    debug_log(f"Prompt prepared, length: {len(prompt)} characters")
    debug_log("Sending request to LiteLLM API...")
    
    try:
        # Make API call using LiteLLM with working configuration
        response = litellm.completion(
            model="sonnet-4-asia",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            custom_llm_provider="openai"
        )
        
        debug_log("SUCCESS: Received response from LiteLLM API")
        
        # Extract the generated description from the API response
        generated_description = response.choices[0].message.content.strip()
        
        debug_log(f"Raw response length: {len(generated_description)}")
        debug_log(f"Raw response first 100 chars: {generated_description[:100]}...")
        
        # Clean up the response to remove unwanted headers and formatting
        cleaned_description = clean_ai_response(generated_description)
        
        debug_log(f"Cleaned response length: {len(cleaned_description)}")
        debug_log(f"Cleaned response first 100 chars: {cleaned_description[:100]}...")
        
        debug_log(f"=== SUCCESSFULLY COMPLETED GENERATION FOR: {test_name} ===")
        return cleaned_description
        
    except Exception as e:
        debug_log(f"CRITICAL ERROR generating description with LiteLLM API: {str(e)}")
        full_error = traceback.format_exc()
        debug_log(f"Full traceback: {full_error}")
        
        # Re-raise the exception so the calling function knows it failed
        raise Exception(f"Failed to generate description for {test_name}: {str(e)}")

############################################
# Save edited CSV data
############################################
@app.route("/save_csv", methods=["POST"])
def save_csv():
   try:
       data = request.json["data"]
       df = pd.DataFrame(data)
       df.to_csv(CSV_PATH, index=False)
       return jsonify({"success": True, "message": "CSV data saved successfully!"})
   except Exception as e:
       return jsonify({"success": False, "message": f"Error saving CSV: {str(e)}"})

############################################
# generate python scripts for missing tests
############################################
@app.route("/generate_scripts", methods=["POST"])
def generate_scripts():
    """AI-powered generation of Python test scripts for missing tests with progress tracking"""
    global script_generation_progress
    
    debug_log("=== STARTING GENERATE_SCRIPTS ENDPOINT ===")
    
    # Initialize progress tracking
    script_generation_progress = {
        'current': 0,
        'total': 0,
        'status': 'starting',
        'message': 'Initializing script generation...',
        'completed_scripts': [],
        'failed_scripts': []
    }
    
    if litellm is None:
        debug_log("ERROR: LiteLLM is not available!")
        script_generation_progress['status'] = 'error'
        script_generation_progress['message'] = 'LiteLLM is not available'
        return jsonify({"success": False, "message": "LiteLLM is not available"})
    
    if not os.path.exists(CSV_PATH):
        script_generation_progress['status'] = 'error'
        script_generation_progress['message'] = 'CSV file not found'
        return jsonify({"success": False, "message": "CSV file not found"})
    
    df = pd.read_csv(CSV_PATH)
    debug_log(f"Loaded CSV with {len(df)} rows")
    
    # Target directory for test scripts (for review before moving to test configuration)
    target_scripts_dir = f"{base_dir}/BMW_IDCevo_IOP_Test_script_generator/scripts"
    debug_log(f"Target scripts directory: {target_scripts_dir}")
    
    if not os.path.exists(target_scripts_dir):
        debug_log(f"Creating target directory: {target_scripts_dir}")
        os.makedirs(target_scripts_dir, exist_ok=True)
    
    # Reference directory to compare against (actual test scripts location)
    reference_scripts_dir = f"{base_dir}/IOP_configuration/Test_environment/Test_scripts"
    
    # Get list of existing script files from the reference directory
    existing_scripts = []
    if os.path.exists(reference_scripts_dir):
        existing_scripts = [f.replace('.py', '') for f in os.listdir(reference_scripts_dir) 
                          if f.endswith('.py') and not f.startswith('_')]
    debug_log(f"Found {len(existing_scripts)} existing scripts in reference directory: {existing_scripts}")
    
    # Find missing scripts by comparing Test Names with existing files
    test_names = df['Test Name'].fillna('').tolist()
    missing_scripts = []
    
    for test_name in test_names:
        if test_name.strip() and test_name not in existing_scripts:
            missing_scripts.append(test_name)
    
    debug_log(f"Found {len(missing_scripts)} missing scripts: {missing_scripts}")
    
    if not missing_scripts:
        script_generation_progress['status'] = 'completed'
        script_generation_progress['message'] = 'All test scripts already exist!'
        return jsonify({"success": True, "message": "All test scripts already exist!"})
    
    # Update progress with total count
    script_generation_progress['total'] = len(missing_scripts)
    script_generation_progress['status'] = 'processing'
    script_generation_progress['message'] = f'Found {len(missing_scripts)} missing scripts. Reading existing scripts for context...'
    
    # Read more existing scripts for context from reference directory (use more examples)
    existing_script_content = []
    script_count_to_read = min(5, len(existing_scripts))  # Read up to 5 reference scripts
    
    for script_name in existing_scripts[:script_count_to_read]:
        script_path = os.path.join(reference_scripts_dir, f"{script_name}.py")
        if os.path.exists(script_path):
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Keep more content but still manageable - focus on key patterns
                    if len(content) > 4000:
                        lines = content.split('\n')
                        # Keep more lines to capture patterns better
                        truncated = '\n'.join(lines[:40] + ['...', '# (content truncated for prompt efficiency)', '...'] + lines[-25:])
                        existing_script_content.append(f"=== {script_name}.py (patterns reference) ===\n{truncated}")
                    else:
                        existing_script_content.append(f"=== {script_name}.py ===\n{content}")
                debug_log(f"Added reference script: {script_name}")
            except Exception as e:
                debug_log(f"Warning: Could not read {script_path}: {e}")
    
    debug_log(f"Using {len(existing_script_content)} reference scripts for pattern matching")
    
    generated_count = 0
    failed_count = 0
    total_to_process = len(missing_scripts)
    failed_scripts = []
    
    script_generation_progress['message'] = 'Starting script generation...'
    
    for i, test_name in enumerate(missing_scripts):
        # Update progress for current script (limit to 95% during processing)
        script_generation_progress['current'] = i + 1
        script_generation_progress['message'] = f'Generating script {i+1}/{total_to_process}: {test_name}'
        
        debug_log(f"--- Processing script {i+1}/{total_to_process}: {test_name} ---")
        
        # Get test case data
        test_row = df[df['Test Name'] == test_name].iloc[0]
        precondition = str(test_row.get('Test Case Precondition', '')).strip()
        description = str(test_row.get('Test Case Description', '')).strip()
        expected_result = str(test_row.get('Test Case Expected Result', '')).strip()
        script_description = str(test_row.get('Test Script Description', '')).strip()
        
        try:
            # Generate Python script using AI
            script_content = generate_python_script(
                test_name, precondition, description, expected_result, 
                script_description, existing_script_content
            )
            
            if script_content and script_content.strip():
                # Save the generated script
                script_filename = os.path.join(target_scripts_dir, f"{test_name}.py")
                with open(script_filename, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                
                generated_count += 1
                script_generation_progress['completed_scripts'].append(test_name)
                debug_log(f"SUCCESS: Generated script for {test_name}")
            else:
                debug_log(f"WARNING: Empty script returned for {test_name}")
                failed_count += 1
                failed_scripts.append(test_name)
                script_generation_progress['failed_scripts'].append(test_name)
                
        except Exception as e:
            debug_log(f"FAILED: Error generating script for {test_name}: {str(e)}")
            debug_log(f"Exception traceback: {traceback.format_exc()}")
            failed_count += 1
            failed_scripts.append(test_name)
            script_generation_progress['failed_scripts'].append(test_name)
        
        # Calculate progress but cap at 95% during processing
        progress_percent = int((i + 1) / total_to_process * 95)  # Cap at 95%
        debug_log(f"Progress: {progress_percent}% - Processed {test_name}")
    
    # Update final progress status - this will trigger 100% completion
    script_generation_progress['status'] = 'completed'
    script_generation_progress['current'] = total_to_process
    script_generation_progress['message'] = 'Finalizing script generation...'
    
    message = f"Generated {generated_count} Python test scripts!"
    if failed_count > 0:
        message += f" {failed_count} failed: {', '.join(failed_scripts)}"
    
    script_generation_progress['message'] = message
    
    debug_log("=== COMPLETED GENERATE_SCRIPTS ENDPOINT ===")
    
    return jsonify({
        "success": True,
        "message": message,
        "generated_count": generated_count,
        "failed_count": failed_count,
        "total_processed": total_to_process,
        "missing_scripts": missing_scripts
    })

def clean_generated_script(script_content):
    """Clean generated script to remove unwanted headers and comments"""
    
    if not script_content or not script_content.strip():
        return script_content
    
    lines = script_content.split('\n')
    cleaned_lines = []
    skip_header = True
    
    for line in lines:
        stripped_line = line.strip()
        
        # Skip header comments at the beginning
        if skip_header:
            # Skip lines that are part of header comments
            if (stripped_line.startswith('"""') or 
                stripped_line.startswith("'''") or
                stripped_line.startswith('AI-Generated') or
                stripped_line.startswith('Generated on') or
                stripped_line.startswith('Test Case Information') or
                stripped_line.startswith('- Precondition:') or
                stripped_line.startswith('- Description:') or
                stripped_line.startswith('- Expected Result:') or
                stripped_line.startswith('- Script Description:') or
                stripped_line == '"""' or
                stripped_line == "'''"):
                continue
            elif stripped_line.startswith('from ') or stripped_line.startswith('import '):
                # Found the actual code start
                skip_header = False
                cleaned_lines.append(line)
            elif not stripped_line:  # Empty line
                continue
            else:
                # Non-import line found, stop skipping
                skip_header = False
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def validate_script_completeness(script_content):
    """Validate that the generated script is complete, not truncated, and uses proper function patterns"""
    
    if not script_content or not script_content.strip():
        debug_log("Script validation failed: Empty script")
        return False
    
    # Check for common signs of truncation
    lines = script_content.strip().split('\n')
    last_line = lines[-1].strip() if lines else ""
    
    # Signs of incomplete script
    truncation_indicators = [
        # Incomplete statements
        lambda line: line.endswith('=') or line.endswith(','),
        # Incomplete function definitions
        lambda line: line.endswith(':') and not line.strip().startswith('#'),
        # Incomplete control structures
        lambda line: any(line.strip().endswith(keyword + ':') for keyword in ['if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally']),
        # Incomplete string literals
        lambda line: line.count('"') % 2 != 0 or line.count("'") % 2 != 0,
        # Very short scripts (likely incomplete)
        lambda line: len(script_content.strip()) < 200,
        # Ends with incomplete comment
        lambda line: line.startswith('#') and len(line) > 50 and not line.endswith('.'),
    ]
    
    for indicator in truncation_indicators:
        if indicator(last_line):
            debug_log(f"Script validation failed: Truncation indicator detected in last line: '{last_line}'")
            return False
    
    # Check for proper function usage patterns
    function_warnings = []
    
    # Check if script uses improper run_adb_command function
    if 'run_adb_command(' in script_content:
        function_warnings.append("Uses undefined run_adb_command() function - should use run_adb() pattern")
    
    # Check if script has proper run_adb pattern
    if 'run_adb(' in script_content:
        # Verify it follows the proper pattern
        has_proper_pattern = ('stdout, stderr, rc = run_adb(' in script_content and
                              'if stderr:' in script_content and
                              'save_to_notepad(' in script_content)
        if not has_proper_pattern:
            function_warnings.append("run_adb() usage doesn't follow proper pattern with error handling")
    
    # Check if script uses proper test_passed boolean flag
    if 'test_passed = "' in script_content:
        function_warnings.append("Uses test_passed as string instead of boolean flag")
    elif 'test_passed =' in script_content and 'test_passed = False' in script_content:
        # Good - uses boolean flag
        pass
    elif 'test_passed' not in script_content:
        function_warnings.append("Missing test_passed boolean flag")
    
    # Check if script uses cleanup_recordings properly
    if 'cleanup_recordings(' in script_content:
        has_proper_cleanup = ('cleanup_recordings(test_passed, test_name)' in script_content)
        if not has_proper_cleanup:
            function_warnings.append("cleanup_recordings() doesn't use proper pattern with test_passed flag")
    
    # Log warnings but don't fail validation (they can be addressed in generation)
    for warning in function_warnings:
        debug_log(f"Script validation warning: {warning}")
    
    # Check for proper Python syntax structure
    try:
        # Basic check - should have at least some common Python keywords
        required_patterns = ['def ', 'import ', 'if ', 'try:']
        has_structure = any(pattern in script_content for pattern in required_patterns)
        
        if not has_structure:
            debug_log("Script validation failed: Missing basic Python structure")
            return False
            
        # Check for balanced parentheses/brackets
        open_parens = script_content.count('(') - script_content.count(')')
        open_brackets = script_content.count('[') - script_content.count(']')
        open_braces = script_content.count('{') - script_content.count('}')
        
        if open_parens != 0 or open_brackets != 0 or open_braces != 0:
            debug_log(f"Script validation failed: Unbalanced brackets - parens: {open_parens}, brackets: {open_brackets}, braces: {open_braces}")
            return False
            
    except Exception as e:
        debug_log(f"Script validation error during syntax check: {e}")
        return False
    
    debug_log("Script validation passed: Script appears complete")
    if function_warnings:
        debug_log(f"Note: {len(function_warnings)} function usage warnings detected")
    return True

def sanitize_script_description_for_api(script_description):
    """Remove security-sensitive commands from script description for API processing"""
    
    sensitive_patterns = [
        # SSH commands
        r'ssh -i [^"]*"[^"]*"[^"]*"[^"]*"',
        r'ssh -i id_ed25519_idcevo[^"]*"[^"]*"',
        # Specific sensitive command patterns
        r'run the following command in Windows cmd to resume DLT logs after reboot:[^.]*\.',
        # Other patterns that might trigger filtering
        r'StrictHostKeyChecking=no',
        r'ConnectTimeout=\d+',
        r'nohup dlt-receive[^"]*>[^"]*&"',
    ]
    
    sanitized = script_description
    replacements = []
    
    for pattern in sensitive_patterns:
        import re
        matches = re.findall(pattern, sanitized, re.IGNORECASE)
        for i, match in enumerate(matches):
            placeholder = f"[SENSITIVE_COMMAND_{len(replacements)}]"
            sanitized = sanitized.replace(match, placeholder)
            replacements.append((placeholder, match))
    
    return sanitized, replacements

def restore_sensitive_commands(script_content, replacements):
    """Restore sensitive commands back into the generated script"""
    
    restored_script = script_content
    
    for placeholder, original_command in replacements:
        # Convert the original command to proper Python code format
        if "ssh -i" in original_command:
            # Convert SSH command to Python format
            python_command = f'command = "{original_command}"'
            python_execution = f"""stdout, stderr, rc = run_cmd(command)
if stderr:
    save_to_notepad(f"[Command failed:] ({{command}}:)")
    save_to_notepad(f"Error text: {{stderr}}\\n")
save_to_notepad(f"[Executed command:] ({{command}}:)")
save_to_notepad(f"Result: {{stdout}}\\n")
assert rc == 0, f"Command {{command}} failed: {{rc}}\\n\""""
            
            # Replace placeholder with proper Python code
            restored_script = restored_script.replace(
                f"# {placeholder}",
                python_execution
            )
            restored_script = restored_script.replace(
                placeholder,
                python_execution
            )
    
    return restored_script

def generate_python_script(test_name, precondition, description, expected_result, script_description, existing_scripts):
    """Generate Python test script using LiteLLM API with proper timeout handling and no header comments"""
    
    debug_log(f"=== STARTING SCRIPT GENERATION FOR: {test_name} ===")
    
    if litellm is None:
        debug_log("ERROR: LiteLLM is not available!")
        raise Exception("LiteLLM is not available")
    
    # Check if this is a security-sensitive test case
    is_sensitive_test = any([
        "ssh -i" in script_description.lower(),
        "dlt-receive" in script_description.lower(),
        "stricthostkeychecking" in script_description.lower(),
        len(script_description) > 3000  # Very long descriptions might also trigger issues
    ])
    
    if is_sensitive_test:
        debug_log(f"Detected security-sensitive test case: {test_name}")
        # Sanitize the script description for API processing
        sanitized_description, sensitive_replacements = sanitize_script_description_for_api(script_description)
        debug_log(f"Sanitized {len(sensitive_replacements)} sensitive commands")
        script_description_for_api = sanitized_description
    else:
        script_description_for_api = script_description
        sensitive_replacements = []
    
    # Configure LiteLLM with working settings and timeout
    litellm.api_base = "https://brllm.harman.com"
    litellm.api_key = "sk-WZrmCvrdiCijVsm9XLVFbw"
    litellm.set_verbose = True
    litellm.request_timeout = 300  # Set 5 minute timeout
    
    # Optimize examples - only include relevant parts and limit size
    optimized_examples = []
    for script in existing_scripts[:2]:  # Reduce to 2 examples
        if len(script) > 3000:  # If script is too long, truncate it
            lines = script.split('\n')
            # Keep first 30 lines and last 10 lines
            truncated = '\n'.join(lines[:30] + ['...', '# (script truncated for brevity)', '...'] + lines[-10:])
            optimized_examples.append(truncated)
        else:
            optimized_examples.append(script)
    
    existing_examples = "\n\n=== EXAMPLE SEPARATOR ===\n\n".join(optimized_examples)
    
    # Create a prompt that emphasizes following exact patterns and functions from reference scripts
    # Use the sanitized script description for API processing
    prompt = f"""You are tasked with generating a COMPLETE Python test script for "{test_name}".

CRITICAL REQUIREMENTS:
1. Use EXACTLY the same functions, imports, and patterns as shown in the examples
2. Follow EXACTLY the steps in the test script description 
3. Use the SAME function names and calling patterns from the examples
4. Do NOT add any header comments or documentation blocks
5. Start directly with the imports like the examples
6. Use the exact same error handling patterns as the examples
7. For any placeholder commands like [SENSITIVE_COMMAND_X], add a comment indicating where sensitive commands should be placed

MANDATORY FUNCTION USAGE PATTERNS:

SCREEN RECORDING SETUP:
- ALWAYS start tests with this exact screen recording pattern for HU:
  # Create recordings folder and start screen recording for HU
  create_recordings_folder()
  save_to_notepad(f"Created recordings folder\\n")

  save_to_notepad(f"Starting screen recording for HU...\\n")
  hu_recording_started = start_screen_recording(f"-s {{HU}}", test_name, "HU")

  if hu_recording_started:
      save_to_notepad(f"HU screen recording started successfully\\n")
  else:
      save_to_notepad(f"Warning: Failed to start HU screen recording\\n")

  time.sleep(2)  # Wait for recordings to initialize

- For Mobile device screen recording, use this pattern:
  save_to_notepad(f"Starting screen recording for Mobile...\\n")
  mobile_recording_started = start_screen_recording(f"-s {{Mobile1}}", test_name, "Mobile")

  if mobile_recording_started:
      save_to_notepad(f"Mobile screen recording started successfully\\n")
  else:
      save_to_notepad(f"Warning: Failed to start Mobile screen recording\\n")

  time.sleep(2)  # Wait for recordings to initialize

ADB COMMANDS:
- Use run_adb() with this exact pattern:
  command = f"shell settings get secure bluetooth_name"
  stdout, stderr, rc = run_adb(command, Mobile1)
  if stderr:
      save_to_notepad(f"[Command failed:] ({{command}}:)")
      save_to_notepad(f"Error text: {{stderr}}\\n")
  save_to_notepad(f"[Executed command:] ({{command}}:)")  
  save_to_notepad(f"Result: {{stdout}}\\n") 
  assert rc == 0, f"Command {{command}} failed: {{rc}}\\n"

SAVE EXCEL SETUP (PASSED/FAILED):
# Check test result
if found == True:
    success_message = f"Multiparty call switching functionality works correctly - test Passed.\n"
    save_to_notepad(f"{{success_message}}\\n")
    save_to_notepad(header="TEST PASSED", color="green")
    save_to_excel(test_name, "Passed", success_message)
    test_passed = True
else:
    assert False, f"Call switching failed - test Failed\n"

except AssertionError as e:
    error_message = str(e)
    save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
    save_to_excel(test_name, "Failed", error_message)

SWITCH USB PORT EXAMPLE:
    # Check USB Matrix status and switch if needed
    status = USB_Matrix_Status()
    if status == 1:
        select_mobile_device(1, 2)
        save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
    else:
        select_mobile_device(1, 1)
        save_to_notepad(f"Switched USB Matrix to port 1\n")       
    time.sleep(3)

except AssertionError as e:
    error_message = str(e)
    save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
    save_to_excel(test_name, "Failed", error_message)

SCREENSHOT EXAMPLE:
        # Take a screenshot of HU screen
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/{{test_name}}\\.png",
            f"pull /sdcard/{{test_name}}\\.png"
        ]
        
        for cmd in commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({{cmd}}\\:)")
                save_to_notepad(f"Error text: {{stderr}}\\\n")
            save_to_notepad(f"[Executed command:] ({{cmd}}\\:)")  
            save_to_notepad(f"Result: {{stdout}}\\\n") 
            assert rc == 0, f"Command {{cmd}}\\ failed: {{rc}}\\\n"

        screenshots_dir = f"{{base_dir}}/Test_results/Screenshots".replace('/', '\\')
        command = f'move {{test_name}}.png "{{screenshots_dir}}"'
        stdout, stderr, rc = run_cmd(command)
        if stderr:
            save_to_notepad(f"[Command failed:] ({{command}}\\:)")
            save_to_notepad(f"Error text: {{stderr}}\\\n")
        save_to_notepad(f"[Executed command:] ({{command}}\\:)")  
        save_to_notepad(f"Result: {{stdout}}\\\n") 
        assert rc == 0, f"Command {{command}}\\ failed: {{rc}}\\\n"
        save_to_notepad(f"Device screenshot saved successfully.\n")

WINDOWS COMMANDS:
- Use run_cmd() for Windows commands:
  command = f"your_windows_command"
  stdout, stderr, rc = run_cmd(command)
  if stderr:
      save_to_notepad(f"[Command failed:] ({{command}}:)")
      save_to_notepad(f"Error text: {{stderr}}\\n")
  save_to_notepad(f"[Executed command:] ({{command}}:)")  
  save_to_notepad(f"Result: {{stdout}}\\n")
  assert rc == 0, f"Command {{command}} failed: {{rc}}\\n"

DELAYS:
- Add time.sleep() calls after commands based on patterns from examples:
  * time.sleep(1) after button clicks
  * time.sleep(2) after settings operations
  * time.sleep(3) after USB matrix operations
  * time.sleep(5) after dial commands
  * time.sleep(10) after pairing operations
  * time.sleep(60) after power on/off operations

ICON CLICKS WITH SCREENSHOTS:
- For find_icon_in_screenshot(), use this complete pattern:
  commands = [
      f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
      f"pull /sdcard/screenshot.png {{path}}",
      f"shell input tap 0 0"  # Will be replaced with actual coordinates
  ]
  
      for i, cmd in enumerate(commands):
          if i == 2:  # Icon tap command
              x, y = find_icon_in_screenshot(f"{{path}}/screenshot.png", f"{{path}}/helpers/Icon_Name.png")
              if x == 0 or y == 0:
                  x, y = find_icon_in_screenshot(f"{{path}}/screenshot.png", f"{{path}}/helpers/Icon_Name_2.png")
              cmd = f"shell input tap {{x}} {{y}}"
          
          stdout, stderr, rc = run_adb(cmd, HU)
          if stderr:
              save_to_notepad(f"[Command failed:] ({{cmd}}:)")
              save_to_notepad(f"Error text: {{stderr}}\\n")
          save_to_notepad(f"[Executed command:] ({{cmd}}:)")  
          save_to_notepad(f"Result: {{stdout}}\\n")
          assert rc == 0, f"Command {{cmd}} failed: {{rc}}\\n"
          
          if i == 2:  # After icon tap
              assert x != 0 and y != 0, f"Icon has not been found on display.\\n"
              save_to_notepad(f"Icon has been found and pressed!\\n")
      
    # Clean up screenshot
    screenshot_path = f"{{base_dir}}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
    cmd = f'del "{{screenshot_path}}"'
    stdout, stderr, rc = run_cmd(cmd)

Test Case: {test_name}
Script Description (implement EXACTLY): {script_description_for_api}

Reference Examples showing EXACT patterns to follow:
{existing_examples}

Generate a Python script that:
- Starts with imports (no header comments)  
- Uses all the exact patterns shown above
- Includes appropriate time.sleep() delays
- Uses proper screenshot handling for icon clicks
- Uses proper assert statements with logging
- Follows the exact steps from the script description
- Is complete and executable

Output ONLY the Python code starting with imports:"""
    
    debug_log(f"Optimized prompt prepared for {test_name}, length: {len(prompt)} characters")
    debug_log("Sending request to LiteLLM API...")
    
    try:
        # Make API call with timeout and retry settings
        response = litellm.completion(
            model="sonnet-4-asia",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=8000,
            timeout=300,  # 5 minute timeout
            custom_llm_provider="openai"
        )
        
        debug_log("SUCCESS: Received response from LiteLLM API")
        
        # Extract the generated script from the API response
        generated_script = response.choices[0].message.content.strip()
        
        # Clean up the response to ensure it's valid Python
        if "```python" in generated_script:
            # Extract code from markdown code blocks
            start = generated_script.find("```python") + 9
            end = generated_script.find("```", start)
            if end > start:
                generated_script = generated_script[start:end].strip()
        elif "```" in generated_script:
            # Extract code from generic code blocks
            start = generated_script.find("```") + 3
            end = generated_script.find("```", start)
            if end > start:
                generated_script = generated_script[start:end].strip()
        
        # If this was a sensitive test case, restore the sensitive commands
        if is_sensitive_test and sensitive_replacements:
            debug_log(f"Restoring {len(sensitive_replacements)} sensitive commands")
            generated_script = restore_sensitive_commands(generated_script, sensitive_replacements)
        
        debug_log(f"Generated script length: {len(generated_script)}")
        debug_log(f"First 150 chars of script: {generated_script[:150]}...")
        debug_log(f"Last 150 chars of script: {generated_script[-150:]}")
        
        # Validate the script is complete and not truncated
        if not validate_script_completeness(generated_script):
            debug_log("WARNING: Script appears to be incomplete, attempting simplified regeneration...")
            
            # Try with a much simpler prompt emphasizing exact patterns from examples
            simple_prompt = f"""Generate Python test script for "{test_name}" using EXACT patterns from examples.

CRITICAL REQUIREMENTS:
- Use run_adb() function with this exact pattern:
  command = f"your_adb_command"
  stdout, stderr, rc = run_adb(command, device)
  if stderr: save_to_notepad(f"[Command failed:] ({{command}}:)")
  save_to_notepad(f"[Executed command:] ({{command}}:)")
  assert rc == 0, f"Command {{command}} failed: {{rc}}\\n"
- Use test_passed = False boolean flag
- Use cleanup_recordings(test_passed, test_name)
- NO header comments

Script Description: {script_description_for_api}

Examples showing exact patterns:
{existing_examples}

Generate Python code starting with imports (no comments):"""
            
            retry_response = litellm.completion(
                model="sonnet-4-asia",
                messages=[{"role": "user", "content": simple_prompt}],
                temperature=0.2,
                max_tokens=6000,
                timeout=180,  # 3 minute timeout for retry
                custom_llm_provider="openai"
            )
            
            generated_script = retry_response.choices[0].message.content.strip()
            
            # Clean up the retry response
            if "```python" in generated_script:
                start = generated_script.find("```python") + 9
                end = generated_script.find("```", start)
                if end > start:
                    generated_script = generated_script[start:end].strip()
            elif "```" in generated_script:
                start = generated_script.find("```") + 3
                end = generated_script.find("```", start)
                if end > start:
                    generated_script = generated_script[start:end].strip()
            
            # If this was a sensitive test case, restore the sensitive commands for retry too
            if is_sensitive_test and sensitive_replacements:
                debug_log(f"Restoring {len(sensitive_replacements)} sensitive commands in retry")
                generated_script = restore_sensitive_commands(generated_script, sensitive_replacements)
            
            debug_log(f"Retry generated script length: {len(generated_script)}")
            debug_log(f"Retry last 150 chars: {generated_script[-150:]}")
        
        # Clean up the script to remove any unwanted comments or headers
        final_script = clean_generated_script(generated_script)
        
        debug_log(f"Final script length: {len(final_script)}")
        debug_log(f"=== SUCCESSFULLY COMPLETED SCRIPT GENERATION FOR: {test_name} ===")
        return final_script
        
    except Exception as e:
        debug_log(f"CRITICAL ERROR generating script with LiteLLM API: {str(e)}")
        full_error = traceback.format_exc()
        debug_log(f"Full traceback: {full_error}")
        
        # Re-raise the exception so the calling function knows it failed
        raise Exception(f"Failed to generate script for {test_name}: {str(e)}")

############################################
# Progress tracking for script generation
############################################
script_generation_progress = {
    'current': 0,
    'total': 0,
    'status': 'idle',
    'message': '',
    'completed_scripts': [],
    'failed_scripts': []
}

@app.route("/get_script_progress", methods=["GET"])
def get_script_progress():
    """Get current progress of script generation"""
    return jsonify(script_generation_progress)

############################################
# Test endpoint to verify LiteLLM works
############################################
@app.route("/test_litellm", methods=["GET"])
def test_litellm():
    """Test endpoint to verify LiteLLM API connection"""
    
    debug_log("=== TESTING LITELLM CONNECTION ===")
    
    if litellm is None:
        debug_log("ERROR: LiteLLM is not available!")
        return jsonify({
            "success": False,
            "message": "LiteLLM is not available - import failed"
        })
    
    try:
        debug_log("LiteLLM imported successfully, testing connection...")
        
        # Configure LiteLLM with working settings
        litellm.api_base = "https://brllm.harman.com"
        litellm.api_key = "sk-WZrmCvrdiCijVsm9XLVFbw"  # Valid Harman LiteLLM key
        litellm.set_verbose = True
        
        debug_log(f"LiteLLM API base set to: {litellm.api_base}")
        debug_log(f"LiteLLM API key set: {litellm.api_key}")
        debug_log(f"LiteLLM verbose mode: {litellm.set_verbose}")
        
        # Simple test prompt
        debug_log("Making test API call...")
        response = litellm.completion(
            model="sonnet-4-asia",
            messages=[{"role": "user", "content": "Say hello and confirm you are working."}],
            max_tokens=50,
            custom_llm_provider="openai"
        )
        
        result = response.choices[0].message.content.strip()
        debug_log(f"LiteLLM test successful: {result}")
        
        return jsonify({
            "success": True,
            "message": "LiteLLM API is working!",
            "response": result
        })
        
    except Exception as e:
        error_details = traceback.format_exc()
        debug_log(f"LiteLLM test failed: {str(e)}")
        debug_log(f"Full error details: {error_details}")
        
        return jsonify({
            "success": False,
            "message": f"LiteLLM API test failed: {str(e)}",
            "error_details": error_details
        })

############################################
@app.route("/")
def index():
   return render_template("index.html")

############################################
app.run(debug=True)
