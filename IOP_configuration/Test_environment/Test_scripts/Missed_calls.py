from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *

test_name = "Missed_calls"

def main():
    save_to_notepad(f"=== Test {test_name} started ===\n")
    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"
    
    try:
        # Check USB Matrix status
        status = USB_Matrix_Status()
        save_to_notepad(f"USB Matrix is connected to port: {status}")
        time.sleep(3)
        
        # Extracting serial numbers for HU and Mobile1
        HU, Mobile1 = get_serial_number()
        
        # Create recordings folder
        create_recordings_folder()
        save_to_notepad(f"Created recordings folder\n")
        
        # Start screen recordings before any test actions
        save_to_notepad(f"Starting screen recordings...\n")
        hu_recording_started = start_screen_recording(f"-s {HU}", test_name, "HU")
        
        if hu_recording_started:
            save_to_notepad(f"HU screen recording started successfully\n")
        else:
            save_to_notepad(f"Warning: Failed to start HU screen recording\n")
        
        # Wait a moment for recordings to initialize
        time.sleep(2)
        
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

        # Navigate to Mobile device in HU display
        found = click_on_device_regex(HU, mobile_name)
        time.sleep(1)
        assert found == True, f"{mobile_name} button has not been found on HU display.\n"
        save_to_notepad(f"{mobile_name} button has been found and pressed on HU display.\n")

        # Navigate to Calls
        found = click_on_device(HU, "Calls")
        time.sleep(1)
        assert found == True, f"Calls button has not been found on HU display.\n"
        save_to_notepad(f"Calls button has been found and pressed on HU display.\n")

        # Navigate to Missed calls
        found = click_on_device(HU, "Missed")
        time.sleep(1)
        assert found == True, f"Missed button has not been found on HU display.\n"
        save_to_notepad(f"Missed button has been found and pressed on HU display.\n")

        # Check if "No" word is present on HU display (indicating no missed calls)
        no_missed_calls_found = find_word_on_device_via_regex(HU, "No")
        time.sleep(1)
        
        if no_missed_calls_found:
            # If "No" is found, there are no missed calls - test passes
            success_message = f"No missed calls found on {mobile_name} device - test passed"
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
        else:
            # If "No" is not found, proceed with missed calls validation
            save_to_notepad(f"Missed calls detected on HU display, proceeding with validation...\n")

            result = phone.get_missed_calls()
            if result is None:
                raise AssertionError("get_missed_calls() returned None - unable to retrieve call data")
            
            extracted_number, extracted_name = result
                    
            # Scroll down on HU display 10 times using the specified coordinates
            for i in range(10):        
                # Check if the search value (name or last 3 digits of number) can be found on HU display using regex
                search_value = extracted_number[-3:] if len(extracted_number) >= 3 else extracted_number
                found = find_word_on_device_via_regex(HU, search_value)
                time.sleep(1)

                if extracted_name != "" and found == False:
                    search_value = extracted_name
                    found = find_word_on_device_via_regex(HU, search_value)
                    time.sleep(1)

                if found == False:
                    swipe_cmd = f"shell input swipe 1700 700 2000 200"
                    stdout, stderr, rc = run_adb(swipe_cmd, HU)
                    if stderr:
                        save_to_notepad(f"[Command failed:] ({swipe_cmd}:)")
                        save_to_notepad(f"Error text: {stderr}\n")
                    save_to_notepad(f"[Executed command:] ({swipe_cmd}:)")  
                    save_to_notepad(f"Result: {stdout}\n")
                    assert rc == 0, f"Swipe command {swipe_cmd} failed: {rc}\n"
                    time.sleep(1)
                    save_to_notepad(f"Scrolled down {i+1} time(s)\n")
                else:
                    break
            
            if found:
                if extracted_name and extracted_name != "":
                    success_message = f"{mobile_name} missed calls were found successfully on HU display using contact name: {extracted_name}"
                else:
                    success_message = f"{mobile_name} missed calls were found successfully on HU display using number digits: {search_value}"
                save_to_notepad(f"{success_message}\n")
                save_to_notepad(header="TEST PASSED", color="green")
                # Save to Excel with test_name, result="Passed" and comment=success_message
                save_to_excel(test_name, "Passed", success_message)
            else:
                if extracted_name and extracted_name != "":
                    raise AssertionError(f"{mobile_name} missed calls with contact name '{extracted_name}' were not found on HU display!")
                else:
                    raise AssertionError(f"{mobile_name} missed calls with number digits '{search_value}' were not found on HU display!")

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

        # Click All button
        found = click_on_device(HU, "All")
        time.sleep(1)
        assert found == True, f"All button has not been found on HU display.\n"
        save_to_notepad(f"All button has been found and pressed on HU display.\n")

        # HU home command
        home_cmd = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(home_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({home_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({home_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {home_cmd} failed: {rc}\n"
        time.sleep(1)

        # Click Mobile device name button with regex from HU display
        found = click_on_device_regex(HU, mobile_name)
        time.sleep(1)
        assert found == True, f"Mobile device name {mobile_name} has not been found on HU display.\n"
        save_to_notepad(f"Mobile device name {mobile_name} has been found and pressed on HU display.\n")

        # Swipe up to scroll up (adjust coordinates as needed)
        swipe_cmd = f"shell input swipe 1700 700 200 2500"
        stdout, stderr, rc = run_adb(swipe_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({swipe_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({swipe_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {swipe_cmd} failed: {rc}\n"
        time.sleep(1)

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

        save_to_notepad(f"Cleanup commands executed successfully.\n")

        # Stop screen recordings
        save_to_notepad(f"Stopping screen recordings...\n")
        stop_screen_recording("HU")
        
        # Clean up recordings based on test result
        cleanup_recordings(True, test_name)
        save_to_notepad(f"Test passed - recordings deleted\n")
        
        save_to_notepad(f"=== Test {test_name} finished ===\n")
        
    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")

        # Click All button
        found = click_on_device(HU, "All")
        time.sleep(1)
        assert found == True, f"All button has not been found on HU display.\n"
        save_to_notepad(f"All button has been found and pressed on HU display.\n")

        # HU home command
        home_cmd = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(home_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({home_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({home_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {home_cmd} failed: {rc}\n"
        time.sleep(1)

        # Click Mobile device name button with regex from HU display
        found = click_on_device_regex(HU, mobile_name)
        time.sleep(1)
        assert found == True, f"Mobile device name {mobile_name} has not been found on HU display.\n"
        save_to_notepad(f"Mobile device name {mobile_name} has been found and pressed on HU display.\n")

        # Swipe up to scroll up (adjust coordinates as needed)
        swipe_cmd = f"shell input swipe 1700 700 200 2500"
        stdout, stderr, rc = run_adb(swipe_cmd, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({swipe_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({swipe_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {swipe_cmd} failed: {rc}\n"
        time.sleep(1)

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
                
        # Stop screen recordings on test failure
        save_to_notepad(f"Stopping screen recordings...\n")
        stop_screen_recording("HU")
        
        # Keep recordings since test failed
        cleanup_recordings(False, test_name)
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