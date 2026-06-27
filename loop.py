import math
import threading
import time
import traceback

import pymem.exception

from hangso import IDHEPHAI_DAOSI, IDTRANGTHAINHANVAT_DICHUYEN
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
                traceback.print_exc()
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
        self.tactu.action_tudongdoisetdo()


class LoopLamMoiTrangThaiTacTu:
    def __init__(self, moitruong: MoiTruong, tactu: TacTu, stop: threading.Event):
        self.moitruong = moitruong
        self.tactu = tactu
        self.stop = stop

        self.thongtindichuyen_banthan = None

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

        thoidiem_hientai = time.time()
        toado_hientai = self.moitruong.get_toado()
        idtrangthai_hientai = self.moitruong.get_idtrangthainhanvat()

        if self.moitruong.get_tennhanvat() == "OsamaDaEĐen" and toado_hientai != (-1, -1) and idtrangthai_hientai == IDTRANGTHAINHANVAT_DICHUYEN:
            is_bidongbang = self.moitruong.get_is_bidongbang()
            tocdo_game = self.moitruong.get_tocdodichuyen()

            if self.thongtindichuyen_banthan:
                thoidiem_cu, toado_cu = self.thongtindichuyen_banthan
                delta_t = thoidiem_hientai - thoidiem_cu

                if delta_t > 0.1:
                    khoangcach_thucte = math.dist(toado_hientai, toado_cu)
                    tocdo_thucte = khoangcach_thucte / delta_t

                    print(f"--- THÔNG SỐ ĐO ĐẠC BẢN THÂN ---")
                    print(f" Trạng thái đóng băng: {is_bidongbang}")
                    print(f" Tốc độ hiển thị trong game: {tocdo_game}")
                    print(f" Quãng đường chạy được: {khoangcach_thucte:.2f} pixel (trong {delta_t:.2f}s)")
                    print(f" Vận tốc thực tế (pixel/giây): {tocdo_thucte:.2f} px/s")

                    self.thongtindichuyen_banthan = (thoidiem_hientai, toado_hientai)
            else:
                self.thongtindichuyen_banthan = (thoidiem_hientai, toado_hientai)
        else:
            self.thongtindichuyen_banthan = None

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

        self.tactu.action_tudongmuavatpham()
        self.tactu.action_tudongdanhtheosautruongnhom()
        self.tactu.action_tudongsuavatpham()
        self.tactu.action_tudongbattathieuungbotro()
        self.tactu.action_tudongnhatvatpham()
        self.tactu.action_tudongmokhoa()
        self.tactu.action_tudongsudungvatpham()
        self.tactu.action_tudongphucsinh()
        self.tactu.action_tudongmoitodoi()
        self.tactu.action_tudongvutvatpham()

        idmuctieu = self.moitruong.get_idmuctieudangchichuot()
        if idmuctieu > 0:
            tenmuctieu = self.moitruong.get_tennhanvat(idmuctieu)
            if tenmuctieu in ["VươngTrùngDương", "TiểuYTiên", "3LanPhaiKhoc"]:
                print("{} hiệu ứng bổ trợ: {}, hiệu ứng của tôi: {}".format(tenmuctieu, self.moitruong.get_hieuungbotros(idmuctieu), self.moitruong.get_hieuungbotros()))