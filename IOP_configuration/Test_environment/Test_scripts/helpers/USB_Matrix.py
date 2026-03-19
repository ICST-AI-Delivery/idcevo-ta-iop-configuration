import serial
import time
import subprocess
import re

device_names = [
    "HU",
    "Mobile"
]
device_commands = {}

# Global variable for serial connection
ser = None

def init_serial_connection():
    """Initialize serial connection when needed"""
    global ser
    if ser is None:
        try:
            ser = serial.Serial(
                port='COM38',
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.3
            )
        except Exception as e:
            print(f"Warning: Could not initialize serial connection to COM38: {e}")
            ser = None
    return ser

def get_adb_devices():
    # Return the list of ADB devices connected
    result = subprocess.run(["adb","devices","-l"], capture_output=True, text=True)
    return result.stdout.splitlines()

def get_serial_number():
    # Return the Serial Numbers of ADB devices connected
    result = subprocess.run(["adb","devices"], capture_output=True, text=True)
    serial_numbers = result.stdout.splitlines()
    
    # Filter out header line and empty lines, get only device lines
    device_lines = [line for line in serial_numbers if line and '\t' in line and 'device' in line]
    
    HU = ""
    Mobile = ""
    
    # Separate BMW and non-BMW devices
    bmw_devices = []
    other_devices = []
    
    for line in device_lines:
        serial_number = line.split('\t')[0]
        # Get device details to check for BMW
        device_details_result = subprocess.run(["adb", "-s", serial_number, "shell", "getprop", "ro.product.model"], capture_output=True, text=True)
        device_model = device_details_result.stdout.strip()
        
        if "BMW" in device_model:
            bmw_devices.append(serial_number)
        else:
            other_devices.append(serial_number)
    
    # Assign BMW device to HU, other device to Mobile
    if bmw_devices:
        HU = bmw_devices[0]
    if other_devices:
        Mobile = other_devices[0]
    
    # If no BMW device found but we have devices, use first device as HU
    if not HU and device_lines:
        HU = device_lines[0].split('\t')[0]
        if len(device_lines) > 1:
            Mobile = device_lines[1].split('\t')[0]
    
    return HU, Mobile

def extract_ports(device_lines):
    # Extracting the ADB ports from device list
    ports = []
    for line in device_lines:
        # Skip empty lines and header
        if not line.strip() or "List of devices" in line:
            continue
            
        # Look for transport_id:number pattern at the end of ADB device lines
        transport_match = re.search(r"transport_id:(\d+)", line)
        if transport_match:
            transport_id = transport_match.group(1)
            ports.append(f":{transport_id}")
    return ports

def map_ports_to_names(ports, names):
    # Associate ports with names from list
    mapping = {}
    for idx, port in enumerate(ports):
        if idx < len(names):
            mapping[port] = names[idx]
        else:
            mapping[port] = f"Device_{idx+1}"
    return mapping

def select_mobile_device_1(hub,usb):
    # Select the hub and usb port for USB Matrix
    usb_matrix_command = f"setusbport({hub},{usb},500,500)"
    print(f"usb_matrix_command: {usb_matrix_command}")

    serial_conn = init_serial_connection()
    if serial_conn:
        serial_conn.write((usb_matrix_command + "\r").encode())
        time.sleep(5)

        expected_device_count = 1
        # Verification logic with retry mechanism
        max_retries = 10
        for attempt in range(max_retries):
            print(f"Verification attempt {attempt + 1}/{max_retries}")
            
            # Check number of ADB devices connected
            try:
                result = subprocess.run(
                    'adb devices | findstr /R "device$" | find /C /V ""',
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                device_count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
                print(f"Number of ADB devices connected: {device_count}")
                
                if device_count == expected_device_count:
                    print(f"Successfully verified {expected_device_count} ADB device(s) connected")
                    return True
                else:
                    print(f"Expected {expected_device_count} device(s), found {device_count}. Attempting USB port reset...")
                    
                    # Switch to different USB port (usb+1)
                    temp_usb_command = f"setusbport({hub},{usb+1},500,500)"
                    print(f"Switching to temporary port: {temp_usb_command}")
                    serial_conn.write((temp_usb_command + "\r").encode())
                    
                    # Wait 5 seconds
                    print("Waiting 5 seconds...")
                    time.sleep(5)
                    
                    # Switch back to original port
                    original_usb_command = f"setusbport({hub},{usb},500,500)"
                    print(f"Switching back to original port: {original_usb_command}")
                    serial_conn.write((original_usb_command + "\r").encode())
                    
                    # Wait another 10 seconds for devices to reconnect
                    print("Waiting 10 seconds for devices to reconnect...")
                    time.sleep(10)
                    
            except subprocess.TimeoutExpired:
                print("ADB command timed out")
            except subprocess.CalledProcessError as e:
                print(f"ADB command failed: {e}")
            except ValueError:
                print("Could not parse device count from ADB output")
            except Exception as e:
                print(f"Error during ADB verification: {e}")
        
        print(f"Failed to verify ADB devices after {max_retries} attempts")
        return False
        
    else:
        print("Warning: Serial connection not available for select_mobile_device")
        return False
    
def select_mobile_device(hub,usb):
    # Select the hub and usb port for USB Matrix
    usb_matrix_command = f"setusbport({hub},{usb},500,500)"
    print(f"usb_matrix_command: {usb_matrix_command}")

    serial_conn = init_serial_connection()
    if serial_conn:
        serial_conn.write((usb_matrix_command + "\r").encode())
        time.sleep(5)

        expected_device_count = 2
        # Verification logic with retry mechanism
        max_retries = 10
        for attempt in range(max_retries):
            print(f"Verification attempt {attempt + 1}/{max_retries}")
            
            # Check number of ADB devices connected
            try:
                result = subprocess.run(
                    'adb devices | findstr /R "device$" | find /C /V ""',
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                device_count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
                print(f"Number of ADB devices connected: {device_count}")
                
                if device_count == expected_device_count:
                    print(f"Successfully verified {expected_device_count} ADB device(s) connected")
                    return True
                else:
                    print(f"Expected {expected_device_count} device(s), found {device_count}. Attempting USB port reset...")
                    
                    # Switch to different USB port (usb+1)
                    temp_usb_command = f"setusbport({hub},{usb+1},500,500)"
                    print(f"Switching to temporary port: {temp_usb_command}")
                    serial_conn.write((temp_usb_command + "\r").encode())
                    
                    # Wait 5 seconds
                    print("Waiting 5 seconds...")
                    time.sleep(5)
                    
                    # Switch back to original port
                    original_usb_command = f"setusbport({hub},{usb},500,500)"
                    print(f"Switching back to original port: {original_usb_command}")
                    serial_conn.write((original_usb_command + "\r").encode())
                    
                    # Wait another 10 seconds for devices to reconnect
                    print("Waiting 10 seconds for devices to reconnect...")
                    time.sleep(10)
                    
            except subprocess.TimeoutExpired:
                print("ADB command timed out")
            except subprocess.CalledProcessError as e:
                print(f"ADB command failed: {e}")
            except ValueError:
                print("Could not parse device count from ADB output")
            except Exception as e:
                print(f"Error during ADB verification: {e}")
        
        print(f"Failed to verify ADB devices after {max_retries} attempts")
        return False
        
    else:
        print("Warning: Serial connection not available for select_mobile_device")
        return False

def USB_Matrix_Status():
    # Select the hub and usb port for USB Matrix
    serial_conn = init_serial_connection()
    if not serial_conn:
        print("Warning: Serial connection not available for USB_Matrix_Status")
        return None
        
    serial_conn.setDTR(True)
    serial_conn.setRTS(True)
    serial_conn.reset_input_buffer()
    time.sleep(0.2)
    serial_conn.write(b"sta\r")
    time.sleep(0.2)
    responses = []
    for _ in range(5):
        line = serial_conn.readline().decode(errors="ignore").strip()
        if line:
            responses.append(line)
    
    if len(responses) < 2:
        print("Warning: Insufficient responses from USB Matrix")
        return None
    
    # Extract the second parameter from the response string
    response_string = responses[1]
    # Use regex to extract parameters from setusbport(param1,param2,param3,param4)
    match = re.search(r'setusbport\((\d+),(\d+),(\d+),(\d+)\)', response_string)
    if match:
        # Return the second parameter as integer
        return int(match.group(2))
    else:
        # Return None or raise an exception if the format is unexpected
        return None
    
def map_devices_to_ports():
    adb_output = get_adb_devices()
    
    
    # Sort device lines so BMW devices come first
    bmw_devices = []
    other_devices = []
    
    for line in adb_output:
        if "BMW" in line:
            bmw_devices.append(line)
        else:
            other_devices.append(line)
    
    # Combine lists with BMW devices first
    sorted_adb_output = bmw_devices + other_devices
    
    ports = extract_ports(sorted_adb_output)
    mapped_devices = map_ports_to_names(ports,device_names)
    for port_key, device_name in mapped_devices.items():
        port = port_key.lstrip(':')
        device_commands[device_name] = f"adb -t {port}"
        print(device_commands[device_name])
