from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Cover_Art"

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
        save_to_notepad(f"Created Mobile device object with name: {mobile_name}\n")
        
        # Start audio playback on Mobile Device 1 from an album with cover art
        phone.play_audio_command()
        save_to_notepad(f"Started audio playback on Mobile Device 1 from album with cover art\n")
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
        
        # Click Source button with regex on HU display
        found = click_on_device_regex(HU, "Source")
        time.sleep(2)
        
        # Click Bluetooth name on HU from Media menu with regex and coordinates
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Bluetooth")
        assert x != 0 and y != 0, f"Bluetooth option not found in Media menu\n"
        
        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked Bluetooth option in Media menu\n")
        time.sleep(3)

        # Skip audio playback forward on HU
        command = f"shell input tap 1520 1030"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Skipped audio playback forward on HU\n")
        time.sleep(3)
        
        # Skip audio playback backwards on HU
        command = f"shell input tap 1120 1030"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        skip_rc = rc
        save_to_notepad(f"Skipped audio playback backwards on HU\n")
        time.sleep(3)
                
        # Check if cover art is displayed on HU screen
        cover_art = phone.cover_art_command()
        save_to_notepad(f"Checking for cover art on HU screen\n")
        time.sleep(2)
        
        # Check if cover art is displayed correctly
        if "avrcpcontroller.BipImageDescriptor: COVERART parsed encoding JPEG" in cover_art:
            save_to_notepad(f"Corver art transferred successfully: {cover_art}\n")
            cover_art_valid = True 
        else:
            save_to_notepad(f"Corver art transfer failed: {cover_art}\n")
            cover_art_valid = False 
        
        if cover_art_valid:
            success_message = f"Audio playback is initiated on HU and HU displays cover art - test Passed."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Cover art display functionality failed - test Failed\n"
            
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
        time.sleep(2)
        
        # Click Bluetooth button with regex on HU display
        found = click_on_device_regex(HU, "Bluetooth")
        assert found, f"Bluetooth button not found on HU display\n"
        save_to_notepad(f"Clicked Bluetooth button on HU display\n")
        time.sleep(2)
        
        # Click Radio button on HU from Media menu to switch from mobile playback to radio
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
        assert x != 0 and y != 0, f"Radio option not found in Media menu\n"
        
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
        assert rc == 0, f"Mobile home command failed: {rc}\n"
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

        # Pause audio on Mobile Device
        phone.pause_audio_command()
        save_to_notepad(f"Paused audio on Mobile Device\n")
        time.sleep(2)
        
        # Click Bluetooth button with regex on HU display
        found = click_on_device_regex(HU, "Bluetooth")
        assert found, f"Bluetooth button not found on HU display\n"
        save_to_notepad(f"Clicked Bluetooth button on HU display\n")
        time.sleep(2)
        
        # Click Radio button on HU from Media menu to switch from mobile playback to radio
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
        assert x != 0 and y != 0, f"Radio option not found in Media menu\n"
        
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