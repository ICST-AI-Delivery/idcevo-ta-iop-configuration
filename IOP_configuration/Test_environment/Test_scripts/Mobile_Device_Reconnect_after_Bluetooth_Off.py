from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Mobile_Device_Reconnect_after_Bluetooth_Off"

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

        # Take screenshot and click Bluetooth icon on HU
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
            f"pull /sdcard/screenshot.png {path}"
        ]
        
        for cmd in commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n") 
            assert rc == 0, f"Command {cmd} failed: {rc}\n"
        
        # Find and click Bluetooth icon
        x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Bluetooth.png")
        if x == 0 or y == 0:
            x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Bluetooth_2.png")
        
        cmd = f"shell input tap {x} {y}"
        stdout, stderr, rc = run_adb(cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {cmd} failed: {rc}\n"
        
        if x == 0 and y == 0:
            assert x != 0 and y != 0, f"Bluetooth icon has not been found on HU display.\n"
        else:
            save_to_notepad(f"Bluetooth icon has been found on HU display!\n")
        
        # Clean up the screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)

        found = click_on_device(HU,"Manage devices")
        time.sleep(1)
        assert found == True, f"Manage devices button has not been found on HU display.\n"
        save_to_notepad(f"Manage devices button has been found and pressed on HU display.\n")

        found = click_on_device(HU,"Smartphones")
        time.sleep(1)
        assert found == True, f"Smartphones button has not been found on HU display.\n"
        save_to_notepad(f"Smartphones button has been found and pressed on HU display.\n")

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
        time.sleep(2) 

        phone.disable_bluetooth()
        assert rc == 0, f"Command failed: {rc}\n" 
        time.sleep(5)

        # Enable Bluetooth on Mobile device
        phone.enable_bluetooth()
        assert rc == 0, f"Command failed: {rc}\n" 
        time.sleep(10)

        # Check if Connected word can be found on HU display
        found = find_word_on_device(HU,"Connected")
        if found == True:
            success_message = f"{mobile_name} has been reconnected successfully with HU after Bluetooth Off."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            # Save to Excel with test_name, result="Passed" and comment=success_message
            save_to_excel(test_name, "Passed", success_message)
            # Mark test as passed for recording cleanup
            test_passed = True
        else:
            assert False, f"{mobile_name} has not been reconnected with HU after Bluetooth Off.\n"

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
        rc = phone.run_home_command()
        assert rc == 0, f"Command failed: {rc}\n"
        
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
