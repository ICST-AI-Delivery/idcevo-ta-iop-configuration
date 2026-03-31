from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Resume_during_after_call"

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

        # Check SIM card status
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device doesn't have SIM card - test skipped\n")
            save_to_excel(test_name, "Skipped", "Mobile device doesn't have SIM card")
            return
        
        # Get mobile1 phone number for incoming call
        phone_number_mobile1 = phone.get_phone_number_command()
        save_to_notepad(f"Mobile1 phone number: {phone_number_mobile1}\n")
        time.sleep(2)
        
        # Start playing music on Mobile Device
        phone.play_audio_command()
        save_to_notepad(f"Started playing music on Mobile Device\n")
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
        time.sleep(2)
        
        # Click Source button
        found = click_on_device_regex(HU, "Source")
        time.sleep(2)
        
        # Click Bluetooth name on HU from Media menu
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Bluetooth")
        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        assert x != 0 and y != 0, f"Bluetooth option not found on display\n"
        time.sleep(2)
        
        # Check USB Matrix status and switch if needed
        current_status = USB_Matrix_Status()
        if current_status == 1:
            select_mobile_device(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")       
        time.sleep(3)
        
        # Get serial numbers for HU and Mobile3
        HU, Mobile3 = get_serial_number()
        
        # Get Mobile device3 bluetooth name
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, Mobile3)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        mobile_name3 = stdout.strip()
        
        # Create Mobile device3 object
        phone3 = create_device(Mobile3, mobile_name3)
        
        # Check SIM card status
        sim_state = phone3.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device doesn't have SIM card - test skipped\n")
            save_to_excel(test_name, "Skipped", "Mobile device doesn't have SIM card")
            return
        
        # Extract mobile3 phone number
        phone_number_mobile3 = phone3.get_phone_number_command()
        save_to_notepad(f"Mobile3 phone number: {phone_number_mobile3}\n")
        
        # Turn Mobile3 screen on
        rc = phone3.run_turn_screen_on_command()
        save_to_notepad(f"Mobile3 screen turned on\n")
        time.sleep(1)
        
        # Unlock Mobile3 screen
        rc = phone3.run_unlock_screen_command()
        save_to_notepad(f"Mobile3 screen unlocked\n")
        time.sleep(1)
        
        # Initiate incoming call from Mobile3 to Mobile1
        rc = phone3.dial_command(phone_number_mobile1)
        save_to_notepad(f"Initiated call from Mobile3 to Mobile1\n")
        time.sleep(5)  # Wait for incoming call to be established
        
        # Switch USB Matrix back to original port
        select_mobile_device(1, status)
        save_to_notepad(f"Switched USB Matrix back to original port {status}\n")
        time.sleep(3)
        
        # Accept call on Mobile Device 1
        rc = phone.answer_call_command()
        save_to_notepad(f"Accepted call on Mobile Device 1\n")
        time.sleep(3)
        
        # End call on Mobile Device1
        phone.end_call_command()
        save_to_notepad(f"Ended call on Mobile Device1\n")
        time.sleep(2)

        # Open Media menu on HU
        command = f"shell input tap 1225 1325"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        time.sleep(2)
        
        # Check if audio playback resumes after call ends
        found = find_word_on_device_via_regex(HU, "Bluetooth")
        # Check test result
        if found:
            success_message = f"Audio playback resume functionality works correctly - test Passed."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Audio resume functionality failed - test Failed\n"
        
        # Take screenshot of HU screen
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
        save_to_notepad(f"Audio paused on Mobile Device\n")
        time.sleep(1)
        
        # Click Bluetooth button
        found = click_on_device_regex(HU, "Bluetooth")
        if found:
            save_to_notepad(f"Bluetooth button clicked\n")
        time.sleep(2)
        
        # Click Radio button to switch from mobile playback to radio
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        if x != 0 and y != 0:
            save_to_notepad(f"Switched from mobile playback to radio\n")
        time.sleep(2)

    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
        save_to_excel(test_name, "Failed", error_message)
    
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
        save_to_excel(test_name, "Failed", error_message)
    
    finally:
        try:

            # End call on Mobile Device1
            phone.end_call_command()
            save_to_notepad(f"Ended call on Mobile Device1\n")
            time.sleep(2)

            # Pause audio on Mobile Device
            phone.pause_audio_command()
            save_to_notepad(f"Audio paused on Mobile Device\n")
            time.sleep(1)

            # Click Bluetooth button
            found = click_on_device_regex(HU, "Bluetooth")
            if found:
                save_to_notepad(f"Bluetooth button clicked\n")
            time.sleep(2)
            
            # Click Radio button to switch from mobile playback to radio
            x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
            command = f"shell input tap {x} {y-100}"
            stdout, stderr, rc = run_adb(command, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")  
            save_to_notepad(f"Result: {stdout}\n") 
            assert rc == 0, f"Command {command} failed: {rc}\n"
            if x != 0 and y != 0:
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
            
            # Clean up HU screenshots
            command = f"shell rm /sdcard/*.png"
            stdout, stderr, rc = run_adb(command, HU)
            
            # Return Mobile device to home
            try:
                rc = phone.run_home_command()
                save_to_notepad(f"Mobile device returned to home\n")
            except:
                pass
            
        except Exception as cleanup_error:
            save_to_notepad(f"Error during cleanup: {cleanup_error}\n")
        
        # Stop screen recording
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
        
        # Keep or delete recordings based on test result
        cleanup_recordings(test_passed, test_name)
        if test_passed:
            save_to_notepad(f"Test passed - recording deleted\n")
        else:
            save_to_notepad(f"Test failed - recording kept for debugging\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")

if __name__ == "__main__":
    main()