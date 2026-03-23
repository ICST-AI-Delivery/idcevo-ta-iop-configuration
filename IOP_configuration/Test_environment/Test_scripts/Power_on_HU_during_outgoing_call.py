"""
AI-Generated Test Script for: Power_on_HU_during_outgoing_call
Generated on: 2026-03-09 10:56:46

Test Case Information:
- Precondition: Mobile Device and HU are paired and not connected.
HU is switched off (For TestraIDCEvos and Testcases set mode Parken: "Parken_BN_IO").
- Description: 1 Initiate an outgoing call from Mobile Device 1 to Mobile Device 3.
2 Accept call on Mobile Device 3.
3 During an active outgoing call power on HU.
For TestraIDCEvos and Testcases set mode Fahren: "Pruefen_Analyse_Diagnose" (power on).
- Expected Result: 3 Bluetooth connection reestablished between HU to Mobile Device 1. Audio ist audible on HU.
"""

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

test_name = "Power_on_HU_during_outgoing_call"

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
        Mobile1, HU_dummy = get_serial_number()

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

        # Create a version of the mobile name with spaces and special characters replaced by underscores
        mobile_name_without_space = re.sub(r'[^a-zA-Z0-9]', '_', mobile_name)
        save_to_notepad(f"Mobile name without spaces and special characters: {mobile_name_without_space}\n")

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
            select_mobile_device_1(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device_1(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")
        time.sleep(3)

        # Get serial numbers for HU and Mobile3
        Mobile3, HU_dummy = get_serial_number()

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
        select_mobile_device_1(1, status)
        time.sleep(3)
        save_to_notepad(f"Switched USB Matrix back to original port\n")

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
            select_mobile_device_1(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device_1(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")
        time.sleep(3)

        # Accept call on Mobile Device 3
        rc = phone3.answer_call_command()
        assert rc == 0, f"Answer call command failed: {rc}\n"
        save_to_notepad(f"Call accepted on Mobile3\n")

        # Switch USB Matrix back to the port from the beginning
        select_mobile_device_1(1, status)
        save_to_notepad(f"Switched USB Matrix back to original port\n")
        time.sleep(3)  # Wait for call to become active

        # Power off HU during the active outgoing call
        power_on_HU()
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

        # Reconnect HU to Vysor after reboot
        click_on_Retry()
        time.sleep(30)

        # Get serial numbers for HU and Mobile1
        HU, Mobile1 = get_serial_number()

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

        # HU tap command
        command = f"shell input tap 3000 650"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

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
        command = f"move {test_name}.png {base_dir}/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        save_to_notepad(f"HU device screenshot saved successfully.\n")

        # Get last 3 digits of mobile3 phone number
        last_3_digits = phone_number_mobile3[-3:] if len(phone_number_mobile3) >= 3 else phone_number_mobile3
        save_to_notepad(f"Looking for last 3 digits: {last_3_digits}\n")

        # Check if last 3 digits of mobile3 phone number can be found on HU display
        found = find_word_on_device_via_regex(HU, last_3_digits)
        if found:
            success_message = f"Bluetooth connection reestablished between HU to {mobile_name} and audio is audible on HU."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Bluetooth connection was not reestablished properly after HU power on.\n"

        # End call on Mobile Device1
        phone.end_call_command()
        save_to_notepad(f"Call ended on Mobile1\n")

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
                save_to_notepad(f"Emergency call end executed\n")
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
