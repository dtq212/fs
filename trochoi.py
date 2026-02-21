import time
import os
import win32gui
import tkinter as tk
import keyboard
from multiprocessing import Process, Manager, freeze_support
from cuaso import CuaSo
from giaodienhienthi import GiaoDienHienThi

def run_bot_process(hwnd, shared_data, command_dict): # Thêm tham số command_dict
    try:
        bot = CuaSo(hwnd, shared_data, command_dict) # Truyền xuống CuaSo
        while not bot.main_stop.is_set():
            if not win32gui.IsWindow(hwnd):
                break
            time.sleep(1)
        bot.tatauto()
    except Exception as e:
        pass

class TroChoiManager:
    def __init__(self):
        self.manager = Manager()
        self.shared_data = self.manager.dict()
        self.command_dict = self.manager.dict() # Kênh truyền lệnh phím tắt
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

        # Khởi chạy luồng bắt phím tập trung
        t_hotkey = threading.Thread(target = self.loop_hotkey, daemon = True)
        t_hotkey.start()

        print("--- ĐANG CHẠY MANAGER ---")
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
                    # Truyền thêm self.command_dict vào Process
                    p = Process(target = run_bot_process, args = (hwnd, self.shared_data, self.command_dict))
                    p.start()
                    self.bot_processes[hwnd] = p

            dead = [h for h, p in self.bot_processes.items() if not p.is_alive()]
            for h in dead:
                del self.bot_processes[h]
                if h in self.shared_data: del self.shared_data[h]
                if h in self.command_dict: del self.command_dict[h] # Dọn dẹp rác

            time.sleep(2)

    def loop_hotkey(self):
        while True:
            hwnd = win32gui.GetForegroundWindow() # Chỉ bắt phím cho tab đang active
            if hwnd in self.bot_processes:
                cmd = None
                if keyboard.is_pressed("ctrl+alt+shift+h"): cmd = "battat_tudongfarmvabanrac"
                elif keyboard.is_pressed("ctrl+alt+shift+r"): cmd = "battat_tudongsuavatpham"
                elif keyboard.is_pressed("ctrl+alt+shift+y"): cmd = "action_test"
                elif keyboard.is_pressed("ctrl+alt+shift+t"): cmd = "battat_tudongdanhtheosautruongnhom"
                elif keyboard.is_pressed("ctrl+alt+shift+f"): cmd = "battat_tudongtimkiemmuctieu"
                elif keyboard.is_pressed("ctrl+alt+shift+b"): cmd = "battat_is_khongdanhcungbang"
                elif keyboard.is_pressed("ctrl+alt+shift+j"): cmd = "battat_is_tudongbattathieuungbotro"
                elif keyboard.is_pressed("ctrl+alt+shift+k"): cmd = "battat_is_tudongmokhoa"
                elif keyboard.is_pressed("ctrl+alt+c"): cmd = "botoanbo_tennhanvattancong"
                elif keyboard.is_pressed("ctrl+alt+x"): cmd = "botoanbo_tennhanvatkhongtancong"
                elif keyboard.is_pressed("ctrl+c"): cmd = "them_tennhanvattancong"
                elif keyboard.is_pressed("ctrl+x"): cmd = "them_tennhanvatkhongtancong"
                elif keyboard.is_pressed("ctrl+d"): cmd = "bat_is_chidanhnguoichoivatrieuhoithu"
                elif keyboard.is_pressed("ctrl+a"): cmd = "tat_is_chidanhnguoichoivatrieuhoithu"
                elif keyboard.is_pressed("ctrl+e"): cmd = "action_batpk"
                elif keyboard.is_pressed("ctrl+q"): cmd = "action_tatpk"

                if cmd:
                    self.command_dict[hwnd] = cmd
                    time.sleep(0.3)
            time.sleep(0.05) 

    def stop_all(self):
        for p in self.bot_processes.values(): p.terminate()
        os._exit(0)

if __name__ == "__main__":
    freeze_support()
    TroChoiManager().run()