import threading
import time
import traceback

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
        self.moitruong.action_timkiemtoanbodiachiham()
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
                x, y = self.moitruong.get_toado()

                tennguoichoixungquanhs = []
                try:
                    id_quet = 0
                    while True:
                        id_quet = self.moitruong.get_idnhanvattieptheo(id_quet)
                        if id_quet <= 0:
                            break
                        if not self.moitruong.get_is_nhanvattontai(id_quet):
                            continue

                        if self.moitruong.get_idloainhanvat(id_quet) == IDLOAINHANVAT_NGUOICHOI:
                            tennguoichoi = self.moitruong.get_tennhanvat(id_quet)
                            if tennguoichoi and tennguoichoi != tennhanvat:
                                tennguoichoixungquanhs.append(tennguoichoi)

                    tennguoichoixungquanhs = sorted(list(set(tennguoichoixungquanhs)))
                except:
                    tennguoichoixungquanhs = []

                info = {
                    "tennhanvat": tennhanvat,
                    "tenbando": self.moitruong.get_tenbandohientai(),
                    "x": x,
                    "y": y,
                    "status": tentrangthainhanvat,
                    "phantramsinhluc": phantramsinhluc,
                    "phantramnoiluc": phantramnoiluc,
                    "is_window_active": self.moitruong.get_is_cuasogamekichhoat(),

                    "_is_tudongdanhtheosautruongnhom": self.tactu._is_tudongdanhtheosautruongnhom,
                    "_is_tudongsuavatpham": self.tactu._is_tudongsuavatpham,
                    "_is_tudongbattathieuungbotro": self.tactu._is_tudongbattathieuungbotro,
                    "_is_tudongtimkiemmuctieu": self.tactu._is_tudongtimkiemmuctieu,
                    "_is_giukhoangcach": self.tactu._is_giukhoangcach,
                    "_is_khongdanhcungbang": self.tactu._is_khongdanhcungbang,
                    "_is_duoitheo": self.tactu._is_duoitheo,
                    "_is_khongsudungnhieukynang": self.tactu._is_khongsudungnhieukynang,
                    "_is_uutientrieuhoithu": self.tactu._is_uutientrieuhoithu,
                    "_is_chidanhnguoichoivatrieuhoithu": self.tactu._is_chidanhnguoichoivatrieuhoithu,

                    "_is_tudongdoisetdo": self.tactu._is_tudongdoisetdo,
                    "_is_phucsinhnhanh": self.tactu._is_phucsinhnhanh,

                    "_tennhanvattancongs": ", ".join(self.tactu._tennhanvattancongs),
                    "_tennhanvatkhongtancongs": ", ".join(self.tactu._tennhanvatkhongtancongs),

                    "_is_tudongfarm": self.tactu._is_tudongfarm,
                    "_is_tudongvutvatpham": self.tactu._is_tudongvutvatpham,
                    "_is_tudongmuavatphamkytrancac": self.tactu._is_tudongmuavatphamkytrancac,
                    "idbandotudongfarm": self.tactu._idbandotudongfarm,
                    "toadoxtudongfarm": self.tactu._toadoxtudongfarm,
                    "toadoytudongfarm": self.tactu._toadoytudongfarm,
                    "_setdo1_map": self.tactu._setdo1_map,
                    "_setdo2_map": self.tactu._setdo2_map,

                    "tennguoichoixungquanhs": tennguoichoixungquanhs,

                    "_is_danhtheotennhanvat": self.tactu._is_danhtheotennhanvat,
                }
                self.shared_data[self.idcuaso] = info

            except Exception as err:
                print(f"Lỗi ở loop_hienthigiaodien: {err}")
                traceback.print_exc()
            time.sleep(0.25)

    def loop_xulyphimtat(self):
        while not self.main_stop.is_set():
            cmd = self.command_dict.get(self.idcuaso)

            if cmd:
                if cmd.startswith("them_tennhanvattancong_theotennhanvat:"):
                    tennhanvat = cmd.split(":", 1)[1]
                    self.tactu.them_tennhanvattancong_theotennhanvat(tennhanvat)
                if cmd == "battat_tudongfarm":
                    self.tactu.battat_tudongfarm()
                elif cmd == "battat_tudongsuavatpham":
                    self.tactu.battat_tudongsuavatpham()
                elif cmd == "action_test":
                    self.tactu.action_test()
                elif cmd == "action_mua1thancauphu":
                    self.tactu.action_mua1thancauphu()
                elif cmd == "battat_tudongdanhtheosautruongnhom":
                    self.tactu.battat_tudongdanhtheosautruongnhom()
                elif cmd == "battat_tudongtimkiemmuctieu":
                    self.tactu.battat_tudongtimkiemmuctieu()
                elif cmd == "battat_is_giukhoangcach":
                    self.tactu.battat_is_giukhoangcach()
                elif cmd == "battat_is_khongdanhcungbang":
                    self.tactu.battat_is_khongdanhcungbang()
                elif cmd == "battat_is_tudongbattathieuungbotro":
                    self.tactu.battat_tudongbattathieuungbotro()
                elif cmd == "battat_is_uutientrieuhoithu":
                    self.tactu.battat_is_uutientrieuhoithu()
                elif cmd == "battat_is_sudungkynangtoadochichuot":
                    self.tactu.battat_is_sudungkynangtoadochichuot()
                elif cmd == "battat_is_tudongmokhoa":
                    self.tactu.battat_tudongmokhoa()
                elif cmd == "battat_is_tudongvutvatpham":
                    self.tactu.battat_is_tudongvutvatpham()
                elif cmd == "battat_is_tudongmuavatphamkytrancac":
                    self.tactu.battat_is_tudongmuavatphamkytrancac()
                elif cmd == "battat_is_tudongdoisetdo":
                    self.tactu.battat_is_tudongdoisetdo()
                elif cmd == "battat_is_duoitheo":
                    self.tactu.battat_is_duoitheo()
                elif cmd == "battat_is_khongsudungnhieukynang":
                    self.tactu.battat_is_khongsudungnhieukynang()
                elif cmd == "battat_phucsinhnhanh":
                    self.tactu.battat_phucsinhnhanh()
                elif cmd == "botoanbo_tennhanvattancong":
                    self.tactu.botoanbo_tennhanvattancong()
                elif cmd == "botoanbo_tennhanvatkhongtancong":
                    self.tactu.botoanbo_tennhanvatkhongtancong()
                elif cmd == "them_tennhanvattancong":
                    self.tactu.them_tennhanvattancong()
                elif cmd == "them_tennhanvatkhongtancong":
                    self.tactu.them_tennhanvatkhongtancong()
                elif cmd == "bat_is_chidanhnguoichoivatrieuhoithu":
                    self.tactu.bat_is_chidanhnguoichoivatrieuhoithu()
                elif cmd == "tat_is_chidanhnguoichoivatrieuhoithu":
                    self.tactu.tat_is_chidanhnguoichoivatrieuhoithu()
                elif cmd == "them_tennhanvattodoitudong":
                    self.tactu.them_tennhanvattodoitudong()
                elif cmd == "botoanbo_tennhanvattodoitudong":
                    self.tactu.botoanbo_tennhanvattodoitudong()
                elif cmd == "battat_is_chidanhnguoichoivatrieuhoithu":
                    self.tactu.battat_is_chidanhnguoichoivatrieuhoithu()
                elif cmd == "battat_is_danhtheotennhanvat":
                    self.tactu.battat_is_danhtheotennhanvat()
                elif cmd == "action_batpk":
                    self.tactu.action_batpk()
                elif cmd == "action_tatpk":
                    self.tactu.action_tatpk()
                elif cmd == "luusetdo_1":
                    self.tactu.luusetdo(1)
                elif cmd == "luusetdo_2":
                    self.tactu.luusetdo(2)
                self.command_dict[self.idcuaso] = None

            time.sleep(0.15)
