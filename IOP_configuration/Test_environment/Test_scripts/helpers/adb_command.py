import subprocess

def run_adb(command, device_id=None):
    # If device_id is provided, prepend it to the command
    if device_id:
        full_command = f"adb -s {device_id} {command}"
    else:
        full_command = f"adb {command}"

    # Run ADB command
    try:
        result = subprocess.run(
            full_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        return stdout, stderr, result.returncode
    except Exception as e:
        return "", f"Error: {e}", -1
    
def run_cmd(command):

    # Run ADB command
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        return stdout, stderr, result.returncode
    except Exception as e:
        return "", f"Error: {e}", -1
