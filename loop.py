import threading
import time
import traceback

import pymem.exception

from hangso import IDTRANGTHAINHANVAT_DUNGIM
from moitruong import MoiTruong
from tactu import TacTu


class LoopTimKiemMucTieu:
    def __init__(self, moitruong: MoiTruong, tactu: TacTu, stop: threading.Event):
        self.moitruong = moitruong
        self.tactu = tactu
        self.stop = stop

    def __del__(self):
        if not self.stop.is_set():
            self.stop.set()

    def loop(self):
        while not self.stop.is_set() and self.moitruong.get_is_cuasogametontai():
            try:
                self.step()
            except (pymem.exception.PymemError, pymem.exception.WinAPIError) as err:
                print("Luồng tìm kiếm mục tiêu: {}".format(err))
                time.sleep(1)
            time.sleep(0.15)

    def step(self):
        if not self.moitruong.get_is_nhanvattontai():
            return
        if self.moitruong.get_is_dangmatketnoi():
            return

class LoopChinh:
    def __init__(self, moitruong: MoiTruong, tactu: TacTu, stop: threading.Event):
        self.moitruong = moitruong
        self.tactu = tactu
        self.stop = stop
        self.i = 0

    def __del__(self):
        if not self.stop.is_set():
            self.stop.set()

    def loop(self):
        while not self.stop.is_set() and self.moitruong.get_is_cuasogametontai():
            try:
                self.step()
            except (pymem.exception.PymemError, pymem.exception.WinAPIError) as err:
                print("Luồng chính: {}: {}".format(err, traceback.format_exc()))
                time.sleep(1)
            time.sleep(0.1)

    def step(self):
        if not self.moitruong.get_is_nhanvattontai():
            return
        if self.moitruong.get_is_dangmatketnoi():
            return


class LoopPhu:
    def __init__(self, moitruong: MoiTruong, tactu: TacTu, stop: threading.Event):
        self.moitruong = moitruong
        self.tactu = tactu
        self.stop = stop
        self.thoidiemthongbaochetgannhat = time.time()

    def __del__(self):
        try:
            pass
        except (pymem.exception.PymemError, pymem.exception.WinAPIError) as err:
            pass
        if not self.stop.is_set():
            self.stop.set()

    def loop(self):
        while not self.stop.is_set() and self.moitruong.get_is_cuasogametontai():
            try:
                self.step()
            except (pymem.exception.PymemError, pymem.exception.WinAPIError) as err:
                print("Luồng phụ: {}: {}".format(err, traceback.format_exc()))
                time.sleep(1)
            time.sleep(0.5)

    def step(self):
        if not self.moitruong.get_is_nhanvattontai():
            return
        if self.moitruong.get_is_dangmatketnoi():
            return

        self.tactu.action_kiemtraxulyloitudongtimduong()

        self.tactu.action_tudongvebanrac()
        self.tactu.action_tudongsuavatpham()
        self.tactu.action_tudongbattathieuungbotro()