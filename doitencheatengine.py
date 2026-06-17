import win32gui
import time


def hide_window_title(target_substring, new_name):
    def callback(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)
        if target_substring in title:
            print(f"[*] Phát hiện cửa sổ: '{title}' (HWND: {hwnd})")
            try:
                win32gui.SetWindowText(hwnd, new_name)
                print(f"[+] Đã đổi tên thành công: '{new_name}'\n")
            except Exception as e:
                print(f"[-] Lỗi khi đổi tên (HWND: {hwnd}): {e}\n")
    win32gui.EnumWindows(callback, None)

if __name__ == "__main__":
    FAKE_NAME = "Chrome"

    try:
        while True:
            hide_window_title("Cheat Engine", FAKE_NAME)
            hide_window_title("The following opcodes", FAKE_NAME)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("Đã dừng kịch bản.")