@echo off
setlocal

REM =============================================================================
REM SSH Key Permission Fixer
REM Fixes Windows file permissions for SSH private keys
REM =============================================================================

set OPENSSH_FILE=bmw_id_rsa

echo ===============================================
echo SSH Key Permission Fixer
echo ===============================================
echo Target key file: %OPENSSH_FILE%
echo ===============================================

REM Check if key file exists
if not exist "%OPENSSH_FILE%" (
    echo ERROR: Key file "%OPENSSH_FILE%" not found!
    echo Please ensure the key file is in the current directory.
    echo.
    echo If you need to convert your .ppk key first, run: convert_ppk_key.bat
    pause
    exit /b 1
)

echo.
echo Current permissions before fix:
icacls "%OPENSSH_FILE%"

echo.
echo Fixing permissions to be SSH-compatible...
echo.

REM Step 1: Remove inheritance
echo [1/4] Removing inheritance...
icacls "%OPENSSH_FILE%" /inheritance:r
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to remove inheritance
    goto :error
)

REM Step 2: Remove all existing permissions
echo [2/4] Removing all existing permissions...
icacls "%OPENSSH_FILE%" /remove:g "Everyone"
icacls "%OPENSSH_FILE%" /remove:g "Users"
icacls "%OPENSSH_FILE%" /remove:g "Authenticated Users"
icacls "%OPENSSH_FILE%" /remove:g "BUILTIN\Users"

REM Step 3: Grant full control only to current user
echo [3/4] Granting permissions only to current user (%USERNAME%)...
icacls "%OPENSSH_FILE%" /grant:r "%USERNAME%":F
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to grant permissions to user
    goto :error
)

REM Step 4: Grant full control to SYSTEM (required by Windows)
echo [4/4] Granting permissions to SYSTEM...
icacls "%OPENSSH_FILE%" /grant:r "SYSTEM":F
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to grant permissions to SYSTEM
    goto :error
)

echo.
echo ✓ Permissions fixed successfully!
echo.
echo New permissions:
icacls "%OPENSSH_FILE%"

echo.
echo ===============================================
echo VERIFICATION
echo ===============================================
echo Testing SSH key with corrected permissions...

REM Test the key with ssh-keygen
where ssh-keygen >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo.
    echo Testing key format and permissions:
    ssh-keygen -l -f "%OPENSSH_FILE%" 2>&1
    if %ERRORLEVEL% == 0 (
        echo ✓ Key is valid and permissions are correct!
        echo.
        echo You can now run: extract_dlt_logs.bat
    ) else (
        echo ⚠ Key format may still have issues, but permissions are now correct.
        echo Try running extract_dlt_logs.bat to test the connection.
    )
) else (
    echo ssh-keygen not found, but permissions have been set correctly.
    echo Try running extract_dlt_logs.bat to test the connection.
)

goto :end

:error
echo.
echo ===============================================
echo ERROR OCCURRED
echo ===============================================
echo Failed to set proper permissions.
echo.
echo ALTERNATIVE METHOD:
echo 1. Right-click on "%OPENSSH_FILE%"
echo 2. Select "Properties"
echo 3. Go to "Security" tab
echo 4. Click "Advanced"
echo 5. Click "Disable inheritance"
echo 6. Choose "Remove all inherited permissions"
echo 7. Click "Add" and add only your user account with Full control
echo 8. Click "Add" and add SYSTEM with Full control
echo 9. Apply changes
echo.
goto :end

:end
echo.
echo ===============================================
pause