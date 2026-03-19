from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time
import pyautogui
import os
import ctypes
import time
import subprocess
import re

test_name = "HU_reconnect_after_Power_Off"

class POINT(ctypes.Structure):
   _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def set_mouse_position(x, y):
   ctypes.windll.user32.SetCursorPos(x, y)

def left_click():
   ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # mouse down
   ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # mouse up

def click_on_Retry():    
    screenshot_path = "D:/traget/IDCevo/IOP_configuration/Test_environment/Test_scripts/pc_screenshot.png"
    
    try:
        # Take screenshot of entire desktop
        save_to_notepad(f"Taking PC desktop screenshot...\n")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        save_to_notepad(f"PC desktop screenshot saved to {screenshot_path}\n")

        path = "D:/traget/IDCevo/IOP_configuration/Test_environment/Test_scripts"
        x, y = find_icon_in_screenshot(f"{path}/pc_screenshot.png", f"{path}/helpers/Retry.png")
        set_mouse_position(x+10, y+10)
        time.sleep(0.05)
        left_click()        
            
        # Clean up screenshot
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            save_to_notepad(f"Deleted PC screenshot\n")
            
    except Exception as e:
        save_to_notepad(f"Error in PC desktop click function: {e}\n")
        
        # Clean up screenshot even on error
        if os.path.exists(screenshot_path):
            try:
                os.remove(screenshot_path)
                save_to_notepad(f"Deleted PC screenshot after error\n")
            except:
                pass

def main():
    save_to_notepad(f"=== Test {test_name} started ===\n")
    path = "D:/traget/IDCevo/IOP_configuration/Test_environment/Test_scripts"
    
    # Initialize test result tracking
    test_passed = False

    try:
        # Check USB Matrix status
        status = USB_Matrix_Status()
        save_to_notepad(f"USB Matrix is connected to port: {status}\n")
        time.sleep(3)
        HU, Mobile1 = get_serial_number()
        
        # Create recordings folder and start screen recording only for Mobile Device
        create_recordings_folder()
        save_to_notepad(f"Created recordings folder\n")
        
        mobile_recording_started = start_screen_recording(f"-s {Mobile1}", test_name, "Mobile1")
        if mobile_recording_started:
            save_to_notepad(f"Mobile1 screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start Mobile1 screen recording\n")
        
        time.sleep(2)  # Wait for recordings to initialize
        
        # Get Mobile device global name
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

        # Create a version of the mobile name with spaces and special characters replaced by underscores
        mobile_name_without_space = re.sub(r'[^a-zA-Z0-9]', '_', mobile_name)
        save_to_notepad(f"Mobile name without spaces and special characters: {mobile_name_without_space}\n")
        
        phone = create_device(Mobile1,mobile_name)

        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Command failed: {rc}\n"  

        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone.run_settings_menu_command()
        assert rc == 0, f"Command failed: {rc}\n" 

        rc = phone.run_bluetooth_menu_command()
        assert rc == 0, f"Command failed: {rc}\n" 
        time.sleep(2)

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
        time.sleep(2) 

        # Run Download Btsnoop commands before reboot
        download_btsnoop_commands = [
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log btsnoop_hci_before_reboot.log",    # HU pull btsnoop1
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log.last btsnoop_hci_before_reboot.log.last"    # HU pull btsnoop2
        ]
        
        for cmd in download_btsnoop_commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Download BTsnoop command {cmd} failed: {rc}\n"
        
        save_to_notepad(f"Download Btsnoop commands executed successfully.\n")
        time.sleep(2)    

        # move the btsnoop logs
        command = f"move btsnoop* D:/traget/IDCevo/IOP_configuration/Test_results"
        stdout, stderr, rc = run_cmd(command)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"

        # Reboot HU using adb command
        reboot_command = f"reboot" # HU reboot command
        stdout, stderr, rc = run_adb(reboot_command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({reboot_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({reboot_command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"HU reboot command {reboot_command} failed: {rc}\n"
        
        # Wait until HU reboots properly
        save_to_notepad("HU is rebooting. Please wait...\n")
        time.sleep(60)  # Wait for HU to fully reboot

        # Restart DLT logs after reboot
        DLT_restart_command = f'ssh -i id_ed25519_idcevo -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@160.48.249.99 "nohup dlt-receive -a localhost -o /var/data/{mobile_name_without_space}.dlt >/dev/null 2>&1 &"'
        save_to_notepad(f"Resuming DLT logs after HU reboot...\n")
        try:
            result = subprocess.run(DLT_restart_command, shell=True, capture_output=True, text=True, timeout=30)
            save_to_notepad(f"[Executed command:] ({DLT_restart_command})\n")
            if result.returncode == 0:
                save_to_notepad(f"DLT logs resumed successfully\n")
            else:
                save_to_notepad(f"DLT restart command failed with return code: {result.returncode}\n")
                save_to_notepad(f"Error: {result.stderr}\n")
        except subprocess.TimeoutExpired:
            save_to_notepad(f"DLT restart command timed out after 30 seconds\n")
        except Exception as e:
            save_to_notepad(f"Error executing DLT restart command: {e}\n")

        # Restart BTsnoop command after reboot
        download_btsnoop_commands = [
            f"shell device_config put bluetooth INIT_default_log_level_str LOG_VERBOSE"    # HU restart BTsnoop after reboot

        ]
        
        for cmd in download_btsnoop_commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Start BTsnoop command {cmd} failed: {rc}\n"

        # Reconnect HU to Vysor after reboot        
        click_on_Retry()
        time.sleep(30)

        # Press on X Icon from HU display 2 times
        for nr in range(1,3):
            commands = [
                f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
                f"pull /sdcard/screenshot.png {path}",
                f"shell input tap 0 0"  # Will be replaced with actual coordinates
            ]
        
            for i, cmd in enumerate(commands):
                if i == 2:  # Bluetooth tap command
                    x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/X.png")
                    if x == 0 or y == 0:
                        x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/X_2.png")
                    cmd = f"shell input tap {x} {y}"
            
                stdout, stderr, rc = run_adb(cmd, HU)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n")
            time.sleep(2)

        # Press on X Icon from HU display 4 times
        for nr in range(1,5):
            commands = [
                f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
                f"pull /sdcard/screenshot.png {path}",
                f"shell input tap 0 0"  # Will be replaced with actual coordinates
            ]
        
            for i, cmd in enumerate(commands):
                if i == 2:  # Bluetooth tap command
                    x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/X_black.png")
                    cmd = f"shell input tap {x} {y}"
            
                stdout, stderr, rc = run_adb(cmd, HU)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n")
            time.sleep(2)

        # Run language commands after test is done
        language_commands = [
            f"shell am start -a android.settings.LOCALE_SETTINGS",   # HU Language Menu
            f"shell input swipe 1200 500 2000 200"   # HU swipe down
        ]
        
        for cmd in language_commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Language command {cmd} failed: {rc}\n"
            time.sleep(2)       
        save_to_notepad(f"Language commands executed successfully.\n")


        # Press on English button from HU display
        found = click_on_device_regex(HU, "English")
        time.sleep(1)  

        if found == False:    
            tap_command = [
                f"shell input tap 200 700",   # HU input tap
                f"shell input swipe 1200 500 2000 200"   # HU swipe down
            ]
            
            for cmd in tap_command:
                stdout, stderr, rc = run_adb(cmd, HU)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n")
                assert rc == 0, f"Language command {cmd} failed: {rc}\n"
                time.sleep(2)       
            save_to_notepad(f"Tap Command executed successfully.\n")  
            # Press on English button from HU display
            found = click_on_device_regex(HU, "English")
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
        cmd = r"del D:\traget\IDCevo\IOP_configuration\Test_environment\Test_scripts\screenshot.png"
        stdout, stderr, rc = run_cmd(cmd)
        
        # Press on Manage Devices button from HU display
        found = click_on_device(HU, "Manage devices")
        time.sleep(1)
        assert found == True, f"Manage devices button has not been found on HU display.\n"
        save_to_notepad(f"Manage devices button has been found and pressed on HU display.\n")
        
        # Press on Smartphones button from HU display
        found = click_on_device(HU, "Smartphones")
        time.sleep(1)
        assert found == True, f"Smartphones button has not been found on HU display.\n"
        save_to_notepad(f"Smartphones button has been found and pressed on HU display.\n")
        
        # Check if "Connected" word can be found on HU display
        found = find_word_on_device(HU, "Connected")
        if found == True:
            success_message = f"HU and {mobile_name} remained connected after HU power off."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            # Save to Excel with test_name, result="Passed" and comment=success_message
            save_to_excel(test_name, "Passed", success_message)
            # Mark test as passed for recording cleanup
            test_passed = True
        else:
            found = click_on_device_with_verification(HU,mobile_name)
            time.sleep(3)
            assert False, f"HU and {mobile_name} were disconnected after the reboot. Test failed.\n"
        
        # Take screenshot on Mobile device screen and save it
        screenshot_commands = [
            f"shell screencap -p /sdcard/{test_name}.png",
            f"pull /sdcard/{test_name}.png",
        ]
        
        for cmd in screenshot_commands:
            stdout, stderr, rc = run_adb(cmd,Mobile1)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Screenshot command {cmd} failed: {rc}\n"
        
        # move the screenshot
        command = f"move {test_name}.png D:/traget/IDCevo/IOP_configuration/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"

        # Run cleanup commands after test is done
        rc = phone.run_home_command()
        assert rc == 0, f"Command failed: {rc}\n"

        rc = phone.run_remove_screenshot_command()
        assert rc == 0, f"Command failed: {rc}\n"

        # HU home
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command,HU)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        save_to_notepad(f"Cleanup commands executed successfully.\n")
        
        # Stop screen recordings
        save_to_notepad(f"Stopping screen recordings...\n")
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
        rc = phone.run_home_command()
        assert rc == 0, f"Command failed: {rc}\n"

        # HU home
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command,HU)
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        # Stop screen recordings on test failure
        save_to_notepad(f"Stopping screen recordings...\n")
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
