from helpers.adb_command import *
from helpers.USB_Matrix import *
from helpers.display_info import *
from helpers.save_to_notepad import *

test_name = "OS_version"

def main():
    save_to_notepad(f"=== Test {test_name} started ===\n")
    
    try:
        # Extracting serial numbers for HU and Mobile1
        HU, Mobile1 = get_serial_number()
        adb_command = f"adb -s {HU}" + r' shell getprop ro.build.version.release'

        # Commands to be executed
        commands = [
            r'dir D:\ /s /b | findstr /r "[0-9][0-9]w[0-9]*\.[0-9]*-[0-9].*images.*idcevo-hv.*Flashbins.*IDCEvo-Artifacts.*tools.*fastboot$"',
            adb_command
        ]

        for cmd in commands:
            stdout, stderr, rc = run_cmd(cmd)

            if cmd == commands[0]:
                stdout = stdout.split("\n")[0]

            # Console display 
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")  
            save_to_notepad(f"Result: {stdout}\n")

            assert rc == 0, f"Command {cmd} failed: {rc}\n" 
            
            if cmd == commands[1]:
                # If adb command returns Android version the test is passed, else test is failed
                assert stdout and len(stdout.strip()) > 0, "OS version not found or empty!"
                success_message = f"OS version successfully retrieved: {stdout}"
                save_to_notepad(f"{success_message}\n")
                save_to_notepad(header="TEST PASSED", color="green")
                # Save to Excel with test_name, result="Passed" and comment=success_message
                save_to_excel(test_name, "Passed", success_message)

        save_to_notepad(f"=== Test {test_name} finished ===\n")
        
    except AssertionError as e:
        error_message = str(e)
        save_to_notepad(header="TEST FAILED", stderr=error_message, color="red")
        save_to_notepad(f"=== Test {test_name} finished ===\n")
        # Save to Excel with test_name, result="Failed" and comment=error_message
        save_to_excel(test_name, "Failed", error_message)
        raise

if __name__ == "__main__":
    main()