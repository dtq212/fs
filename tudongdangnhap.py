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
    #{"user": "kngaivacham", "pass": "hateva12", "char_name": "KNgạiVaChạm"},
    {"user": "thichvacham2", "pass": "hateva12", "char_name": "ThíchVaChạm"},
    {"user": "laotsezu1", "pass": "hateva12", "char_name": "LaotsezuI"},
    {"user": "laotsezu2", "pass": "hateva12", "char_name": "LaotsezuII"},
    {"user": "laotsezu3", "pass": "hateva12", "char_name": "LaotsezuIII"},
    {"user": "laotsezu4", "pass": "hateva12", "char_name": "LaotsezuIV"},
    {"user": "laotsezu5", "pass": "hateva12", "char_name": "LaotsezuV"},
    {"user": "laotsezu6", "pass": "hateva12", "char_name": "LaotsezuVI"},
    {"user": "laotsezu7", "pass": "hateva12", "char_name": "LaotsezuVII"},
    {"user": "laotsezu8", "pass": "hateva12", "char_name": "LaotsezuVVIII"},
    {"user": "laotsezu9", "pass": "hateva12", "char_name": "LaotsezuIX"},
    {"user": "laotsezu10", "pass": "hateva12", "char_name": "LaotsezuX"},
    {"user": "laotsezu11", "pass": "hateva12", "char_name": "LaotsezuXI"},
    {"user": "laotsezu12", "pass": "hateva12", "char_name": "LaotsezuXII"},
    #{"user": "laotsezu13", "pass": "hateva12", "char_name": "LaotsezuXIII"},
]

THOI_GIAN_QUET_LAI = 5

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


def lay_danh_sach_nhan_vat_online():
    ds_online = []
    print(f"[{time.strftime('%H:%M:%S')}] 🔍 Đang quét các cửa sổ game (Fs1:)...")

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)

            if "Fs1:" in title:
                try:
                    moitruong = MoiTruong(hwnd)

                    if moitruong.get_is_nhanvattontai():
                        tennhanvat = moitruong.get_tennhanvat()
                        if tennhanvat:
                            print(f"   -> Thấy cửa sổ '{title}' đang online nhân vật: {tennhanvat}")
                            ds_online.append(tennhanvat)
                    else:
                        print(f"   -> Thấy cửa sổ '{title}' nhưng chưa đăng nhập nhân vật.")
                except Exception as e:
                    pass

    win32gui.EnumWindows(callback, None)
    return ds_online

def force_kill_window(hwnd):
    try:
        if not hwnd: return
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        print(f"   -> Đang Force Kill process PID: {pid} để bỏ qua popup xác nhận...")
        subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"❌ Lỗi khi kill game: {e}")

def quy_trinh_dang_nhap(account):
    user = account["user"]
    password = account["pass"]
    char_name = account.get("char_name", "Unknown")

    print(f"\n▶️ Bắt đầu login: {user} (NV: {char_name})")

    thu_muc_game = os.path.dirname(DUONGDAN_GAME)
    if not os.path.exists(DUONGDAN_GAME):
        print(f"❌ Lỗi: Không tìm thấy file game tại {DUONGDAN_GAME}")
        return

    try:
        process = subprocess.Popen(DUONGDAN_GAME, cwd = thu_muc_game)
        pid = process.pid
        print(f"   -> Đã mở game (PID: {pid}). Đang đợi cửa sổ xuất hiện...")
    except Exception as e:
        print(f"❌ Lỗi khi mở file exe: {e}")
        return

    hwnd = 0
    for i in range(30):
        hwnd = lay_hwnd_tu_pid(pid)
        if hwnd:
            time.sleep(1)
            break
        time.sleep(1)

    if not hwnd:
        print("❌ Quá thời gian chờ, không tìm thấy cửa sổ game.")
        return

    print(f"   -> Đã bắt được cửa sổ (HWND: {hwnd}).")
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
    print("   -> Chờ 10s để game tải tài nguyên...")
    time.sleep(6)

    print("   -> Ấn Enter (Vào màn hình đăng nhập)")
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)
    time.sleep(1)
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)
    time.sleep(2)

    print(f"   -> Nhập tài khoản: {user}")
    BackgroundInput.type_text(hwnd, user)
    time.sleep(1)

    print("   -> Click vào ô mật khẩu")
    BackgroundInput.click(hwnd, 403, 289)
    time.sleep(1)

    print("   -> Nhập mật khẩu")
    BackgroundInput.type_text(hwnd, password)
    time.sleep(1)

    print("   -> Ấn Enter (Login)")
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)

    print("   -> Chờ 5s server phản hồi...")
    time.sleep(2)

    print("   -> Ấn Enter (Chọn nhân vật/Vào game)")
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)

    time.sleep(2)
    BackgroundInput.press_key(hwnd, win32con.VK_RETURN)

    print("   -> Chờ 5s để vào map...")
    time.sleep(5)

    try:
        moitruong = MoiTruong(hwnd)
        if moitruong.get_is_nhanvattontai():
            tennhanvat = moitruong.get_tennhanvat()
            print(f"✅ Đăng nhập hoàn tất! Đang online nhân vật: {tennhanvat}")
        else:
            force_kill_window(hwnd)
    except:
        pass


def main():
    print("=== AUTO LOGIN PHONG THẦN (WINDOW TITLE: Fs1:) ===")
    print(f"Chế độ: Chạy liên tục (Quét mỗi {THOI_GIAN_QUET_LAI}s)")
    print("Nhấn Ctrl + C tại cửa sổ này để dừng tool.\n")

    while True:
        try:
            nhan_vat_dang_online = lay_danh_sach_nhan_vat_online()
            so_luong_can_login = 0

            for acc in DANH_SACH_TAI_KHOAN:
                char_name = acc.get("char_name", "")
                user = acc["user"]

                if char_name in nhan_vat_dang_online:
                    continue
                else:
                    print(f"⚠️ Phát hiện tài khoản {user} (NV: {char_name}) chưa online.")
                    quy_trinh_dang_nhap(acc)
                    so_luong_can_login += 1

                    print("💤 Nghỉ 10s trước khi xử lý acc tiếp theo...")
                    time.sleep(10)

            if so_luong_can_login == 0:
                print(f"✅ Tất cả {len(DANH_SACH_TAI_KHOAN)} tài khoản đều đang online.")

            print(f"⏳ Chờ {THOI_GIAN_QUET_LAI} giây quét lại...")
            time.sleep(THOI_GIAN_QUET_LAI)

        except KeyboardInterrupt:
            print("\nĐã dừng tool thủ công.")
            break
        except Exception as e:
            print(f"\n❌ Lỗi không xác định trong vòng lặp chính: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()