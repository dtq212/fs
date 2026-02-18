import time
import os
import win32gui
import tkinter as tk
from multiprocessing import Process, Manager, freeze_support
from cuaso import CuaSo
from giaodienhienthi import GiaoDienHienThi


def run_bot_process(hwnd, shared_data):
    try:
        print(f"--> [DEBUG] Đang khởi tạo Bot cho HWND: {hwnd}")
        bot = CuaSo(hwnd, shared_data)
        while not bot.main_stop.is_set():
            if not win32gui.IsWindow(hwnd):
                break
            time.sleep(1)
        bot.tatauto()
    except Exception as e:
        print(f"--> [ERROR] Bot Crash (HWND {hwnd}): {e}")


class TroChoiManager:
    def __init__(self):
        self.manager = Manager()
        self.shared_data = self.manager.dict()
        self.bot_processes = {}

    def _timcuasogame(self):
        ds_hwnd = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and "Fs1: " in title:
                    ds_hwnd.append(hwnd)

        win32gui.EnumWindows(callback, None)
        return ds_hwnd

    def run(self):
        root = tk.Tk()
        gui = GiaoDienHienThi(root, self.shared_data)

        import threading
        t_scan = threading.Thread(target = self.loop_scan, daemon = True)
        t_scan.start()

        print("--- ĐANG CHẠY MANAGER ---")
        print("Lưu ý: Phải chạy bằng quyền Administrator để đọc được tên nhân vật!")

        try:
            root.mainloop()
        except KeyboardInterrupt:
            pass
        self.stop_all()

    def loop_scan(self):
        while True:
            game_hwnds = self._timcuasogame()

            for hwnd in game_hwnds:
                if hwnd not in self.bot_processes:
                    print(f"Phát hiện cửa sổ mới: {hwnd} -> Đang thử kết nối...")
                    p = Process(target = run_bot_process, args = (hwnd, self.shared_data))
                    p.start()
                    self.bot_processes[hwnd] = p

            dead = [h for h, p in self.bot_processes.items() if not p.is_alive()]
            for h in dead:
                print(f"Bot {h} đã dừng.")
                del self.bot_processes[h]
                if h in self.shared_data: del self.shared_data[h]

            time.sleep(2)

    def stop_all(self):
        for p in self.bot_processes.values(): p.terminate()
        os._exit(0)


if __name__ == "__main__":
    freeze_support()
    TroChoiManager().run()