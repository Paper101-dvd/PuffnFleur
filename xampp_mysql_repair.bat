@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "XAMPP_ROOT="
set "MYSQL_DIR="
set "DATA_DIR=D:\data\db"

if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe" (
  set "XAMPP_ROOT=C:\Program Files\MySQL\MySQL Server 8.0"
  set "MYSQL_DIR=C:\Program Files\MySQL\MySQL Server 8.0"
  goto found_xampp
)

for %%D in (
  C:\xampp
  D:\xampp
  E:\xampp
  C:\XAMPP
  D:\XAMPP
  E:\XAMPP
  C:\Program Files\xampp
  D:\Program Files\xampp
  E:\Program Files\xampp
  C:\Program Files\XAMPP
  D:\Program Files\XAMPP
  E:\Program Files\XAMPP
) do (
  if exist "%%~fD\mysql\bin\mysqld.exe" (
    set "XAMPP_ROOT=%%~fD"
    set "MYSQL_DIR=%%~fD\mysql"
    goto found_xampp
  )
)

:found_xampp
if not defined MYSQL_DIR (
  echo XAMPP was not detected automatically.
  echo Using the MySQL data folder you provided: %DATA_DIR%
  set "XAMPP_ROOT=D:\xampp"
  set "MYSQL_DIR=D:\xampp\mysql"
)

echo XAMPP root: %XAMPP_ROOT%
echo MySQL data folder: %DATA_DIR%

if not exist "%MYSQL_DIR%\bin\mysqld.exe" (
  echo MySQL binary was not found at "%MYSQL_DIR%\bin\mysqld.exe".
  echo Update MYSQL_DIR in this script if your XAMPP install is elsewhere.
  pause
  exit /b 1
)

echo Stopping MySQL processes...
taskkill /F /IM mysqld.exe 2>nul
taskkill /F /IM mysqld-nt.exe 2>nul
taskkill /F /IM mysqld_safe.exe 2>nul

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set "DT=%%I"
for %%F in ("%DATA_DIR%") do set "DATA_NAME=%%~nxF"
for %%F in ("%DATA_DIR%") do set "BACKUP_DIR=%%~dpF!DATA_NAME!_backup_%DT:~0,8%_%DT:~8,6%"

if exist "%DATA_DIR%" (
  echo Backing up existing data directory...
  if exist "%BACKUP_DIR%" rmdir /s /q "%BACKUP_DIR%"
  ren "%DATA_DIR%" "!DATA_NAME!_backup_%DT:~0,8%_%DT:~8,6%"
)

mkdir "%DATA_DIR%" 2>nul
pushd "%MYSQL_DIR%\bin"
mysqld --initialize-insecure --console
popd

echo.
echo MySQL has been reinitialized.
echo.
echo Next steps:
echo 1. Start MySQL from XAMPP Control Panel.
echo 2. Open phpMyAdmin.
echo 3. Login with user root and password blank unless you set one.
echo.
echo If you had important databases, restore them from the backup directory:
echo %BACKUP_DIR%
pause
