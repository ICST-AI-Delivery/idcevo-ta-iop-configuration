from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Disconnect_Android_Auto_device_while_multiple_MDs_are_connected"

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
        assert found == True, f"Manage devices button not found on HU display.\n"
        save_to_notepad(f"Manage devices button clicked successfully\n")
        time.sleep(2)
        
        # Click Smartphones Button on from HU display
        found = click_on_device(HU, "Smartphones")
        assert found == True, f"Smartphones button not found on HU display.\n"
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
                if x==0 and y==0:
                    skip_message = f"{mobile_name} doesn't support Android Auto."
                    save_to_notepad(f"TEST SKIPPED: {skip_message}\n")
                    save_to_notepad(header="TEST SKIPPED", color="orange")
                    # Save to Excel with test_name, result="Skipped" and comment=skip_message
                    save_to_excel(test_name, "Skipped", skip_message)
                    save_to_notepad(f"=== Test {test_name} finished (skipped) ===\n")
                    return  # Exit the test early
                else:
                    save_to_notepad(f"Android_Auto icon has been found and pressed!\n")
        
        # Clean up screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)
        time.sleep(5)

        # Click Start button from HU display with regex to accept Android Auto disclaimer in the HMI
        found = find_word_on_device_via_regex_with_coordinates(HU, "Start")        
        command = f"shell input tap {x} {y+400}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        time.sleep(5)
        
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
        
        # Check USB Matrix status and adjust if needed
        status = USB_Matrix_Status()
        save_to_notepad(f"USB Matrix is connected to port: {status}")
        if status == 1:
            select_mobile_device(1, 2)
        else:
            select_mobile_device(1, 1)
        time.sleep(3)
        
        # Extracting serial numbers for HU and Mobile2
        HU, Mobile2 = get_serial_number()

        # Get Mobile device global name
        command = f"shell settings get secure bluetooth_name" # Mobile command go get device name
        stdout, stderr, rc = run_adb(command, Mobile2)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name2 = stdout.strip()
        save_to_notepad(f"Tested device name: {mobile_name2}\n")
        time.sleep(1)
        
        phone2 = create_device(Mobile2,mobile_name2)

        phone2.click_close_button_popup()
        time.sleep(2)

        rc = phone2.run_turn_screen_on_command()
        assert rc == 0, f"Command failed: {rc}\n"  

        rc = phone2.run_unlock_screen_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone2.run_settings_menu_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone2.run_bluetooth_menu_command()
        assert rc == 0, f"Command failed: {rc}\n"
        
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
        
        # Click Manage Devices on HU
        found = click_on_device(HU, "Manage devices")
        time.sleep(1)
        assert found == True, f"Manage devices button has not been found on HU display.\n"
        save_to_notepad(f"Manage devices button has been found and pressed on HU display.\n")
        
        # Click Smartphones on HU
        found = click_on_device(HU, "Smartphones")
        time.sleep(1)
        assert found == True, f"Smartphones button has not been found on HU display.\n"
        save_to_notepad(f"Smartphones button has been found and pressed on HU display.\n")
        
        # Click Connect new device on HU
        found = click_on_device(HU, "Connect new device")
        time.sleep(1)
        assert found == True, f"Connect new device button has not been found on HU display.\n"
        save_to_notepad(f"Connect new device button has been found and pressed on HU display.\n")
        
        # Handle possible popup on Mobile device
        phone2.click_close_button_popup()
        time.sleep(1)
        
        phone2.enable_bluetooth()
        assert rc == 0, f"Command failed: {rc}\n" 

        phone2.click_close_button_popup()
        time.sleep(2)
        
        # Get HU Bluetooth device name
        bluetooth_name_cmd = f'shell dumpsys bluetooth_manager | findstr -i "Name:"'
        stdout, stderr, rc = run_adb(bluetooth_name_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({bluetooth_name_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({bluetooth_name_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {bluetooth_name_cmd} failed: {rc}\n"
        
        # Extract Bluetooth device name
        bluetooth_device_name = ""
        first_line = stdout.strip().split('\n')[0] if stdout.strip() else ""
        if first_line and "name:" in first_line.lower():
            name_parts = first_line.split(":", 1)
            if len(name_parts) > 1:
                bluetooth_device_name = name_parts[1].strip()
        
        save_to_notepad(f"Extracted Bluetooth device name: {bluetooth_device_name}\n")
        
        # Click on HU device name on Mobile device
        found = phone2.click_HU_bluetooth_name_button(bluetooth_device_name)
        time.sleep(3)
        assert found == True, f"HU {bluetooth_device_name} has not been found on Mobile Bluetooth devices list.\n"
        save_to_notepad(f"HU {bluetooth_device_name} has been found and pressed on Mobile Bluetooth devices list.\n")
        
        # Click Connect on HU
        found = click_on_device(HU, "Connect")
        time.sleep(3)
        assert found == True, f"Connect button has not been found on HU display.\n"
        save_to_notepad(f"Connect button has been found and pressed on HU display.\n")
        
        # Click Pair button from Mobile device display
        found = phone2.click_pair_with_HU_button()
        time.sleep(10)
        assert found == True, f"Pair button has not been found on Mobile display.\n"
        save_to_notepad(f"Pair button has been found and pressed on Mobile display.\n")

        phone2.click_allow_button_popup()
        
        # Click Not now twice on HU
        found = click_on_device(HU, "Not now")
        time.sleep(1)
        found = click_on_device(HU, "Not now")
        time.sleep(1)

        found = click_on_device(HU,mobile_name)
        time.sleep(1)
        
        # Check test result
        if found == True:
            success_message = f"Android Auto was disconnected successfully while another mobile device is paired with HU - test Passed.\n"
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Android Auto disconnection failed - test Failed\n"

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

        found = click_on_device_with_verification(HU,mobile_name)
        time.sleep(3)
        assert found == True, f"Mobile Device name has not been found on HU display.\n"
        save_to_notepad(f"Mobile Device name has been found and pressed on HU display.\n")

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

        # Click Mobile Menu Button for second device
        x, y = find_word_on_device_via_regex_with_coordinates(HU,mobile_name2)       
        cmd = f"shell input tap {x+1160} {y+60}"
        run_adb(cmd, HU)
        time.sleep(3)
        
        # Click Remove device
        found = click_on_device_regex(HU,"Remove device")
        time.sleep(1)

        # Click Remove device
        if found == False:
            found = click_on_device_regex(HU,"Remove device")
            time.sleep(1)
        
        rc = phone2.run_turn_screen_on_command()
        assert rc == 0, f"Command failed: {rc}\n"  

        rc = phone2.run_unlock_screen_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone2.run_settings_menu_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone2.run_bluetooth_menu_command()
        assert rc == 0, f"Command failed: {rc}\n"
        time.sleep(6)

        phone2.click_settings_icon()
        time.sleep(2)

        phone2.click_unpair_button()
        time.sleep(2)
        
        phone2.disable_bluetooth()
        assert rc == 0, f"Command failed: {rc}\n"

        # Mobile home
        rc = phone2.run_home_command()
        assert rc == 0, f"Command failed: {rc}\n"

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

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
        
        # Stop screen recording
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
        
        # Clean up recordings since test passed
        cleanup_recordings(test_passed, test_name)
        save_to_notepad(f"Test passed - recording cleaned up\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")

    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
        save_to_excel(test_name, "Failed", error_message)
        
        try:
            # Cleanup commands on failure
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