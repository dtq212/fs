import os
import subprocess
import time
import win32gui
import win32con
import win32process
from tienich import BackgroundInput
from moitruong import MoiTruong

DUONGDAN_GAME = r"D:\TamGioiPhanTranhPC\game.exe"

DANH_SACH_TAI_KHOAN = [
    {"user": "taikhoan1", "pass": "matkhau1"},
    {"user": "taikhoan2", "pass": "matkhau2"},
]

def lay_hwnd_tu_pid(pid):
    hwnd_found = 0

    def callback(hwnd, _):
        nonlocal hwnd_found
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnd_found = hwnd
            except:
                pass

    win32gui.EnumWindows(callback, None)
    return hwnd_found

def kiem_tra_nhan_vat_online(hwnd):
    try:
        mt = MoiTruong(hwnd)
        if mt.get_is_nhanvattontai():
            ten = mt.get_tennhanvat()
            if ten and len(ten) > 0:
                print(f"   -> Đã vào game thành công. Tên NV: {ten}")
                return True
        return False
    except Exception as e:
        print(f"   -> Không đọc được memory (có thể do chưa update moitruong.py): {e}")
        return False

def quy_trinh_dang_nhap(account):
    user = account["user"]
    password = account["pass"]

    print(f"\n[AUTO] Bắt đầu đăng nhập cho: {user}")

    thu_muc_game = os.path.dirname(DUONGDAN_GAME)
    if not os.path.exists(DUONGDAN_GAME):
        print(f"❌ Lỗi: Không tìm thấy file game tại {DUONGDAN_GAME}")
        return

    try:
        process = subprocess.Popen(DUONGDAN_GAME, cwd = thu_muc_game)
        pid = process.pid
        print(f"   -> Đã mở game (PID: {pid}). Đang tìm cửa sổ...")
    except Exception as e:
        print(f"❌ Lỗi khi mở file exe: {e}")
        return

    hwnd = 0
    for i in range(30):
        hwnd = lay_hwnd_tu_pid(pid)
        if hwnd: break
        time.sleep(1)

    if not hwnd:
        print("❌ Quá thời gian chờ, không tìm thấy cửa sổ game.")
        return

    print(f"   -> Đã thấy cửa sổ (HWND: {hwnd}).")

    print("   -> Chờ 10s để load tài nguyên...")
    time.sleep(10)

    print("   -> Ấn Enter (1)")
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)

    time.sleep(1)

    print("   -> Ấn Enter (2)")
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)
    time.sleep(1)

    print(f"   -> Nhập tài khoản: {user}")
    BackgroundInput.type_text(hwnd, user)
    time.sleep(0.5)

    print("   -> Ấn Tab")
    BackgroundInput.press_key(hwnd, win32con.VK_TAB)
    time.sleep(0.5)

    print("   -> Nhập mật khẩu")
    BackgroundInput.type_text(hwnd, password)
    time.sleep(0.5)

    print("   -> Ấn Enter (Xác nhận Login)")
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)

    print("   -> Chờ 5s...")
    time.sleep(5)

    print("   -> Ấn Enter (Vào game)")
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)

    print("   -> Chờ 5s load map...")
    time.sleep(5)

    print("   -> Kiểm tra trạng thái nhân vật...")
    if kiem_tra_nhan_vat_online(hwnd):
        print(f"✅ Đăng nhập thành công cho {user}!")
    else:
        print(f"⚠️ Không thấy tên nhân vật. Đóng game để thử lại sau.")
        try:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        except:
            pass

def main():
    print("=== AUTO LOGIN PHONG THẦN ===")
    for acc in DANH_SACH_TAI_KHOAN:
        quy_trinh_dang_nhap(acc)
        print("   -> Nghỉ 5s trước khi log acc tiếp theo...")
        time.sleep(5)


if __name__ == "__main__":
    main()