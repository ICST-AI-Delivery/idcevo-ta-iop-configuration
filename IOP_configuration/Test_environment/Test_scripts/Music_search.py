from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time
import re

test_name = "Music_search"

def main():
    save_to_notepad(f"=== Test {test_name} started ===\n")
    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"
    
    # Initialize test result tracking
    test_passed = False

    try:
        # Check USB Matrix status
        status = USB_Matrix_Status()
        save_to_notepad(f"USB Matrix is connected to port: {status}\n")
        time.sleep(3)
        
        # Get serial numbers for HU and Mobile1
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
        
        # Create Mobile device object
        phone = create_device(Mobile1, mobile_name)
        save_to_notepad(f"Created mobile device object for {mobile_name}\n")
        
        # Open Media menu on HU
        command = f"shell input tap 1225 1325"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Opened Media menu on HU\n")
        time.sleep(2)
        
        # Click Source button with regex on HU display
        found = click_on_device_regex(HU, "Source")
        time.sleep(1)
        
        # Click Search Button from HU display
        found = click_on_device_regex(HU, "Search")
        assert found == True, f"Search button not found on HU display\n"
        save_to_notepad(f"Clicked Search button on HU\n")
        time.sleep(1)
        
        # Extract the radio names from HU
        command = f"shell dumpsys broadcastradio | findstr -i metadata"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Extracted Radio names from HU.\n")
        
        # Extract the first radio name from the output
        radio_name = ""
        match = re.search(r'\.RDS_PS=([^,\]]+)', stdout)
        if match:
            radio_name = match.group(1).strip()
            save_to_notepad(f"Extracted radio name: {radio_name}\n")
        else:
            save_to_notepad(f"No radio name found in metadata output\n")       
        time.sleep(2)
        
        # Type each character from radio_name dynamically
        if radio_name:
            save_to_notepad(f"Starting to type radio name: '{radio_name}'\n")
            
            for i, char in enumerate(radio_name):
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
                        
                        stdout_temp, stderr, rc = run_adb(cmd, HU)
                        if stderr:
                            save_to_notepad(f"[Command failed:] ({cmd}:)")
                            save_to_notepad(f"Error text: {stderr}\n")
                        save_to_notepad(f"[Executed command:] ({cmd}:)")  
                        save_to_notepad(f"Result: {stdout_temp}\n")
                        assert rc == 0, f"Command {cmd} failed: {rc}\n"
                        
                        if j == 2:  # After Space tap
                            assert x != 0 and y != 0, f"Space icon has not been found on HU display.\n"
                            save_to_notepad(f"Space character has been found and pressed on HU display!\n")
                    
                    # Clean up screenshot
                    screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
                    cleanup_cmd = f'del "{screenshot_path}"'
                    stdout_temp, stderr, rc = run_cmd(cleanup_cmd)
                    if stderr:
                        save_to_notepad(f"[Command failed:] ({cleanup_cmd}:)")
                        save_to_notepad(f"Error text: {stderr}\n")
                    save_to_notepad(f"[Executed command:] ({cleanup_cmd}:)")  
                    save_to_notepad(f"Result: {stdout_temp}\n")
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
            
        # Check if the radio name can be found on HU display
        found = find_word_on_device_via_regex(HU, radio_name)
        if found == True:
            # Check test result
            success_message = f"Music search functionality works correctly - test Passed."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Music search functionality doesn't work correctly - test Failed.\n"
        
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

        screenshots_dir = f"{base_dir}/Test_results/Screenshots".replace('/', '\\')
        command = f'move {test_name}.png "{screenshots_dir}"'
        stdout, stderr, rc = run_cmd(command)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Device screenshot saved successfully.\n")
        
        # Return to home menu - HU commands
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        command = f"shell rm /sdcard/*.png"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        # Return to home menu - Mobile device commands
        rc = phone.run_home_command()
        assert rc == 0, f"Failed to return mobile device to home\n"
        save_to_notepad(f"Returned to home menu on both devices\n")
        
        # Stop screen recording
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
        
        # Clean up recordings based on test result
        cleanup_recordings(test_passed, test_name)
        if test_passed:
            save_to_notepad(f"Test passed - recording deleted\n")
        else:
            save_to_notepad(f"Test failed - recording kept for debugging\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")

    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
        save_to_excel(test_name, "Failed", error_message)
        
        # Cleanup commands on test failure
        try:
            # Return to home menu - HU commands
            command = f"shell input keyevent 3"
            stdout, stderr, rc = run_adb(command, HU)
            
            command = f"shell rm /sdcard/*.png"
            stdout, stderr, rc = run_adb(command, HU)
            
            # Return to home menu - Mobile device commands
            rc = phone.run_home_command()
            
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