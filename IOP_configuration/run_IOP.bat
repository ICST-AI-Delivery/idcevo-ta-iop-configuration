@echo off
echo.
echo ==============================================
echo STARTING TESTS EXECUTION WITH USB PORT LOOP
echo ==============================================
echo.

REM --- Create temporary batch file for each port ---
echo Creating temporary batch files for USB port configuration...

for %%N in (1,2,3,5) do (
   echo @echo off > temp_port_%%N.bat
   echo setlocal EnableDelayedExpansion >> temp_port_%%N.bat
   echo set "USB_MATRIX_COM_PORT=COM38" >> temp_port_%%N.bat
   echo set "SWITCH_COM_PORT=COM36" >> temp_port_%%N.bat
   echo set "BASE_DIR=D:\traget\IDCevo\BMW_IDCevo_IOP_Test_Setup\IOP_configuration" >> temp_port_%%N.bat
   echo set "SUITE_PATH=!BASE_DIR!\Test_environment\IOP_suite.txt" >> temp_port_%%N.bat
   echo set "TEST_DIR=!BASE_DIR!\Test_environment\Test_scripts" >> temp_port_%%N.bat
   echo set "RESULTS_DIR=!BASE_DIR!\Test_results" >> temp_port_%%N.bat
   echo set "SCREENSHOT_DIR=!RESULTS_DIR!\Screenshots" >> temp_port_%%N.bat
   echo set "RECORDING_DIR=!RESULTS_DIR!\Recordings" >> temp_port_%%N.bat
   echo echo ============================================== >> temp_port_%%N.bat
   echo echo DELETING PREVIOUS RESULTS >> temp_port_%%N.bat
   echo echo ============================================== >> temp_port_%%N.bat
   echo if exist "!RESULTS_DIR!\IOP_logs.html" ^( >> temp_port_%%N.bat
   echo    del /f /q "!RESULTS_DIR!\IOP_logs.html" >> temp_port_%%N.bat
   echo    echo Deleted: IOP_logs.html >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo IOP_logs.html not found. >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo if exist "!RESULTS_DIR!\IOP_results.xls" ^( >> temp_port_%%N.bat
   echo    del /f /q "!RESULTS_DIR!\IOP_results.xls" >> temp_port_%%N.bat
   echo    echo Deleted: IOP_results.xls >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo IOP_results.xls not found. >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo if exist "!RESULTS_DIR!\*.dlt" ^( >> temp_port_%%N.bat
   echo    del /f /q "!RESULTS_DIR!\*.dlt" >> temp_port_%%N.bat
   echo    echo Deleted: DLT logs  >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo DLT logs not found. >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo if exist "!RESULTS_DIR!\bugreport*" ^( >> temp_port_%%N.bat
   echo    del /f /q "!RESULTS_DIR!\bugreport*" >> temp_port_%%N.bat
   echo    echo Deleted: Bugreport  >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo Bugreport not found. >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo if exist "!RESULTS_DIR!\btsnoop*" ^( >> temp_port_%%N.bat
   echo    del /f /q "!RESULTS_DIR!\btsnoop*" >> temp_port_%%N.bat
   echo    echo Deleted: Btsnoop logs  >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo Btsnoop not found. >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo if exist "!SCREENSHOT_DIR!\*.png" ^( >> temp_port_%%N.bat
   echo    del /f /q "!SCREENSHOT_DIR!\*.png" >> temp_port_%%N.bat
   echo    echo Deleted: screenshots >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo screenshots not found. >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo if exist "!RECORDING_DIR!\*.mp4" ^( >> temp_port_%%N.bat
   echo    del /f /q "!RECORDING_DIR!\*.mp4" >> temp_port_%%N.bat
   echo    echo Deleted: recordings >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo recordings not found. >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo echo ---------------------------------------------- >> temp_port_%%N.bat
   echo echo Configuring USB port %%N via serial ^(COM38^) >> temp_port_%%N.bat
   echo echo ---------------------------------------------- >> temp_port_%%N.bat
   echo echo Calling Python script with port: %%N >> temp_port_%%N.bat
   echo python "!BASE_DIR!\Test_environment\Test_scripts\helpers\send_USB_command.py" %%N >> temp_port_%%N.bat
   echo IF ERRORLEVEL 1 ^( >> temp_port_%%N.bat
   echo    echo WARNING: Issue configuring USB port %%N, but continuing with tests... >> temp_port_%%N.bat
   echo ^) ELSE ^( >> temp_port_%%N.bat
   echo    echo USB port %%N configured successfully. >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo echo. >> temp_port_%%N.bat
   echo echo Running test suite for USB port %%N >> temp_port_%%N.bat
   echo echo Getting device name from connected device... >> temp_port_%%N.bat
   echo echo Detecting ADB devices... >> temp_port_%%N.bat
   echo set "MOBILE_DEVICE_ID=" >> temp_port_%%N.bat
   echo set "MOBILE_DEVICE_COUNT=0" >> temp_port_%%N.bat
   echo set "BMW_DEVICE_ID=" >> temp_port_%%N.bat
   echo set "BMW_DEVICE_COUNT=0" >> temp_port_%%N.bat
   echo echo ============================================== >> temp_port_%%N.bat
   echo echo CONNECTED ADB DEVICES: >> temp_port_%%N.bat
   echo echo ============================================== >> temp_port_%%N.bat
   echo for /f "skip=1 tokens=1,2" %%%%a in ^('adb devices 2^^^>nul'^) do ^( >> temp_port_%%N.bat
   echo    if "%%%%b"=="device" ^( >> temp_port_%%N.bat
   echo       for /f "tokens=*" %%%%c in ^('adb -s %%%%a shell getprop ro.product.model 2^^^>nul'^) do ^( >> temp_port_%%N.bat
   echo          echo Found device: %%%%a - Model: %%%%c >> temp_port_%%N.bat
   echo          echo %%%%c ^| findstr /i /c:"BMW" ^>nul >> temp_port_%%N.bat
   echo          if not errorlevel 1 ^( >> temp_port_%%N.bat
   echo             echo Found BMW device: %%%%a >> temp_port_%%N.bat
   echo             set /a BMW_DEVICE_COUNT+=1 >> temp_port_%%N.bat
   echo             if not defined BMW_DEVICE_ID ^( >> temp_port_%%N.bat
   echo                echo Using first BMW device: %%%%a >> temp_port_%%N.bat
   echo                set "BMW_DEVICE_ID=%%%%a" >> temp_port_%%N.bat
   echo             ^) else ^( >> temp_port_%%N.bat
   echo                echo Found additional BMW device: %%%%a >> temp_port_%%N.bat
   echo             ^) >> temp_port_%%N.bat
   echo          ^) else ^( >> temp_port_%%N.bat
   echo             echo %%%%c ^| findstr /i /c:"IDcEvo" ^>nul >> temp_port_%%N.bat
   echo             if not errorlevel 1 ^( >> temp_port_%%N.bat
   echo                echo Skipping IDcEvo device: %%%%a >> temp_port_%%N.bat
   echo             ^) else ^( >> temp_port_%%N.bat
   echo                set /a MOBILE_DEVICE_COUNT+=1 >> temp_port_%%N.bat
   echo                if not defined MOBILE_DEVICE_ID ^( >> temp_port_%%N.bat
   echo                   echo Using first non-BMW mobile device: %%%%a >> temp_port_%%N.bat
   echo                   set "MOBILE_DEVICE_ID=%%%%a" >> temp_port_%%N.bat
   echo                ^) else ^( >> temp_port_%%N.bat
   echo                   echo Found additional mobile device: %%%%a >> temp_port_%%N.bat
   echo                ^) >> temp_port_%%N.bat
   echo             ^) >> temp_port_%%N.bat
   echo          ^) >> temp_port_%%N.bat
   echo       ^) >> temp_port_%%N.bat
   echo    ^) >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo echo Total mobile devices found: ^^!MOBILE_DEVICE_COUNT^^! >> temp_port_%%N.bat
   echo echo Total BMW devices found: ^^!BMW_DEVICE_COUNT^^! >> temp_port_%%N.bat
   echo echo ============================================== >> temp_port_%%N.bat
   echo REM Configure Bluetooth logging on BMW device >> temp_port_%%N.bat
   echo if defined BMW_DEVICE_ID ^( >> temp_port_%%N.bat
   echo    echo Configuring Bluetooth logging on BMW device: !BMW_DEVICE_ID! >> temp_port_%%N.bat
   echo    adb -s ^^!BMW_DEVICE_ID^^! shell device_config put bluetooth INIT_default_log_level_str LOG_VERBOSE >> temp_port_%%N.bat
   echo    if not errorlevel 1 ^( >> temp_port_%%N.bat
   echo       echo Bluetooth logging configuration successful on BMW device >> temp_port_%%N.bat
   echo    ^) else ^( >> temp_port_%%N.bat
   echo       echo WARNING: Failed to configure Bluetooth logging on BMW device >> temp_port_%%N.bat
   echo    ^) >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo No BMW device found for Bluetooth configuration >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo echo ============================================== >> temp_port_%%N.bat
   echo if defined MOBILE_DEVICE_ID ^( >> temp_port_%%N.bat
   echo    echo Querying device name from mobile device: !MOBILE_DEVICE_ID! >> temp_port_%%N.bat
   echo    if not defined DEVICE_NAME ^( >> temp_port_%%N.bat
   echo       for /f "tokens=*" %%%%a in ^('adb -s !MOBILE_DEVICE_ID! shell settings get secure bluetooth_name 2^^^>nul'^) do ^( >> temp_port_%%N.bat
   echo          set "TEMP_NAME=%%%%a" >> temp_port_%%N.bat
   echo          if not "!TEMP_NAME!"=="null" if not "!TEMP_NAME!"=="" set "DEVICE_NAME=!TEMP_NAME!" >> temp_port_%%N.bat
   echo       ^) >> temp_port_%%N.bat
   echo    ^) >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    if not defined DEVICE_NAME ^( >> temp_port_%%N.bat
   echo       for /f "tokens=*" %%%%a in ^('adb shell settings get secure bluetooth_name 2^^^>nul'^) do ^( >> temp_port_%%N.bat
   echo          set "TEMP_NAME=%%%%a" >> temp_port_%%N.bat
   echo          if not "!TEMP_NAME!"=="null" if not "!TEMP_NAME!"=="" set "DEVICE_NAME=!TEMP_NAME!" >> temp_port_%%N.bat
   echo       ^) >> temp_port_%%N.bat
   echo    ^) >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo if defined DEVICE_NAME ^( >> temp_port_%%N.bat
   echo    echo Raw device name: !DEVICE_NAME! >> temp_port_%%N.bat
   echo    echo Final device name: !DEVICE_NAME! >> temp_port_%%N.bat
   echo    set "CLEAN_NAME=!DEVICE_NAME!" >> temp_port_%%N.bat
   echo    set "CLEAN_NAME=!CLEAN_NAME: =_!" >> temp_port_%%N.bat
   echo    set "CLEAN_NAME=!CLEAN_NAME:/=_!" >> temp_port_%%N.bat
   echo    set "CLEAN_NAME=!CLEAN_NAME:\=_!" >> temp_port_%%N.bat
   echo    set "CLEAN_NAME=!CLEAN_NAME:+=_!" >> temp_port_%%N.bat
   echo    set "CLEAN_NAME=!CLEAN_NAME:'=_!" >> temp_port_%%N.bat
   echo    echo Device name detected: !CLEAN_NAME! >> temp_port_%%N.bat
   echo    set "FOLDER_PATH=!BASE_DIR!\IOP_results_!CLEAN_NAME!" >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo No device name detected or ADB command failed, using default name. >> temp_port_%%N.bat
   echo    set "CLEAN_NAME=Unknown_Device" >> temp_port_%%N.bat
   echo    set "FOLDER_PATH=!BASE_DIR!\IOP_results_!CLEAN_NAME!" >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo echo. >> temp_port_%%N.bat
   echo ssh -i id_ed25519_idcevo -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@160.48.249.99 "killall dlt-receive" >> temp_port_%%N.bat
   echo ssh -i id_ed25519_idcevo -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@160.48.249.99 "rm -f /var/data/*.dlt" >> temp_port_%%N.bat
   echo ssh -i id_ed25519_idcevo -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@160.48.249.99 "nohup dlt-receive -a localhost -o /var/data/!CLEAN_NAME!.dlt >/dev/null 2>&1 &" >> temp_port_%%N.bat
   echo for /f "usebackq delims=" %%%%i in ^("!SUITE_PATH!"^) do ^( >> temp_port_%%N.bat
   echo    echo Running %%%%i ... >> temp_port_%%N.bat
   echo    python "!TEST_DIR!\%%%%i.py" >> temp_port_%%N.bat
   echo    echo ------------------------------- >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo echo. >> temp_port_%%N.bat
   echo echo Completed test suite for USB port %%N >> temp_port_%%N.bat
   echo echo ---------------------------------------------- >> temp_port_%%N.bat
   echo echo. >> temp_port_%%N.bat
   echo echo. >> temp_port_%%N.bat
   echo ssh -i id_ed25519_idcevo -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@160.48.249.99 "killall dlt-receive" >> temp_port_%%N.bat
   echo scp -i id_ed25519_idcevo root@160.48.249.99:/var/data/!CLEAN_NAME!.dlt !BASE_DIR!\Test_results >> temp_port_%%N.bat
   echo ssh -i id_ed25519_idcevo -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@160.48.249.99 "rm -f /var/data/!CLEAN_NAME!.dlt" >> temp_port_%%N.bat
   echo python "!BASE_DIR!\Test_environment\Test_scripts\helpers\Bluetooth_logs_HU_Mobile_Device.py" >> temp_port_%%N.bat
   echo echo ============================================== >> temp_port_%%N.bat
   echo echo Creating results folder... >> temp_port_%%N.bat
   echo echo ============================================== >> temp_port_%%N.bat
   echo if exist "!FOLDER_PATH!" ^( >> temp_port_%%N.bat
   echo    rmdir /s /q "!FOLDER_PATH!" >> temp_port_%%N.bat
   echo    echo Deleted existing folder: !FOLDER_PATH! >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
   echo echo Copying results from: !RESULTS_DIR! >> temp_port_%%N.bat
   echo echo Folder destination: !FOLDER_PATH! >> temp_port_%%N.bat
   echo robocopy "!RESULTS_DIR!" "!FOLDER_PATH!" /E /R:3 /W:1 >> temp_port_%%N.bat
   echo if exist "!FOLDER_PATH!" ^( >> temp_port_%%N.bat
   echo    echo Results folder created successfully: !FOLDER_PATH! >> temp_port_%%N.bat
   echo    echo Folder contents copied from: ^^!RESULTS_DIR^^! >> temp_port_%%N.bat
   echo ^) else ^( >> temp_port_%%N.bat
   echo    echo ERROR: Folder creation failed! Check if the Results directory exists and you have proper permissions. >> temp_port_%%N.bat
   echo    echo Results directory path: !RESULTS_DIR! >> temp_port_%%N.bat
   echo    echo Intended folder path: !FOLDER_PATH! >> temp_port_%%N.bat
   echo    if exist "!RESULTS_DIR!" ^( >> temp_port_%%N.bat
   echo       echo Results directory exists. >> temp_port_%%N.bat
   echo    ^) else ^( >> temp_port_%%N.bat
   echo       echo ERROR: Results directory does not exist! >> temp_port_%%N.bat
   echo    ^) >> temp_port_%%N.bat
   echo ^) >> temp_port_%%N.bat
)

REM --- Execute each temporary batch file ---
for %%N in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16) do (
   echo.
   echo ===============================================
   echo PROCESSING USB PORT %%N
   echo ===============================================
   call temp_port_%%N.bat
)

REM --- Clean up temporary files ---
echo.
echo Cleaning up temporary files...
for %%N in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16) do (
   if exist temp_port_%%N.bat del temp_port_%%N.bat
)

echo.
echo ===============================================
echo ALL USB PORTS PROCESSED SUCCESSFULLY
echo ===============================================
