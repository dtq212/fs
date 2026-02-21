import threading
import time

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
    def __init__(self, idcuaso, shared_data, command_dict):
        self.idcuaso = idcuaso
        self.shared_data = shared_data
        self.command_dict = command_dict

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
        if not hasattr(self, "tennhanvat"):
            return
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
            
        if self.idcuaso in self.command_dict:
            del self.command_dict[self.idcuaso]

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
                    "_is_uutientrieuhoithu": self.tactu._is_uutientrieuhoithu,
                    "_is_chidanhnguoichoivatrieuhoithu": self.tactu._is_chidanhnguoichoivatrieuhoithu,
                    "_is_uutienmuctieusinhluc": self.tactu._is_uutienmuctieusinhluc,

                    "_tennhanvattancongs": ", ".join(self.tactu._tennhanvattancongs),
                    "_tennhanvatkhongtancongs": ", ".join(self.tactu._tennhanvatkhongtancongs),

                    "idbandotudongfarm": self.tactu._idbandotudongfarm,
                    "toadoxtudongfarm": self.tactu._toadoxtudongfarm,
                    "toadoytudongfarm": self.tactu._toadoytudongfarm,
                }
                self.shared_data[self.idcuaso] = info

            except Exception:
                pass
            time.sleep(1.0) 

    def loop_xulyphimtat(self):
        while not self.main_stop.is_set():
            cmd = self.command_dict.get(self.idcuaso)
            
            if cmd:
                if cmd == "battat_tudongfarmvabanrac": self.tactu.battat_tudongfarmvabanrac()
                elif cmd == "battat_tudongsuavatpham": self.tactu.battat_tudongsuavatpham()
                elif cmd == "action_test": self.tactu.action_test()
                elif cmd == "battat_tudongdanhtheosautruongnhom": self.tactu.battat_tudongdanhtheosautruongnhom()
                elif cmd == "battat_tudongtimkiemmuctieu": self.tactu.battat_tudongtimkiemmuctieu()
                elif cmd == "battat_is_khongdanhcungbang": self.tactu.battat_is_khongdanhcungbang()
                elif cmd == "battat_is_tudongbattathieuungbotro": self.tactu.battat_tudongbattathieuungbotro()
                elif cmd == "battat_is_uutientrieuhoithu": self.tactu.battat_is_uutientrieuhoithu()
                elif cmd == "battat_is_tudongmokhoa": self.tactu.battat_tudongmokhoa()
                elif cmd == "botoanbo_tennhanvattancong": self.tactu.botoanbo_tennhanvattancong()
                elif cmd == "botoanbo_tennhanvatkhongtancong": self.tactu.botoanbo_tennhanvatkhongtancong()
                elif cmd == "them_tennhanvattancong": self.tactu.them_tennhanvattancong()
                elif cmd == "them_tennhanvatkhongtancong": self.tactu.them_tennhanvatkhongtancong()
                elif cmd == "bat_is_chidanhnguoichoivatrieuhoithu": self.tactu.bat_is_chidanhnguoichoivatrieuhoithu()
                elif cmd == "tat_is_chidanhnguoichoivatrieuhoithu": self.tactu.tat_is_chidanhnguoichoivatrieuhoithu()
                elif cmd == "action_batpk": self.tactu.action_batpk()
                elif cmd == "action_tatpk": self.tactu.action_tatpk()
                
                self.command_dict[self.idcuaso] = None

            time.sleep(0.15)