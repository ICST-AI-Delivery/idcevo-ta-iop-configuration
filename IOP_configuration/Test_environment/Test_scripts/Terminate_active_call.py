"""
AI-Generated Test Script for: Terminate_active_call
Generated on: 2026-03-04 16:32:38

Test Case Information:
- Precondition: Mobile Device and HU are connected.
Synchronisation is finished.
- Description: 1 Initiate an outgoing call from Mobile Device 1 to Mobile Device 3.
2 Accept call on Mobile Device 3.
3 Terminate call on HU.
- Expected Result: 3 Call is terminated on Mobile Device and HU.
"""

from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Terminate_active_call"

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
        
        # Get serial numbers for HU and Mobile1
        HU, Mobile1 = get_serial_number()
        
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
        save_to_notepad(f"Mobile1 device name: {mobile_name}\n")
        time.sleep(1)

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

        # Create Mobile device object
        phone = create_device(Mobile1, mobile_name)
        
        # Check SIM state on Mobile1
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            skip_message = "Mobile device doesn't have SIM card on it"
            save_to_notepad(f"{skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", skip_message)
            return
        
        save_to_notepad(f"Mobile1 SIM state: {sim_state}\n")
        
        # Extract mobile1 phone number
        phone_number_mobile1 = phone.get_phone_number_command()
        save_to_notepad(f"Mobile1 phone number: {phone_number_mobile1}\n")
        
        # Check USB Matrix status and switch if needed
        status = USB_Matrix_Status()
        if status == 1:
            select_mobile_device(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")       
        time.sleep(3)
        
        # Get serial numbers for HU and Mobile3
        HU, Mobile3 = get_serial_number()
        
        # Get Mobile3 device bluetooth name
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, Mobile3)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile3_name = stdout.strip()
        save_to_notepad(f"Mobile3 device name: {mobile3_name}\n")
        time.sleep(1)
        
        # Create Mobile device3 object
        phone3 = create_device(Mobile3, mobile3_name)
        
        # Check SIM state on Mobile3
        sim_state = phone3.check_SIM_command()
        if "LOADED" not in sim_state:
            skip_message = "Mobile device3 doesn't have SIM card on it"
            save_to_notepad(f"{skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", skip_message)
            return
        
        save_to_notepad(f"Mobile3 SIM state: {sim_state}\n")
        
        # Extract mobile3 phone number
        phone_number_mobile3 = phone3.get_phone_number_command()
        save_to_notepad(f"Mobile3 phone number: {phone_number_mobile3}\n")

        # Switch USB Matrix back to the port from the beginning
        select_mobile_device(1, status)
        time.sleep(3)
        save_to_notepad(f"Switched USB Matrix back to original port\n")

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
        
        # Turn Mobile screen on
        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Turn screen on command failed: {rc}\n"
        save_to_notepad(f"Mobile1 screen turned on\n")
        
        # Unlock Mobile screen
        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Unlock screen command failed: {rc}\n"
        save_to_notepad(f"Mobile1 screen unlocked\n")
        
        # Initiate outgoing call from Mobile Device 1 to Mobile Device 3
        rc = phone.dial_command(phone_number_mobile3)
        assert rc == 0, f"Dial command failed: {rc}\n"
        save_to_notepad(f"Initiated outgoing call from Mobile1 to Mobile3 ({phone_number_mobile3})\n")        
        time.sleep(5)  # Wait for call to start setting up
        
        # Check USB Matrix status and switch if needed
        status = USB_Matrix_Status()
        if status == 1:
            select_mobile_device(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")       
        time.sleep(3)
        
        # Accept call on Mobile Device 3
        rc = phone3.answer_call_command()
        assert rc == 0, f"Answer call command failed: {rc}\n"
        save_to_notepad(f"Call accepted on Mobile3\n")
        time.sleep(3)  # Wait for call to become active
        
        # Switch USB Matrix back to the port from the beginning
        select_mobile_device(1, status)
        save_to_notepad(f"Switched USB Matrix back to original port\n")
        time.sleep(3)
        
        # Try to click End Call Button first
        found = click_on_device_regex(HU, "End")
        if found:
            save_to_notepad(f"End call button has been found and pressed on HU display.\n")
        else:
            # If End Call button not found, try to click Red Phone icon
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
            
            # Find and click Red Phone icon
            x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/End_Call.png")
            
            if x != 0 and y != 0:
                cmd = f"shell input tap {x} {y}"
                stdout, stderr, rc = run_adb(cmd, HU)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n") 
                assert rc == 0, f"Command {cmd} failed: {rc}\n"
                save_to_notepad(f"Red Phone icon has been found and pressed on HU display.\n")
            else:
                assert False, f"Neither End call button nor Red Phone icon has been found on HU display.\n"
            
            # Clean up the screenshot
            cmd = r"del D:\traget\IDCevo\IOP_configuration\Test_environment\Test_scripts\screenshot.png"
            stdout, stderr, rc = run_cmd(cmd)
        time.sleep(3)  # Wait for call to be terminated
        
        # Check if "Contacts" word can be found on HU display
        found = find_word_on_device_via_regex(HU, "Contacts")
        if found:
            success_message = f"Call was terminated successfully on {mobile_name} and HU"
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Call termination failed - Contacts not found on HU display.\n"
        
        # Take screenshot on HU screen
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
        command = f"move {test_name}.png D:/traget/IDCevo/IOP_configuration/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        save_to_notepad(f"HU device screenshot saved successfully.\n")
        
        # Run cleanup commands after test is done
        # HU commands
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
        
        # Mobile device commands
        rc = phone.run_home_command()
        assert rc == 0, f"Mobile home command failed: {rc}\n"
        
        save_to_notepad(f"Cleanup commands executed successfully.\n")

        # Stop screen recording on HU
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
            # End call if still active
            try:
                phone.end_call_command()
                save_to_notepad(f"Emergency call end executed on Mobile1\n")
            except:
                pass
            
            # HU cleanup commands
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

            # Mobile device home
            rc = phone.run_home_command()
            assert rc == 0, f"Mobile home command failed: {rc}\n"
            
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