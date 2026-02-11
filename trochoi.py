import os
import subprocess
import sys
import threading
import time
import signal

import keyboard
import win32api
import win32event
import win32gui
import winerror

from cuaso import CuaSo
from moitruong import MoiTruong
from tienich import phatam

CREATE_NO_WINDOW = 0x08000000
VK_F11 = 0x7A
VK_CONTROL = 0x11

def loop_cuaso(cuaso: CuaSo):
    try:
        cuaso.loop()
    except:
        pass


class TroChoiWorker:
    def __init__(self, target_hwnd):
        self.cuaso = None
        self.target_hwnd = target_hwnd
        self.is_dangchay = threading.Event()

    def khoidong(self):
        if not win32gui.IsWindow(self.target_hwnd):
            return

        self.cuaso = CuaSo(self.target_hwnd)

        if not self._kiemtranhanvathople():
            return

        threading.Thread(target = loop_cuaso, args = [self.cuaso], daemon = True).start()
        self.loop_quanly()

    def _kiemtranhanvathople(self):
        try:
            if not self.cuaso.moitruong.get_is_nhanvattontai():
                return False
            tennhanvat = self.cuaso.moitruong.get_tennhanvat()
            if not tennhanvat or len(tennhanvat) == 0:
                return False
            return True
        except:
            return False

    def loop_quanly(self):
        thoigianmatnhanvat = 0

        while not self.is_dangchay.is_set():
            try:
                if not win32gui.IsWindow(self.target_hwnd):
                    os.kill(os.getpid(), signal.SIGTERM)
                    break

                if self.cuaso.main_stop.is_set():
                    self.is_dangchay.set()
                    break

                if win32api.GetAsyncKeyState(VK_CONTROL) & 0x8000 and win32api.GetAsyncKeyState(VK_F11) & 0x8000:
                    self.is_dangchay.set()
                    break

                if not self._kiemtranhanvathople():
                    if thoigianmatnhanvat == 0:
                        thoigianmatnhanvat = time.time()
                    elif time.time() - thoigianmatnhanvat > 2:
                        os.kill(os.getpid(), signal.SIGTERM)
                        break
                else:
                    thoigianmatnhanvat = 0

            except Exception:
                os.kill(os.getpid(), signal.SIGTERM)
                break

            time.sleep(0.5)

        if self.cuaso:
            try:
                self.cuaso.main_stop.set()
                if hasattr(self.cuaso, "systray"):
                    self.cuaso.systray.shutdown()
            except:
                pass

        os._exit(0)


class TroChoiManager:
    def __init__(self):
        self.tientrinhautos = {}
        self.lock = threading.Lock()
        self.is_running = True
        self.current_metric = None

        print("=" * 50)
        print("TOOL PHONG THẦN")
        print("-" * 50)
        print("Nhấn phím Ctrl + F11 để dừng toàn bộ!")
        print("=" * 50)

    def stop_all(self):
        print("\nĐang dừng toàn bộ hệ thống...")
        self.is_running = False
        with self.lock:
            for hwnd, proc in self.tientrinhautos.items():
                try:
                    proc.kill()
                except:
                    pass
        time.sleep(1)
        os._exit(0)

    def _timcuasogame(self):
        ds_hwnd = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and "Fs1: " in title:
                    ds_hwnd.append(hwnd)

        win32gui.EnumWindows(callback, None)
        return ds_hwnd

    def _kiemtradudieukienkichhoatauto(self, hwnd):
        try:
            moitruong = MoiTruong(hwnd)
            if not moitruong.get_is_nhanvattontai():
                return False
            tennhanvat = moitruong.get_tennhanvat()
            if not tennhanvat or len(tennhanvat) == 0:
                return False
            return True
        except Exception as err:
            raise
            return False

    def _kichhoatauto(self, hwnd):
        with self.lock:
            if hwnd in self.tientrinhautos:
                return

            print(f"-> Phát hiện cửa sổ {hwnd} đã vào game -> Kích hoạt Auto!")

            script_path = os.path.abspath(__file__)
            cmd = [sys.executable, "-u", script_path, "--child", str(hwnd)]

            try:
                proc = subprocess.Popen(cmd, stdout = sys.stdout, stderr = sys.stderr)
                self.tientrinhautos[hwnd] = proc
            except Exception:
                pass

    def run(self):
        time.sleep(1)
        while self.is_running:
            if win32api.GetAsyncKeyState(VK_CONTROL) & 0x8000 and win32api.GetAsyncKeyState(VK_F11) & 0x8000:
                self.stop_all()
                break

            with self.lock:
                dead_hwnds = []
                for h, p in self.tientrinhautos.items():
                    if p.poll() is not None:
                        dead_hwnds.append(h)

                for h in dead_hwnds:
                    del self.tientrinhautos[h]

            game_hwnds = self._timcuasogame()
            for hwnd in game_hwnds:
                if hwnd not in self.tientrinhautos:
                    if self._kiemtradudieukienkichhoatauto(hwnd):
                        self._kichhoatauto(hwnd)

            time.sleep(0.5)


if __name__ == "__main__":
    if "--child" in sys.argv:
        try:
            idx = sys.argv.index("--child")
            target_hwnd = int(sys.argv[idx + 1])
            worker = TroChoiWorker(target_hwnd)
            worker.khoidong()
        except Exception:
            os.kill(os.getpid(), signal.SIGTERM)
    else:
        mutex_name = "Global_Tool_PhongThan_Manager_Mutex"
        mutex = win32event.CreateMutex(None, True, mutex_name)

        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            phatam("Tool quản lý đang chạy rồi")
            time.sleep(2)
            sys.exit(0)

        manager = TroChoiManager()
        try:
            manager.run()
        except KeyboardInterrupt:
            pass