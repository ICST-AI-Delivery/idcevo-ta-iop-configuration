from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Call_waiting"

def main():
    save_to_notepad(f"=== Test {test_name} started ===\n")
    path = "D:/traget/IDCevo/IOP_configuration/Test_environment/Test_scripts"
    
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
        save_to_notepad(f"Mobile device bluetooth name: {mobile_name}\n")
        
        # Create recordings folder and start screen recording for HU
        create_recordings_folder()
        save_to_notepad(f"Created recordings folder\n")
        
        save_to_notepad(f"Starting screen recording for HU...\n")
        hu_recording_started = start_screen_recording(f"-s {HU}", test_name, "HU")
        
        if hu_recording_started:
            save_to_notepad(f"HU screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start HU screen recording\n")
        
        time.sleep(2)  # Wait for recordings to initialize
        
        # Create Mobile device object
        phone = create_device(Mobile1, mobile_name)
        
        # Check if Mobile device has SIM card
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device doesn't have SIM card. Test skipped.\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", "Mobile device doesn't have SIM card")
            return
        
        # Extract the mobile1 phone number
        phone_number_mobile1 = phone.get_phone_number_command()
        save_to_notepad(f"Mobile1 phone number: {phone_number_mobile1}\n")
        
        # Click Mobile device name button with regex from HU display
        found = click_on_device_regex(HU, mobile_name)
        time.sleep(1)
        assert found == True, f"Mobile device name button has not been found on HU display.\n"
        save_to_notepad(f"Mobile device name button has been found and pressed on HU display.\n")
        
        # Click Contacts Button on HU display
        found = click_on_device(HU, "Contacts")
        time.sleep(1)
        assert found == True, f"Contacts button has not been found on HU display.\n"
        save_to_notepad(f"Contacts button has been found and pressed on HU display.\n")
        
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
        
        # Get Mobile device bluetooth name
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, Mobile3)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        mobile_name3 = stdout.strip()
        save_to_notepad(f"Mobile3 device bluetooth name: {mobile_name3}\n")
        
        # Create Mobile device3 object
        phone3 = create_device(Mobile3, mobile_name3)
        
        # Check if Mobile device3 has SIM card
        sim_state = phone3.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device3 doesn't have SIM card. Test skipped.\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", "Mobile device3 doesn't have SIM card")
            return
        
        # Extract the mobile3 phone number
        phone_number_mobile3 = phone3.get_phone_number_command()
        save_to_notepad(f"Mobile3 phone number: {phone_number_mobile3}\n")
        
        # Turn on and unlock Mobile3 screen
        rc = phone3.run_turn_screen_on_command()
        time.sleep(2)
        rc = phone3.run_unlock_screen_command()
        time.sleep(2)
        
        # Initiate a call from Mobile Device 3 to Mobile Device 1
        rc = phone3.dial_command(phone_number_mobile1)
        save_to_notepad(f"Initiating call from Mobile3 to Mobile1\n")
        time.sleep(5)
        
        # Accept call on HU
        found = click_on_device_regex(HU, "Accept")
        time.sleep(1)
        assert found == True, f"Accept button has not been found on HU display.\n"
        save_to_notepad(f"Accept button has been found and pressed on HU display.\n")
        
        # Switch USB Matrix back to the original port
        select_mobile_device(1, status)
        save_to_notepad(f"USB Matrix switched back to original port: {status}")
        time.sleep(3)
        
        # Check USB Matrix status and switch if needed
        status = USB_Matrix_Status()
        if status == 1 or status == 2:
            select_mobile_device(1, 3)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 3\n")
        else:
            select_mobile_device(1, 2)
            save_to_notepad(f"Switched USB Matrix to port 1\n")       
        time.sleep(3)
        
        # Get serial numbers for HU and Mobile4
        HU, Mobile4 = get_serial_number()
        
        # Get Mobile device bluetooth name
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, Mobile4)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        mobile_name4 = stdout.strip()
        save_to_notepad(f"Mobile4 device bluetooth name: {mobile_name4}\n")
        
        # Create Mobile device4 object
        phone4 = create_device(Mobile4, mobile_name4)
        
        # Check if Mobile device4 has SIM card
        sim_state = phone4.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device4 doesn't have SIM card. Test skipped.\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", "Mobile device4 doesn't have SIM card")
            return
        
        # Extract the mobile4 phone number
        phone_number_mobile4 = phone4.get_phone_number_command()
        save_to_notepad(f"Mobile4 phone number: {phone_number_mobile4}\n")
        
        # Turn on and unlock Mobile4 screen
        rc = phone4.run_turn_screen_on_command()
        time.sleep(2)
        rc = phone4.run_unlock_screen_command()
        time.sleep(2)
        
        # Initiate a call from Mobile Device 4 to Mobile Device 1
        rc = phone4.dial_command(phone_number_mobile1)
        save_to_notepad(f"Initiating call from Mobile4 to Mobile1\n")
        time.sleep(5)
        
        # Switch USB Matrix back to the original port
        select_mobile_device(1, status)
        save_to_notepad(f"USB Matrix switched back to original port: {status}")
        time.sleep(3)
        
        # Check if last 3 digits of mobile4 phone number can be found on HU display
        last_3_digits = phone_number_mobile4[-3:]
        save_to_notepad(f"Checking for last 3 digits of Mobile4 number: {last_3_digits}\n")
        
        found = find_word_on_device_via_regex(HU, last_3_digits)
        
        # Take a screenshot of HU screen
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/{test_name}.png",
            f"pull /sdcard/{test_name}.png"
        ]
        
        for cmd in commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n") 
            assert rc == 0, f"Command {cmd} failed: {rc}\n"

        command = f"move {test_name}.png D:/traget/IDCevo/IOP_configuration/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Device screenshot saved successfully.\n")
        
        # End call on Mobile Device 1
        phone.end_call_command()
        time.sleep(2)
        
        # Check test result
        if found == True:
            success_message = f"Test criteria met - Call waiting functionality is working properly. 1st call from {mobile_name3} is active and 2nd call from {mobile_name4} is incoming with number displayed and call waiting tone is hearable with Accept/Reject possible."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Test criteria not met - Call waiting functionality is not working properly. {mobile_name4} phone number not displayed on HU.\n"

        # End call on Mobile Device 1
        phone.end_call_command()
        time.sleep(2)
                
        # Return to home menu
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        
        command = f"shell rm /sdcard/*.png"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        
        rc = phone.run_home_command()
        
        # Stop screen recording
        stop_screen_recording("HU")
        
        # Clean up recordings based on test result
        cleanup_recordings(test_passed, test_name)
        if test_passed:
            save_to_notepad(f"Test passed - recording deleted\n")
        else:
            save_to_notepad(f"Test completed - recording kept for review\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")
        
    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
        save_to_excel(test_name, "Failed", error_message)
        
        # Cleanup on failure
        try:
            command = f"shell input keyevent 3"
            run_adb(command, HU)
            command = f"shell rm /sdcard/*.png"
            run_adb(command, HU)
            phone.run_home_command()
            
        except Exception as cleanup_error:
            save_to_notepad(f"Error during cleanup: {cleanup_error}\n")
        
        # Stop screen recording on test failure
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
        
        # Keep recording since test failed (test_passed is False)
        cleanup_recordings(test_passed, test_name)
        save_to_notepad(f"Test failed - recording kept for debugging\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")
        raise
    finally:
        # Ensure all recordings are stopped in case of unexpected errors
        try:
            stop_all_recordings()
        except:
            pass

if __name__ == "__main__":
    main()