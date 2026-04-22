from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Phonecall_while_in_Android_Auto"

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
        
        # Check SIM state
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            skip_message = f"Mobile device doesn't have SIM card - test Skipped.\n"
            save_to_notepad(f"{skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", skip_message)
            return
        
        # Extract mobile1 phone number
        phone_number_mobile1 = phone.get_phone_number_command()
        save_to_notepad(f"Mobile1 phone number: {phone_number_mobile1}\n")
        
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
        time.sleep(1)
        
        # Click Manage Devices Button from HU display
        found = click_on_device(HU, "Manage devices")
        assert found, f"Manage devices button not found on HU display.\n"
        save_to_notepad(f"Manage devices button clicked successfully\n")
        time.sleep(2)
        
        # Click Smartphones Button from HU display
        found = click_on_device(HU, "Smartphones")
        assert found, f"Smartphones button not found on HU display.\n"
        save_to_notepad(f"Smartphones button clicked successfully\n")
        time.sleep(2)
        
        # Click Android Auto icon from HU display
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
            f"pull /sdcard/screenshot.png {path}",
            f"shell input tap 0 0"  # Will be replaced with actual coordinates
        ]
        
        for i, cmd in enumerate(commands):
            if i == 2:  # Icon tap command
                x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Android_Auto.png")
                if x == 0 or y == 0:
                    x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Android_Auto_2.png")
                cmd = f"shell input tap {x+20} {y+20}"
            
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {cmd} failed: {rc}\n"
            
            if i == 2:  # After icon tap
                if x == 0 and y == 0:
                    skip_message = f"Mobile device doesn't support Android Auto - test Skipped.\n"
                    save_to_notepad(f"{skip_message}\n")
                    save_to_notepad(header="TEST SKIPPED", color="yellow")
                    save_to_excel(test_name, "Skipped", skip_message)
                    return
                save_to_notepad(f"Android Auto icon has been found and pressed!\n")
        
        # Clean up screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)
        time.sleep(2)
        
        # Click Start button on HU
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Start")
        command = f"shell input tap {x} {y+400}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Start button clicked successfully\n")
        time.sleep(3)
        
        # Go to HU Android Auto call menu
        command = f"shell input tap 550 700"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
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
        
        # Get Mobile3 device bluetooth name
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
        
        # Check SIM state for Mobile3
        sim_state = phone3.check_SIM_command()
        if "LOADED" not in sim_state:
            skip_message = f"Mobile device3 doesn't have SIM card - test Skipped.\n"
            save_to_notepad(f"{skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="yellow")
            save_to_excel(test_name, "Skipped", skip_message)
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
        
        # Initiate call from Mobile3 to Mobile1
        rc = phone3.dial_command(phone_number_mobile1)
        save_to_notepad(f"Call initiated from Mobile3 to Mobile1\n")
        time.sleep(5)  # Wait for incoming call to be established
        
        # Switch USB Matrix back to original port
        select_mobile_device(1, status)
        save_to_notepad(f"Switched USB Matrix back to original port {status}\n")
        time.sleep(3)
        
        # Answer call on Mobile1
        rc = phone.answer_call_command()
        save_to_notepad(f"Call answered on Mobile1\n")
        time.sleep(3)
        
        # Check if last 3 digits of mobile3 phone number can be found on HU display
        last_3_digits = phone_number_mobile3[-3:]
        commands = [
            f"shell screencap -p /sdcard/screenshot.png", # HU command to take screenshot
            f"pull /sdcard/screenshot.png {path}", # HU command to save screenshot on PC
            f"shell input tap 0 0" # HU command to click last 3 digits word
        ]

        for cmd in commands:
            x = 0
            y = 0
            if cmd == commands[2]:
                x,y = find_word_in_screenshot(f"{path}/screenshot.png",last_3_digits)
                cmd = f"shell input tap {x} {y}"

            stdout, stderr, rc = run_adb(cmd, HU)
            # Console display
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")
            save_to_notepad(f"Result: {stdout}\n")

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

        if x != 0 & y != 0:
            found = True
        
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
        
        # End call on Mobile1
        phone.end_call_command()
        save_to_notepad(f"Call ended on Mobile1\n")
        time.sleep(2)
        
        # Check test result
        if found == True:
            success_message = f"Phonecall while in Android Auto functionality works correctly - test Passed.\n"
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Phonecall audio functionality while in Android Auto failed - test Failed\n"
        
        # Return to home menu on HU
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        time.sleep(2)

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
        
        # Click Manage Devices Button from HU display
        found = click_on_device(HU, "Manage devices")
        assert found, f"Manage devices button not found on HU display\n"
        save_to_notepad(f"Manage devices button clicked successfully\n")
        time.sleep(2)
        
        # Click Smartphones Button on from HU display
        found = click_on_device(HU, "Smartphones")
        assert found, f"Smartphones button not found on HU display\n"
        save_to_notepad(f"Smartphones button clicked successfully\n")
        time.sleep(2)
        
        # Click Android Auto disconnect icon from HU display
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
            f"pull /sdcard/screenshot.png {path}",
            f"shell input tap 0 0"  # Will be replaced with actual coordinates
        ]
        
        for i, cmd in enumerate(commands):
            if i == 2:  # Icon tap command
                x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Android_Auto_disconnect.png")
                if x == 0 or y == 0:
                    x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Android_Auto_disconnect_2.png")
                cmd = f"shell input tap {x+20} {y+20}"
            
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {cmd} failed: {rc}\n"
            
            if i == 2:  # After icon tap
                if x==0 and y==0:
                    skip_message = f"{mobile_name} doesn't support Android Auto."
                    save_to_notepad(f"TEST SKIPPED: {skip_message}\n")
                    save_to_notepad(header="TEST SKIPPED", color="orange")
                    # Save to Excel with test_name, result="Skipped" and comment=skip_message
                    save_to_excel(test_name, "Skipped", skip_message)
                    save_to_notepad(f"=== Test {test_name} finished (skipped) ===\n")
                    return  # Exit the test early
                else:
                    save_to_notepad(f"Android_Auto_disconnect icon has been found and pressed!\n")
        
        # Clean up screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)
        time.sleep(5)
        
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
        save_to_notepad(f"Mobile device returned to home\n")
        
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
        
        # Cleanup commands on test failure
        try:
            # End any active calls
            try:
                phone.end_call_command()
                phone3.end_call_command()
            except:
                pass
            
            # Return to home menu
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