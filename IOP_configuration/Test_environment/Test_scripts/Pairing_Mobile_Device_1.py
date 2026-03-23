from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Pairing_Mobile_Device_1"

def main():
    save_to_notepad(f"=== Test {test_name} started ===\n")
    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"
    
    # Initialize test result tracking
    test_passed = False

    try:
        # Check on which port is USB Matrix connected
        status = USB_Matrix_Status()
        save_to_notepad(f"USB Matrix is connected to port: {status}")
        time.sleep(3)
        # Extracting serial numbers for HU and Mobile1
        HU, Mobile1 = get_serial_number()
        
        # Create recordings folder
        create_recordings_folder()
        save_to_notepad(f"Created recordings folder\n")
        
        # Start screen recordings before any test actions
        save_to_notepad(f"Starting screen recordings...\n")
        hu_recording_started = start_screen_recording(f"-s {HU}", test_name, "HU")
        mobile_recording_started = start_screen_recording(f"-s {Mobile1}", test_name, "Mobile1")
        
        if hu_recording_started:
            save_to_notepad(f"HU screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start HU screen recording\n")
            
        if mobile_recording_started:
            save_to_notepad(f"Mobile1 screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start Mobile1 screen recording\n")
        
        # Wait a moment for recordings to initialize
        time.sleep(2)

        command = f"shell settings get secure bluetooth_name" # Mobile1 command go get device name
        stdout, stderr, rc = run_adb(command, Mobile1)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {Mobile1} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] (adb -s {Mobile1} {command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command adb -s {Mobile1} {command} failed: {rc}\n"

        mobile_name = stdout 
        save_to_notepad(f"Tested device name: {mobile_name}\n")
        time.sleep(1)

        phone = create_device(Mobile1,mobile_name)

        phone.click_close_button_popup()
        time.sleep(2)

        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Command failed: {rc}\n"  

        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone.run_settings_menu_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone.run_bluetooth_menu_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        # Click Bluetooth Icon commands
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png", # HU command to take screenshot
            f"pull /sdcard/screenshot.png {path}", # HU command to save screenshot on PC
            f"shell input tap 0 0" # HU command go to Bluetooth
        ]

        for cmd in commands:
            x = 0
            y = 0
            if cmd == commands[2]:
                x,y = find_icon_in_screenshot(f"{path}/screenshot.png",f"{path}/helpers/Bluetooth.png")
                if x == 0 or y == 0:
                    x,y = find_icon_in_screenshot(f"{path}/screenshot.png",f"{path}/helpers/Bluetooth_2.png")
                cmd = f"shell input tap {x} {y}"

            stdout, stderr, rc = run_adb(cmd, HU)

            # Console display 
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n") 

            assert rc == 0, f"Command {cmd} failed: {rc}\n"
            if cmd == commands[2]:
                if x==0 & y==0:
                    assert x!=0 & y!=0, f"Bluetooth icon has not been found on HU display.\n"
                else:
                    save_to_notepad(f"Bluetooth icon has been found on HU display!\n")

        # delete the screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        command = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(command)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"

        found = click_on_device(HU,"Manage devices")
        time.sleep(1)
        assert found == True, f"Manage devices button has not been found on HU display.\n"
        save_to_notepad(f"Manage devices button has been found and pressed on HU display.\n")

        found = click_on_device(HU,"Not now")
        time.sleep(1)
        assert found == True, f"Not Now button has not been found on HU display.\n"
        save_to_notepad(f"Not now button has been found and pressed on HU display.\n")

        found = click_on_device(HU,"Smartphones")
        time.sleep(1)
        assert found == True, f"Smartphones button has not been found on HU display.\n"
        save_to_notepad(f"Smartphones button has been found and pressed on HU display.\n")

        phone.click_close_button_popup()
        time.sleep(2)

        phone.enable_bluetooth()
        assert rc == 0, f"Command failed: {rc}\n" 

        phone.click_close_button_popup()
        time.sleep(2)

        found = click_on_device(HU,"Cancel")
        time.sleep(3)

        # Run the command to get Bluetooth Name for HU
        bluetooth_name_cmd = f'shell dumpsys bluetooth_manager | findstr -i "Name:"'
        stdout, stderr, rc = run_adb(bluetooth_name_cmd,HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({bluetooth_name_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({bluetooth_name_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {bluetooth_name_cmd} failed: {rc}\n"
        
        # Extract the first line from the command output
        first_line = stdout.strip().split('\n')[0] if stdout.strip() else ""
        save_to_notepad(f"First line extracted: {first_line}\n")
        
        # Extract Bluetooth device name from the first line (after "Name: " or "name: ")
        bluetooth_device_name = ""
        if first_line:
            # Handle both "Name:" and "name:" cases (case insensitive)
            if "name:" in first_line.lower():
                # Split by ":" and get the part after it, then strip whitespace
                name_parts = first_line.split(":", 1)
                if len(name_parts) > 1:
                    bluetooth_device_name = name_parts[1].strip()
        
        save_to_notepad(f"Extracted Bluetooth device name: {bluetooth_device_name}\n")        
        
        found = phone.click_HU_bluetooth_name_button(bluetooth_device_name)
        time.sleep(3)
        assert found == True, f"HU {bluetooth_device_name} has not been found on Mobile Bluetooth devices list.\n"
        save_to_notepad(f"HU {bluetooth_device_name} has been found and pressed on Mobile Bluetooth devices list.\n")
        
        # Click Connect Button from HU display
        found = click_on_device(HU, "Connect")
        time.sleep(1)
        assert found == True, f"Connect button has not been found on HU display.\n"
        save_to_notepad(f"Connect button has been found and pressed on HU display.\n")

        # Click Pair button from Mobile device display
        found = phone.click_pair_with_HU_button()
        time.sleep(10)
        assert found == True, f"Pair button has not been found on Mobile display.\n"
        save_to_notepad(f"Pair button has been found and pressed on Mobile display.\n")

        phone.click_allow_button_popup()

        found = click_on_device(HU, "Not now")
        time.sleep(1)

        found = click_on_device(HU, "Not now")
        time.sleep(1)

        found = click_on_device(HU,"Smartphones")
        time.sleep(1)
        assert found == True, f"Smartphones button has not been found on HU display.\n"
        save_to_notepad(f"Smartphones button has been found and pressed on HU display.\n")

        found = click_on_device(HU, "Not now")
        time.sleep(1)

        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/{test_name}.png", # HU command to take screenshot
            f"pull /sdcard/{test_name}.png" # HU command to save screenshot on PC
        ]

        for cmd in commands:
            found = False
            if cmd == commands[0]:
                found = find_word_on_device(HU,mobile_name)

            stdout, stderr, rc = run_adb(cmd, HU)

            # Console display 
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n") 

            assert rc == 0, f"Command {cmd} failed: {rc}\n"
            if cmd == commands[0]:
                if found == False:
                    assert found == True, f"{mobile_name} has not been found on HU Bluetooth devices list.\n"
                else:
                    success_message = f"HU has been paired successfully with {mobile_name}."
                    save_to_notepad(f"{success_message}\n")
                    save_to_notepad(header="TEST PASSED", color="green")
                    # Save to Excel with test_name, result="Passed" and comment=success_message
                    save_to_excel(test_name, "Passed", success_message)
                    # Mark test as passed for recording cleanup
                    test_passed = True

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

        # Mobile home
        rc = phone.run_home_command()
        assert rc == 0, f"Command failed: {rc}\n"
        
        save_to_notepad(f"Cleanup commands executed successfully.\n")

        # Stop screen recordings
        save_to_notepad(f"Stopping screen recordings...\n")
        stop_screen_recording("HU")
        stop_screen_recording("Mobile1")
        
        # Clean up recordings based on test result
        cleanup_recordings(test_passed, test_name)
        if test_passed:
            save_to_notepad(f"Test passed - recordings deleted\n")
        else:
            save_to_notepad(f"Test completed - recordings kept for review\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")
    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")

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

        # Mobile home
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command,Mobile1)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
                    
        # Stop screen recordings on test failure
        save_to_notepad(f"Stopping screen recordings...\n")
        stop_screen_recording("HU")
        stop_screen_recording("Mobile1")
        
        # Keep recordings since test failed (test_passed is False)
        cleanup_recordings(test_passed, test_name)
        save_to_notepad(f"Test failed - recordings kept for debugging\n")
        
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