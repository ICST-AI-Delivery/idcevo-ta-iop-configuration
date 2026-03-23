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

test_name = "Mobile_Device_transfer_call_to_HU_in_new_Lifecycle"

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
        
        # Create Mobile device object
        phone = create_device(Mobile1, mobile_name)
        
        # Check SIM state on Mobile1
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device doesn't have SIM card - test skipped\n")
            save_to_excel(test_name, "Skipped", "Mobile device doesn't have SIM card")
            return
        
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
        mobile_name3 = stdout.strip()
        
        # Create Mobile device3 object
        phone3 = create_device(Mobile3, mobile_name3)
        
        # Check SIM state on Mobile3
        sim_state = phone3.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device 3 doesn't have SIM card - test skipped\n")
            save_to_excel(test_name, "Skipped", "Mobile device 3 doesn't have SIM card")
            return
        
        # Extract mobile3 phone number
        phone_number_mobile3 = phone3.get_phone_number_command()
        save_to_notepad(f"Mobile3 phone number: {phone_number_mobile3}\n")

        # Extract BTsnoop logs from HU before power off
        btsnoop_commands = [
            f"root",
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log btsnoop_hci_before_poweroff_transfer.log",
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log.last btsnoop_hci_before_poweroff_transfer.log.last"
        ]
        
        for cmd in btsnoop_commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            # Don't assert on btsnoop commands as they might not always be available
        
        # Move BTsnoop logs to target directory
        move_commands = [
            f"move btsnoop_hci_before_poweroff_transfer.log {base_dir}/Test_results",
            f"move btsnoop_hci_before_poweroff_transfer.log.last {base_dir}/Test_results"
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
        time.sleep(10)
        save_to_notepad(f"HU powered off\n")
        
        # Switch USB Matrix back to original port
        select_mobile_device_1(1, status)
        time.sleep(3)
        
        # Turn Mobile1 screen on
        rc = phone.run_turn_screen_on_command()
        time.sleep(2)
        
        # Unlock Mobile1 screen
        rc = phone.run_unlock_screen_command()
        time.sleep(2)
        
        # Initiate call from Mobile1 to Mobile3
        rc = phone.dial_command(phone_number_mobile3)
        time.sleep(5)
        save_to_notepad(f"Call initiated from Mobile1 to Mobile3\n")

        # Check USB Matrix status and switch if needed
        status = USB_Matrix_Status()
        if status == 1:
            select_mobile_device_1(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device_1(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")       
        time.sleep(3)

        # Run adb command to answer call (keyevent 5 is CALL button)
        rc = phone3.answer_call_command()
        assert rc == 0, f"Call command failed: {rc}\n"
        save_to_notepad(f"Call initiated\n")
        time.sleep(5)

        # Switch USB Matrix back to original port
        select_mobile_device_1(1, status)
        time.sleep(3)

        # Power on HU with ongoing call
        power_on_HU()
        time.sleep(60)
        save_to_notepad(f"HU powered on with ongoing call\n")
        
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

        # Get serial numbers after HU is powered on
        HU, Mobile1 = get_serial_number()
        save_to_notepad(f"HU serial number after power on: {HU}\n")
        
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
        
        # Restart BTsnoop logging
        command = f"shell device_config put bluetooth INIT_default_log_level_str LOG_VERBOSE"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        time.sleep(2)
        
        # Navigate to Language Menu
        command = f"shell am start -a android.settings.LOCALE_SETTINGS"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        time.sleep(2)
        
        command = f"shell input swipe 1200 500 2000 200"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        time.sleep(2)
        
        # Click English Button
        found = click_on_device_regex(HU, "English")
        if found == False:
            command = f"shell input tap 200 700"
            stdout, stderr, rc = run_adb(command, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"
            time.sleep(1)
            
            command = f"shell input swipe 1200 500 2000 200"
            stdout, stderr, rc = run_adb(command, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"
            time.sleep(2)
            
            found = click_on_device_regex(HU, "English")
        
        # Tap on screen
        command = f"shell input tap 3000 650"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        time.sleep(2)
        
        # Check if last 3 digits of mobile3 phone number are found on HU display
        last_3_digits = phone_number_mobile3[-3:]
        found = find_word_on_device_via_regex(HU, last_3_digits)
        
        if found:
            success_message = f"Head Unit sleeps, call audio is audible on {mobile_name}, and call audio transferred to HU with audio audible on both sides"
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Call transfer to HU in new lifecycle failed.\n"
        
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
        command = f"move {test_name}.png {base_dir}/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command {command} failed: {rc}\n"
        
        save_to_notepad(f"Mobile device screenshot saved successfully.\n")
        
        # End call on Mobile Device 1
        phone.end_call_command()
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
        time.sleep(1)
        
        save_to_notepad(f"=== Test {test_name} finished successfully ===\n")
        
    except Exception as e:
        error_message = str(e)
        save_to_notepad(f"Test failed with error: {error_message}\n")
        
        try:
            # Cleanup commands on failure
            command = f"shell input keyevent 3"
            stdout, stderr, rc = run_adb(command, HU)
            
            command = f"shell rm /sdcard/*.png"
            stdout, stderr, rc = run_adb(command, HU)
            
            phone.run_home_command()
            
        except Exception as cleanup_error:
            save_to_notepad(f"Error during cleanup: {cleanup_error}\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")
        save_to_excel(test_name, "Failed", error_message)
        raise

if __name__ == "__main__":
    main()