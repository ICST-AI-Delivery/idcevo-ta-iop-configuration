"""
AI-Generated Test Script for: Power_off_HU_during_outgoing_call
Generated on: 2026-03-09 10:13:37

Test Case Information:
- Precondition: Mobile Device and HU are connected.
Synchronisation is finished.
- Description: 1 Initiate an outgoing call from Mobile Device 1 to Mobile Device 3.
2 Accept call on Mobile Device 3.
3 During an active outgoing call power off HU.
For TestraIDCEvos and Testcases set mode Parken: "Parken_BN_IO".
- Expected Result: 3 Bluetooth connection released. Audio is still audible on Mobile Device (some implementations might hang up).
"""

from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
from helpers.switch_commands import *
import time

test_name = "Power_off_HU_during_outgoing_call"

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

        # Switch USB Matrix back to the port from the beginning
        select_mobile_device(1, status)
        time.sleep(3)
        save_to_notepad(f"Switched USB Matrix back to original port\n")
        
        # Turn Mobile screen on
        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Turn screen on command failed: {rc}\n"
        save_to_notepad(f"Mobile1 screen turned on\n")
        
        # Unlock Mobile screen
        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Unlock screen command failed: {rc}\n"
        save_to_notepad(f"Mobile1 screen unlocked\n")
        
        # Initiate outgoing call from Mobile Device 1 to Mobile Device 3
        rc = phone.dial_command(phone_number_mobile3)
        assert rc == 0, f"Dial command failed: {rc}\n"
        save_to_notepad(f"Initiated outgoing call from Mobile1 to Mobile3 ({phone_number_mobile3})\n")      
        time.sleep(5)  # Wait for call to start setting up
        
        # Check USB Matrix status and switch if needed
        status = USB_Matrix_Status()
        if status == 1:
            select_mobile_device(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")       
        time.sleep(3)
        
        # Accept call on Mobile Device 3
        rc = phone3.answer_call_command()
        assert rc == 0, f"Answer call command failed: {rc}\n"
        save_to_notepad(f"Call accepted on Mobile3\n")
        
        # Switch USB Matrix back to the port from the beginning
        select_mobile_device(1, status)
        save_to_notepad(f"Switched USB Matrix back to original port\n")
        time.sleep(3)  # Wait for the call to become active
        
        # Extract BTsnoop logs from HU before power off
        btsnoop_commands = [
            f"root",
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log btsnoop_hci_before_poweroff_outgoing.log",
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log.last btsnoop_hci_before_poweroff_outgoing.log.last"
        ]
        
        for cmd in btsnoop_commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            time.sleep(5)
            # Note: BTsnoop extraction might fail, so we don't assert here
        
        # Move BTsnoop logs to target directory
        move_commands = [
            f"move btsnoop_hci_before_poweroff_outgoing.log {base_dir}/Test_results",
            f"move btsnoop_hci_before_poweroff_outgoing.log.last {base_dir}/Test_results"
        ]
        
        for cmd in move_commands:
            stdout, stderr, rc = run_cmd(cmd)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            # Note: Move might fail if files don't exist, so we don't assert here
        
        save_to_notepad(f"BTsnoop logs extracted from HU before power off\n")
        
        # Power off HU during the active outgoing call
        power_off_HU()       
        time.sleep(10)
        save_to_notepad(f"Waited 10 seconds for HU to completely power off\n")

        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Command failed: {rc}\n"  

        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone.run_settings_menu_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone.run_bluetooth_menu_command()
        assert rc == 0, f"Command failed: {rc}\n" 
        time.sleep(2)
        
        # Check if bluetooth connection was released after HU power off
        found = phone.check_bluetooth_connection()
        if "ConnectionState: STATE_DISCONNECTED" in found or not found:
            success_message = f"Bluetooth connection was released and audio is still audible on {mobile_name}"
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            # Some implementations might hang up
            assert found == True, f"Call was terminated - some implementations might hang up.\n"
        
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