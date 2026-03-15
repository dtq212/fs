@echo off
setlocal

rem --- CẤU HÌNH ĐƯỜNG DẪN DỰA TRÊN ẢNH CỦA BẠN ---
set NDK_PATH=D:\Program Files\Android
rem Trỏ thẳng vào file make.exe mà bạn vừa chụp ảnh thấy trong thư mục bin
set MAKE_EXE=%NDK_PATH%\prebuilt\windows-x86_64\bin\make.exe
rem ----------------------------------------------

echo [1/3] Dang don dep thu muc build...
if exist build rmdir /s /q build
mkdir build
cd build

echo [2/3] Dang cau hinh CMake bang Make (NDK r27d)...
cmake -G "Unix Makefiles" ^
    -DCMAKE_MAKE_PROGRAM="%MAKE_EXE%" ^
    -DCMAKE_TOOLCHAIN_FILE="%NDK_PATH%\build\cmake\android.toolchain.cmake" ^
    -DANDROID_ABI=x86 ^
    -DANDROID_PLATFORM=android-21 ^
    -DCMAKE_BUILD_TYPE=Release ^
    ..

echo [3/3] Dang bat dau bien dich...
"%MAKE_EXE%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =============================================
    echo THANH CONG! File .so nam tai:
    echo %cd%\libautofarm_core.so
    echo =============================================
) else (
    echo.
    echo [!] CO LOI XAY RA TRONG QUA TRINH BUILD.
)

pause