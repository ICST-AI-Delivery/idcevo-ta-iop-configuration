from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Audio_playback_during_phonebook_download"

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
        HU, Mobile1 = get_serial_number()

        # Create recordings folder and start screen recording for HU and for Mobile Device
        create_recordings_folder()
        save_to_notepad(f"Created recordings folder\n")

        save_to_notepad(f"Starting screen recordings...\n")
        hu_recording_started = start_screen_recording(f"-s {HU}", test_name, "HU")
        mobile_recording_started = start_screen_recording(f"-s {Mobile1}", test_name, "Mobile1")

        if hu_recording_started:
            save_to_notepad(f"HU screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start HU screen recording\n")

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
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        save_to_notepad(f"Tested device name: {mobile_name}\n")
        time.sleep(1)

        phone = create_device(Mobile1,mobile_name)

        phone.play_audio_command()
        time.sleep(2)

        phone.click_close_button_popup()
        time.sleep(2)

        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Command failed: {rc}\n"

        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Command failed: {rc}\n"

        rc = phone.run_settings_menu_command()
        assert rc == 0, f"Command failed: {rc}\n"

        rc = phone.run_bluetooth_menu_command()
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

        # Click Manage Devices Button from HU display
        found = click_on_device(HU, "Manage devices")
        time.sleep(1)
        assert found == True, f"Manage devices button has not been found on HU display.\n"
        save_to_notepad(f"Manage devices button has been found and pressed on HU display.\n")

        # Click Not now Button from HU display
        found = click_on_device(HU, "Not now")
        time.sleep(1)
        assert found == True, f"Not now button has not been found on HU display.\n"
        save_to_notepad(f"Not now button has been found and pressed on HU display.\n")

        # Click Smartphones Button from HU display
        found = click_on_device(HU, "Smartphones")
        time.sleep(1)
        assert found == True, f"Smartphones button has not been found on HU display.\n"
        save_to_notepad(f"Smartphones button has been found and pressed on HU display.\n")

        phone.click_close_button_popup()
        time.sleep(2)

        phone.enable_bluetooth()
        assert rc == 0, f"Command failed: {rc}\n"

        phone.click_close_button_popup()
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

        found = phone.click_HU_bluetooth_name_button(bluetooth_device_name)
        time.sleep(3)
        assert found == True, f"HU {bluetooth_device_name} has not been found on Mobile Bluetooth devices list.\n"
        save_to_notepad(f"HU {bluetooth_device_name} has been found and pressed on Mobile Bluetooth devices list.\n")

        # Click Connect Button from HU display
        found = click_on_device(HU, "Connect")
        time.sleep(1)
        assert found == True, f"Connect button has not been found on HU display.\n"
        save_to_notepad(f"Connect button has been found and pressed on HU display.\n")

        # Click Pair button from Mobile device display
        found = phone.click_pair_with_HU_button()
        time.sleep(10)
        assert found == True, f"Pair button has not been found on Mobile display.\n"
        save_to_notepad(f"Pair button has been found and pressed on Mobile display.\n")

        found = click_on_device(HU, "Not now")
        time.sleep(1)

        # Run adb command to go to HU home screen
        home_command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(home_command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({home_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({home_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Home command {home_command} failed: {rc}\n"
        save_to_notepad(f"Navigated to HU home screen.\n")
        time.sleep(2)

        found = click_on_device(HU, "Not now")
        time.sleep(1)

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

        # Check if Contacts word can be found on HU display with regex
        found = find_word_on_device_via_regex(HU, "Contacts")
        if found == True:
            success_message = f"{mobile_name} Phonebook is downloading during audio playback."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            # Save to Excel with test_name, result="Passed" and comment=success_message
            save_to_excel(test_name, "Passed", success_message)
            # Mark test as passed for recording cleanup
            test_passed = True
        else:
            assert False, f"{mobile_name} Phonebook download failed during audio playback.\n"

        # Take screenshot
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/{test_name}.png",
            f"pull /sdcard/{test_name}.png"
        ]

        for cmd in commands:
            stdout, stderr, rc = run_adb(cmd,HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {cmd} failed: {rc}\n"

        # move the screenshot
        command = f"move {test_name}.png {base_dir}/Test_results/Screenshots"
        stdout, stderr, rc = run_cmd(command)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        save_to_notepad(f"HU device screenshot saved successfully.\n")

        phone.click_allow_button_popup()

        phone.pause_audio_command()
        assert rc == 0, f"Audio pause command failed: {rc}\n"
        save_to_notepad(f"Audio playback paused on Mobile device.\n")

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

        # Click Manage Devices Button from HU display
        found = click_on_device(HU, "Manage devices")
        time.sleep(1)
        assert found == True, f"Manage devices button has not been found on HU display.\n"
        save_to_notepad(f"Manage devices button has been found and pressed on HU display.\n")

        # Click Smartphones Button from HU display
        found = click_on_device(HU, "Smartphones")
        time.sleep(1)
        assert found == True, f"Smartphones button has not been found on HU display.\n"
        save_to_notepad(f"Smartphones button has been found and pressed on HU display.\n")

        # Commands to be executed
        menu_commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png", # HU command to take screenshot
            f"pull /sdcard/screenshot.png {path}", # HU command to save screenshot on PC
            f"shell input tap 0 0" # HU command go to Mobile Menu Button
        ]
        for cmd in menu_commands:
            x = 0
            y = 0
            if cmd == menu_commands[2]:
                x,y = find_icon_in_screenshot(f"{path}/screenshot.png",f"{path}/helpers/Mobile_Menu_Button.png")
                if x == 0 or y == 0:
                    x,y = find_icon_in_screenshot(f"{path}/screenshot.png",f"{path}/helpers/Mobile_Menu_Button_2.png")
                cmd = f"shell input tap {x+60} {y+60}"

            stdout, stderr, rc = run_adb(cmd,HU)

            # Console display
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")
            save_to_notepad(f"Result: {stdout}\n")

            assert rc == 0, f"Command {cmd} failed: {rc}\n"
            if cmd == menu_commands[2]:
                if x==0 & y==0:
                    assert x!=0 & y!=0, f"Mobile Menu Button icon has not been found on HU display.\n"
                else:
                    save_to_notepad(f"Mobile Menu Button icon has been found on HU display!\n")

        # Clean up the screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)

        found = click_on_device_regex(HU,"Remove device")
        time.sleep(1)
        assert found == True, f"Remove device button has not been found on HU display.\n"
        save_to_notepad(f"Remove device button has been found and pressed on HU display.\n")

        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Command failed: {rc}\n"

        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Command failed: {rc}\n"

        rc = phone.run_settings_menu_command()
        assert rc == 0, f"Command failed: {rc}\n"

        rc = phone.run_bluetooth_menu_command()
        assert rc == 0, f"Command failed: {rc}\n"
        time.sleep(3)

        phone.click_settings_icon()
        time.sleep(2)

        phone.click_unpair_button()
        time.sleep(2)

        phone.disable_bluetooth()
        assert rc == 0, f"Command failed: {rc}\n"

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

        # Stop screen recordings
        save_to_notepad(f"Stopping screen recordings...\n")
        stop_screen_recording("HU")
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
        # Save to Excel with test_name, result="Failed" and comment=error_message
        save_to_excel(test_name, "Failed", error_message)

        # Run adb command to go to HU home screen
        home_command = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(home_command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({home_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({home_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Home command {home_command} failed: {rc}\n"
        save_to_notepad(f"Navigated to HU home screen.\n")
        time.sleep(2)

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

        # Click Manage Devices Button from HU display
        found = click_on_device(HU, "Manage devices")
        time.sleep(1)

        # Click Not now Button from HU display
        found = click_on_device(HU, "Not now")
        time.sleep(1)

        # Click Smartphones Button from HU display
        found = click_on_device(HU, "Smartphones")
        time.sleep(1)

        # Commands to be executed
        menu_commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png", # HU command to take screenshot
            f"pull /sdcard/screenshot.png {path}", # HU command to save screenshot on PC
            f"shell input tap 0 0" # HU command go to Mobile Menu Button
        ]
        for cmd in menu_commands:
            x = 0
            y = 0
            if cmd == menu_commands[2]:
                x,y = find_icon_in_screenshot(f"{path}/screenshot.png",f"{path}/helpers/Mobile_Menu_Button.png")
                if x == 0 or y == 0:
                    x,y = find_icon_in_screenshot(f"{path}/screenshot.png",f"{path}/helpers/Mobile_Menu_Button_2.png")
                cmd = f"shell input tap {x+60} {y+60}"

            stdout, stderr, rc = run_adb(cmd,HU)

            # Console display
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")
            save_to_notepad(f"Result: {stdout}\n")

            assert rc == 0, f"Command {cmd} failed: {rc}\n"
            if cmd == menu_commands[2]:
                if x==0 & y==0:
                    save_to_notepad(f"Mobile Menu Button icon has not been found on HU display.\n")
                else:
                    save_to_notepad(f"Mobile Menu Button icon has been found on HU display!\n")

        # Clean up the screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)

        found = click_on_device_regex(HU,"Remove device")
        time.sleep(1)

        rc = phone.run_turn_screen_on_command()

        rc = phone.run_unlock_screen_command()

        rc = phone.run_settings_menu_command()

        rc = phone.run_bluetooth_menu_command()
        time.sleep(3)

        phone.click_close_button_popup()
        time.sleep(2)

        # Click OK button from Mobile device display
        phone.click_OK_button()
        time.sleep(3)

        phone.click_settings_icon()
        time.sleep(2)

        phone.click_unpair_button()
        time.sleep(2)

        phone.disable_bluetooth()

        # Run cleanup commands even on failure
        try:
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
        except Exception as cleanup_error:
            save_to_notepad(f"Error during cleanup: {cleanup_error}\n")

        # Stop screen recordings on test failure
        save_to_notepad(f"Stopping screen recordings...\n")
        stop_screen_recording("HU")
        stop_screen_recording("Mobile1")

        # Keep recordings since test failed (test_passed is False)
        cleanup_recordings(test_passed, test_name)
        save_to_notepad(f"Test failed - recordings kept for debugging\n")

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
