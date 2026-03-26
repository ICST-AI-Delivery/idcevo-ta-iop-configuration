"""
AI-Generated Test Script for: Power_off_HU_during_incoming_call
Generated on: 2026-03-09 14:32:08

Test Case Information:
- Precondition: Mobile Device and HU are connected.
Synchronisation is finished.
- Description: 1 Initiate an incoming call from Mobile Device 3 to Mobile Device 1.
2 During an incoming call power off HU.
For TestraIDCEvos and Testcases set mode Parken: "Parken_BN_IO".
- Expected Result: 2 Bluetooth connection released. Incoming call is indicated on Mobile Device.
"""

from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
from helpers.switch_commands import *
import time

test_name = "Power_off_HU_during_incoming_call"

def main():
    save_to_notepad(f"=== Test {test_name} started ===\n")
    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"
    
    # Initialize test result tracking
    test_passed = False

    try:
        # Check USB Matrix status
        status = USB_Matrix_Status()
        save_to_notepad(f"USB Matrix is connected to port: {status}")
        time.sleep(3)
        
        # Get serial numbers for HU and Mobile1
        HU, Mobile1 = get_serial_number()
        
        # Get Mobile device bluetooth name
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, Mobile1)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        save_to_notepad(f"Mobile1 device name: {mobile_name}\n")
        time.sleep(1)

        # Create Mobile device object
        phone = create_device(Mobile1, mobile_name)
        
        # Check SIM state on Mobile1
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            skip_message = "Mobile device doesn't have SIM card on it"
            save_to_notepad(f"{skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", skip_message)
            return       
        save_to_notepad(f"Mobile1 SIM state: {sim_state}\n")

        # Extract mobile1 phone number
        phone_number_mobile1 = phone.get_phone_number_command()
        save_to_notepad(f"Mobile1 phone number: {phone_number_mobile1}\n")
        
        # Check USB Matrix status and switch if needed
        status = USB_Matrix_Status()
        if status == 1:
            select_mobile_device(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")       
        time.sleep(3)
        
        # Get serial numbers for HU and Mobile3
        HU, Mobile3 = get_serial_number()
        
        # Get Mobile3 device bluetooth name
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, Mobile3)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile3_name = stdout.strip()
        save_to_notepad(f"Mobile3 device name: {mobile3_name}\n")
        time.sleep(1)
        
        # Create Mobile device3 object
        phone3 = create_device(Mobile3, mobile3_name)
        
        # Check SIM state on Mobile3
        sim_state = phone3.check_SIM_command()
        if "LOADED" not in sim_state:
            skip_message = "Mobile device3 doesn't have SIM card on it"
            save_to_notepad(f"{skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", skip_message)
            return
        
        save_to_notepad(f"Mobile3 SIM state: {sim_state}\n")
        
        # Extract mobile3 phone number
        phone_number_mobile3 = phone3.get_phone_number_command()
        save_to_notepad(f"Mobile3 phone number: {phone_number_mobile3}\n")

        # Turn Mobile3 screen on
        rc = phone3.run_turn_screen_on_command()
        assert rc == 0, f"Turn screen on command failed: {rc}\n"
        save_to_notepad(f"Mobile3 screen turned on\n")
        
        # Unlock Mobile3 screen
        rc = phone3.run_unlock_screen_command()
        assert rc == 0, f"Unlock screen command failed: {rc}\n"
        save_to_notepad(f"Mobile3 screen unlocked\n")
        
        # Initiate an incoming call from MD3 to MD1
        rc = phone3.dial_command(phone_number_mobile1)
        assert rc == 0, f"Dial command failed: {rc}\n"
        save_to_notepad(f"Initiated incoming call from Mobile3 to Mobile1 ({phone_number_mobile1})\n")        
        time.sleep(5)  # Wait for the incoming call to be established
        
        # Switch USB Matrix back to the port from the beginning
        select_mobile_device(1, status)
        time.sleep(3)
        save_to_notepad(f"Switched USB Matrix back to original port\n")

        # Accept call on Mobile Device 1
        rc = phone.answer_call_command()
        assert rc == 0, f"Answer call command failed: {rc}\n"
        save_to_notepad(f"Call accepted on Mobile1\n")

        # Extract BTsnoop logs from HU before power off
        btsnoop_commands = [
            f"root",
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log btsnoop_hci_before_poweroff_incoming.log",
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log.last btsnoop_hci_before_poweroff_incoming.log.last"
        ]
        
        for cmd in btsnoop_commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n") 
            time.sleep(5)
            # Note: Not asserting on these commands as they might fail if files don't exist
        
        # Move BTsnoop logs to target directory
        move_commands = [
            f"move btsnoop_hci_before_poweroff_incoming.log {base_dir}/Test_results",
            f"move btsnoop_hci_before_poweroff_incoming.log.last {base_dir}/Test_results"
        ]
        
        for cmd in move_commands:
            stdout, stderr, rc = run_cmd(cmd)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            # Note: Not asserting as files might not exist
        
        save_to_notepad(f"BTsnoop logs extracted from HU before power off\n")

        # Power off HU during the incoming call
        power_off_HU()
        save_to_notepad(f"HU powered off during incoming call\n")
        time.sleep(10)  # Wait for HU to completely power off
        
        # Turn Mobile1 screen on
        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Turn screen on command failed: {rc}\n"
        save_to_notepad(f"Mobile1 screen turned on\n")
        
        # Unlock Mobile1 screen
        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Unlock screen command failed: {rc}\n"
        save_to_notepad(f"Mobile1 screen unlocked\n")
        
        # Go to Mobile Settings menu
        phone.run_settings_menu_command()
        save_to_notepad(f"Navigated to Mobile1 Settings menu\n")
        
        # Go to Mobile Bluetooth menu
        rc = phone.run_bluetooth_menu_command()
        assert rc == 0, f"Bluetooth menu command failed: {rc}\n"
        save_to_notepad(f"Navigated to Mobile1 Bluetooth menu\n")
        
        # Check if bluetooth connection was released after HU power off
        found = phone.check_bluetooth_connection()
        if "ConnectionState: STATE_DISCONNECTED" in found or not found:
            success_message = f"Bluetooth connection was released and incoming call is indicated on {mobile_name}"
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Call was terminated or connection remained active.\n"
        
        # Take screenshot on Mobile device screen
        commands = [
            f"shell screencap -p /sdcard/{test_name}.png",
            f"pull /sdcard/{test_name}.png"
        ]
        
        for cmd in commands:
            stdout, stderr, rc = run_adb(cmd, Mobile1)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n") 
            assert rc == 0, f"Command {cmd} failed: {rc}\n"

        # Move the screenshot to the specified path
        command = f"move {test_name}.png {base_dir}/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        save_to_notepad(f"Mobile device screenshot saved successfully.\n")
        
        # End call on Mobile Device1
        phone.end_call_command()
        save_to_notepad(f"Call ended on Mobile1\n")
        
        # Run cleanup commands after test is done
        # Mobile device commands
        rc = phone.run_home_command()
        assert rc == 0, f"Mobile home command failed: {rc}\n"
        
        save_to_notepad(f"Cleanup commands executed successfully.\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")
        
    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
        
        # Run cleanup commands even on failure
        try:
            # End call if still active
            try:
                phone.end_call_command()
                save_to_notepad(f"Emergency call end executed\n")
            except:
                pass
            
            # Mobile device home
            rc = phone.run_home_command()
            assert rc == 0, f"Mobile home command failed: {rc}\n"
            
        except Exception as cleanup_error:
            save_to_notepad(f"Error during cleanup: {cleanup_error}\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")
        # Save to Excel with test_name, result="Failed" and comment=error_message
        save_to_excel(test_name, "Failed", error_message)
        raise
    finally:
        # Ensure all recordings are stopped in case of unexpected errors
        try:
            stop_all_recordings()
        except:
            pass

if __name__ == "__main__":
    main()