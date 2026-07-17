import os
import time
import tkinter as tk
import traceback
from multiprocessing import Process, Manager, freeze_support

import keyboard
import win32gui

from cuaso_fs import CuaSo
from giaodienhienthi_fs import GiaoDienHienThi

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def run_bot_process(hwnd, shared_data, command_dict):
    try:
        bot = CuaSo(hwnd, shared_data, command_dict)
        while not bot.main_stop.is_set():
            if not win32gui.IsWindow(hwnd):
                break
            time.sleep(1)
        bot.tatauto()
    except Exception as e:
        print(f"\n[CRASH TẠI PROCESS CON - HWND {hwnd}]:")
        traceback.print_exc()
        time.sleep(10)


class TroChoiManager:
    def __init__(self):
        self.manager = Manager()
        self.shared_data = self.manager.dict()
        self.command_dict = self.manager.dict()
        self.bot_processes = {}

    def _timcuasogame(self):
        ds_hwnd = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and "TGPC:" in title:
                    ds_hwnd.append(hwnd)

        win32gui.EnumWindows(callback, None)
        return ds_hwnd

    def run(self):
        root = tk.Tk()
        gui = GiaoDienHienThi(root, self.shared_data, self.command_dict)

        import threading
        t_scan = threading.Thread(target = self.loop_scan, daemon = True)
        t_scan.start()

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
                    p = Process(target = run_bot_process, args = (hwnd, self.shared_data, self.command_dict))
                    p.start()
                    self.bot_processes[hwnd] = p

            dead = [h for h, p in self.bot_processes.items() if not p.is_alive()]
            for h in dead:
                del self.bot_processes[h]
                if h in self.shared_data: del self.shared_data[h]
                if h in self.command_dict: del self.command_dict[h]  # Dọn dẹp rác

            time.sleep(2)

    def loop_hotkey(self):
        while True:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd in self.bot_processes:
                cmd = None
                if keyboard.is_pressed("ctrl+alt+shift+c"):
                    cmd = "battat_is_danhtheotennhanvat"
                elif keyboard.is_pressed("ctrl+alt+shift+u"):
                    cmd = "action_test"
                elif keyboard.is_pressed("ctrl+alt+shift+y"):
                    cmd = "action_mua1thancauphu"
                elif keyboard.is_pressed("ctrl+alt+shift+t"):
                    cmd = "battat_tudongdanhtheosautruongnhom"
                elif keyboard.is_pressed("ctrl+alt+shift+f"):
                    cmd = "battat_tudongtimkiemmuctieu"
                elif keyboard.is_pressed("ctrl+alt+shift+b"):
                    cmd = "battat_is_khongdanhcungbang"
                elif keyboard.is_pressed("ctrl+alt+shift+j"):
                    cmd = "battat_is_tudongbattathieuungbotro"
                elif keyboard.is_pressed("ctrl+alt+shift+k"):
                    cmd = "battat_is_giukhoangcach"
                elif keyboard.is_pressed("ctrl+alt+shift+l"):
                    cmd = "battat_is_tudongmokhoa"
                elif keyboard.is_pressed("ctrl+alt+shift+w"):
                    cmd = "battat_is_tudongdoisetdo"
                elif keyboard.is_pressed("ctrl+alt+shift+p"):
                    cmd = "battat_is_duoitheo"
                elif keyboard.is_pressed("ctrl+alt+shift+o"):
                    cmd = "battat_is_khongsudungnhieukynang"
                elif keyboard.is_pressed("ctrl+alt+shift+n"):
                    cmd = "battat_phucsinhnhanh"
                elif keyboard.is_pressed("ctrl+alt+shift+m"):
                    cmd = "battat_is_tudongmuavatphamkytrancac"
                elif keyboard.is_pressed("ctrl+alt+c"):
                    cmd = "botoanbo_tennhanvattancong"
                elif keyboard.is_pressed("ctrl+alt+x"):
                    cmd = "botoanbo_tennhanvatkhongtancong"
                elif keyboard.is_pressed("ctrl+alt+v"):
                    cmd = "botoanbo_tennhanvattodoitudong"
                elif keyboard.is_pressed("ctrl+alt+1"):
                    cmd = "luusetdo_1"
                elif keyboard.is_pressed("ctrl+alt+2"):
                    cmd = "luusetdo_2"
                elif keyboard.is_pressed("ctrl+q"):
                    cmd = "action_tatpk"
                elif keyboard.is_pressed("ctrl+e"):
                    cmd = "action_batpk"
                elif keyboard.is_pressed("ctrl+c"):
                    cmd = "them_tennhanvattancong"
                elif keyboard.is_pressed("ctrl+x"):
                    cmd = "them_tennhanvatkhongtancong"
                elif keyboard.is_pressed("ctrl+v"):
                    cmd = "them_tennhanvattodoitudong"
                elif keyboard.is_pressed("ctrl+d"):
                    cmd = "bat_is_chidanhnguoichoivatrieuhoithu"
                elif keyboard.is_pressed("ctrl+s"):
                    cmd = "battat_is_uutientrieuhoithu"
                elif keyboard.is_pressed("ctrl+a"):
                    cmd = "tat_is_chidanhnguoichoivatrieuhoithu"
                elif keyboard.is_pressed("ctrl+g"):
                    cmd = "battat_is_sudungkynangtoadochichuot"
                elif keyboard.is_pressed("ctrl+alt+shift+z"):
                    cmd = "battat_is_khonguutiengiapsi"
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