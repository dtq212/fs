import threading
import time
import traceback

import pymem.exception

from moitruong import MoiTruong
from tactu import TacTu

class LoopChinh:
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
                print("Luồng chính: {}".format(err))
                time.sleep(1)

            except Exception as err:
                print("{}".format(err))
            time.sleep(0.2)

    def step(self):
        if not self.moitruong.get_is_nhanvattontai():
            return
        if self.moitruong.get_is_dangmatketnoi():
            return
        self.tactu.action_tudongtimkiemmuctieu()
        self.tactu.action_xulydichuyenuutien()
        self.tactu.action_xulytancong()
        self.tactu.action_dongbotoadohientai()
        self.tactu.action_tudongdoisetdo()

class LoopLamMoiTrangThaiTacTu:
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
                print("Luồng làm mới trạng thái tác tử: {}".format(err))
                time.sleep(1)
            except Exception as err:
                print("{}".format(err))
            time.sleep(0.2)

    def step(self):
        if not self.moitruong.get_is_nhanvattontai():
            return
        if self.moitruong.get_is_dangmatketnoi():
            return
        self.tactu.action_lammoitrangthaitactu()
        self.tactu.action_kiemtraxulyloitudongtimduong()

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
            except Exception as err:
                print("{}".format(err))
            time.sleep(0.2)

    def step(self):
        if not self.moitruong.get_is_nhanvattontai():
            return
        if self.moitruong.get_is_dangmatketnoi():
            return

        self.tactu.action_tudongfarm()
        self.tactu.action_tudongvutvatpham()
        self.tactu.action_tudongmuavatpham()
        self.tactu.action_tudongdanhtheosautruongnhom()
        self.tactu.action_tudongsuavatpham()
        self.tactu.action_tudongbattathieuungbotro()
        self.tactu.action_tudongmokhoa()
        self.tactu.action_tudongsudungvatpham()
        self.tactu.action_tudongphucsinh()
        self.tactu.action_tudongmoitodoi()
        self.moitruong.action_vohieuhoagiamxuatchieukhithaydo()