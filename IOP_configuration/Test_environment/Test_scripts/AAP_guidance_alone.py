from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *
from helpers.android_mobile_menu import *
import threading
import time

test_name = "AAP_guidance_alone"

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
        save_to_notepad(f"Created Mobile device object\n")
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
                    save_to_notepad(f"Android Auto icon not found - Mobile device doesn't support Android Auto\n")
                    save_to_notepad(header="TEST SKIPPED", color="yellow")
                    save_to_excel(test_name, "Skipped", "Mobile device doesn't support Android Auto")
                    return
                save_to_notepad(f"Android Auto icon has been found and pressed!\n")
        
        # Clean up screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)
        time.sleep(3)
        
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
        
        # Click Search Button from HU display
        command = f"shell input tap 1050 125"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked Search button on Android Auto Navigation interface to search for a destination\n")
        time.sleep(3)

        # Click Android Auto navigation interface to select a destination
        command = f"shell input tap 1100 230"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked Android Auto navigation interface to select a destination\n")
        time.sleep(3)
        
        # Press Google Maps UI for turn-by-turn instructions
        command = f"shell input tap 900 230"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Google Maps UI pressed for turn-by-turn instructions\n")
        time.sleep(5)

        # Click Start Button from HU display
        command = f"shell input tap 1000 550"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Clicked Start button on Android Auto Navigation interface to start the guidance for the selected destination\n")
        time.sleep(10)
        
        # Press Google Maps UI again for navigation guidance
        command = f"shell input tap 900 175"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Google Maps UI pressed again for navigation guidance\n")
        time.sleep(1)
        
        try:  
            # Use Windows shell command with pipe to filter AudioFocus AudioManager entries directly
            command = f'adb -s {HU} logcat | findstr /I "AudioFocus AudioManager"'
            
            # Use a more aggressive approach to ensure termination
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Collect output for 10 seconds using a timeout mechanism
            output_lines = []
            start_time = time.time()
            timeout_duration = 10.0  # 10 seconds
            process_killed = False
            
            def kill_process_tree():
                nonlocal process_killed
                try:
                    if os.name == 'nt':  # Windows
                        # Kill the entire process tree to ensure all child processes are terminated
                        subprocess.run(f"taskkill /F /T /PID {process.pid}", shell=True, 
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        process.terminate()
                        time.sleep(0.1)
                        if process.poll() is None:
                            process.kill()
                    process_killed = True
                except:
                    pass
            
            # Start a timer to kill the process after timeout
            timer = threading.Timer(timeout_duration, kill_process_tree)
            timer.start()
            
            # Read output with timeout
            try:
                while time.time() - start_time < timeout_duration and not process_killed:
                    try:
                        # Use a shorter timeout for readline to check more frequently
                        line = process.stdout.readline()
                        if line:
                            output_lines.append(line.strip())
                        elif process.poll() is not None:
                            # Process has terminated naturally
                            break
                        else:
                            # Small sleep to prevent busy waiting
                            time.sleep(0.01)
                    except:
                        break
            except:
                pass
            
            # Cancel the timer if process finished early
            timer.cancel()
            
            # Ensure process is definitely killed
            if not process_killed:
                kill_process_tree()
            
            # Wait a moment for cleanup
            time.sleep(0.2)
            
            # Try to get any remaining output/errors without blocking
            stderr = ""
            try:
                # Don't wait for communicate if process was forcibly killed
                if process.poll() is not None:
                    _, stderr = process.communicate(timeout=0.1)
                else:
                    stderr = "Process forcibly terminated after timeout"
            except:
                stderr = "Process terminated after timeout"
            
            stdout = "\n".join(output_lines)
            
            save_to_notepad(f'[Executed command with 10s timeout:] (adb -s {HU} logcat | findstr /I "AudioFocus AudioManager")')
            save_to_notepad(f"Result: {stdout}\n")
            
            if stderr and "terminated after timeout" not in stderr and "forcibly terminated" not in stderr:
                save_to_notepad(f"[Command had errors:] (logcat command)")
                save_to_notepad(f"Error text: {stderr}\n")

            if not stdout:
                stdout = ""
            
        except Exception as e:
            save_to_notepad(f"Error in audio focus: {e}\n")
            # Make sure to kill any lingering processes
            try:
                if os.name == 'nt':
                    subprocess.run("taskkill /F /IM adb.exe", shell=True, 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass

        # Check if audio focus is set to guidance
        if "Audio session started, type: GUIDANCE" in stdout:
            save_to_notepad(f"Audio focus was set on Guidance successfully: {stdout}\n")
            audio_focus_started = True 
        else:
            save_to_notepad(f"Audio focus set failed: {stdout}\n")
            audio_focus_started = False 

        # Check test result
        if audio_focus_started == True:
            success_message = f"AAP navigation audio functionality works correctly - test Passed."
            save_to_notepad(f"{success_message}\n")
            save_to_notepad(header="TEST PASSED", color="green")
            save_to_excel(test_name, "Passed", success_message)
            test_passed = True
        else:
            assert False, f"AAP navigation audio functionality failed - test Failed"
        
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
        
        # Press Google Maps UI again for closing navigation guidance
        command = f"shell input tap 850 1100"
        stdout, stderr, rc = run_adb(command, HU)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"
        save_to_notepad(f"Google Maps UI pressed for closing navigation guidance\n")
        time.sleep(1)

        # Go to HU home screen
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
        assert found, f"Manage devices button not found on display.\n"
        save_to_notepad(f"Manage devices button clicked successfully\n")
        time.sleep(2)
        
        # Click Smartphones Button from HU display
        found = click_on_device(HU, "Smartphones")
        assert found, f"Smartphones button not found on display.\n"
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
                assert x != 0 and y != 0, f"Android Auto disconnect icon has not been found on display.\n"
                save_to_notepad(f"Android Auto disconnect icon has been found and pressed!\n")
        
        # Clean up screenshot
        screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
        cmd = f'del "{screenshot_path}"'
        stdout, stderr, rc = run_cmd(cmd)
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
        
        # Clean up HU screenshots
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
        save_to_notepad(f"Mobile device returned to home menu\n")
        
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
        
        try:
            # Cleanup commands on failure
            command = f"shell input keyevent 3"
            stdout, stderr, rc = run_adb(command, HU)
            
            command = f"shell rm /sdcard/*.png"
            stdout, stderr, rc = run_adb(command, HU)
            
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