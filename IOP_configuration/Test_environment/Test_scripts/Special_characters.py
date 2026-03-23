from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time
import re

test_name = "Special_characters"

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

        stdout = phone.get_contacts_name_command()
        assert rc == 0, f"Query contacts command failed: {rc}\n"
        
        # Extract all display_names into a list and find first contact with special characters
        contact_with_special_chars = None
        special_chars_pattern = re.compile(r'[\$%&\*\+!@#\^\(\)\[\]\{\}\\|;:"\',<>?/~`]')
        
        lines = stdout.strip().split('\n')
        for line in lines:
            if line.strip() and '=' in line:
                # Parse the line format: Row: 0 _id=X, display_name=Y
                fields = line.split(',')
                display_name = None
                
                for field in fields:
                    field = field.strip()
                    if 'display_name=' in field:
                        display_name = field.split('=', 1)[1].strip()
                        break
                
                # Check if display_name contains special characters
                if display_name and special_chars_pattern.search(display_name):
                    contact_with_special_chars = display_name
                    save_to_notepad(f"Found first contact with special characters: '{contact_with_special_chars}'\n")
                    break
        
        if contact_with_special_chars is None:
            assert False, f"No contact found with special characters in mobile device contacts.\n"

        stdout = phone.get_contacts_data2_command()
        assert rc == 0, f"Data2 query command failed: {rc}\n"
        
        # Extract all data2 values into a list
        data2_list = []
        lines = stdout.strip().split('\n')
        for line in lines:
            if line.strip() and 'data2=' in line:
                data2_value = line.split('data2=', 1)[1].strip()
                if data2_value:
                    data2_list.append(data2_value)
        
        save_to_notepad(f"Extracted data2 list: {data2_list}\n")

        # Check if contact_with_special_chars is found in data2 list
        if contact_with_special_chars in data2_list:
            # Click on the full contact name with verification from HU display
            click_target = contact_with_special_chars
            save_to_notepad(f"Contact '{contact_with_special_chars}' found in data2 list. Will click on full contact name.\n")
        else:
            stdout = phone.get_contacts_data3_command()
            assert rc == 0, f"Data3 query command failed: {rc}\n"
            
            # Extract last name from data3 results
            last_name = None
            lines = stdout.strip().split('\n')
            for line in lines:
                if line.strip() and 'data3=' in line:
                    data3_value = line.split('data3=', 1)[1].strip()
                    if data3_value and special_chars_pattern.search(data3_value):
                        last_name = data3_value
                        save_to_notepad(f"Found last name with special characters from data3: '{last_name}'\n")
                        break
            
            if last_name is None:
                assert False, f"No last name with special characters found in data3 results.\n"
            
            click_target = last_name
            save_to_notepad(f"Contact '{contact_with_special_chars}' not found in data2 list. Will click on last name: '{last_name}'\n")

        # Scroll down on HU display 10 times using the specified coordinates
        for i in range(10):
            # Click on the target (either full contact name or last name) with verification from HU display
            found = click_on_device_with_verification(HU, click_target)
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

        assert found == True, f"Target '{click_target}' has not been found on HU display.\n"
        save_to_notepad(f"Target '{click_target}' has been found and pressed on HU display.\n")

        # Check if special characters from the clicked target can be found on HU display with regex
        # Extract special characters from the click target for verification
        special_chars_in_name = special_chars_pattern.findall(click_target)
        if special_chars_in_name:
            # Check each special character individually with regex
            all_chars_found = True
            save_to_notepad(f"Checking individual special characters: {special_chars_in_name}\n")
            
            for char in special_chars_in_name:
                char_found = find_word_on_device_via_regex(HU, char)
                if char_found:
                    save_to_notepad(f"Special character '{char}' found on HU display\n")
                else:
                    save_to_notepad(f"Special character '{char}' NOT found on HU display\n")
                    all_chars_found = False
            
            found = all_chars_found
        else:
            # Fallback to checking for the full click target
            found = find_word_on_device_via_regex(HU, re.escape(click_target))
        if found == True:
            success_message = f"{mobile_name} Contact with special characters is displayed successfully on HU."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            # Save to Excel with test_name, result="Passed" and comment=success_message
            save_to_excel(test_name, "Passed", success_message)
            # Mark test as passed for recording cleanup
            test_passed = True
        else:
            assert False, f"{mobile_name} Contact with special characters is not displayed on HU.\n"

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