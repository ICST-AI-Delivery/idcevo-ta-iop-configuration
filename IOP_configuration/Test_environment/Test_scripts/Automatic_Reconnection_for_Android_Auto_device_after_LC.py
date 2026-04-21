from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
from helpers.switch_commands import *
import time
import pyautogui
import os
import ctypes
import time
import subprocess
import re

test_name = "Automatic_Reconnection_for_Android_Auto_device_after_LC"

class POINT(ctypes.Structure):
   _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def set_mouse_position(x, y):
   ctypes.windll.user32.SetCursorPos(x, y)

def left_click():
   ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # mouse down
   ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # mouse up

def click_on_Retry():
    base_dir = extract_base_dir_from_batch()
    screenshot_path = f"{base_dir}/Test_environment/Test_scripts/pc_screenshot.png"

    try:
        # Take screenshot of entire desktop
        save_to_notepad(f"Taking PC desktop screenshot...\n")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        save_to_notepad(f"PC desktop screenshot saved to {screenshot_path}\n")

        path = f"{base_dir}/Test_environment/Test_scripts"
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

        save_to_notepad(f"Starting screen recording for Mobile Device...\n")
        mobile_recording_started = start_screen_recording(f"-s {Mobile1}", test_name, "Mobile1")

        if mobile_recording_started:
            save_to_notepad(f"Mobile1 screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start Mobile1 screen recording\n")

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
        assert found, f"Manage devices button not found on display.\n"
        save_to_notepad(f"Manage devices button clicked successfully\n")
        time.sleep(2)
        
        # Click Smartphones Button from HU display
        found = click_on_device(HU, "Smartphones")
        assert found, f"Smartphones button not found on display.\n"
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
                    success_message = f"Mobile device doesn't support Android Auto - test Skipped.\n"
                    save_to_notepad(f"{success_message}\n")
                    save_to_notepad(header="TEST SKIPPED", color="yellow")
                    save_to_excel(test_name, "Skipped", success_message)
                    return
                save_to_notepad(f"Android Auto icon has been found and pressed!\n")
        
        # Clean up screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)        
        time.sleep(2)
        
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
        
        # Go to HU home screen
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Navigated to HU home screen\n")
        time.sleep(2)
        
        # Extract BTsnoop logs from HU before lifecycle
        commands = [
            "root",
            "pull /data/misc/bluetooth/logs/btsnoop_hci.log btsnoop_hci_before_LC.log",
            "pull /data/misc/bluetooth/logs/btsnoop_hci.log.last btsnoop_hci_before_LC.log.last"
        ]
        
        for cmd in commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
        
        # Move BTsnoop logs to target directory
        move_commands = [
            f"move btsnoop_hci_before_LC.log {base_dir}/Test_results",
            f"move btsnoop_hci_before_LC.log.last {base_dir}/Test_results"
        ]
        
        for cmd in move_commands:
            stdout, stderr, rc = run_cmd(cmd)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            # Don't assert on move commands as files might not exist
        
        save_to_notepad(f"BTsnoop logs extracted from HU before power off\n")
        
        # Power off HU
        power_off_HU()
        save_to_notepad(f"HU powered off\n")
        time.sleep(10)  # Wait for HU to completely power off
        
        # Power on HU to perform lifecycle
        power_on_HU()
        save_to_notepad(f"HU powered on - lifecycle performed\n")
        time.sleep(60)  # Wait for HU to boot up and establish Bluetooth connection

        # Create a version of the mobile name with spaces and special characters replaced by underscores
        mobile_name_without_space = re.sub(r'[^a-zA-Z0-9]', '_', mobile_name)
        save_to_notepad(f"Mobile name without spaces and special characters: {mobile_name_without_space}\n")

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

        # Click Retry icon button from PC display
        click_on_Retry()
        save_to_notepad(f"Clicked Retry button\n")
        time.sleep(30)  # Wait for HU to initialize properly
        
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

        # Clean up the screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)
        
        # Restart BTsnoop logging after power on
        command = f"shell device_config put bluetooth INIT_default_log_level_str LOG_VERBOSE"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"BTsnoop logging restarted\n")
        time.sleep(2)

        # Return to home menu - HU commands
        command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        time.sleep(2)

        # Navigate on Language Menu
        commands = [
            "shell am start -a android.settings.LOCALE_SETTINGS",
            "shell input swipe 1200 500 2000 200"
        ]
        
        for cmd in commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {cmd} failed: {rc}\n"
            time.sleep(2)
        
        save_to_notepad(f"Navigated to Language Menu\n")

        # Click English Button from HU display
        found = click_on_device_regex(HU, "English")
        if not found:
            commands = [
                "shell input tap 200 700",
                "shell input swipe 1200 500 2000 200"
            ]
            
            for cmd in commands:
                stdout, stderr, rc = run_adb(cmd, HU)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n")
                assert rc == 0, f"Command {cmd} failed: {rc}\n"
                time.sleep(2)
            
            found = click_on_device_regex(HU, "English")
        
        assert found, f"English button not found on display.\n"
        save_to_notepad(f"English button clicked successfully\n")
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
        assert found, f"Manage devices button not found on display.\n"
        save_to_notepad(f"Manage devices button clicked successfully\n")
        time.sleep(2)
        
        # Click Smartphones Button from HU display
        found = click_on_device(HU, "Smartphones")
        assert found, f"Smartphones button not found on display.\n"
        save_to_notepad(f"Smartphones button clicked successfully\n")
        time.sleep(2)
        
        # Check if Android Auto icon can be found on HU display
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
        
        x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Android_Auto.png")
        if x == 0 or y == 0:
            x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Android_Auto_2.png")
        
        # Clean up screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)
        
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
        
        # Check test result
        if x != 0 and y != 0:
            success_message = f"Android Auto icon found after lifecycle - automatic reconnection successful - test Passed.\n"
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Android Auto icon not found after lifecycle - automatic reconnection failed - test Failed.\n"

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
        
        command = f"shell rm /sdcard/*.png"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        
        # Return to home menu - Mobile device commands
        rc = phone.run_home_command()
        save_to_notepad(f"Mobile device returned to home\n")
        
        # Stop screen recording and cleanup
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("Mobile1")
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
        stop_screen_recording("Mobile1")
        
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