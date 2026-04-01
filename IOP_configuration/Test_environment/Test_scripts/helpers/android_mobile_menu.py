import time
import datetime
from .adb_command import *
from .USB_Matrix import *
from .display_info import *
from .save_to_notepad import *

# =====================================================
# DEVICE CLASS
# =====================================================
class AndroidDevice:
   def __init__(self, device_id, mobile_name):
       self.device_id = device_id
       self.mobile_name = mobile_name

   # =================================================
   # UNIVERSAL FUNCTIONS CALLED FROM TESTS
   # =================================================
   def conference_call(self):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("conference_call")
       if func:
           func(self.device_id)
       else:
           self.conference_call_command()

   def enable_bluetooth(self):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("enable_bluetooth")
       if func:
           func(self.device_id)
       else:
           self.run_enable_bluetooth_command()

   def disable_bluetooth(self):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("disable_bluetooth")
       if func:
           func(self.device_id)
       else:
           self.run_disable_bluetooth_command()

   def get_received_calls(self):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("get_received_calls")
       if func:
           return func(self.device_id)
       else:
           return self.get_received_calls_command()

   def get_dialed_calls(self):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("get_dialed_calls")
       if func:
           return func(self.device_id)
       else:
           return self.get_dialed_calls_command()

   def get_missed_calls(self):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("get_missed_calls")
       if func:
           return func(self.device_id)
       else:
           return self.get_missed_calls_command()

   def get_combined_calls(self):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("get_combined_calls")
       if func:
           return func(self.device_id)
       else:
           return self.get_combined_calls_command()

   def get_call_history_with_timestamps(self):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("get_call_history_with_timestamps")
       if func:
           return func(self.device_id)
       else:
           return self.get_call_history_with_timestamps_command()

   def transfer_audio_to_mobile(self, bluetooth_HU_name):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("transfer_audio_to_mobile")
       if func:
           return func(self.device_id, bluetooth_HU_name)
       else:
           return self.transfer_audio_to_mobile_command(bluetooth_HU_name)

   def transfer_audio_to_HU(self, bluetooth_HU_name):
       func = DEVICE_MENU.get(
           self.mobile_name,
           {}
       ).get("transfer_audio_to_HU")
       if func:
           return func(self.device_id, bluetooth_HU_name)
       else:
           return self.transfer_audio_to_HU_command(bluetooth_HU_name)

   # =================================================
   # DEFAULT ANDROID IMPLEMENTATION
   # =================================================

   def run_remove_screenshot_command(self):
        # Run starting commands on Mobile device
        command = f"shell rm /sdcard/*.png"     # Mobile remove screenshot
        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def run_home_command(self):
        # Run starting commands on Mobile device
        command = f"shell input keyevent 3"     # Mobile home screen
        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def click_close_button_popup(self):
        found = click_action_keywords(self.device_id,primary_keywords=["Close", "Cancel", "Not now", "Later"])
        if found == True:
            save_to_notepad(f"Clicked Close button pop up completed via keywords\n")
        else:
            save_to_notepad(f"Clicked Close button pop up not completed via keywords\n")

   def conference_call_command(self):
        found = click_on_device_regex(self.device_id,"Merge")
        if found == True:
            save_to_notepad(f"Clicked Merge button completed via keywords\n")
        else:
            save_to_notepad(f"Clicked Merge button not completed via keywords\n")

   def run_turn_screen_on_command(self):
        # Run starting commands on Mobile device
        command = f"shell input keyevent 224"     # Mobile turn screen on
        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def run_unlock_screen_command(self):
        # Run starting commands on Mobile device
        command = f"shell wm dismiss-keyguard"     # Mobile unlock screen command

        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def run_settings_menu_command(self):
        # Run starting commands on Mobile device
        command = f"shell am start -a android.settings.SETTINGS"     # Mobile Settings command

        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def run_bluetooth_menu_command(self):
        # Run starting commands on Mobile device
        command = f"shell am start -a android.settings.BLUETOOTH_SETTINGS"     # Mobile Bluetooth command

        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def run_enable_bluetooth_command(self):
        # Run starting commands on Mobile device
        command = f"shell svc bluetooth enable"     # Mobile Bluetooth command

        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")

        found = click_on_device_regex(self.device_id,"Pair new device")
        if found == True:
            save_to_notepad(f"Pair new device button clicked successfully\n")
        else:
            save_to_notepad(f"Pair new device button could not be clicked\n")

   def click_HU_bluetooth_name_button(self, bluetooth_HU_name):
        found = click_on_device_regex(self.device_id,bluetooth_HU_name)
        return found

   def click_pair_with_HU_button(self):
        found = toggle_switch_widget(self.device_id, enable=True)
        if found == True:
            save_to_notepad(f"Toggle switch Pair enabled successfully\n")
        else:
            save_to_notepad(f"Toggle switch Pair could not be enabled\n")
        time.sleep(1)

        found = click_action_keywords(self.device_id,primary_keywords=["Pair", "PAIR", "Authorize"])
        return found

   def click_allow_button_popup(self):
        found = click_action_keywords(self.device_id, primary_keywords=["Allow", "Authorize", "YES", "OK"])
        if found == True:
            save_to_notepad(f"Clicked Allow button pop up completed via keywords\n")
        else:
            save_to_notepad(f"Clicked Allow button pop up not completed via keywords\n")

        time.sleep(2)
        found = click_action_keywords(self.device_id, primary_keywords=["Allow", "Authorize", "YES", "OK"])
        if found == True:
            save_to_notepad(f"Clicked Allow button pop up completed via keywords\n")
        else:
            save_to_notepad(f"Clicked Allow button pop up not completed via keywords\n")

   def click_settings_icon(self):
        found = click_action_keywords(self.device_id, primary_keywords=["Allow", "Authorize", "YES", "OK"])
        if found == True:
            save_to_notepad(f"Clicked Allow button pop up completed via keywords\n")
        else:
            save_to_notepad(f"Clicked Allow button pop up not completed via keywords\n")

        time.sleep(2)

        found = click_on_icon(self.device_id,
                                desc_keywords=["Device Settings", "details", "more"],
                                resource_ids=["com.android.settings:id/settings_button","com.samsung.android.settings:id/settings_button"]
                            )
        if found == True:
            save_to_notepad(f"Settings Icon clicked via keywords\n")
        else:
            save_to_notepad(f"Settings Icon not clicked via keywords\n")

   def activate_shuffle_mode_command(self):
        # Run adb command to get son title on Mobile device
        song_title_command = f"shell dumpsys media_session | findstr description="
        stdout, stderr, rc = run_adb(song_title_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({song_title_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({song_title_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        
        # Extract the song title from the metadata
        # Format: metadata: size=7, description=Beautiful Pain (feat. Sia), Eminem, Eminem
        if stdout and "description=" in stdout:
            # Find the description part
            desc_start = stdout.find("description=") + len("description=")
            desc_end = stdout.find(",", desc_start)
            if desc_end == -1:
                desc_end = len(stdout)
            
            # Extract the full song title
            song_title = stdout[desc_start:desc_end].strip()
            save_to_notepad(f"Extracted song title: '{song_title}'\n")
            
            # Extract the first word from the title
            if song_title:
                first_word = song_title.split()[0]
                save_to_notepad(f"First word of song title: '{first_word}'\n")
                time.sleep(3)

        found = click_on_device_regex(self.device_id, first_word)
        if found == True:
            save_to_notepad(f"Song Title clicked via regex\n")
        else:
            save_to_notepad(f"Song Title not clicked via regex\n")
        time.sleep(2)

        found = click_on_icon(self.device_id,
                                desc_keywords=["Shuffle on"],
                                resource_ids=["com.google.android.apps.youtube.music:id/queue_shuffle_button"]
                            )
        if found == True:
            save_to_notepad(f"Shuffle Icon clicked via keywords\n")
        else:
            save_to_notepad(f"Shuffle Icon not clicked via keywords\n")
        return found
   
   def deactivate_shuffle_mode_command(self):
        found = click_on_icon(self.device_id,
                                desc_keywords=["Shuffle on"],
                                resource_ids=["com.google.android.apps.youtube.music:id/queue_shuffle_button"]
                            )
        if found == True:
            save_to_notepad(f"Shuffle Icon clicked via keywords\n")
        else:
            save_to_notepad(f"Shuffle Icon not clicked via keywords\n")
        time.sleep(2)

        # Run back command on Mobile device
        command = f"shell input keyevent 4"     # Mobile back
        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")


   def click_unpair_button(self):
        found = click_action_keywords(self.device_id,primary_keywords=["forget", "unpair"],confirm_keywords=["forget device", "unpair","remove device"])
        if found == True:
            save_to_notepad(f"Clicked Unpair button completed via keywords\n")
        else:
            save_to_notepad(f"Clicked Unpair button not completed via keywords\n")
        time.sleep(2)

        found = click_action_keywords_fixed(self.device_id,primary_keywords=["forget", "unpair"],confirm_keywords=["forget device", "unpair","remove device"])
        if found == True:
            save_to_notepad(f"Clicked Unpair button completed via fixed keywords\n")
        else:
            save_to_notepad(f"Clicked Unpair button not completed via fixed keywords\n")

   def run_disable_bluetooth_command(self):
        # Run starting commands on Mobile device
        command = f"shell svc bluetooth disable"     # Mobile Bluetooth command

        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def click_OK_button(self):
        found = click_on_device(self.device_id, "OK")
        if found == True:
            save_to_notepad(f"Clicked OK button completed\n")
        else:
            save_to_notepad(f"Clicked OK button not completed\n")

   def click_Cancel_button(self):
        found = click_action_keywords(self.device_id,primary_keywords=["Cancel", "DON'T ALLOW"])
        return found

   def run_reboot_command(self):
        # Run starting commands on Mobile device
        command = f"reboot"     # Mobile reboot command

        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def run_developer_options_menu_command(self):
        # Run starting commands on Mobile device
        command = f"shell am start -a android.settings.APPLICATION_DEVELOPMENT_SETTINGS"     # Mobile Developer Options command

        stdout, stderr, rc = run_adb(command, self.device_id)
        save_to_notepad(f"[Executed command:] (adb -s {self.device_id} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {self.device_id} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        return rc

   def run_linkloss_command(self):
        # Run adb command on Mobile device: adb shell am force-stop com.android.bluetooth. Wait 5 seconds with bluetooth module disabled
        disable_command = f"shell am force-stop com.android.bluetooth"
        stdout, stderr, rc = run_adb(disable_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({disable_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({disable_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return rc

   def check_SIM_command(self):
        sim_check_command = f"shell getprop gsm.sim.state"
        stdout, stderr, rc = run_adb(sim_check_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
        save_to_notepad(f"SIM state result: {stdout}\n")
        return stdout.strip()

   def get_phone_number_command(self):
        phone_number_mobile = extract_phone_number_from_adb(f"adb -s {self.device_id} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile}")
        if phone_number_mobile == None:
            phone_number_mobile = extract_phone_number_from_adb(f"adb -s {self.device_id} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile}")
        return phone_number_mobile

   def dial_command(self, phone_number_mobile1):
        # Run adb command to start dialer with specific phone number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:+{phone_number_mobile1}"
        stdout, stderr, rc = run_adb(dial_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({dial_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({dial_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return rc

   def answer_call_command(self):
        # Run adb command to answer call (keyevent 5 is CALL button)
        call_command = f"shell input keyevent 5"
        stdout, stderr, rc = run_adb(call_command,self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({call_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({call_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return rc

   def end_call_command(self):
        # Run adb command to end call (keyevent 6)
        call_command = f"shell input keyevent 6"
        stdout, stderr, rc = run_adb(call_command,self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({call_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({call_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return rc

   def play_audio_command(self):
        # Run Audio play commands on Mobile device
        audio_play_commands = [
            f"shell monkey -p com.google.android.apps.youtube.music -c android.intent.category.LAUNCHER 1",     # Mobile open YT Music
            f"shell monkey -p com.gbox.com.google.android.apps.youtube.music -c android.intent.category.LAUNCHER 1",     # Mobile open YT Music
            f"shell input keyevent 85"      # Mobile play audio command
        ]

        for cmd in audio_play_commands:
            stdout, stderr, rc = run_adb(cmd,self.device_id)

            # Console display
            if stderr:
                save_to_notepad(f"[Command failed:] ({cmd}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({cmd}:)")
            save_to_notepad(f"Result: {stdout}\n")
            time.sleep(5)

   def pause_audio_command(self):
        # Run adb command to pause audio on Mobile device
        audio_pause_command = f"shell input keyevent 85"
        stdout, stderr, rc = run_adb(audio_pause_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({audio_pause_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({audio_pause_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        time.sleep(3)
        return rc
   
   def skip_forward_audio_command(self):
        # Run adb command to skip to next song on Mobile device
        skip_forward_command = f"shell input keyevent 87"
        stdout, stderr, rc = run_adb(skip_forward_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({skip_forward_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({skip_forward_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        time.sleep(3)
        return rc
   
   def skip_backward_audio_command(self):
        # Run adb command to skip to previous song on Mobile device
        skip_backward_command = f"shell input keyevent 88"
        stdout, stderr, rc = run_adb(skip_backward_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({skip_backward_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({skip_backward_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        time.sleep(3)
        return rc
   
   def fast_forward_command(self):
        for _ in range(20):
            # Run adb command to fast-forward song on Mobile device
            fast_forward_command = f"shell cmd media_session dispatch fast-forward"
            stdout, stderr, rc = run_adb(fast_forward_command, self.device_id)
            if stderr:
                save_to_notepad(f"[Command failed:] ({fast_forward_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({fast_forward_command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            time.sleep(0.03)
        return rc
   
   def fast_rewind_command(self):
        for _ in range(20):
            # Run adb command to rewind song on Mobile device
            rewind_command = f"shell cmd media_session dispatch rewind"
            stdout, stderr, rc = run_adb(rewind_command, self.device_id)
            if stderr:
                save_to_notepad(f"[Command failed:] ({rewind_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({rewind_command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            time.sleep(0.03)
        return rc
   
   def song_title_command(self):
        # Run adb command to get son title on Mobile device
        song_title_command = f"shell dumpsys media_session | findstr description="
        stdout, stderr, rc = run_adb(song_title_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({song_title_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({song_title_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        
        # Extract the song title from the metadata
        # Format: metadata: size=7, description=Beautiful Pain (feat. Sia), Eminem, Eminem
        if stdout and "description=" in stdout:
            try:
                # Find the description part
                desc_start = stdout.find("description=") + len("description=")
                desc_end = stdout.find(",", desc_start)
                if desc_end == -1:
                    desc_end = len(stdout)
                
                # Extract the full song title
                song_title = stdout[desc_start:desc_end].strip()
                save_to_notepad(f"Extracted song title: '{song_title}'\n")
                
                # Extract the first word from the title
                if song_title:
                    first_word = song_title.split()[0]
                    save_to_notepad(f"First word of song title: '{first_word}'\n")
                    time.sleep(3)
                    return first_word
                else:
                    save_to_notepad(f"Warning: Could not extract song title from stdout\n")
                    time.sleep(3)
                    return ""
            except Exception as e:
                save_to_notepad(f"Error extracting song title: {e}\n")
                time.sleep(3)
                return ""
        else:
            save_to_notepad(f"Warning: No description found in stdout\n")
            time.sleep(3)
            return ""
        
   def artist_name_command(self):
        # Run adb command to get artist name on Mobile device
        artist_name_command = f"shell dumpsys media_session | findstr description="
        stdout, stderr, rc = run_adb(artist_name_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({artist_name_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({artist_name_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        
        # Extract the artist name from the metadata
        # Format: metadata: size=7, description=Beautiful Pain (feat. Sia), Eminem, Eminem
        # Artist name is after the first comma following the song title
        if stdout and "description=" in stdout:
            try:
                # Find the description part
                desc_start = stdout.find("description=") + len("description=")
                desc_end = stdout.find(",", desc_start)
                if desc_end == -1:
                    save_to_notepad(f"Warning: Could not find comma after song title\n")
                    time.sleep(3)
                    return ""
                
                # Find the artist name (after the first comma)
                artist_start = desc_end + 1
                artist_end = stdout.find(",", artist_start)
                if artist_end == -1:
                    artist_end = len(stdout)
                
                # Extract the full artist name
                artist_name = stdout[artist_start:artist_end].strip()
                save_to_notepad(f"Extracted artist name: '{artist_name}'\n")
                
                # Extract the first word from the artist name
                if artist_name:
                    first_word = artist_name.split()[0]
                    save_to_notepad(f"First word of artist name: '{first_word}'\n")
                    time.sleep(3)
                    return first_word
                else:
                    save_to_notepad(f"Warning: Could not extract artist name from stdout\n")
                    time.sleep(3)
                    return ""
            except Exception as e:
                save_to_notepad(f"Error extracting artist name: {e}\n")
                time.sleep(3)
                return ""
        else:
            save_to_notepad(f"Warning: No description found in stdout\n")
            time.sleep(3)
            return ""
        
   def album_name_command(self):
        # Run adb command to get album name on Mobile device
        album_name_command = f"shell dumpsys media_session | findstr description="
        stdout, stderr, rc = run_adb(album_name_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({album_name_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({album_name_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        
        # Extract the album name from the metadata
        # Format: metadata: size=7, description=Beautiful Pain (feat. Sia), Eminem, Eminem
        # Album name is after the second comma following the song title (second value)
        if stdout and "description=" in stdout:
            try:
                # Find the description part
                desc_start = stdout.find("description=") + len("description=")
                desc_end = stdout.find(",", desc_start)
                if desc_end == -1:
                    save_to_notepad(f"Warning: Could not find comma after song title\n")
                    time.sleep(3)
                    return ""
                
                # Find the first comma after the description
                first_comma = desc_end
                second_comma_start = first_comma + 1
                second_comma = stdout.find(",", second_comma_start)
                if second_comma == -1:
                    save_to_notepad(f"Warning: Could not find second comma after song title\n")
                    time.sleep(3)
                    return ""
                
                # Find the album name (after the second comma)
                album_start = second_comma + 1
                album_end = stdout.find(",", album_start)
                if album_end == -1:
                    album_end = len(stdout)
                
                # Extract the full album name
                album_name = stdout[album_start:album_end].strip()
                save_to_notepad(f"Extracted album name: '{album_name}'\n")
                
                # Extract the first word from the album name
                if album_name:
                    first_word = album_name.split()[0]
                    save_to_notepad(f"First word of album name: '{first_word}'\n")
                    time.sleep(3)
                    return first_word
                else:
                    save_to_notepad(f"Warning: Could not extract album name from stdout\n")
                    time.sleep(3)
                    return ""
            except Exception as e:
                save_to_notepad(f"Error extracting album name: {e}\n")
                time.sleep(3)
                return ""
        else:
            save_to_notepad(f"Warning: No description found in stdout\n")
            time.sleep(3)
            return ""
        
   def cover_art_command(self):
        # Run adb command to get logcat COVERART entries with a 1-second timeout
        import os
        import threading
        
        try:  
            # Use a different approach that avoids shell pipes on Windows
            # Start logcat process without pipe to avoid termination issues
            process = subprocess.Popen(
                ["adb", "-s", self.device_id, "logcat"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Collect output for 1 second using a timeout mechanism
            output_lines = []
            start_time = time.time()
            timeout_duration = 10.0  # 10 seconds
            
            def read_output():
                try:
                    for line in iter(process.stdout.readline, ''):
                        if time.time() - start_time >= timeout_duration:
                            break
                        if "COVERART" in line.upper():
                            output_lines.append(line.strip())
                except:
                    pass
            
            # Start reading in a separate thread
            reader_thread = threading.Thread(target=read_output)
            reader_thread.daemon = True
            reader_thread.start()
            
            # Wait for the timeout duration
            time.sleep(timeout_duration)
            
            # Force terminate the process using different methods
            try:
                if os.name == 'nt':  # Windows
                    # Use taskkill to force terminate on Windows
                    subprocess.run(f"taskkill /F /PID {process.pid}", shell=True, 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    process.terminate()
                
                # Give a moment for termination
                time.sleep(0.1)
                
                # If still running, kill it
                if process.poll() is None:
                    process.kill()
                    
            except:
                # Fallback - just kill it
                try:
                    process.kill()
                except:
                    pass
            
            # Wait for reader thread to finish (with timeout)
            reader_thread.join(timeout=0.5)
            
            # Get any remaining stderr
            stderr = ""
            try:
                _, stderr = process.communicate(timeout=0.5)
            except:
                stderr = "Process terminated after timeout"
            
            stdout = "\n".join(output_lines)
            
            save_to_notepad(f"[Executed command with 1s timeout:] (adb -s {self.device_id} logcat | filter for COVERART)")
            save_to_notepad(f"Result: {stdout}\n")
            
            if stderr and "terminated after timeout" not in stderr:
                save_to_notepad(f"[Command had errors:] (logcat command)")
                save_to_notepad(f"Error text: {stderr}\n")

            return stdout if stdout else ""
            
        except Exception as e:
            save_to_notepad(f"Error in cover_art_command: {e}\n")
            return ""

   def get_contacts_name_and_photo_id_command(self):
        # Run adb command to query contacts on mobile device
        query_command = f'shell content query --uri content://com.android.contacts/contacts --projection _id:display_name:photo_id'
        stdout, stderr, rc = run_adb(query_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({query_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({query_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def get_contacts_data2_command(self):
        # Query contact data2 (display names) to check if contact_with_special_chars exists
        data2_query_command = f"shell content query --uri content://com.android.contacts/data --projection data2 --where mimetype=\\'vnd.android.cursor.item/name\\'"
        stdout, stderr, rc = run_adb(data2_query_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({data2_query_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({data2_query_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def get_contacts_data3_command(self):
        # Query data3 (last names) to extract the last name
        data3_query_command = f"shell content query --uri content://com.android.contacts/data --projection data3 --where mimetype=\\'vnd.android.cursor.item/name\\'"
        stdout, stderr, rc = run_adb(data3_query_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({data3_query_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({data3_query_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def check_contacts_photo_data_command(self, contact_id):
        # Run adb command to check for photo data using the extracted contact ID
        photo_query_command = f'shell "content query --uri content://com.android.contacts/data --where \\"contact_id={contact_id} AND mimetype=\'vnd.android.cursor.item/photo\'\\" --projection contact_id:data15"'
        stdout, stderr, rc = run_adb(photo_query_command,self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({photo_query_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({photo_query_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def get_contacts_name_command(self):
        # Run adb command to query all contacts on mobile device
        query_command = f'shell content query --uri content://com.android.contacts/contacts --projection _id:display_name'
        stdout, stderr, rc = run_adb(query_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({query_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({query_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def get_contacts_name_with_postal_address_command(self):
        # Run the command to get contacts with postal addresses
        postal_cmd = f'shell "content query --uri content://com.android.contacts/data --projection display_name:data1:mimetype --where \\"mimetype=\'vnd.android.cursor.item/postal-address_v2\'\\"'
        stdout, stderr, rc = run_adb(postal_cmd, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({postal_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({postal_cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def get_contacts_name_from_SIM_command(self):
        # Run the command to get all contacts from SIM card on mobile device
        sim_contacts_cmd = f'shell "content query --uri content://icc/adn"'
        stdout, stderr, rc = run_adb(sim_contacts_cmd, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({sim_contacts_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({sim_contacts_cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def get_received_calls_command(self):
        # Run the command to get received calls from mobile device (type=1 means incoming calls)
        calls_cmd = f'shell content query --uri content://call_log/calls --projection number:date:duration:type:name | findstr /I "type=1"'
        stdout, stderr, rc = run_adb(calls_cmd, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({calls_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({calls_cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

        # Extract the first received call number and name from the result
        extracted_number = None
        extracted_name = None
        lines = stdout.strip().split('\n')
        if lines and lines[0].strip():  # Check if we have at least one line with content
            first_line = lines[0].strip()
            save_to_notepad(f"First received call record: {first_line}\n")

            # Extract name from the first row (format: number=..., date=..., duration=..., type=1, name=...)
            name_match = re.search(r"name=([^,]*)", first_line)
            if name_match:
                extracted_name = name_match.group(1).strip()
                save_to_notepad(f"Extracted full name: '{extracted_name}'\n")

                # Extract only the last name if the name contains multiple words
                if extracted_name and extracted_name != "":
                    name_parts = extracted_name.split()
                    if len(name_parts) > 1:
                        last_name = name_parts[-1]  # Get the last word as the last name
                        save_to_notepad(f"Extracted last name: '{last_name}'\n")
                        extracted_name = last_name  # Use only the last name
                    else:
                        save_to_notepad(f"Single name found, using as is: '{extracted_name}'\n")

            # Extract number from the first row
            number_match = re.search(r"number=([^,]+)", first_line)
            if number_match:
                full_number = number_match.group(1).strip()
                save_to_notepad(f"Extracted full number: {full_number}\n")

                # Check if name field is empty or not
                if not extracted_name or extracted_name == "":
                    # Name is empty - use last 3 digits of number
                    if len(full_number) >= 3:
                        extracted_number = full_number[-3:] if len(full_number) >= 3 else full_number
                        save_to_notepad(f"Name field is empty, using last 3 digits for search: {extracted_number}\n")
                    else:
                        extracted_number = full_number
                        save_to_notepad(f"Name field is empty, number has fewer than last 3, using full number: {extracted_number}\n")
                else:
                    # Name is not empty - use the last name for validation
                    save_to_notepad(f"Name field is not empty, using last name for search: {extracted_name}\n")
            else:
                save_to_notepad(f"Warning: Could not extract number from first call record\n")
        else:
            save_to_notepad(f"Warning: No received calls found in call log\n")

        if extracted_name == "":
            extracted_name = "dummy_name"

        return full_number, extracted_name

   def get_dialed_calls_command(self):
        # Run the command to get dialed calls from mobile device (type=1 means incoming calls)
        calls_cmd = f'shell content query --uri content://call_log/calls --projection number:date:duration:type:name | findstr /I "type=2"'
        stdout, stderr, rc = run_adb(calls_cmd, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({calls_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({calls_cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

        # Extract the first dialed call number and name from the result
        extracted_number = None
        extracted_name = None
        lines = stdout.strip().split('\n')
        if lines and lines[0].strip():  # Check if we have at least one line with content
            first_line = lines[0].strip()
            save_to_notepad(f"First dialed call record: {first_line}\n")

            # Extract name from the first row (format: number=..., date=..., duration=..., type=1, name=...)
            name_match = re.search(r"name=([^,]*)", first_line)
            if name_match:
                extracted_name = name_match.group(1).strip()
                save_to_notepad(f"Extracted full name: '{extracted_name}'\n")

                # Extract only the last name if the name contains multiple words
                if extracted_name and extracted_name != "":
                    name_parts = extracted_name.split()
                    if len(name_parts) > 1:
                        last_name = name_parts[-1]  # Get the last word as the last name
                        save_to_notepad(f"Extracted last name: '{last_name}'\n")
                        extracted_name = last_name  # Use only the last name
                    else:
                        save_to_notepad(f"Single name found, using as is: '{extracted_name}'\n")

            # Extract number from the first row
            number_match = re.search(r"number=([^,]+)", first_line)
            if number_match:
                full_number = number_match.group(1).strip()
                save_to_notepad(f"Extracted full number: {full_number}\n")

                # Check if name field is empty or not
                if not extracted_name or extracted_name == "":
                    # Name is empty - use last 3 digits of number
                    if len(full_number) >= 3:
                        extracted_number = full_number[-3:] if len(full_number) >= 3 else full_number
                        save_to_notepad(f"Name field is empty, using last 3 digits for search: {extracted_number}\n")
                    else:
                        extracted_number = full_number
                        save_to_notepad(f"Name field is empty, number has fewer than last 3, using full number: {extracted_number}\n")
                else:
                    # Name is not empty - use the last name for validation
                    save_to_notepad(f"Name field is not empty, using last name for search: {extracted_name}\n")
            else:
                save_to_notepad(f"Warning: Could not extract number from first call record\n")
        else:
            save_to_notepad(f"Warning: No dialed calls found in call log\n")

        if extracted_name == "":
            extracted_name = "dummy_name"

        return full_number, extracted_name

   def get_missed_calls_command(self):
        # Run the command to get missed calls from mobile device (type=1 means incoming calls)
        calls_cmd = f'shell content query --uri content://call_log/calls --projection number:date:duration:type:name | findstr /I "type=3"'
        stdout, stderr, rc = run_adb(calls_cmd, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({calls_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({calls_cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

        # Extract the first missed call number and name from the result
        extracted_number = None
        extracted_name = None
        lines = stdout.strip().split('\n')
        if lines and lines[0].strip():  # Check if we have at least one line with content
            first_line = lines[0].strip()
            save_to_notepad(f"First missed call record: {first_line}\n")

            # Extract name from the first row (format: number=..., date=..., duration=..., type=1, name=...)
            name_match = re.search(r"name=([^,]*)", first_line)
            if name_match:
                extracted_name = name_match.group(1).strip()
                save_to_notepad(f"Extracted full name: '{extracted_name}'\n")

                # Extract only the last name if the name contains multiple words
                if extracted_name and extracted_name != "":
                    name_parts = extracted_name.split()
                    if len(name_parts) > 1:
                        last_name = name_parts[-1]  # Get the last word as the last name
                        save_to_notepad(f"Extracted last name: '{last_name}'\n")
                        extracted_name = last_name  # Use only the last name
                    else:
                        save_to_notepad(f"Single name found, using as is: '{extracted_name}'\n")

            # Extract number from the first row
            number_match = re.search(r"number=([^,]+)", first_line)
            if number_match:
                full_number = number_match.group(1).strip()
                save_to_notepad(f"Extracted full number: {full_number}\n")

                # Check if name field is empty or not
                if not extracted_name or extracted_name == "":
                    # Name is empty - use last 3 digits of number
                    if len(full_number) >= 3:
                        extracted_number = full_number[-3:] if len(full_number) >= 3 else full_number
                        save_to_notepad(f"Name field is empty, using last 3 digits for search: {extracted_number}\n")
                    else:
                        extracted_number = full_number
                        save_to_notepad(f"Name field is empty, number has fewer than last 3, using full number: {extracted_number}\n")
                else:
                    # Name is not empty - use the last name for validation
                    save_to_notepad(f"Name field is not empty, using last name for search: {extracted_name}\n")
            else:
                save_to_notepad(f"Warning: Could not extract number from first call record\n")
        else:
            save_to_notepad(f"Warning: No missed calls found in call log\n")

        if extracted_name == "":
            extracted_name = "dummy_name"

        return full_number, extracted_name

   def get_combined_calls_command(self):
        # Run adb command on mobile device to get all call history (first three rows)
        command = f'shell content query --uri content://call_log/calls --projection number:date:duration:type:name'
        stdout, stderr, rc = run_adb(command, self.device_id)

        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")

        # Initialize search_value string array
        search_value = []

        if stdout.strip():
            # Extract the first three call records from the command result
            rows = stdout.strip().split('\n')[:3]

            for i, row in enumerate(rows):
                if row.strip():
                    save_to_notepad(f"Processing call record #{i+1}: {row}\n")

                    # Extract name, number and type from the row
                    name_match = re.search(r"name=([^,]*)", row)
                    number_match = re.search(r'number=([+]?\d+)', row)
                    type_match = re.search(r'type=(\d+)', row)

                    extracted_name = None
                    extracted_number = None
                    current_search_value = None

                    # Extract name from the row
                    if name_match:
                        extracted_name = name_match.group(1).strip()
                        save_to_notepad(f"Extracted full name: '{extracted_name}'\n")

                        # Check if name is null, NULL, or empty
                        if extracted_name and extracted_name != "" and extracted_name.lower() != "null":
                            name_parts = extracted_name.split()
                            if len(name_parts) > 1:
                                last_name = name_parts[-1]  # Get the last word as the last name
                                save_to_notepad(f"Extracted last name: '{last_name}'\n")
                                extracted_name = last_name  # Use only the last name
                            else:
                                save_to_notepad(f"Single name found, using as is: '{extracted_name}'\n")
                        else:
                            # Name is null, NULL, or empty - treat as no name
                            extracted_name = None
                            save_to_notepad(f"Name field is null/empty, will use number digits instead\n")

                    if number_match and type_match:
                        full_number = number_match.group(1)
                        call_type = int(type_match.group(1))

                        # Remove special characters like + first
                        cleaned_number = re.sub(r'[^\d]', '', full_number)  # Remove all non-digit characters
                        save_to_notepad(f"Extracted full number: {cleaned_number}\n")

                        # Check if name field is empty or not
                        if not extracted_name or extracted_name == "":
                            # Name is empty - use digits based on call type
                            if call_type in [1, 3]:  # incoming and missed calls - first 4 characters
                        # Name is empty - use last 3 digits of number
                                if len(cleaned_number) >= 3:
                                    extracted_number = cleaned_number[-3:]
                                    current_search_value = extracted_number
                                    save_to_notepad(f"Name field is empty, using first 4 digits for search: {extracted_number}\n")
                                else:
                                    extracted_number = cleaned_number
                                    current_search_value = extracted_number
                                    save_to_notepad(f"Name field is empty, number has fewer than 4 digits, using full number: {extracted_number}\n")
                            elif call_type == 2:  # outgoing calls - first 2 characters
                        # Name is empty - use last 3 digits of number
                                if len(cleaned_number) >= 3:
                                    extracted_number = cleaned_number[-3:]
                                    current_search_value = extracted_number
                                    save_to_notepad(f"Name field is empty, using first 2 digits for search: {extracted_number}\n")
                                else:
                                    extracted_number = cleaned_number
                                    current_search_value = extracted_number
                                    save_to_notepad(f"Name field is empty, number has fewer than 2 digits, using full number: {extracted_number}\n")
                            else:
                                extracted_number = cleaned_number
                                current_search_value = extracted_number
                                save_to_notepad(f"Unknown call type, using full number: {extracted_number}\n")
                        else:
                            # Name is not empty - use the last name for validation
                            current_search_value = extracted_name
                            save_to_notepad(f"Name field is not empty, using last name for search: {extracted_name}\n")

                    # Add current search value to the array if it exists
                    if current_search_value:
                        search_value.append(current_search_value)
                        save_to_notepad(f"Added '{current_search_value}' to search_value array\n")

        save_to_notepad(f"Final search_value array: {search_value}\n")
        return search_value

   def get_call_history_with_timestamps_command(self):
        # Run the command to get dialed calls from mobile device (type=1 means incoming calls)
        calls_cmd = f'shell content query --uri content://call_log/calls --projection number:date:duration:type:name'
        stdout, stderr, rc = run_adb(calls_cmd, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({calls_cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({calls_cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

        # Extract the first contact date from the result
        extracted_date = None
        formatted_date = None
        lines = stdout.strip().split('\n')
        if lines and lines[0].strip():  # Check if we have at least one line with content
            first_line = lines[0].strip()
            save_to_notepad(f"First timestamp call record: {first_line}\n")

            # Extract date from the first row (format: number=..., date=..., duration=..., type=1, name=...)
            date_match = re.search(r"date=([^,]*)", first_line)
            if date_match:
                extracted_date = date_match.group(1).strip()
                save_to_notepad(f"Extracted full date: '{extracted_date}'\n")

                # Convert timestamp (in milliseconds) to human-readable format
                try:
                    # Convert string to integer and then to seconds (div by 1000)
                    timestamp_ms = int(extracted_date)
                    timestamp_sec = timestamp_ms / 1000

                    # Convert to datetime object
                    dt_object = datetime.fromtimestamp(timestamp_sec)

                    # Format as "Mar 03, 13:02"
                    formatted_date = dt_object.strftime("%b %d, %H:%M")
                    save_to_notepad(f"Formatted date: '{formatted_date}'\n")
                except (ValueError, TypeError) as e:
                    save_to_notepad(f"Error converting timestamp: {e}\n")
                    formatted_date = extracted_date  # Fallback to original format
        else:
            save_to_notepad(f"Warning: No calls found in call log\n")

        # Ensure we always return a string for regex search compatibility
        result = formatted_date if formatted_date else extracted_date
        return str(result) if result is not None else ""

   def enable_airplane_mode_command(self):
        # Run adb command on Mobile device: adb shell settings put global airplane_mode_on 1. Wait 5 seconds with airplane mode on
        disable_command = f"shell settings put global airplane_mode_on 1"
        stdout, stderr, rc = run_adb(disable_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({disable_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({disable_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return rc

   def disable_airplane_mode_command(self):
        # Run adb command on Mobile device: adb shell settings put global airplane_mode_on 0. Wait 15 seconds with airplane mode off
        disable_command = f"shell settings put global airplane_mode_on 0"
        stdout, stderr, rc = run_adb(disable_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({disable_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({disable_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return rc

   def mute_unmute_microphone_command(self):
        found = click_action_keywords(self.device_id,primary_keywords=["Mute", "microphone", "Mic off"])
        if found == True:
            save_to_notepad(f"Mute/Unmute button pressed successfully\n")
        else:
            save_to_notepad(f"Mute/Unmute button could not be pressed\n")
            base_dir = extract_base_dir_from_batch()
            path = f"{base_dir}/Test_environment/Test_scripts"
            # Click Phone Word commands
            commands = [
                f"shell screencap -p /sdcard/screenshot.png", # Mobile command to take screenshot
                f"pull /sdcard/screenshot.png {path}", # Mobile command to save screenshot on PC
                f"shell input tap 0 0" # Mobile command to click Phone word
            ]

            for cmd in commands:
                x = 0
                y = 0
                if cmd == commands[2]:
                    x,y = find_word_in_screenshot(f"{path}/screenshot.png","Phone")
                    cmd = f"shell input tap {x} {y-100}"

                stdout, stderr, rc = run_adb(cmd, self.device_id)
                # Console display
                if stderr:
                    save_to_notepad(f"[Command failed:] ({cmd}:)")
                    save_to_notepad(f"Error text: {stderr}\n")
                save_to_notepad(f"[Executed command:] ({cmd}:)")
                save_to_notepad(f"Result: {stdout}\n")

            # delete the screenshot
            screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
            command = f'del "{screenshot_path}"'
            stdout, stderr, rc = run_cmd(command)
            # Console display
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            if rc == 0:
                found = True
        return found

   def transfer_audio_to_mobile_command(self, bluetooth_HU_name):
        found = click_on_device_regex(self.device_id,bluetooth_HU_name)
        return found

   def transfer_audio_to_HU_command(self, bluetooth_HU_name):
        found = click_on_device_regex(self.device_id,bluetooth_HU_name)
        return found

   def check_bluetooth_connection(self):
        # Run adb command on Mobile device: adb shell settings put global airplane_mode_on 0. Wait 15 seconds with airplane mode off
        check_bluetooth_connection_command = f'shell dumpsys bluetooth_manager | findstr -i "connected"'
        stdout, stderr, rc = run_adb(check_bluetooth_connection_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({check_bluetooth_connection_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({check_bluetooth_connection_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def check_music_from_internal_memory_command(self):
        # Run adb command to query internal memory music on mobile device
        query_command = f'shell find /sdcard/Music -type f -iname "*.mp3" -o -iname "*.m4a" -o -iname "*.wav" -o -iname "*.aac"'
        stdout, stderr, rc = run_adb(query_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({query_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({query_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return stdout

   def play_music_from_internal_memory_command(self,song):
        # URL encode the song path: convert spaces to %20 and add file:// prefix
        import urllib.parse
        formatted_song = "file://" + urllib.parse.quote(song)

        # Run adb command to play internal memory music on mobile device
        play_music_command = f'shell am start -a android.intent.action.VIEW -d {formatted_song} -t audio/mpeg'
        stdout, stderr, rc = run_adb(play_music_command, self.device_id)
        if stderr:
            save_to_notepad(f"[Command failed:] ({play_music_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({play_music_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        return rc
# =====================================================
# HUAWEI P40 Pro IMPLEMENTATION
# =====================================================
def huawei_p40_pro_enable_bt(device):
    found = toggle_switch_widget(device, enable=True)
    if found == True:
        save_to_notepad(f"Toggle switch Bluetooth enabled successfully\n")
    else:
        save_to_notepad(f"Toggle switch Bluetooth could not be enabled\n")

def huawei_p40_pro_disable_bt(device):
    found = toggle_switch_widget(device, enable=False)
    if found == True:
        save_to_notepad(f"Toggle switch Bluetooth disabled successfully\n")
    else:
        save_to_notepad(f"Toggle switch Bluetooth could not be disabled\n")

    time.sleep(3)
    if found == False:
        found = toggle_switch_widget(device, enable=False)
        if found == True:
            save_to_notepad(f"Toggle switch Bluetooth disabled successfully\n")
        else:
            save_to_notepad(f"Toggle switch Bluetooth could not be disabled\n")

def huawei_p40_pro_get_received_calls(device):
        test_name = "Received_calls"
        status = USB_Matrix_Status()

        # Get Mobile device global name
        command = f"shell settings get secure bluetooth_name" # Mobile1 command go get device name
        stdout, stderr, rc = run_adb(command, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        time.sleep(1)

        # Check if Mobile device has a SIM card
        save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
        sim_check_command = f"shell getprop gsm.sim.state"
        stdout, stderr, rc = run_adb(sim_check_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
        save_to_notepad(f"SIM state result: {stdout}\n")
        assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

        sim_state = stdout.strip()
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

        phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")
        if phone_number_mobile1 == None:
            phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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

        phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        if phone_number_mobile2 == None:
            phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        time.sleep(2)

        # Run adb command to start dialer with specific phone number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:+{phone_number_mobile1}"
        stdout, stderr, rc = run_adb(dial_command, Mobile2)
        if stderr:
            save_to_notepad(f"[Command failed:] ({dial_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({dial_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Dial command {dial_command} failed: {rc}\n"
        save_to_notepad(f"Dialer started with phone number +{phone_number_mobile1}\n")
        time.sleep(5)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        # Run adb command to answer call (keyevent 5 is CALL button)
        call_command = f"shell input keyevent 5"
        stdout, stderr, rc = run_adb(call_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({call_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({call_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {call_command} failed: {rc}\n"
        save_to_notepad(f"Call initiated\n")
        time.sleep(5)

        # Get Mobile device global name first (needed for potential skip message)
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        save_to_notepad(f"Mobile device name: {mobile_name}\n")

        # Run adb command to end call (keyevent 6 is END_CALL button)
        end_command = f"shell input keyevent 6"
        stdout, stderr, rc = run_adb(end_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({end_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({end_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {end_command} failed: {rc}\n"
        save_to_notepad(f"Call ended\n")
        time.sleep(2)

        extracted_name = "dummy_name"
        extracted_number = phone_number_mobile2[-3:] if len(phone_number_mobile2) >= 3 else phone_number_mobile2
        return extracted_number, extracted_name

def huawei_p40_pro_get_dialed_calls(device):
        test_name = "Dialed_calls"
        status = USB_Matrix_Status()

        # Get Mobile device global name
        command = f"shell settings get secure bluetooth_name" # Mobile1 command go get device name
        stdout, stderr, rc = run_adb(command, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        time.sleep(1)

        # Check if Mobile device has a SIM card
        save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
        sim_check_command = f"shell getprop gsm.sim.state"
        stdout, stderr, rc = run_adb(sim_check_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
        save_to_notepad(f"SIM state result: {stdout}\n")
        assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

        sim_state = stdout.strip()
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

        phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")
        if phone_number_mobile1 == None:
            phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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

        phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        if phone_number_mobile2 == None:
            phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        time.sleep(2)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        # Run adb command to start dialer with specific phone number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:+{phone_number_mobile2}"
        stdout, stderr, rc = run_adb(dial_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({dial_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({dial_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Dial command {dial_command} failed: {rc}\n"
        save_to_notepad(f"Dialer started with phone number +{phone_number_mobile2}\n")
        time.sleep(5)

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)

            # Run adb command to answer call (keyevent 5 is CALL button)
            call_command = f"shell input keyevent 5"
            stdout, stderr, rc = run_adb(call_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({call_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({call_command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Call command {call_command} failed: {rc}\n"
            save_to_notepad(f"Call initiated\n")
            time.sleep(5)
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)

            # Run adb command to answer call (keyevent 5 is CALL button)
            call_command = f"shell input keyevent 5"
            stdout, stderr, rc = run_adb(call_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({call_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({call_command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Call command {call_command} failed: {rc}\n"
            save_to_notepad(f"Call initiated\n")
            time.sleep(5)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        # Get Mobile device global name first (needed for potential skip message)
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        save_to_notepad(f"Mobile device name: {mobile_name}\n")

        # Run adb command to end call (keyevent 6 is END_CALL button)
        end_command = f"shell input keyevent 6"
        stdout, stderr, rc = run_adb(end_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({end_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({end_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {end_command} failed: {rc}\n"
        save_to_notepad(f"Call ended\n")
        time.sleep(2)

        extracted_name = "dummy_name"
        extracted_number = phone_number_mobile2[-3:] if len(phone_number_mobile2) >= 3 else phone_number_mobile2
        return extracted_number, extracted_name

def huawei_p40_pro_get_missed_calls(device):
        test_name = "Missed_calls"
        status = USB_Matrix_Status()

        # Get Mobile device global name
        command = f"shell settings get secure bluetooth_name" # Mobile1 command go get device name
        stdout, stderr, rc = run_adb(command, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        time.sleep(1)

        # Check if Mobile device has a SIM card
        save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
        sim_check_command = f"shell getprop gsm.sim.state"
        stdout, stderr, rc = run_adb(sim_check_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
        save_to_notepad(f"SIM state result: {stdout}\n")
        assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

        sim_state = stdout.strip()
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

        phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")
        if phone_number_mobile1 == None:
            phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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

        phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        if phone_number_mobile2 == None:
            phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        time.sleep(2)

        # Run adb command to start dialer with specific phone number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:+{phone_number_mobile1}"
        stdout, stderr, rc = run_adb(dial_command, Mobile2)
        if stderr:
            save_to_notepad(f"[Command failed:] ({dial_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({dial_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Dial command {dial_command} failed: {rc}\n"
        save_to_notepad(f"Dialer started with phone number +{phone_number_mobile1}\n")
        time.sleep(5)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        # Run adb command to end call (keyevent 6 is END_CALL button)
        call_command = f"shell input keyevent 6"
        stdout, stderr, rc = run_adb(call_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({call_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({call_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {call_command} failed: {rc}\n"
        save_to_notepad(f"Call initiated\n")
        time.sleep(5)

        extracted_name = "dummy_name"
        extracted_number = phone_number_mobile2[-3:] if len(phone_number_mobile2) >= 3 else phone_number_mobile2
        return extracted_number, extracted_name

def huawei_p40_pro_get_combined_calls(device):
        test_name = "Combined_call_history"
        status = USB_Matrix_Status()

        # Get Mobile device global name
        command = f"shell settings get secure bluetooth_name" # Mobile1 command go get device name
        stdout, stderr, rc = run_adb(command, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        time.sleep(1)

        search_value = []

        # Check if Mobile device has a SIM card
        save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
        sim_check_command = f"shell getprop gsm.sim.state"
        stdout, stderr, rc = run_adb(sim_check_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
        save_to_notepad(f"SIM state result: {stdout}\n")
        assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

        sim_state = stdout.strip()
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

        phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")
        if phone_number_mobile1 == None:
            phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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

        phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        if phone_number_mobile2 == None:
            phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        time.sleep(2)

        # Run adb command to start dialer with specific phone number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:+{phone_number_mobile1}"
        stdout, stderr, rc = run_adb(dial_command, Mobile2)
        if stderr:
            save_to_notepad(f"[Command failed:] ({dial_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({dial_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Dial command {dial_command} failed: {rc}\n"
        save_to_notepad(f"Dialer started with phone number +{phone_number_mobile1}\n")
        time.sleep(5)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        # Run adb command to answer call (keyevent 5 is CALL button)
        call_command = f"shell input keyevent 5"
        stdout, stderr, rc = run_adb(call_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({call_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({call_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {call_command} failed: {rc}\n"
        save_to_notepad(f"Call initiated\n")
        time.sleep(5)

        # Get Mobile device global name first (needed for potential skip message)
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        save_to_notepad(f"Mobile device name: {mobile_name}\n")

        # Run adb command to end call (keyevent 6 is END_CALL button)
        end_command = f"shell input keyevent 6"
        stdout, stderr, rc = run_adb(end_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({end_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({end_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {end_command} failed: {rc}\n"
        save_to_notepad(f"Call ended\n")
        time.sleep(2)

        extracted_number = phone_number_mobile2[-3:] if len(phone_number_mobile2) >= 3 else phone_number_mobile2
        # Add current search value to the array if it exists
        if extracted_number:
            search_value.append(extracted_number)
            save_to_notepad(f"Added '{extracted_number}' to search_value array\n")

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

        # Run adb command to start dialer with specific phone number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:+{phone_number_mobile1}"
        stdout, stderr, rc = run_adb(dial_command, Mobile2)
        if stderr:
            save_to_notepad(f"[Command failed:] ({dial_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({dial_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Dial command {dial_command} failed: {rc}\n"
        save_to_notepad(f"Dialer started with phone number +{phone_number_mobile1}\n")
        time.sleep(5)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        # Get Mobile device global name first (needed for potential skip message)
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        save_to_notepad(f"Mobile device name: {mobile_name}\n")

        # Run adb command to end call (keyevent 6 is END_CALL button)
        end_command = f"shell input keyevent 6"
        stdout, stderr, rc = run_adb(end_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({end_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({end_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {end_command} failed: {rc}\n"
        save_to_notepad(f"Call ended\n")
        time.sleep(5)

        extracted_number = phone_number_mobile2[-3:] if len(phone_number_mobile2) >= 3 else phone_number_mobile2
        # Add current search value to the array if it exists
        if extracted_number:
            search_value.append(extracted_number)
            save_to_notepad(f"Added '{extracted_number}' to search_value array\n")

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

        # Run adb command to start dialer with specific phone number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:+{phone_number_mobile1}"
        stdout, stderr, rc = run_adb(dial_command, Mobile2)
        if stderr:
            save_to_notepad(f"[Command failed:] ({dial_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({dial_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Dial command {dial_command} failed: {rc}\n"
        save_to_notepad(f"Dialer started with phone number +{phone_number_mobile1}\n")
        time.sleep(5)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        # Get Mobile device global name first (needed for potential skip message)
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        save_to_notepad(f"Mobile device name: {mobile_name}\n")

        # Run adb command to end call (keyevent 6 is END_CALL button)
        end_command = f"shell input keyevent 6"
        stdout, stderr, rc = run_adb(end_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({end_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({end_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {end_command} failed: {rc}\n"
        save_to_notepad(f"Call ended\n")
        time.sleep(5)

        extracted_number = phone_number_mobile2[-3:] if len(phone_number_mobile2) >= 3 else phone_number_mobile2
        # Add current search value to the array if it exists
        if extracted_number:
            search_value.append(extracted_number)
            save_to_notepad(f"Added '{extracted_number}' to search_value array\n")

        return search_value

def huawei_p40_pro_get_call_history_with_timestamps(device):
        test_name = "Time_stamps"
        status = USB_Matrix_Status()

        # Get Mobile device global name
        command = f"shell settings get secure bluetooth_name" # Mobile1 command go get device name
        stdout, stderr, rc = run_adb(command, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        time.sleep(1)

        # Check if Mobile device has a SIM card
        save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
        sim_check_command = f"shell getprop gsm.sim.state"
        stdout, stderr, rc = run_adb(sim_check_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
        save_to_notepad(f"SIM state result: {stdout}\n")
        assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

        sim_state = stdout.strip()
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

        phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")
        if phone_number_mobile1 == None:
            phone_number_mobile1 = extract_phone_number_from_adb(f"adb -s {device} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile1} for port {status}")

        if status == 1:
            select_mobile_device(1, 2)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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
        else:
            select_mobile_device(1, 1)
            # Map the detected devices to corresponding ADB transport ID
            time.sleep(3)
            # Extracting serial numbers for HU and Mobile2
            HU, Mobile2 = get_serial_number()
            # Get Mobile device global name first (needed for potential skip message)
            command = f"shell settings get secure bluetooth_name"
            stdout, stderr, rc = run_adb(command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({command}:)")
            save_to_notepad(f"Result: {stdout}\n")
            assert rc == 0, f"Command {command} failed: {rc}\n"

            mobile_name = stdout.strip()
            save_to_notepad(f"Mobile device name: {mobile_name}\n")

            # Check if Mobile device has a SIM card
            save_to_notepad(f"Checking if {mobile_name} has a SIM card...\n")
            sim_check_command = f"shell getprop gsm.sim.state"
            stdout, stderr, rc = run_adb(sim_check_command, Mobile2)
            if stderr:
                save_to_notepad(f"[Command failed:] ({sim_check_command}:)")
                save_to_notepad(f"Error text: {stderr}\n")
            save_to_notepad(f"[Executed command:] ({sim_check_command}:)")
            save_to_notepad(f"SIM state result: {stdout}\n")
            assert rc == 0, f"Command {sim_check_command} failed: {rc}\n"

            sim_state = stdout.strip()
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

        phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 13")
        save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        if phone_number_mobile2 == None:
            phone_number_mobile2 = extract_phone_number_from_adb(f"adb -s {Mobile2} shell service call iphonesubinfo 10")
            save_to_notepad(f"Extracted phone number: {phone_number_mobile2} for port 1")
        time.sleep(2)

        # Run adb command to start dialer with specific phone number
        dial_command = f"shell am start -a android.intent.action.CALL -d tel:+{phone_number_mobile1}"
        stdout, stderr, rc = run_adb(dial_command, Mobile2)
        if stderr:
            save_to_notepad(f"[Command failed:] ({dial_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({dial_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Dial command {dial_command} failed: {rc}\n"
        save_to_notepad(f"Dialer started with phone number +{phone_number_mobile1}\n")
        time.sleep(5)

        # Switch USB Matrix port back
        select_mobile_device(1, status)
        time.sleep(3)

        # Run adb command to answer call (keyevent 5 is CALL button)
        call_command = f"shell input keyevent 5"
        stdout, stderr, rc = run_adb(call_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({call_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({call_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {call_command} failed: {rc}\n"
        save_to_notepad(f"Call initiated\n")
        time.sleep(5)

        # Get Mobile device global name first (needed for potential skip message)
        command = f"shell settings get secure bluetooth_name"
        stdout, stderr, rc = run_adb(command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Command {command} failed: {rc}\n"

        mobile_name = stdout.strip()
        save_to_notepad(f"Mobile device name: {mobile_name}\n")

        # Run adb command to end call (keyevent 6 is END_CALL button)
        end_command = f"shell input keyevent 6"
        stdout, stderr, rc = run_adb(end_command, device)
        if stderr:
            save_to_notepad(f"[Command failed:] ({end_command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({end_command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        assert rc == 0, f"Call command {end_command} failed: {rc}\n"
        save_to_notepad(f"Call ended\n")
        time.sleep(2)

        # Extract timestamp from PC system time (when dial command was executed)
        extracted_timestamp = datetime.now().strftime("%b %d, %H:%M")
        save_to_notepad(f"PC timestamp extracted: '{extracted_timestamp}'\n")
        return str(extracted_timestamp)

def huawei_p40_pro_transfer_audio_to_HU(device, bluetooth_HU_name):
    # Run input tap command on Mobile device
    command = f"shell input tap 950 2200"     # Mobile input tap
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")

    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found

def huawei_p40_pro_transfer_audio_to_mobile(device, bluetooth_HU_name):

    # Run input tap command on Mobile device
    command = f"shell input tap 950 2200"     # Mobile input tap
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")

    found = click_on_device_regex(device,"Handset")
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found
# =====================================================
# Xperia5 IMPLEMENTATION
# =====================================================
def Xperia5_transfer_audio_to_mobile(device, bluetooth_HU_name):
    # Run input swipe command on Mobile device
    command = f"shell input swipe 500 60 400 400"     # Mobile input swipe
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(3)

    found = click_on_device_regex(device,"call")
    if found == True:
        save_to_notepad(f"call button pressed successfully\n")
    else:
        save_to_notepad(f"call button could not be pressed\n")
    time.sleep(3)
    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")

    found = click_on_device_regex(device,"Phone")
    if found == True:
        save_to_notepad(f"Phone button pressed successfully\n")
    else:
        save_to_notepad(f"Phone button could not be pressed\n")
    return found

def Xperia5_transfer_audio_to_HU(device, bluetooth_HU_name):
    found = click_on_device_regex(device,"Phone")
    if found == True:
        save_to_notepad(f"Phone button pressed successfully\n")
    else:
        save_to_notepad(f"Phone button could not be pressed\n")
        # Run home command on Mobile device
        command = f"shell input keyevent 3"     # Mobile home
        stdout, stderr, rc = run_adb(command, device)
        save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
        save_to_notepad(f"Result: {stdout}\n")
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        found = click_on_device_regex(device,"Phone")

    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found

# =====================================================
# Legion Phone2 Pro IMPLEMENTATION
# =====================================================
def legion_phone2_Pro_transfer_audio_to_mobile(device, bluetooth_HU_name):
    found = click_on_device_regex(device,"Bluetooth")
    if found == True:
        save_to_notepad(f"Bluetooth button pressed successfully\n")
    else:
        save_to_notepad(f"Bluetooth button could not be pressed\n")

    found = click_on_device_regex(device,"Phone")
    if found == True:
        save_to_notepad(f"Phone button pressed successfully\n")
    else:
        save_to_notepad(f"Phone button could not be pressed\n")
    return found

def legion_phone2_Pro_transfer_audio_to_HU(device, bluetooth_HU_name):
    found = click_on_device_regex(device,"Hands")
    if found == True:
        save_to_notepad(f"Hands button pressed successfully\n")
    else:
        save_to_notepad(f"Hands button could not be pressed\n")

    found = click_on_device_regex(device,"Bluetooth")
    if found == True:
        save_to_notepad(f"Bluetooth button pressed successfully\n")
    else:
        save_to_notepad(f"Bluetooth button could not be pressed\n")
    return found

# =====================================================
# OPPO Find X8 Pro IMPLEMENTATION
# =====================================================
def oppo_find_x8_pro_transfer_audio_to_HU(device, bluetooth_HU_name):
    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"
    # Click Phone Word commands
    commands = [
        f"shell screencap -p /sdcard/screenshot.png", # Mobile command to take screenshot
        f"pull /sdcard/screenshot.png {path}", # Mobile command to save screenshot on PC
        f"shell input tap 0 0" # Mobile command to click Phone word
    ]

    for cmd in commands:
        x = 0
        y = 0
        if cmd == commands[2]:
            x,y = find_word_in_screenshot(f"{path}/screenshot.png","Phone")
            cmd = f"shell input tap {x} {y-100}"

        stdout, stderr, rc = run_adb(cmd, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

    # delete the screenshot
    screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
    command = f'del "{screenshot_path}"'
    stdout, stderr, rc = run_cmd(command)
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] ({command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    save_to_notepad(f"[Executed command:] ({command}:)")
    save_to_notepad(f"Result: {stdout}\n")

    found = click_action_keywords(device, primary_keywords=["Allow", "Authorize", "YES"])
    if found == True:
        save_to_notepad(f"Clicked Allow button pop up completed via keywords\n")
    else:
        save_to_notepad(f"Clicked Allow button pop up not completed via keywords\n")

    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found

def oppo_find_x8_pro_transfer_audio_to_mobile(device, bluetooth_HU_name):
    # Run input swipe command on Mobile device
    command = f"shell input swipe 500 60 400 400"     # Mobile input swipe
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")

    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"

    found = click_on_device_regex(device,"Phone")
    if found == True:
        save_to_notepad(f"Phone button pressed successfully\n")
    else:
        save_to_notepad(f"Phone button could not be pressed\n")
    time.sleep(3)

    # Click Phone Word commands
    commands = [
        f"shell screencap -p /sdcard/screenshot.png", # Mobile command to take screenshot
        f"pull /sdcard/screenshot.png {path}", # Mobile command to save screenshot on PC
        f"shell input tap 0 0" # Mobile command to click Phone word
    ]

    for cmd in commands:
        x = 0
        y = 0
        if cmd == commands[2]:
            # Split bluetooth_HU_name by space and use only the first part
            bluetooth_name_first_part = bluetooth_HU_name.split()[0]
            x,y = find_word_in_screenshot(f"{path}/screenshot.png",bluetooth_name_first_part)
            cmd = f"shell input tap {x} {y-100}"

        stdout, stderr, rc = run_adb(cmd, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

    # delete the screenshot
    screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
    command = f'del "{screenshot_path}"'
    stdout, stderr, rc = run_cmd(command)
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] ({command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    save_to_notepad(f"[Executed command:] ({command}:)")
    save_to_notepad(f"Result: {stdout}\n")

    found = click_on_device_regex(device,"Phone")
    if found == True:
        save_to_notepad(f"Phone button pressed successfully\n")
    else:
        save_to_notepad(f"Phone button could not be pressed\n")
    return found

# =====================================================
# OPPO F17 IMPLEMENTATION
# =====================================================
def oppo_F17_enable_bt(device):
    # Run input tap command on Mobile device
    command = f"shell input tap 600 2200"     # Mobile input tap
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(2) 

    found = click_on_device_regex(device, "Bluetooth")
    if found == True:
        save_to_notepad(f"Button Bluetooth enabled successfully\n")
    else:
        save_to_notepad(f"Button Bluetooth could not be enabled\n")

def oppo_F17_disable_bt(device):
    found = click_on_device_regex(device, "Bluetooth")
    if found == True:
        save_to_notepad(f"Button Bluetooth disabled successfully\n")
    else:
        save_to_notepad(f"Button Bluetooth could not be disabled\n")

def oppo_F17_transfer_audio_to_mobile(device, bluetooth_HU_name):
    # Run back command on Mobile device
    command = f"shell input keyevent 3"     # Mobile back
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(3)

    # Run input swipe command on Mobile device
    command = f"shell input swipe 500 60 400 400"     # Mobile input swipe
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(3)

    found = click_on_device_regex(device,"call")
    if found == True:
        save_to_notepad(f"call button pressed successfully\n")
    else:
        save_to_notepad(f"call button could not be pressed\n")
    time.sleep(3)
    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")

    found = click_on_device_regex(device,"Phone")
    if found == True:
        save_to_notepad(f"Phone button pressed successfully\n")
    else:
        save_to_notepad(f"Phone button could not be pressed\n")
    return found

def oppo_F17_conference_call(device):
    # Run back command on Mobile device
    command = f"shell input keyevent 3"     # Mobile back
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(3)

    # Run input swipe command on Mobile device
    command = f"shell input swipe 500 60 400 400"     # Mobile input swipe
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(3)

    found = click_on_device_regex(device,"call")
    if found == True:
        save_to_notepad(f"call button pressed successfully\n")
    else:
        save_to_notepad(f"call button could not be pressed\n")
    time.sleep(3)

    found = click_on_device_regex(device,"Merge")
    if found == True:
        save_to_notepad(f"Clicked Merge button completed via keywords\n")
    else:
        save_to_notepad(f"Clicked Merge button not completed via keywords\n")
    time.sleep(3)

# =====================================================
# Pixel 9 Pro IMPLEMENTATION
# =====================================================
def pixel_9_pro_transfer_audio_to_HU(device, bluetooth_HU_name):
    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"
    # Click Phone Word commands
    commands = [
        f"shell screencap -p /sdcard/screenshot.png", # Mobile command to take screenshot
        f"pull /sdcard/screenshot.png {path}", # Mobile command to save screenshot on PC
        f"shell input tap 0 0" # Mobile command to click Phone word
    ]

    for cmd in commands:
        x = 0
        y = 0
        if cmd == commands[2]:
            x,y = find_word_in_screenshot(f"{path}/screenshot.png","Phone")
            cmd = f"shell input tap {x} {y-100}"

        stdout, stderr, rc = run_adb(cmd, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

    # delete the screenshot
    screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
    command = f'del "{screenshot_path}"'
    stdout, stderr, rc = run_cmd(command)
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] ({command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    save_to_notepad(f"[Executed command:] ({command}:)")
    save_to_notepad(f"Result: {stdout}\n")

    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found

def pixel_9_pro_transfer_audio_to_mobile(device, bluetooth_HU_name):
    # Run input swipe command on Mobile device
    command = f"shell input swipe 500 60 400 400"     # Mobile input swipe
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(3)

    found = click_on_device_regex(device,"call")
    if found == True:
        save_to_notepad(f"call button pressed successfully\n")
    else:
        save_to_notepad(f"call button could not be pressed\n")
    time.sleep(3)

    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"

    # Click Phone Word commands
    commands = [
        f"shell screencap -p /sdcard/screenshot.png", # Mobile command to take screenshot
        f"pull /sdcard/screenshot.png {path}", # Mobile command to save screenshot on PC
        f"shell input tap 0 0" # Mobile command to click Phone word
    ]

    for cmd in commands:
        x = 0
        y = 0
        if cmd == commands[2]:
            # Split bluetooth_HU_name by space and use only the first part
            bluetooth_name_first_part = bluetooth_HU_name.split()[0]
            x,y = find_word_in_screenshot(f"{path}/screenshot.png",bluetooth_name_first_part)
            cmd = f"shell input tap {x} {y-100}"

        stdout, stderr, rc = run_adb(cmd, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

    # delete the screenshot
    screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
    command = f'del "{screenshot_path}"'
    stdout, stderr, rc = run_cmd(command)
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] ({command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    save_to_notepad(f"[Executed command:] ({command}:)")
    save_to_notepad(f"Result: {stdout}\n")

    found = click_on_device_regex(device,"Phone")
    if found == True:
        save_to_notepad(f"Phone button pressed successfully\n")
    else:
        save_to_notepad(f"Phone button could not be pressed\n")
    return found
# =====================================================
# MI 9 IMPLEMENTATION
# =====================================================
def mi_9_transfer_audio_to_HU(device, bluetooth_HU_name):
    found = click_action_keywords(device,primary_keywords=["Close", "Cancel", "Not now"])
    if found == True:
        save_to_notepad(f"Clicked Close button pop up completed via keywords\n")
    else:
        save_to_notepad(f"Clicked Close button pop up not completed via keywords\n")

    # Run input tap command on Mobile device
    command = f"shell input tap 200 2000"     # Mobile input tap
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(2)

    found = click_on_device_regex(device,"Bluetooth")
    if found == True:
        save_to_notepad(f"Bluetooth button pressed successfully\n")
    else:
        save_to_notepad(f"Bluetooth button could not be pressed\n")
    return found

def mi_9_transfer_audio_to_mobile(device, bluetooth_HU_name):
    # Run input tap command on Mobile device
    command = f"shell input tap 200 2000"     # Mobile input tap
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(2)

    found = click_on_device_regex(device,"Speaker")
    if found == True:
        save_to_notepad(f"Speaker button pressed successfully\n")
    else:
        save_to_notepad(f"Speaker button could not be pressed\n")
    return found

# =====================================================
# OnePlus 13 IMPLEMENTATION
# =====================================================
def oneplus_13_transfer_audio_to_HU(device, bluetooth_HU_name):
    base_dir = extract_base_dir_from_batch()
    path = f"{base_dir}/Test_environment/Test_scripts"
    # Click Phone Word commands
    commands = [
        f"shell screencap -p /sdcard/screenshot.png", # Mobile command to take screenshot
        f"pull /sdcard/screenshot.png {path}", # Mobile command to save screenshot on PC
        f"shell input tap 0 0" # Mobile command to click Phone word
    ]

    for cmd in commands:
        x = 0
        y = 0
        if cmd == commands[2]:
            x,y = find_word_in_screenshot(f"{path}/screenshot.png","Phone")
            cmd = f"shell input tap {x} {y-100}"

        stdout, stderr, rc = run_adb(cmd, device)
        # Console display
        if stderr:
            save_to_notepad(f"[Command failed:] ({cmd}:)")
            save_to_notepad(f"Error text: {stderr}\n")
        save_to_notepad(f"[Executed command:] ({cmd}:)")
        save_to_notepad(f"Result: {stdout}\n")

    # delete the screenshot
    screenshot_path = f"{base_dir}/Test_environment/Test_scripts/screenshot.png".replace('/', '\\')
    command = f'del "{screenshot_path}"'
    stdout, stderr, rc = run_cmd(command)
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] ({command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    save_to_notepad(f"[Executed command:] ({command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    time.sleep(2)

    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found

# =====================================================
# motorola one fusion IMPLEMENTATION
# =====================================================
def motorola_one_fusion_transfer_audio_to_HU(device, bluetooth_HU_name):
    found = click_on_device_regex(device,"Phone")
    if found == True:
        save_to_notepad(f"Phone button pressed successfully\n")
    else:
        save_to_notepad(f"Phone button could not be pressed\n")

    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found

def motorola_one_fusion_conference_call(device):
    # Run input swipe command on Mobile device
    command = f"shell input swipe 500 60 400 400"     # Mobile input swipe
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(3)

    found = click_on_device_regex(device,"call")
    if found == True:
        save_to_notepad(f"call button pressed successfully\n")
    else:
        save_to_notepad(f"call button could not be pressed\n")
    time.sleep(3)

    found = click_on_device_regex(device,"Merge")
    if found == True:
        save_to_notepad(f"Clicked Merge button completed via keywords\n")
    else:
        save_to_notepad(f"Clicked Merge button not completed via keywords\n")

# =====================================================
# POCO F7 Ultra IMPLEMENTATION
# =====================================================
def poco_f7_ultra_conference_call(device):
    # Run input swipe command on Mobile device
    command = f"shell input swipe 500 60 400 400"     # Mobile input swipe
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    time.sleep(3)

    found = click_on_device_regex(device,"call")
    if found == True:
        save_to_notepad(f"call button pressed successfully\n")
    else:
        save_to_notepad(f"call button could not be pressed\n")
    time.sleep(3)

    found = click_on_device_regex(device,"More")
    if found == True:
        save_to_notepad(f"More button pressed successfully\n")
    else:
        save_to_notepad(f"More button could not be pressed\n")
    time.sleep(3)

    found = click_on_device_regex(device,"Merge")
    if found == True:
        save_to_notepad(f"Clicked Merge button completed via keywords\n")
    else:
        save_to_notepad(f"Clicked Merge button not completed via keywords\n")
    time.sleep(3)

# =====================================================
# HUAWEI Mate 40 Pro IMPLEMENTATION
# =====================================================
def huawei_mate40_pro_transfer_audio_to_HU(device, bluetooth_HU_name):
    # Run input tap command on Mobile device
    command = f"shell input tap 900 2000"     # Mobile input tap
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")

    found = click_on_device_regex(device,bluetooth_HU_name)
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found

def huawei_mate40_pro_transfer_audio_to_mobile(device, bluetooth_HU_name):

    # Run input tap command on Mobile device
    command = f"shell input tap 900 2000"     # Mobile input tap
    stdout, stderr, rc = run_adb(command, device)
    save_to_notepad(f"[Executed command:] (adb -s {device} {command}:)")
    save_to_notepad(f"Result: {stdout}\n")
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] (adb -s {device} {command}:)")
        save_to_notepad(f"Error text: {stderr}\n")

    found = click_on_device_regex(device,"Handset")
    if found == True:
        save_to_notepad(f"{bluetooth_HU_name} button pressed successfully\n")
    else:
        save_to_notepad(f"{bluetooth_HU_name} button could not be pressed\n")
    return found

def huawei_mate40_pro_conference_call(device):
    x,y = find_word_on_device_via_regex_with_coordinates(device,"Merge")
    cmd = f"shell input tap {x} {y-100}"

    stdout, stderr, rc = run_adb(cmd, device)
    # Console display
    if stderr:
        save_to_notepad(f"[Command failed:] ({cmd}:)")
        save_to_notepad(f"Error text: {stderr}\n")
    save_to_notepad(f"[Executed command:] ({cmd}:)")
    save_to_notepad(f"Result: {stdout}\n")

# DEVICE MENU REGISTRY
# =====================================================
DEVICE_MENU = {
   "Galaxy S22": {
       # uses defaults
   },
   "HUAWEI P40 Pro": {
       "enable_bluetooth": huawei_p40_pro_enable_bt,
       "disable_bluetooth": huawei_p40_pro_disable_bt,
       "get_received_calls": huawei_p40_pro_get_received_calls,
       "get_dialed_calls": huawei_p40_pro_get_dialed_calls,
       "get_missed_calls": huawei_p40_pro_get_missed_calls,
       "get_combined_calls": huawei_p40_pro_get_combined_calls,
       "get_call_history_with_timestamps": huawei_p40_pro_get_call_history_with_timestamps,
       "transfer_audio_to_mobile": huawei_p40_pro_transfer_audio_to_mobile,
       "transfer_audio_to_HU": huawei_p40_pro_transfer_audio_to_HU
   },
   "HUAWEI Mate 40 Pro": {
       "enable_bluetooth": huawei_p40_pro_enable_bt,
       "disable_bluetooth": huawei_p40_pro_disable_bt,
       "get_received_calls": huawei_p40_pro_get_received_calls,
       "get_dialed_calls": huawei_p40_pro_get_dialed_calls,
       "get_missed_calls": huawei_p40_pro_get_missed_calls,
       "get_combined_calls": huawei_p40_pro_get_combined_calls,
       "get_call_history_with_timestamps": huawei_p40_pro_get_call_history_with_timestamps,
       "transfer_audio_to_mobile": huawei_mate40_pro_transfer_audio_to_mobile,
       "transfer_audio_to_HU": huawei_mate40_pro_transfer_audio_to_HU,
       "conference_call": huawei_mate40_pro_conference_call
   },
   "MI 9": {
       "enable_bluetooth": huawei_p40_pro_enable_bt,
       "disable_bluetooth": huawei_p40_pro_disable_bt,
       "get_received_calls": huawei_p40_pro_get_received_calls,
       "get_dialed_calls": huawei_p40_pro_get_dialed_calls,
       "get_missed_calls": huawei_p40_pro_get_missed_calls,
       "get_combined_calls": huawei_p40_pro_get_combined_calls,
       "get_call_history_with_timestamps": huawei_p40_pro_get_call_history_with_timestamps,
       "transfer_audio_to_mobile": mi_9_transfer_audio_to_mobile,
       "transfer_audio_to_HU": mi_9_transfer_audio_to_HU
   },
   "POCO F7 Ultra": {
       "enable_bluetooth": huawei_p40_pro_enable_bt,
       "disable_bluetooth": huawei_p40_pro_disable_bt,
       "get_received_calls": huawei_p40_pro_get_received_calls,
       "get_dialed_calls": huawei_p40_pro_get_dialed_calls,
       "get_missed_calls": huawei_p40_pro_get_missed_calls,
       "get_combined_calls": huawei_p40_pro_get_combined_calls,
       "get_call_history_with_timestamps": huawei_p40_pro_get_call_history_with_timestamps,
       "transfer_audio_to_mobile": Xperia5_transfer_audio_to_mobile,
       "transfer_audio_to_HU": motorola_one_fusion_transfer_audio_to_HU,
       "conference_call": poco_f7_ultra_conference_call
   },
   "Xperia5": {
       "get_received_calls": huawei_p40_pro_get_received_calls,
       "get_dialed_calls": huawei_p40_pro_get_dialed_calls,
       "get_missed_calls": huawei_p40_pro_get_missed_calls,
       "get_combined_calls": huawei_p40_pro_get_combined_calls,
       "get_call_history_with_timestamps": huawei_p40_pro_get_call_history_with_timestamps,
       "transfer_audio_to_mobile": Xperia5_transfer_audio_to_mobile,
       "transfer_audio_to_HU": Xperia5_transfer_audio_to_HU
   },
   "OPPO Find X8 Pro": {
       "transfer_audio_to_mobile": oppo_find_x8_pro_transfer_audio_to_mobile,
       "transfer_audio_to_HU": oppo_find_x8_pro_transfer_audio_to_HU
   },
   "OPPO F17": {
       "enable_bluetooth": oppo_F17_enable_bt,
       "disable_bluetooth": oppo_F17_disable_bt,
       "get_received_calls": huawei_p40_pro_get_received_calls,
       "get_dialed_calls": huawei_p40_pro_get_dialed_calls,
       "get_missed_calls": huawei_p40_pro_get_missed_calls,
       "get_combined_calls": huawei_p40_pro_get_combined_calls,
       "get_call_history_with_timestamps": huawei_p40_pro_get_call_history_with_timestamps,
       "transfer_audio_to_mobile": oppo_F17_transfer_audio_to_mobile,
       "transfer_audio_to_HU": oppo_find_x8_pro_transfer_audio_to_HU,
       "conference_call": oppo_F17_conference_call
   },
   "OnePlus 13": {
       "transfer_audio_to_mobile": oppo_find_x8_pro_transfer_audio_to_mobile,
       "transfer_audio_to_HU": oneplus_13_transfer_audio_to_HU
   },
   "OnePlus Open": {
       "transfer_audio_to_mobile": Xperia5_transfer_audio_to_mobile,
       "transfer_audio_to_HU": motorola_one_fusion_transfer_audio_to_HU,
       "conference_call": poco_f7_ultra_conference_call
   },
   "Pixel 9 Pro": {
       "transfer_audio_to_mobile": pixel_9_pro_transfer_audio_to_mobile,
       "transfer_audio_to_HU": pixel_9_pro_transfer_audio_to_HU
   },
   "one fusion": {
       "get_received_calls": huawei_p40_pro_get_received_calls,
       "get_dialed_calls": huawei_p40_pro_get_dialed_calls,
       "get_missed_calls": huawei_p40_pro_get_missed_calls,
       "get_combined_calls": huawei_p40_pro_get_combined_calls,
       "transfer_audio_to_mobile": Xperia5_transfer_audio_to_mobile,
       "transfer_audio_to_HU": motorola_one_fusion_transfer_audio_to_HU,
       "conference_call": motorola_one_fusion_conference_call
   },
   "Legion Phone2 Pro": {
       "transfer_audio_to_mobile": legion_phone2_Pro_transfer_audio_to_mobile,
       "transfer_audio_to_HU": legion_phone2_Pro_transfer_audio_to_HU
   }
}

# =====================================================
# FACTORY FUNCTION
# =====================================================
def create_device(device_id, mobile_name):
   return AndroidDevice(
       device_id,
       mobile_name
   )
