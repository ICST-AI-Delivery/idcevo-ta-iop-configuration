from adb_command import *
from USB_Matrix import *
from display_info import *
from save_to_notepad import *
import time

def main():
    path = "D:/traget/IDCevo/IOP_configuration/Test_environment/Test_scripts"

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
            save_to_notepad(f"[Command failed:] (adb -s {Mobile1} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] (adb -s {Mobile1} {command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        assert rc == 0, f"Command adb -s {Mobile1} {command} failed: {rc}\n"

        mobile_name = stdout 
        save_to_notepad(f"Tested device name: {mobile_name}\n")
        time.sleep(1)

        command = f"shell input keyevent 224"     # Mobile turn screen on
        stdout, stderr, rc = run_adb(command, Mobile1)
        save_to_notepad(f"[Executed command:] (adb -s {Mobile1} {command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {Mobile1} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        assert rc == 0, f"Command failed: {rc}\n"  

        command = f"shell wm dismiss-keyguard"     # Mobile unlock screen command
        stdout, stderr, rc = run_adb(command, Mobile1)
        save_to_notepad(f"[Executed command:] (adb -s {Mobile1} {command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {Mobile1} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        assert rc == 0, f"Command failed: {rc}\n" 

        command = f"shell am start -a android.settings.SETTINGS"     # Mobile Settings command
        stdout, stderr, rc = run_adb(command, Mobile1)
        save_to_notepad(f"[Executed command:] (adb -s {Mobile1} {command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {Mobile1} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        assert rc == 0, f"Command failed: {rc}\n" 

        command = f"shell am start -a android.settings.APPLICATION_DEVELOPMENT_SETTINGS"     # Mobile Developer Options command
        stdout, stderr, rc = run_adb(command, Mobile1)
        save_to_notepad(f"[Executed command:] (adb -s {Mobile1} {command}:)")  
        save_to_notepad(f"Result: {stdout}\n") 
        # Console display 
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {Mobile1} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        assert rc == 0, f"Command failed: {rc}\n" 

        # Click Bug report Button from Mobile1 display
        found = click_on_device_with_verification(Mobile1, "Bug report")
        time.sleep(1)

        # Click Bug report Button from Mobile1 display
        if found == False:
            found = click_on_device_regex(Mobile1, "bug")
            time.sleep(1)

        # Commands to be executed
        menu_commands = [
            f"shell screencap -p /sdcard/screenshot.png", # Mobile1 command to take screenshot
            f"pull /sdcard/screenshot.png {path}", # Mobile1 command to save screenshot on PC
            f"shell input tap 0 0" # Mobile1 command go download Full report
        ]
        for cmd in menu_commands[0:4]:
            x = 0
            y = 0
            if cmd == menu_commands[2]:
                x, y = find_word_on_device_via_regex_with_coordinates(Mobile1,"Full report")
                if x != 0 and y != 0:
                    cmd = f"shell input tap {x-40} {y+15}"

            stdout, stderr, rc = run_adb(cmd, Mobile1)

            # Console display 
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n") 
        time.sleep(2)

        # Clean up the screenshot
        cmd = r"del D:\traget\IDCevo\IOP_configuration\Test_environment\Test_scripts\screenshot.png"
        stdout, stderr, rc = run_cmd(cmd)

        # Click Report Button from Mobile1 display
        found = click_action_keywords(Mobile1,primary_keywords=["Report", "REPORT"])
        time.sleep(1)

        # Wait for the report to download
        time.sleep(300)

        # Mobile Device back command
        back_cmd = f"shell input keyevent 4"
        stdout, stderr, rc = run_adb(back_cmd, Mobile1)
        if stderr:
            save_to_notepad(f"[Command failed:] ({back_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({back_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {back_cmd} failed: {rc}\n"
        time.sleep(1)

        # Mobile Device back command
        home_cmd = f"shell input keyevent 3"
        stdout, stderr, rc = run_adb(home_cmd, Mobile1)
        if stderr:
            save_to_notepad(f"[Command failed:] ({home_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({home_cmd}:)")  
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Swipe command {home_cmd} failed: {rc}\n"
        time.sleep(1)

        # Run Download Bug report commands
        download_bug_report_commands = [
            f"for /f %f in ('adb -s {Mobile1} shell \"ls /bugreports/*.zip\"') do adb -s {Mobile1} pull %f",   # Mobile1 pull bugreports
            f"adb -s {Mobile1} shell rm /bugreports/*.zip",    # Mobile1 cleanup bugreports
            f"move bugreport* D:/traget/IDCevo/IOP_configuration/Test_results"
        ]
        
        for cmd in download_bug_report_commands:
            stdout, stderr, rc = run_cmd(cmd)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
        
        save_to_notepad(f"Download Bug report commands executed successfully.\n")
        time.sleep(2)

        # Run ADB root commands
        ADB_root_command = [
            f"root"    # HU adb root
        ]
        
        for cmd in ADB_root_command:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
        
        save_to_notepad(f"ADB root command executed successfully.\n")
        time.sleep(10)

        HU, Mobile1 = get_serial_number()

        # Run Download Btsnoop commands
        download_btsnoop_commands = [
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log",    # HU pull btsnoop1
            f"pull /data/misc/bluetooth/logs/btsnoop_hci.log.last"    # HU pull btsnoop2
        ]
        
        for cmd in download_btsnoop_commands:
            stdout, stderr, rc = run_adb(cmd, HU)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Download BTsnoop command {cmd} failed: {rc}\n"

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
        
        save_to_notepad(f"Download Btsnoop commands executed successfully.\n")
        time.sleep(2)

        # Run cleanup commands after test is done
        cleanup_commands = [
            f"shell input keyevent 3",   # Mobile home
            f"shell rm /sdcard/*.png"   # Mobile cleanup
        ]
        
        for cmd in cleanup_commands:
            stdout, stderr, rc = run_adb(cmd, Mobile1)
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Cleanup command {cmd} failed: {rc}\n"
        
        save_to_notepad(f"Cleanup commands executed successfully.\n")

    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(stderr=error_message)
        
        # Run cleanup commands even on failure
        try:
            # Run cleanup commands after test is done
            cleanup_commands = [
                f"shell input keyevent 3",   # Mobile home
                f"shell rm /sdcard/*.png"   # Mobile cleanup
            ]
            
            for cmd in cleanup_commands:
                stdout, stderr, rc = run_adb(cmd, Mobile1)
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cmd}:)")  
                save_to_notepad(f"Result: {stdout}\n")
                assert rc == 0, f"Cleanup command {cmd} failed: {rc}\n"
            
            save_to_notepad(f"Cleanup commands executed successfully.\n")
        except Exception as cleanup_error:
            save_to_notepad(f"Error during cleanup: {cleanup_error}\n")
        
        raise

if __name__ == "__main__":
    main()