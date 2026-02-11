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
        self.idnguoichoi = 0
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

        title_ban_dau = f"{CHUACHONHANVAT} ({idcuaso})"
        self.systray = SysTrayIcon(icon_path, title_ban_dau, on_quit = self.tatauto)
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
        last_hover_text = None
        thoi_gian_mat_ket_noi = 0

        while not self.main_stop.is_set() and self.moitruong.get_is_cuasogametontai():
            if not self.moitruong.get_is_dangmatketnoi():
                thoi_gian_mat_ket_noi = 0

                tennhanvat = self.moitruong.get_tendoituong()
                idnguoichoi = self.moitruong.get_idnguoichoi()

                if idnguoichoi != self.idnguoichoi:
                    if idnguoichoi:
                        if self.idnguoichoi:
                            self.tactu.luuthietlap(self.idnguoichoi)
                        self.tactu.taithietlap(idnguoichoi)
                        if tennhanvat and tennhanvat != last_hover_text:
                            self.systray.update(hover_text = tennhanvat)
                            last_hover_text = tennhanvat
                    elif self.idnguoichoi:
                        self.tactu.luuthietlap(self.idnguoichoi)
                        if CHUACHONHANVAT != last_hover_text:
                            self.systray.update(hover_text = CHUACHONHANVAT)
                            last_hover_text = CHUACHONHANVAT

                    self.idnguoichoi = idnguoichoi
                    self.tennhanvat = tennhanvat

                elif idnguoichoi and time.time() - self.thoidiemluuthietlapgannhat > 1.:
                    self.thoidiemluuthietlapgannhat = time.time()
                    self.tactu.luuthietlap(idnguoichoi)
            else:
                self.tennhanvat = False
                self.idnguoichoi = 0

                if CHUACHONHANVAT != last_hover_text:
                    self.systray.update(hover_text = CHUACHONHANVAT)
                    last_hover_text = CHUACHONHANVAT

                if thoi_gian_mat_ket_noi == 0:
                    thoi_gian_mat_ket_noi = time.time()
                elif time.time() - thoi_gian_mat_ket_noi > 1.:
                    break

            time.sleep(1)

        self.tatauto()

    def loop_xulyphimtat(self):
        while not self.main_stop.is_set():
            if self.moitruong.get_is_cuasogamekichhoat():

                if keyboard.is_pressed("ctrl+alt+shift+b"):
                    self.tactu.action_vebanrac()
                    time.sleep(0.3)

                if keyboard.is_pressed("ctrl+alt+shift+h"):
                    self.tactu.battat_tudongvebanrac()
                    time.sleep(0.3)

            time.sleep(0.05)