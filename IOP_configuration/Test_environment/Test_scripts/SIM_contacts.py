from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time
import re

test_name = "SIM_contacts"

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
        HU, Mobile1 = get_serial_number()

        # Get Mobile device global name
        command = f"shell settings get secure bluetooth_name" # Mobile1 command go get device name
        stdout, stderr, rc = run_adb(command, Mobile1)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        mobile_name = stdout.strip()
        save_to_notepad(f"Tested device name: {mobile_name}\n")
        time.sleep(1)
        
        phone = create_device(Mobile1,mobile_name)
        
        # Check if Mobile device has a SIM card
        save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")        
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            skip_message = f"{mobile_name} doesn't have a SIM card on it."
            save_to_notepad(f"TEST SKIPPED: {skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="orange")
            # Save to Excel with test_name, result="Skipped" and comment=skip_message
            save_to_excel(test_name, "Skipped", skip_message)
            save_to_notepad(f"=== Test {test_name} finished (skipped) ===\n")
            return  # Exit the test early
        else:
            save_to_notepad(f"{mobile_name} has a SIM card (state: {sim_state}). Continuing test...\n")

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
        
        # Click Mobile device name button with regex from HU display
        found = click_on_device_regex(HU, mobile_name)
        time.sleep(1)
        assert found == True, f"Mobile device name {mobile_name} has not been found on HU display.\n"
        save_to_notepad(f"Mobile device name {mobile_name} has been found and pressed on HU display.\n")

        # Click Contacts Button from HU display
        found = click_on_device(HU, "Contacts")
        time.sleep(1)
        assert found == True, f"Contacts button has not been found on HU display.\n"
        save_to_notepad(f"Contacts button has been found and pressed on HU display.\n")

        stdout = phone.get_contacts_name_from_SIM_command()
        assert rc == 0, f"Command failed: {rc}\n"
        
        # Extract SIM contact names from the output
        sim_contacts = []
        lines = stdout.strip().split('\n')
        for line in lines:
            if "name=" in line:
                match = re.search(r"name=([^,]+)", line)
                if match:
                    contact_name = match.group(1)
                    sim_contacts.append(contact_name)
                    save_to_notepad(f"First contact in SIM contacts: {contact_name}\n")
                    break

        stdout = phone.get_contacts_data3_command()
        assert rc == 0, f"Data3 query command failed: {rc}\n"
            
        # Extract last name from data3 results
        last_name = None
        lines = stdout.strip().split('\n')
        for line in lines:
            if line.strip() and 'data3=' in line:
                data3_value = line.split('data3=', 1)[1].strip()
                if data3_value and data3_value in contact_name:
                    last_name = data3_value
                    save_to_notepad(f"Found last name on SIM contacts from data3: '{last_name}'\n")
                    break
        
        # If last name is empty, query data2 (first names)
        first_name = None
        if last_name is None:
            save_to_notepad(f"No last name found. Trying to get first name...\n")
            stdout = phone.get_contacts_data2_command()
            assert rc == 0, f"Data2 query command failed: {rc}\n"
            
            # Extract first name from data2 results
            lines = stdout.strip().split('\n')
            for line in lines:
                if line.strip() and 'data2=' in line:
                    data2_value = line.split('data2=', 1)[1].strip()
                    if data2_value and data2_value in contact_name:
                        first_name = data2_value
                        save_to_notepad(f"Found first name on SIM contacts from data2: '{first_name}'\n")
                        break
        
        # Only fail if both first and last names are empty
        if last_name is None and first_name is None:
            assert False, f"No first or last name on SIM contacts found in data results.\n"
        
        # Use last name if available, otherwise use first name
        click_target = last_name if last_name is not None else first_name
        save_to_notepad(f"Using '{click_target}' as the search target.\n")

        # Scroll down on HU display 10 times using the specified coordinates
        for i in range(10):
            # Check if contact word can be found on HU display
            found = find_word_on_device(HU, click_target)
            time.sleep(1)
            if found == False:
                swipe_cmd = f"shell input swipe 1700 700 2000 200"
                stdout, stderr, rc = run_adb(swipe_cmd, HU)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({swipe_cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({swipe_cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n")
                assert rc == 0, f"Swipe command {swipe_cmd} failed: {rc}\n"
                time.sleep(1)
                save_to_notepad(f"Scrolled down {i+1} time(s)\n")
            else:
                break

        if found == True:
            success_message = f"{mobile_name} Contact from SIM card is displayed successfully on HU."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            # Save to Excel with test_name, result="Passed" and comment=success_message
            save_to_excel(test_name, "Passed", success_message)
            # Mark test as passed for recording cleanup
            test_passed = True
        else:
            assert False, f"{mobile_name} Contact from SIM card is not displayed on HU.\n"

        # Take screenshot
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/{test_name}.png",
            f"pull /sdcard/{test_name}.png"
        ]
        
        for cmd in commands:
            stdout, stderr, rc = run_adb(cmd,HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n") 
            assert rc == 0, f"Command {cmd} failed: {rc}\n"

        # move the screenshot
        command = f"move {test_name}.png {base_dir}/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        save_to_notepad(f"HU device screenshot saved successfully.\n")

        # HU home command
        home_cmd = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(home_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({home_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({home_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {home_cmd} failed: {rc}\n"
        time.sleep(1)

        # Click Mobile device name button with regex from HU display
        found = click_on_device_regex(HU, mobile_name)
        time.sleep(1)
        assert found == True, f"Mobile device name {mobile_name} has not been found on HU display.\n"
        save_to_notepad(f"Mobile device name {mobile_name} has been found and pressed on HU display.\n")

        # Swipe up to scroll up (adjust coordinates as needed)
        swipe_cmd = f"shell input swipe 1700 700 200 2500"
        stdout, stderr, rc = run_adb(swipe_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({swipe_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({swipe_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {swipe_cmd} failed: {rc}\n"
        time.sleep(1)

        # Run cleanup commands after test is done
        cleanup_commands = [
            f"shell input keyevent 3",   # HU home
            f"shell rm /sdcard/*.png"   # HU cleanup
        ]
        
        for cmd in cleanup_commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Cleanup command {cmd} failed: {rc}\n"
        
        save_to_notepad(f"Cleanup commands executed successfully.\n")

        # Stop screen recording
        save_to_notepad(f"Stopping screen recording...\n")
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
        
        # Run cleanup commands even on failure
        try:
            # HU home command
            home_cmd = f"shell input keyevent 3"
            stdout, stderr, rc = run_adb(home_cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({home_cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({home_cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Swipe command {home_cmd} failed: {rc}\n"
            time.sleep(1)

            # Click Mobile device name button with regex from HU display
            found = click_on_device_regex(HU, mobile_name)
            time.sleep(1)
            assert found == True, f"Mobile device name {mobile_name} has not been found on HU display.\n"
            save_to_notepad(f"Mobile device name {mobile_name} has been found and pressed on HU display.\n")

            # Swipe up to scroll up (adjust coordinates as needed)
            swipe_cmd = f"shell input swipe 1700 700 200 2500"
            stdout, stderr, rc = run_adb(swipe_cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({swipe_cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({swipe_cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Swipe command {swipe_cmd} failed: {rc}\n"
            time.sleep(1)

            # Run cleanup commands after test is done
            cleanup_commands = [
                f"shell input keyevent 3",   # HU home
                f"shell rm /sdcard/*.png"   # HU cleanup
            ]
            
            for cmd in cleanup_commands:
                stdout, stderr, rc = run_adb(cmd, HU)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n")
                assert rc == 0, f"Cleanup command {cmd} failed: {rc}\n"
        except Exception as cleanup_error:
            save_to_notepad(f"Error during cleanup: {cleanup_error}\n")
        
        # Stop screen recording on test failure
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
        
        # Keep recording since test failed (test_passed is False)
        cleanup_recordings(test_passed, test_name)
        save_to_notepad(f"Test failed - recording kept for debugging\n")
        
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