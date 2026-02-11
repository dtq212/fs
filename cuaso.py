import os
import threading
import time

import keyboard
from infi.systray import SysTrayIcon

from hangso import *
from loop import (
    LoopTimKiemMucTieu,
    LoopChinh,
    LoopPhu,
)
from moitruong import MoiTruong
from tactu import TacTu

def khoidong_looptimkiemmuctieu(moitruong, tactu, stop):
    LoopTimKiemMucTieu(moitruong, tactu, stop).loop()

def khoidong_loopchinh(moitruong, tactu, stop):
    LoopChinh(moitruong, tactu, stop).loop()


def khoidong_loopphu(moitruong, tactu, stop):
    LoopPhu(moitruong, tactu, stop).loop()

class CuaSo:
    def __init__(self, idcuaso):
        self.moitruong = MoiTruong(idcuaso)
        self.tactu = TacTu(self.moitruong)
        self.tennhanvat = False
        self.dbidnhanvat = 0
        self.main_stop = threading.Event()

        self.luongs = (
            threading.Thread(target = khoidong_looptimkiemmuctieu, args = [self.moitruong, self.tactu, self.main_stop], daemon = True),
            threading.Thread(target = khoidong_loopchinh, args = [self.moitruong, self.tactu, self.main_stop], daemon = True),
            threading.Thread(target = khoidong_loopphu, args = [self.moitruong, self.tactu, self.main_stop], daemon = True),
        )

        for luong in self.luongs:
            luong.start()

        threading.Thread(target = self.loop_xulyphimtat, daemon = True).start()

        icon_path = os.path.join("_internal", "icon", "icon.ico")
        if not os.path.exists(icon_path):
            icon_path = None

        titlebandau = f"{CHUACHONHANVAT} ({idcuaso})"
        self.systray = SysTrayIcon(icon_path, titlebandau, on_quit = self.tatauto)
        self.systray.start()

        self.thoidiemluuthietlapgannhat = time.time()

    def __del__(self):
        self.tatauto()

    def _chotoanbocacluongdunghan(self):
        for luong in self.luongs:
            if luong.is_alive():
                luong.join(timeout = 0.2)

    def tatauto(self, *args, **kwargs):
        self.main_stop.set()

        self._chotoanbocacluongdunghan()

        try:
            self.systray.shutdown()
        except:
            pass

    def loop(self):
        title = None
        thoigianmatketnoi = 0

        while not self.main_stop.is_set() and self.moitruong.get_is_cuasogametontai():
            if not self.moitruong.get_is_dangmatketnoi():
                thoigianmatketnoi = 0

                tennhanvat = self.moitruong.get_tennhanvat()
                dbidnhanvat = self.moitruong.get_dbidnhanvat()

                if dbidnhanvat != self.dbidnhanvat:
                    if dbidnhanvat:
                        if self.dbidnhanvat:
                            self.tactu.luuthietlap(self.dbidnhanvat)
                        self.tactu.taithietlap(dbidnhanvat)
                        if tennhanvat and tennhanvat != title:
                            self.systray.update(hover_text = tennhanvat)
                            title = tennhanvat
                    elif self.dbidnhanvat:
                        self.tactu.luuthietlap(self.dbidnhanvat)
                        if CHUACHONHANVAT != title:
                            self.systray.update(hover_text = CHUACHONHANVAT)
                            title = CHUACHONHANVAT

                    self.dbidnhanvat = dbidnhanvat
                    self.tennhanvat = tennhanvat

                elif dbidnhanvat and time.time() - self.thoidiemluuthietlapgannhat > 1.:
                    self.thoidiemluuthietlapgannhat = time.time()
                    self.tactu.luuthietlap(dbidnhanvat)
            else:
                self.tennhanvat = False
                self.dbidnhanvat = 0

                if CHUACHONHANVAT != title:
                    self.systray.update(hover_text = CHUACHONHANVAT)
                    title = CHUACHONHANVAT

                if thoigianmatketnoi == 0:
                    thoigianmatketnoi = time.time()
                elif time.time() - thoigianmatketnoi > 1.:
                    break

            time.sleep(1)

        self.tatauto()

    def loop_xulyphimtat(self):
        while not self.main_stop.is_set():
            if self.moitruong.get_is_cuasogamekichhoat():

                if keyboard.is_pressed("ctrl+alt+shift+h"):
                    self.tactu.battat_tudongvebanrac()
                    time.sleep(0.3)

                if keyboard.is_pressed("ctrl+alt+shift+r"):
                    self.tactu.battat_tudongsuavatpham()
                    time.sleep(0.3)

                if keyboard.is_pressed("ctrl+alt+shift+t"):
                    self.tactu.action_test()
                    time.sleep(0.3)

            time.sleep(0.05)