"""
AI-Generated Test Script for: Time_stamps
Generated on: 2026-03-03 12:07:30

Test Case Information:
- Precondition: Mobile Device and HU are connected.
Synchronisation is finished.
Some calls are listed in call list.
- Description: 1 CheIDCEvo if timestamps on Mobile Device and HU for call history are the same.
- Expected Result: 1 Timestamps are correct.
"""

from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Time_stamps"

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
        time.sleep(1)
        
        # Create Mobile device object
        phone = create_device(Mobile1, mobile_name)
        
        # Click Mobile device name button with regex from HU display
        found = click_on_device_regex(HU, mobile_name)
        time.sleep(1)
        assert found == True, f"Mobile device name {mobile_name} has not been found on HU display.\n"
        save_to_notepad(f"Mobile device name {mobile_name} has been found and pressed on HU display.\n")

        # Click Calls Button from HU display
        found = click_on_device(HU, "Calls")
        time.sleep(1)
        assert found == True, f"Calls button has not been found on HU display.\n"
        save_to_notepad(f"Calls button has been found and pressed on HU display.\n")

        # Get call history with timestamps from mobile device
        result = phone.get_call_history_with_timestamps()
        assert result is not None, f"Failed to get call history with timestamps from mobile device.\n"
        save_to_notepad(f"Retrieved call history with timestamps from mobile device.\n")
        
        # Extract call timestamps from mobile device
        mobile_timestamps = result  # Assuming the function returns timestamps directly
        save_to_notepad(f"Extracted timestamps from mobile device: {mobile_timestamps}\n")
        
        # Extract only the first part of timestamps (e.g., "Mar 11" from "Mar 11, 09:52")
        # Split by comma and take the first part, then strip any whitespace
        mobile_timestamps_short = mobile_timestamps.split(',')[1].strip() if ',' in mobile_timestamps else mobile_timestamps.strip()
        save_to_notepad(f"Using shortened timestamp for verification: {mobile_timestamps_short}\n")

        # Scroll down on HU display 10 times using the specified coordinates
        for i in range(10):        
            found = find_word_on_device_via_regex(HU, mobile_timestamps_short)
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
        
        # Check if timestamps match between Mobile device and HU
        if found:
            success_message = f"Call history timestamps are synchronized correctly between {mobile_name} and HU. Timestamps match successfully."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            # Save to Excel with test_name, result="Passed" and comment=success_message
            save_to_excel(test_name, "Passed", success_message)
            # Mark test as passed for recording cleanup
            test_passed = True
        else:
            assert False, f"Call history timestamps are not synchronized properly between {mobile_name} and HU.\n"

        # Take screenshot on HU screen and save it
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

        # Move the screenshot to the specified path
        screenshots_dir = f"{base_dir}/Test_results/Screenshots".replace('/', '\\')
        command = f'move {test_name}.png "{screenshots_dir}"'
        stdout, stderr, rc = run_cmd(command)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"

        # Run adb command on HU to go to home screen
        home_command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(home_command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({home_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({home_command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Home command {home_command} failed: {rc}\n"
        time.sleep(1)

        # Click Mobile device name button with regex from HU display
        found = click_on_device_regex(HU, mobile_name)
        time.sleep(1)
        assert found == True, f"Mobile device name {mobile_name} has not been found on HU display.\n"
        save_to_notepad(f"Mobile device name {mobile_name} has been found and pressed on HU display.\n")

        # Run swipe command on HU display
        swipe_command = f"shell input swipe 1700 700 200 2500"
        stdout, stderr, rc = run_adb(swipe_command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({swipe_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({swipe_command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {swipe_command} failed: {rc}\n"
        time.sleep(1)

        # Run cleanup commands after test is done to return to home menu
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

        # Stop screen recording on HU after test is done
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
        
        # Clean up recordings based on test result - keep if failed, delete if passed
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
            # Run adb command on HU to go to home screen
            home_command = f"shell input keyevent 3"
            stdout, stderr, rc = run_adb(home_command, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({home_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({home_command}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            time.sleep(1)

            # Click Mobile device name button with regex from HU display
            found = click_on_device_regex(HU, mobile_name)
            time.sleep(1)

            # Run swipe command on HU display
            swipe_command = f"shell input swipe 1700 700 200 2500"
            stdout, stderr, rc = run_adb(swipe_command, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({swipe_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({swipe_command}:)")  
            save_to_notepad(f"Result: {stdout}\n")
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