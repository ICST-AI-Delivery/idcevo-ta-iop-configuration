from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Reconnect_as_inactive_audio_source"

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
        save_to_notepad(f"Mobile device bluetooth name: {mobile_name}\n")
        
        # Create Mobile device object
        phone = create_device(Mobile1, mobile_name)
        save_to_notepad(f"Created mobile device object\n")
        
        # Play audio on Mobile Device 1
        phone.play_audio_command()
        save_to_notepad(f"Started audio playback on Mobile Device 1\n")
        time.sleep(3)
        
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
        
        # Click Source button with regex from HU display
        found = click_on_device_regex(HU, "Source")
        time.sleep(1)
        assert found == True, f"Source button has not been found on HU display.\n"
        save_to_notepad(f"Source button has been found and pressed on HU display.\n")

        # Click Bluetooth name on HU from Media menu
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Bluetooth")
        assert x != 0 and y != 0, f"Bluetooth name not found on HU display\n"

        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked on Bluetooth name\n")
        time.sleep(1)

        # Click Bluetooth button with regex from HU display
        found = click_on_device_regex(HU, "Bluetooth")
        time.sleep(1)
        assert found == True, f"Bluetooth button has not been found on HU display.\n"
        save_to_notepad(f"Bluetooth button has been found and pressed on HU display.\n")

        # Click Radio Button to switch from audio playback to Radio
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
        assert x != 0 and y != 0, f"Radio not found on HU display\n"

        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked on Radio\n")
        time.sleep(1)
        
        # Click Bluetooth icon from HU display
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
            f"pull /sdcard/screenshot.png {path}",
            f"shell input tap 0 0"  # Will be replaced with actual coordinates
        ]
        
        for i, cmd in enumerate(commands):
            if i == 2:  # Icon tap command
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
            
            if i == 2:  # After icon tap
                assert x != 0 and y != 0, f"Bluetooth icon has not been found on display.\n"
                save_to_notepad(f"Bluetooth icon has been found and pressed!\n")
        
        # Clean up screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)
        time.sleep(2)
        
        # Click Manage Devices Button
        found = click_on_device(HU, "Manage devices")
        assert found, f"Manage devices button not found on HU display\n"
        save_to_notepad(f"Clicked Manage devices button\n")
        time.sleep(2)
        
        # Click Smartphones Button
        found = click_on_device(HU, "Smartphones")
        assert found, f"Smartphones button not found on HU display\n"
        save_to_notepad(f"Clicked Smartphones button\n")
        time.sleep(2)
        
        # Enable airplane mode to simulate putting Mobile Device in shielding bag
        phone.enable_airplane_mode_command()
        save_to_notepad(f"Enabled airplane mode on Mobile Device to simulate shielding bag\n")
        time.sleep(5)  # Wait 5 seconds with airplane mode enabled
        
        # Disable airplane mode
        phone.disable_airplane_mode_command()
        save_to_notepad(f"Disabled airplane mode on Mobile Device\n")
        time.sleep(2)
        
        # Run linkloss command to simulate getting Mobile Device out of shielding bag
        phone.run_linkloss_command()
        save_to_notepad(f"Ran linkloss command to simulate removing from shielding bag\n")
        time.sleep(15)  # Wait 15 seconds for bluetooth connection to be re-established
        
        # Check if "Connected" word can be found on HU display
        found = find_word_on_device(HU, "Connected")
        
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
        
        # Pause audio on Mobile Device
        phone.pause_audio_command()
        save_to_notepad(f"Paused audio on Mobile Device\n")
        time.sleep(1)
        
        # Check test result
        if found == True:
            success_message = f"Bluetooth connection is re-established, Radio is playing and audio playback is inactive source - test Passed."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Bluetooth connection was not re-established after removing from shielding - test Failed"

        # Return to home menu - HU commands
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        time.sleep(1)
        
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
        save_to_notepad(f"Returned Mobile device to home menu\n")
        
        # Stop screen recording and cleanup
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
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
        
        try:
            # Return to home menu on failure - HU commands
            command = f"shell input keyevent 3"
            stdout, stderr, rc = run_adb(command, HU)
            
            command = f"shell rm /sdcard/*.png"
            stdout, stderr, rc = run_adb(command, HU)

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