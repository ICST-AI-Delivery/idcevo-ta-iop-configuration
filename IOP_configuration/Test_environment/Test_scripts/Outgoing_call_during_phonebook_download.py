from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Outgoing_call_during_phonebook_download"

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

        # Check if Mobile device has a SIM card
        save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            skip_message = f"{mobile_name} doesn't have a SIM card on it."
            save_to_notepad(f"TEST SKIPPED: {skip_message}\n")
            save_to_notepad(header="TEST SKIPPED", color="orange")
            # Save to Excel with test_name, result="Skipped" and comment=skip_message
            save_to_excel(test_name, "Skipped", skip_message)
            save_to_notepad(f"=== Test {test_name} finished (skipped) ===\n")
            return  # Exit the test early
        else:
            save_to_notepad(f"{mobile_name} has a SIM card (state: {sim_state}). Continuing test...\n")

        phone_number_mobile1 = phone.get_phone_number_command()

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name" # Mobile2 command go get device name
            stdout, stderr, rc = run_adb(command, Mobile2)
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

            phone2 = create_device(Mobile2,mobile_name)

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_state = phone2.check_SIM_command()
            if "LOADED" not in sim_state:
                skip_message = f"{mobile_name} doesn't have a SIM card on it."
                save_to_notepad(f"TEST SKIPPED: {skip_message}\n")
                save_to_notepad(header="TEST SKIPPED", color="orange")
                # Save to Excel with test_name, result="Skipped" and comment=skip_message
                save_to_excel(test_name, "Skipped", skip_message)
                save_to_notepad(f"=== Test {test_name} finished (skipped) ===\n")
                return  # Exit the test early
            else:
                save_to_notepad(f"{mobile_name} has a SIM card (state: {sim_state}). Continuing test...\n")

            phone_number_mobile2 = phone2.get_phone_number_command()
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name" # Mobile2 command go get device name
            stdout, stderr, rc = run_adb(command, Mobile2)
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

            phone2 = create_device(Mobile2,mobile_name)

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_state = phone2.check_SIM_command()
            if "LOADED" not in sim_state:
                skip_message = f"{mobile_name} doesn't have a SIM card on it."
                save_to_notepad(f"TEST SKIPPED: {skip_message}\n")
                save_to_notepad(header="TEST SKIPPED", color="orange")
                # Save to Excel with test_name, result="Skipped" and comment=skip_message
                save_to_excel(test_name, "Skipped", skip_message)
                save_to_notepad(f"=== Test {test_name} finished (skipped) ===\n")
                return  # Exit the test early
            else:
                save_to_notepad(f"{mobile_name} has a SIM card (state: {sim_state}). Continuing test...\n")

            phone_number_mobile2 = phone2.get_phone_number_command()
        time.sleep(2)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        rc = phone.run_turn_screen_on_command()
        assert rc == 0, f"Command failed: {rc}\n"

        rc = phone.run_unlock_screen_command()
        assert rc == 0, f"Command failed: {rc}\n"
        time.sleep(2)

        rc = phone.dial_command(phone_number_mobile2)
        assert rc == 0, f"Dial command failed: {rc}\n"
        save_to_notepad(f"Dialer started with phone number +{phone_number_mobile2}\n")
        time.sleep(5)

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)

            # Run adb command to answer call (keyevent 5 is CALL button)
            rc = phone2.answer_call_command()
            assert rc == 0, f"Call command failed: {rc}\n"
            save_to_notepad(f"Call initiated\n")
            time.sleep(5)
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)

            # Run adb command to answer call (keyevent 5 is CALL button)
            rc = phone2.answer_call_command()
            assert rc == 0, f"Call command failed: {rc}\n"
            save_to_notepad(f"Call initiated\n")
            time.sleep(5)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

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

        # Create recordings folder and start screen recording for HU and Mobile device
        create_recordings_folder()
        save_to_notepad(f"Created recordings folder\n")

        save_to_notepad(f"Starting screen recording for HU...\n")
        hu_recording_started = start_screen_recording(f"-s {HU}", test_name, "HU")

        if hu_recording_started:
            save_to_notepad(f"HU screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start HU screen recording\n")

        save_to_notepad(f"Starting screen recording for Mobile device...\n")
        mobile_recording_started = start_screen_recording(f"-s {Mobile1}", test_name, "Mobile")

        if mobile_recording_started:
            save_to_notepad(f"Mobile device screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start Mobile device screen recording\n")

        time.sleep(2)  # Wait for recording to initialize

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

        found = click_on_device(HU, "Not now")
        time.sleep(1)

        # Extract last 3 digits from phone number before clicking
        last_3_digits = phone_number_mobile2[-3:] if len(phone_number_mobile2) >= 3 else phone_number_mobile2
        save_to_notepad(f"Extracted last 3 digits from phone number {phone_number_mobile2}: {last_3_digits}\n")

        # Click Mobile device name button with regex from HU display (using last 3 digits only)
        found = click_on_device_regex(HU, last_3_digits)
        time.sleep(5)
        assert found == True, f"Mobile device number last 3 digits {last_3_digits} has not been found on HU display.\n"
        save_to_notepad(f"Mobile device number last 3 digits {last_3_digits} has been found and pressed on HU display.\n")

        # Click Left Arrow Icon icon from HU display
        commands = [
            f"shell screencap -d 4633128631561747456 -p /sdcard/screenshot.png",
            f"pull /sdcard/screenshot.png {path}",
            f"shell input tap 0 0"  # Will be replaced with actual coordinates
        ]

        for i, cmd in enumerate(commands):
            if i == 2:  # Left Arrow tap command
                x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Left_Arrow.png")
                if x == 0 or y == 0:
                    x, y = find_icon_in_screenshot(f"{path}/screenshot.png", f"{path}/helpers/Left_Arrow_2.png")
                cmd = f"shell input tap {x} {y}"

            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {cmd} failed: {rc}\n"

            if i == 2:  # After Left Arrow tap
                assert x != 0 and y != 0, f"Left Arrow icon has not been found on HU display.\n"
                save_to_notepad(f"Left Arrow icon has been found and pressed on HU display!\n")

        # Clean up the screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)

        # Click Contacts Button from HU display
        found = click_on_device(HU, "Contacts")
        time.sleep(1)
        assert found == True, f"Contacts button has not been found on HU display.\n"
        save_to_notepad(f"Contacts button has been found and pressed on HU display.\n")

        # Check if Contacts word can be found on HU display with regex during outgoing call
        found = find_word_on_device_via_regex(HU, "Contacts")
        if found == True:
            success_message = f"{mobile_name} Phonebook is downloading to HU during outgoing call."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            # Save to Excel with test_name, result="Passed" and comment=success_message
            save_to_excel(test_name, "Passed", success_message)
            # Mark test as passed for recording cleanup
            test_passed = True
        else:
            assert False, f"{mobile_name} Phonebook download failed during outgoing call.\n"

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

        # Run command to go back to home on HU
        home_cmd = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(home_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({home_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({home_cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Home command {home_cmd} failed: {rc}\n"
        time.sleep(2)

        # Run adb command to end call (keyevent 6 is END_CALL button)
        phone.end_call_command()
        assert rc == 0, f"End call command failed: {rc}\n"
        save_to_notepad(f"Call ended\n")
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

        # Stop screen recording
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
        stop_screen_recording("Mobile")

        # Clean up recording based on test result
        cleanup_recordings(test_passed, test_name)
        if test_passed:
            save_to_notepad(f"Test passed - recording deleted\n")
        else:
            save_to_notepad(f"Test completed - recording kept for review\n")

        save_to_notepad(f"=== Test {test_name} finished ===\n")

    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
        # Save to Excel with test_name, result="Failed" and comment=error_message
        save_to_excel(test_name, "Failed", error_message)

        # Run adb command to end call (keyevent 6 is END_CALL button)
        phone.end_call_command()
        time.sleep(2)

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
        assert rc == 0, f"Command failed: {rc}\n"

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

        # Stop screen recording on test failure
        save_to_notepad(f"Stopping screen recording...\n")
        stop_screen_recording("HU")
        stop_screen_recording("Mobile")

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
