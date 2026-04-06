from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Internal_memory"

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
        save_to_notepad(f"Created Mobile device object\n")
        time.sleep(2)
        
        result = phone.check_music_from_internal_memory_command()
        if result is None:
            raise AssertionError("check_music_from_internal_memory_command() returned None - unable to retrieve music data")
        
        # Check if result is empty (no music stored on internal memory)
        if not result or (isinstance(result, str) and result.strip() == "") or (isinstance(result, list) and len(result) == 0):
            skip_message = "No music found on internal memory - skipping test"
            save_to_notepad(f"{skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", skip_message)
            
            # Stop and delete recordings since test is skipped
            save_to_notepad(f"Stopping screen recording...\n")
            stop_screen_recording("HU")
            cleanup_recordings(True, test_name)  # Pass True to delete recordings
            save_to_notepad(f"Test skipped - recording deleted\n")
            
            save_to_notepad(f"=== Test {test_name} finished (skipped) ===\n")
            return
        
        # Save only the first line if result is not empty
        if isinstance(result, str):
            first_line = result.split('\n')[0].strip()
        elif isinstance(result, list):
            first_line = str(result[0]).strip() if len(result) > 0 else ""
        else:
            first_line = str(result).strip()
        
        save_to_notepad(f"First music entry found: {first_line}\n")
                
        # Play music from internal memory of Mobile Device
        rc = phone.play_music_from_internal_memory_command(first_line)
        save_to_notepad(f"Started playing music from internal memory\n")
        time.sleep(5)

        # Check test result
        if rc == 0:
            success_message = f"Music from internal memory is transmitted to HU successfully - test Passed."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert rc == 0, f"Music transmission from internal memory failed - test Failed"

        # Run the tap commands on HU to open the Media Menu
        tap_cmd = f"shell input tap 1225 1325"  # Media Menu coordinates
        stdout, stderr, rc = run_adb(tap_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({tap_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({tap_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {tap_cmd} failed: {rc}\n"

        # Click Source button with regex on HU display
        found = click_on_device_regex(HU, "Source")
        time.sleep(2)

        # Click Bluetooth Audio on HU from Media menu
        x, y = find_word_on_device_via_regex_with_coordinates(HU,"Bluetooth")        
        cmd = f"shell input tap {x} {y-100}"
        run_adb(cmd, HU)
        time.sleep(3)

        # Take a screenshot of HU screen and save it
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
        save_to_notepad(f"Audio paused on Mobile device\n")
        time.sleep(2)

        # Click Bluetooth button with regex on HU display
        found = click_on_device_regex(HU, "Bluetooth")
        assert found == True, f"Bluetooth button not found on HU display\n"
        save_to_notepad(f"Clicked Bluetooth button on HU\n")
        time.sleep(2)
        
        # Click Radio button on HU from Media menu
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
        assert x != 0 and y != 0, f"Radio option not found on HU display\n"
        
        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Switched from mobile playback to radio\n")
        time.sleep(2)
        
        # Return to home menu - HU commands
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        time.sleep(1)
        
        command = f"shell rm /sdcard/*.png"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        time.sleep(1)
        
        # Return to home menu - Mobile device commands
        rc = phone.run_home_command()
        save_to_notepad(f"Mobile device returned to home\n")
        time.sleep(1)
        
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
        
        # Pause audio on Mobile Device
        phone.pause_audio_command()
        save_to_notepad(f"Audio paused on Mobile device\n")
        time.sleep(2)

        # Click Bluetooth button with regex on HU display
        found = click_on_device_regex(HU, "Bluetooth")
        assert found == True, f"Bluetooth button not found on HU display\n"
        save_to_notepad(f"Clicked Bluetooth button on HU\n")
        time.sleep(2)
        
        # Click Radio button on HU from Media menu
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
        assert x != 0 and y != 0, f"Radio option not found on HU display\n"
        
        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Switched from mobile playback to radio\n")
        time.sleep(2)
        
        try:
            # Return to home menu on failure - HU commands
            command = f"shell input keyevent 3"
            stdout, stderr, rc = run_adb(command, HU)
            
            command = f"shell rm /sdcard/*.png"
            stdout, stderr, rc = run_adb(command, HU)
            
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