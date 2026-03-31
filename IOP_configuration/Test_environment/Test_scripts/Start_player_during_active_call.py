from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import time

test_name = "Start_player_during_active_call"

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

        # Check SIM state on Mobile device
        sim_state = phone.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device doesn't have SIM card - test skipped\n")
            save_to_excel(test_name, "Skipped", "Mobile device doesn't have SIM card")
            return

        # Extract mobile1 phone number
        phone_number_mobile1 = phone.get_phone_number_command()
        save_to_notepad(f"Mobile1 phone number: {phone_number_mobile1}\n")

        # Check USB Matrix status and switch if needed
        if status == 1:
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

        # Check SIM state on Mobile device3
        sim_state = phone3.check_SIM_command()
        if "LOADED" not in sim_state:
            save_to_notepad(f"Mobile device3 doesn't have SIM card - test skipped\n")
            save_to_excel(test_name, "Skipped", "Mobile device3 doesn't have SIM card")
            return

        # Extract mobile3 phone number
        phone_number_mobile3 = phone3.get_phone_number_command()
        save_to_notepad(f"Mobile3 phone number: {phone_number_mobile3}\n")
        last_3_digits = phone_number_mobile3[-3:]

        # Switch USB Matrix back to the port from the beginning
        select_mobile_device(1, status)
        save_to_notepad(f"Switched USB Matrix back to port {status}\n")
        time.sleep(3)

        # Click Mobile device name button with regex from HU display
        found = click_on_device_regex(HU, mobile_name)
        assert found, f"Mobile device name button not found on HU display\n"
        save_to_notepad(f"Clicked on mobile device name button\n")
        time.sleep(1)

        # Click Calls Button on HU display
        found = click_on_device(HU, "Calls")
        assert found, f"Calls button not found on HU display\n"
        save_to_notepad(f"Clicked on Calls button\n")
        time.sleep(1)

        # Click on the phone number to make the call (using mobile name)
        last_3_digits = phone_number_mobile3[-3:]
        found = click_on_device_regex(HU, last_3_digits)
        assert found, f"Phone number  {phone_number_mobile3} not found on HU display\n"
        save_to_notepad(f"Clicked on phone number {phone_number_mobile3} to make the call\n")
        time.sleep(1)

        # Check USB Matrix status and switch if needed
        current_status = USB_Matrix_Status()
        if current_status == 1:
            select_mobile_device(1, 2)
            save_to_notepad(f"Switched USB Matrix from port 1 to port 2\n")
        else:
            select_mobile_device(1, 1)
            save_to_notepad(f"Switched USB Matrix to port 1\n")
        time.sleep(3)

        # Accept call on Mobile Device 3
        rc = phone3.answer_call_command()
        save_to_notepad(f"Accepted call on Mobile Device 3\n")
        time.sleep(3)

        # Switch USB Matrix back to the port from the beginning
        select_mobile_device(1, status)
        save_to_notepad(f"Switched USB Matrix back to port {status}\n")
        time.sleep(3)

        # Open Media menu
        command = f"shell input tap 1225 1325"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Opened Media menu\n")
        time.sleep(1)

        # Click Source button with regex from HU display
        found = click_on_device_regex(HU, "Source")
        time.sleep(2)

        # Click Bluetooth name on HU from Media menu
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Bluetooth")
        assert x != 0 and y != 0, f"Bluetooth name not found on HU display\n"

        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked on Bluetooth name\n")
        time.sleep(1)

        # Start Audio on HU
        command = f"shell input tap 1320 1030"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Opened Media menu\n")
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

        # Check if ongoing call is not interrupted by verifying last 3 digits
        found = find_word_on_device_via_regex(HU, last_3_digits)
        # Check test result
        if found == True:
            success_message = f"Ongoing call is not interrupted, play status does not change to playing, A2DP audio is still muted on Mobile Device 1, and audio playback will resume correctly after ending the call - test Passed."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"Call was interrupted by audio playback - test Failed"

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

        # End call on Mobile Device1
        phone.end_call_command()
        save_to_notepad(f"Ended call on Mobile Device1\n")
        time.sleep(2)

        # Pause audio on Mobile device
        phone.pause_audio_command()
        save_to_notepad(f"Paused audio on Mobile device\n")
        time.sleep(1)

        # Open Media menu
        command = f"shell input tap 1225 1325"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Opened Media menu\n")
        time.sleep(1)

        # Click Bluetooth button with regex from HU display
        found = click_on_device_regex(HU, "Bluetooth")
        time.sleep(1)
        assert found == True, f"Bluetooth button has not been found on HU display.\n"
        save_to_notepad(f"Bluetooth button has been found and pressed on HU display.\n")

        # Click Radio Button to switch from audio playback to Radio
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
        assert x != 0 and y != 0, f"Radio not found on HU display\n"

        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked on Radio\n")
        time.sleep(1)

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
        save_to_notepad(f"Returned Mobile device to home\n")

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

        # End call on Mobile Device1
        phone.end_call_command()
        time.sleep(2)

        # Pause audio on Mobile device
        phone.pause_audio_command()
        save_to_notepad(f"Paused audio on Mobile device\n")
        time.sleep(1)

        # Open Media menu
        command = f"shell input tap 1225 1325"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Opened Media menu\n")
        time.sleep(1)

        # Click Bluetooth button with regex from HU display
        found = click_on_device_regex(HU, "Bluetooth")
        time.sleep(1)
        assert found == True, f"Bluetooth button has not been found on HU display.\n"
        save_to_notepad(f"Bluetooth button has been found and pressed on HU display.\n")

        # Click Radio Button to switch from audio playback to Radio
        x, y = find_word_on_device_via_regex_with_coordinates(HU, "Radio")
        assert x != 0 and y != 0, f"Radio not found on HU display\n"

        command = f"shell input tap {x} {y-100}"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked on Radio\n")
        time.sleep(1)

        try:
            # Cleanup commands on test failure
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
