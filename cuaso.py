import threading
import time
import keyboard

from hangso import *
from loop import (
    LoopChinh,
    LoopPhu,
    LoopLamMoiTrangThaiTacTu,
)
from moitruong import MoiTruong
from tactu import TacTu


def khoidong_loopchinh(moitruong, tactu, stop):
    LoopChinh(moitruong, tactu, stop).loop()


def khoidong_looplammoitrangthaitactu(moitruong, tactu, stop):
    LoopLamMoiTrangThaiTacTu(moitruong, tactu, stop).loop()


def khoidong_loopphu(moitruong, tactu, stop):
    LoopPhu(moitruong, tactu, stop).loop()


class CuaSo:
    def __init__(self, idcuaso, shared_data):
        self.idcuaso = idcuaso
        self.shared_data = shared_data

        self.moitruong = MoiTruong(idcuaso)
        self.tactu = TacTu(self.moitruong)
        self.main_stop = threading.Event()

        self.tennhanvat = None
        self.thoidiemluuthietlap = time.time()

        self.luongs = (
            threading.Thread(target = khoidong_looplammoitrangthaitactu, args = [self.moitruong, self.tactu, self.main_stop], daemon = True),
            threading.Thread(target = khoidong_loopchinh, args = [self.moitruong, self.tactu, self.main_stop], daemon = True),
            threading.Thread(target = khoidong_loopphu, args = [self.moitruong, self.tactu, self.main_stop], daemon = True),
        )

        for luong in self.luongs:
            luong.start()

        threading.Thread(target = self.loop_xulyphimtat, daemon = True).start()
        threading.Thread(target = self.loop_hienthigiaodien, daemon = True).start()

    def __del__(self):
        self.tatauto()

    def _chotoanbocacluongdunghan(self):
        for luong in self.luongs:
            if luong.is_alive():
                luong.join(timeout = 0.2)

    def tatauto(self, *args, **kwargs):
        if self.tennhanvat:
            self.tactu.luuthietlap(self.tennhanvat)

        self.main_stop.set()
        self._chotoanbocacluongdunghan()

        if self.idcuaso in self.shared_data:
            del self.shared_data[self.idcuaso]

    def loop_hienthigiaodien(self):
        while not self.main_stop.is_set():
            try:
                if not self.moitruong.get_is_cuasogametontai():
                    break

                tennhanvat = self.moitruong.get_tennhanvat()

                if tennhanvat and tennhanvat != self.tennhanvat:
                    if self.tennhanvat:
                        self.tactu.luuthietlap(self.tennhanvat)

                    self.tactu.taithietlap(tennhanvat)
                    print(f"-> Đã tải cấu hình cho: {tennhanvat}")

                    self.tennhanvat = tennhanvat
                    self.thoidiemluuthietlap = time.time()

                elif tennhanvat and (time.time() - self.thoidiemluuthietlap > 1.0):
                    self.tactu.luuthietlap(tennhanvat)
                    self.thoidiemluuthietlap = time.time()

                if not tennhanvat:
                    time.sleep(1.)
                    continue

                phantramsinhluc = 0
                phantramnoiluc = 0
                try:
                    sinhluchientai = self.moitruong.get_sinhluchientai()
                    sinhluctoida = self.moitruong.get_sinhluctoida()
                    if sinhluctoida > 0:
                        phantramsinhluc = int((sinhluchientai / sinhluctoida) * 100)
                except:
                    pass

                idtrangthainhanvat = self.moitruong.get_idtrangthainhanvat()
                tentrangthainhanvat = "Đứng im"
                if idtrangthainhanvat == IDTRANGTHAINHANVAT_DICHUYEN:
                    tentrangthainhanvat = "Di chuyển"
                elif idtrangthainhanvat == IDTRANGTHAINHANVAT_TANCONG:
                    tentrangthainhanvat = "Tấn công"
                elif idtrangthainhanvat == IDTRANGTHAINHANVAT_DACHET:
                    tentrangthainhanvat = "Đã chết"

                info = {
                    "tennhanvat": tennhanvat,
                    "tenbando": self.moitruong.get_tenbandohientai(),
                    "x": self.moitruong.get_toadox(),
                    "y": self.moitruong.get_toadoy(),
                    "status": tentrangthainhanvat,
                    "phantramsinhluc": phantramsinhluc,
                    "phantramnoiluc": phantramnoiluc,
                    "is_window_active": self.moitruong.get_is_cuasogamekichhoat(),

                    "_is_tudongfarmvabanrac": self.tactu._is_tudongfarmvabanrac,
                    "_is_tudongdanhtheosautruongnhom": self.tactu._is_tudongdanhtheosautruongnhom,
                    "_is_tudongsuavatpham": self.tactu._is_tudongsuavatpham,
                    "_is_tudongbattathieuungbotro": self.tactu._is_tudongbattathieuungbotro,
                    "_is_tudongtimkiemmuctieu": self.tactu._is_tudongtimkiemmuctieu,
                    "_is_tudongboquamuctieumaucao": self.tactu._is_tudongboquamuctieumaucao,
                    "_is_khongdanhcungbang": self.tactu._is_khongdanhcungbang,
                    "_is_uutiennguoichoi": self.tactu._is_uutiennguoichoi,
                    "_is_chidanhnguoichoivatrieuhoithu": self.tactu._is_chidanhnguoichoivatrieuhoithu,
                    "_is_uutienmuctieusinhluc": self.tactu._is_uutienmuctieusinhluc
                }
                self.shared_data[self.idcuaso] = info

            except Exception:
                pass
            time.sleep(0.5)

    def loop_xulyphimtat(self):
        while not self.main_stop.is_set():
            if self.moitruong.get_is_cuasogamekichhoat():
                if keyboard.is_pressed("ctrl+alt+shift+h"):
                    self.tactu.battat_tudongfarmvabanrac()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+alt+shift+r"):
                    self.tactu.battat_tudongsuavatpham()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+alt+shift+y"):
                    self.tactu.action_test()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+alt+shift+t"):
                    self.tactu.battat_tudongdanhtheosautruongnhom()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+alt+shift+f"):
                    self.tactu.battat_tudongtimkiemmuctieu()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+alt+shift+b"):
                    self.tactu.battat_is_khongdanhcungbang()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+alt+c"):
                    self.tactu.botoanbo_tennhanvattancong()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+alt+x"):
                    self.tactu.botoanbo_tennhanvatkhongtancong()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+c"):
                    self.tactu.them_tennhanvattancong()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+x"):
                    self.tactu.them_tennhanvatkhongtancong()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+d"):
                    self.tactu.bat_is_chidanhnguoichoivatrieuhoithu()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+a"):
                    self.tactu.tat_is_chidanhnguoichoivatrieuhoithu()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+e"):
                    self.tactu.action_batpk()
                    time.sleep(0.3)
                if keyboard.is_pressed("ctrl+q"):
                    self.tactu.action_tatpk()
                    time.sleep(0.3)

            time.sleep(0.05)