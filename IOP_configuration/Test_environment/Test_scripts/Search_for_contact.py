from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time
import re

test_name = "Search_for_contact"

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

        # Click Search Button from HU display with verification
        found = click_on_device_with_verification(HU, "Search")
        time.sleep(1)
        assert found == True, f"Search button has not been found on HU display.\n"
        save_to_notepad(f"Search button has been found and pressed on HU display.\n")

        stdout = phone.get_contacts_name_command()
        assert rc == 0, f"Query contacts command failed: {rc}\n"
        
        # Extract contact names - find one with only letters, digits, and spaces
        lines = stdout.strip().split('\n')
        valid_contacts = []
        
        def has_special_characters(name):
            """Check if name contains special characters (not letters, digits, or spaces)"""
            return not re.match(r'^[a-zA-Z0-9\s]+$', name)
        
        def extract_first_and_last_name(full_name):
            """Extract first and last name from full name"""
            parts = full_name.strip().split()
            if len(parts) >= 2:
                first_name = parts[0]
                last_name = parts[-1]
                return first_name, last_name
            elif len(parts) == 1:
                return parts[0], ""
            return "", ""
        
        # Collect all potential valid contacts first
        for line in lines:
            if "display_name=" in line:
                # Extract full names including spaces, stopping at comma or end of string
                match = re.search(r"display_name=([^,]+)", line)
                if match:
                    potential_name = match.group(1).strip()
                    if potential_name and potential_name != "null":
                        # Extract first and last name
                        first_name, last_name = extract_first_and_last_name(potential_name)
                        
                        # Check if first name or last name contains special characters
                        first_has_special = has_special_characters(first_name) if first_name else False
                        last_has_special = has_special_characters(last_name) if last_name else False
                        
                        save_to_notepad(f"Checking contact: {potential_name} (First: '{first_name}', Last: '{last_name}')\n")
                        save_to_notepad(f"First name has special chars: {first_has_special}, Last name has special chars: {last_has_special}\n")
                        
                        # If either first or last name has special characters, skip this contact
                        if first_has_special or last_has_special:
                            save_to_notepad(f"Skipping contact '{potential_name}' due to special characters in name\n")
                            continue
                        
                        # This contact has valid names (only letters, digits, spaces)
                        valid_contacts.append(potential_name)
                        save_to_notepad(f"Found potentially valid contact: {potential_name}\n")
        
        # If no valid contact found, raise an error
        if not valid_contacts:
            assert False, "No contact found with names containing only letters, digits, and spaces\n"
        
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
        
        stdout = phone.get_contacts_data3_command()
        assert rc == 0, f"Data3 query command failed: {rc}\n"
        
        # Extract all data3 values that aren't null
        data3_dict = {}
        lines = stdout.strip().split('\n')
        for line in lines:
            if line.strip() and 'data3=' in line:
                data3_value = line.split('data3=', 1)[1].strip()
                if data3_value:
                    # Try to associate data3 with contact names
                    for contact in valid_contacts:
                        if data3_value in contact:
                            data3_dict[contact] = data3_value
        
        save_to_notepad(f"Extracted data3 dictionary: {data3_dict}\n")
        
        # Find a valid contact (with either data2 or data3 not NULL)
        contact_name = None
        click_target = None
        
        for potential_contact in valid_contacts:
            # Check if in data2 list
            if potential_contact in data2_list:
                contact_name = potential_contact
                click_target = potential_contact
                save_to_notepad(f"Selected contact '{contact_name}' found in data2 list. Will click on full contact name.\n")
                save_to_notepad(f"Found valid contact: {contact_name}\n")
                break
            # Check if in data3 dictionary
            elif potential_contact in data3_dict:
                contact_name = potential_contact
                click_target = data3_dict[potential_contact]
                save_to_notepad(f"Selected contact '{contact_name}' found in data3. Will click on last name: '{click_target}'\n")
                save_to_notepad(f"Found valid contact: {contact_name}\n")
                break
            else:
                save_to_notepad(f"Skipping contact '{potential_contact}' as it has both data2=NULL and data3=NULL\n")
        
        # If no valid contact found (both data2 and data3 are NULL for all contacts), raise an error
        if contact_name is None:
            assert False, "No valid contact found. All contacts have both data2=NULL and data3=NULL\n"

        # Type each character from click_target dynamically
        save_to_notepad(f"Starting to type contact name: '{click_target}'\n")
        
        for i, char in enumerate(click_target):
            if char == ' ':
                # Handle space character using Space.png icon
                commands = [
                    f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
                    f"pull /sdcard/screenshot.png {path}",
                    f"shell input tap 0 0"  # Will be replaced with actual coordinates
                ]
                
                for j, cmd in enumerate(commands):
                    if j == 2:  # Space tap command
                        x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Space.png")
                        if x == 0 or y == 0:
                            x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Space_2.png")
                        cmd = f"shell input tap {x} {y}"
                    
                    stdout, stderr, rc = run_adb(cmd, HU)
                    if stderr:
                        save_to_notepad(f"[Command failed:] ({cmd}:)")
                        save_to_notepad(f"Error text: {stderr}\n")
                    save_to_notepad(f"[Executed command:] ({cmd}:)")  
                    save_to_notepad(f"Result: {stdout}\n")
                    assert rc == 0, f"Command {cmd} failed: {rc}\n"
                    
                    if j == 2:  # After Space tap
                        assert x != 0 and y != 0, f"Space icon has not been found on HU display.\n"
                        save_to_notepad(f"Space character has been found and pressed on HU display!\n")
                
                # Clean up screenshot
                cleanup_cmd = r"del D:\traget\IDCevo\IOP_configuration\Test_environment\Test_scripts\screenshot.png"
                stdout, stderr, rc = run_cmd(cleanup_cmd)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cleanup_cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cleanup_cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n")
                assert rc == 0, f"Command {cleanup_cmd} failed: {rc}\n"
            else:
                # Handle regular characters (convert to lowercase)
                char_to_click = char.lower()
                found = click_on_device_with_verification(HU, char_to_click)
                time.sleep(1)
                assert found == True, f"Button '{char_to_click}' has not been found on HU display.\n"
                save_to_notepad(f"Button '{char_to_click}' has been found and pressed on HU display.\n")
            
            time.sleep(0.5)  # Small delay between characters

        # Wait a moment for search results to appear
        time.sleep(2)

        # Check if the extracted Contact can be found on HU display
        found = find_word_on_device_via_regex(HU, click_target)
        if found == True:
            success_message = f"{mobile_name} Contact was found successfully on HU using search bar."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            # Save to Excel with test_name, result="Passed" and comment=success_message
            save_to_excel(test_name, "Passed", success_message)
            # Mark test as passed for recording cleanup
            test_passed = True
        else:
            assert False, f"{mobile_name} Contact was not found on HU using search bar.\n"

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
        command = f"move {test_name}.png D:/traget/IDCevo/IOP_configuration/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        save_to_notepad(f"HU device screenshot saved successfully.\n")

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