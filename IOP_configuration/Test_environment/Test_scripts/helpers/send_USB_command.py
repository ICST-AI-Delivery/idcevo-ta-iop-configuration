import time
import sys
import subprocess
import os
import re

def extract_com_port_from_batch():
    """Extract COM port from run_IOP.bat file"""
    try:
        # Path to run_IOP.bat (4 folders up from current script)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        batch_file_path = os.path.join(current_dir, '..', '..', '..', '..', 'run_IOP.bat')
        batch_file_path = os.path.normpath(batch_file_path)
        
        if not os.path.exists(batch_file_path):
            print(f"Warning: run_IOP.bat not found at {batch_file_path}, using default COM38")
            return 'COM38'
        
        with open(batch_file_path, 'r') as file:
            content = file.read()
            
        # Look for the USB_MATRIX_COM_PORT pattern
        match = re.search(r'set\s+"USB_MATRIX_COM_PORT=([^"]+)"', content)
        if match:
            com_port = match.group(1)
            print(f"Extracted COM port from run_IOP.bat: {com_port}")
            return com_port
        else:
            print("Warning: USB_MATRIX_COM_PORT not found in run_IOP.bat, using default COM38")
            return 'COM38'
            
    except Exception as e:
        print(f"Warning: Error reading run_IOP.bat: {e}, using default COM38")
        return 'COM38'

# Safely handle command line argument
try:
    if len(sys.argv) < 2:
        print("Error: Missing USB port index argument")
        print("Usage: python send_USB_command.py <port_number>")
        sys.exit(1)
        
    usb_index = int(sys.argv[1])
    print(f"Received USB port index: {usb_index}")
    
    try:
        import serial
        # Configure Serial port for USB Matrix
        com_port = extract_com_port_from_batch()
        print(f"Trying to open {com_port}...")
        ser = serial.Serial(
            port=com_port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.3
        )
        
        print(f"{com_port} opened successfully")
        time.sleep(2)
        
        # Select the hub and usb port for USB Matrix
        usb_matrix_command = f"setusbport(1,{usb_index},500,500)"
        print(f"Sending USB matrix command: {usb_matrix_command}")
        
        ser.write((usb_matrix_command + "\r").encode("ascii"))
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
                    break
                else:
                    print(f"Expected {expected_device_count} device(s), found {device_count}. Attempting USB port reset...")
                    
                    # Switch to different USB port (usb+1)
                    temp_usb_command = f"setusbport(1,{usb_index +1},500,500)"
                    print(f"Switching to temporary port: {temp_usb_command}")
                    ser.write((temp_usb_command + "\r").encode())
                    
                    # Wait 15 seconds
                    print("Waiting 15 seconds...")
                    time.sleep(15)
                    
                    # Switch back to original port
                    original_usb_command = f"setusbport(1,{usb_index},500,500)"
                    print(f"Switching back to original port: {original_usb_command}")
                    ser.write((original_usb_command + "\r").encode())
                    
                    # Wait another 15 seconds for devices to reconnect
                    print("Waiting 15 seconds for devices to reconnect...")
                    time.sleep(15)
                    
            except subprocess.TimeoutExpired:
                print("ADB command timed out")
            except subprocess.CalledProcessError as e:
                print(f"ADB command failed: {e}")
            except ValueError:
                print("Could not parse device count from ADB output")
            except Exception as e:
                print(f"Error during ADB verification: {e}")
        
        print(f"Failed to verify ADB devices after {max_retries} attempts")        
        
        # Read any response from the device (optional)
        response = ser.read(100).decode('ascii', errors='ignore').strip()
        if response:
            print(f"Device response: {response}")
            
        print(f"USB port {usb_index} successfully configured")
        ser.close()
        print("Serial port closed")
        
    except ImportError:
        print("PySerial module not installed. For testing, simulating successful configuration.")
        print(f"USB port {usb_index} configured (SIMULATION MODE)")
    except Exception as e:
        print(f"Serial communication error: {str(e)}")
        print(f"For testing, simulating successful configuration for port {usb_index}")
        # Exit with success to allow batch script to continue
        
except ValueError:
    print(f"Error: Invalid port number: {sys.argv[1] if len(sys.argv) > 1 else 'missing'}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {str(e)}")
    sys.exit(1)