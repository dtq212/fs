import os
import shutil
import py_compile
import subprocess

# --- CẤU HÌNH ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(PROJECT_DIR, "build_temp")
VENV_DIR = os.path.join(PROJECT_DIR, ".venv")
OUTPUT_EXE = "AutoPhongThan_Debug.exe"  # Đổi tên thành bản Debug

WINRAR_PATH = r"C:\Program Files\WinRAR\WinRAR.exe"


def main():
    print("🚀 BẮT ĐẦU BUILD BẢN DEBUG ĐỂ TÌM LỖI...")

    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)

    if os.path.exists(os.path.join(PROJECT_DIR, OUTPUT_EXE)):
        os.remove(os.path.join(PROJECT_DIR, OUTPUT_EXE))

    print("1. Đang biên dịch mã nguồn sang bytecode (.pyc)...")
    for file in os.listdir(PROJECT_DIR):
        if file.endswith(".py") and file != os.path.basename(__file__):
            file_goc = os.path.join(PROJECT_DIR, file)
            file_dich = os.path.join(BUILD_DIR, file + "c")
            py_compile.compile(file_goc, cfile = file_dich)

    print("2. Đang copy môi trường Python (.venv)...")
    shutil.copytree(VENV_DIR, os.path.join(BUILD_DIR, ".venv"))

    print("3. Tạo file khởi chạy Debug (hiện CMD và Pause)...")
    bat_content = """@echo off
cd /d "%~dp0"
echo Dang khoi chay Python...
".venv\\Scripts\\python.exe" "trochoi.pyc"
echo.
echo ===================================
echo Tool da bi dong (Crash). Xem loi o tren!
pause
"""
    with open(os.path.join(BUILD_DIR, "run_debug.bat"), "w") as f:
        f.write(bat_content)

    print("4. Tạo cấu hình đóng gói SFX (Bỏ chế độ TempMode)...")
    sfx_config = """Path=AutoPhongThan_Data
    Setup=run_debug.bat
    Silent=1
    Overwrite=1
    """
    config_path = os.path.join(BUILD_DIR, "sfx_config.txt")
    with open(config_path, "w") as f:
        f.write(sfx_config)


    print("5. Đang nén thành 1 file EXE duy nhất (Vui lòng chờ)...")
    if not os.path.exists(WINRAR_PATH):
        print(f"❌ LỖI: Không tìm thấy WinRAR tại {WINRAR_PATH}")
        return

    items_to_add = [f for f in os.listdir(BUILD_DIR)]

    rar_cmd = [
                  WINRAR_PATH, "a", "-sfx", f"-z{config_path}",
                  os.path.join(PROJECT_DIR, OUTPUT_EXE)
              ] + items_to_add

    subprocess.run(rar_cmd, stdout = subprocess.DEVNULL, cwd = BUILD_DIR)

    print("6. Đang dọn dẹp file tạm...")
    shutil.rmtree(BUILD_DIR)

    print(f"\n✅ THÀNH CÔNG! File của bạn đã sẵn sàng tại: {os.path.join(PROJECT_DIR, OUTPUT_EXE)}")


if __name__ == "__main__":
    main()