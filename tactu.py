import math
import random
import re
import time

import pymem

from hangso import *
from moitruong import MoiTruong
from tienich import luuthietlap as util_luuthietlap
from tienich import taithietlap as util_taithietlap, phatam

class TacTu:
    def __init__(self, moitruong: MoiTruong):
        self._phantramsinhluchientai = 100.
        self._phantramsinhlucmatdi = 0.
        self._is_tudongdanhtheosautruongnhom = False
        self._is_uutientrieuhoithu = False
        self._is_tudongtimkiemmuctieu = False
        self._is_khongdanhcungbang = False
        self._is_chidanhnguoichoivatrieuhoithu = False
        self._tennhanvattancongs = set() # {"108HoaHit1", "108Loveisi", "108kiuasud"}
        self._tennhanvatkhongtancongs = set()

        self.moitruong = moitruong

        self._is_tudongsuavatpham = True
        self._is_tudongbattathieuungbotro = True
        self._is_tudongmokhoa = False

        self._thoidiemkiemtrasuavatphamgannhat = 0.

        self._thoidiemnhanvatdungimgannhat = 0.
        self._thoidiemnhanvattudongtimduongdungimgannhat = 0.

        self._tenbandohientai = False
        self._thoidiemthaydoibandogannhat = 0.

        self._thoidiemtudongnhatdogannhat = 0.

        self._yeucaudichuyentheosautruongnhom = None
        self._yeucaudichuyenfarm = None

        self._idtrieuhoithu = -1

        self._yeucaudichuyentancong = None
        self._thoidiembathieuungbotrogannhat = 0.
        self._is_sudungkynangtoadochichuot = False

        self._is_tudongdoisetdo = False

        self._thoidiemthongbaohetquanamthuygannhat = 0.

        self._thoidiemtamngungtanconggannhat = 0.

        self._is_tudongfarm = False
        self._idbandotudongfarm = 0
        self._toadoxtudongfarm = 0
        self._toadoytudongfarm = 0
        self._is_dadichuyentoivitrifarm = False

        self._is_dangxulybanrac = False

        self._toadodichtudongtimduonggannhat = None

        self._is_tudongvutvatpham = False
        self._thoidiemvutvatphamgannhat = 0.
        self._is_tudongmuavatphamkytrancac = False

        self._thoidiemdongbotoadohientaigannhat = 0.
        self._thoidiemyeucaubienthan = 0.

        self._is_giukhoangcach = False
        self._thoidiemtudongtimduonggannhat = 0.

        self._tennhanvattodoitudongs = set()
        self._thoidiemmoitodoigannhat_map = {}
        self._thoidiemnhanloimoitodoigannhat_map = {}

        self._is_duoitheo = True
        self._is_khongsudungnhieukynang = False
        self._is_dangdondeprac = False

        self._setdo1goc_map = {}
        self._setdo2goc_map = {}
        self._setdo1_map = {}
        self._setdo2_map = {}

        self._toadokiemtrabiket = (0, 0)
        self._thoidiemkiemtrabiket = 0.
        self._is_dangbiket = False

        self._is_phucsinhnhanh = True

    def __del__(self):
        try:
            self.moitruong.action_tatvohieuhoathietlapmuctieutancong()
            self.moitruong.action_tatvohieuhoathietlapmuctieudangchon()
            pass
        except (pymem.exception.PymemError, pymem.exception.WinAPIError):
            pass

    def luuthietlap(self, tennhanvat):
        if not tennhanvat:
            return
            
        thietlap = {
            "is_phucsinhnhanh": self._is_phucsinhnhanh,
            "is_danhtheosautruongnhom": self._is_tudongdanhtheosautruongnhom,
            "is_tudongsuavatpham": self._is_tudongsuavatpham,
            "is_tudongbattathieuungbotro": self._is_tudongbattathieuungbotro,

            "is_uutientrieuhoithu": self._is_uutientrieuhoithu,
            "is_tudongtimkiemmuctieu": self._is_tudongtimkiemmuctieu,
            "is_khongdanhcungbang": self._is_khongdanhcungbang,
            "is_chidanhnguoichoivatrieuhoithu": self._is_chidanhnguoichoivatrieuhoithu,
            "tennhanvattancongs": self._tennhanvattancongs,
            "tennhanvatkhongtancongs": self._tennhanvatkhongtancongs,
            "tennhanvattodoitudongs": list(self._tennhanvattodoitudongs),
            "is_tudongmokhoa": self._is_tudongmokhoa,
            "is_tudongdoisetdo": self._is_tudongdoisetdo,

            "is_tudongfarm": self._is_tudongfarm,
            "is_tudongvutvatpham": self._is_tudongvutvatpham,
            "is_tudongmuavatphamkytrancac": self._is_tudongmuavatphamkytrancac,
            "idbandotudongfarm": self._idbandotudongfarm,
            "toadoxtudongfarm": self._toadoxtudongfarm,
            "toadoytudongfarm": self._toadoytudongfarm,

            "is_giukhoangcach": self._is_giukhoangcach,
            "is_duoitheo": self._is_duoitheo,
            "is_khongsudungnhieukynang": self._is_khongsudungnhieukynang,
            "setdo1_goc": self._setdo1goc_map,
            "setdo2_goc": self._setdo2goc_map,
        }

        util_luuthietlap(str(tennhanvat), thietlap)

    def taithietlap(self, tennhanvat):
        if not tennhanvat:
            return

        thietlap = util_taithietlap(str(tennhanvat))
        if thietlap:
            if "is_phucsinhnhanh" in thietlap:
                self._is_phucsinhnhanh = thietlap["is_phucsinhnhanh"]
            if "is_danhtheosautruongnhom" in thietlap:
                self._is_tudongdanhtheosautruongnhom = thietlap["is_danhtheosautruongnhom"]

            if "is_tudongsuavatpham" in thietlap:
                self._is_tudongsuavatpham = thietlap["is_tudongsuavatpham"]

            if "is_tudongbattathieuungbotro" in thietlap:
                self._is_tudongbattathieuungbotro = thietlap["is_tudongbattathieuungbotro"]

            if "is_uutientrieuhoithu" in thietlap:
                self._is_uutientrieuhoithu = thietlap["is_uutientrieuhoithu"]

            if "is_tudongtimkiemmuctieu" in thietlap:
                self._is_tudongtimkiemmuctieu = thietlap["is_tudongtimkiemmuctieu"]

            if "is_khongdanhcungbang" in thietlap:
                self._is_khongdanhcungbang = thietlap["is_khongdanhcungbang"]

            if "is_chidanhnguoichoivatrieuhoithu" in thietlap:
                self._is_chidanhnguoichoivatrieuhoithu = thietlap["is_chidanhnguoichoivatrieuhoithu"]

            if "tennhanvattancongs" in thietlap:
                self._tennhanvattancongs = thietlap["tennhanvattancongs"]

            if "tennhanvatkhongtancongs" in thietlap:
                self._tennhanvatkhongtancongs = thietlap["tennhanvatkhongtancongs"]

            if "tennhanvattodoitudongs" in thietlap:
                self._tennhanvattodoitudongs = set(thietlap["tennhanvattodoitudongs"])

            if "is_tudongmokhoa" in thietlap:
                self._is_tudongmokhoa = thietlap["is_tudongmokhoa"]

            if "is_tudongdoisetdo" in thietlap:
                self._is_tudongdoisetdo = thietlap["is_tudongdoisetdo"]

            if "is_tudongfarm" in thietlap:
                self._is_tudongfarm = thietlap["is_tudongfarm"]

            if "is_tudongvutvatpham" in thietlap:
                self._is_tudongvutvatpham = thietlap["is_tudongvutvatpham"]

            if "is_tudongmuavatphamkytrancac" in thietlap:
                self._is_tudongmuavatphamkytrancac = thietlap["is_tudongmuavatphamkytrancac"]

            if "idbandotudongfarm" in thietlap:
                self._idbandotudongfarm = thietlap["idbandotudongfarm"]

            if "toadoxtudongfarm" in thietlap:
                self._toadoxtudongfarm = thietlap["toadoxtudongfarm"]

            if "toadoytudongfarm" in thietlap:
                self._toadoytudongfarm = thietlap["toadoytudongfarm"]

            if "is_giukhoangcach" in thietlap:
                self._is_giukhoangcach = thietlap["is_giukhoangcach"]
            if "is_duoitheo" in thietlap:
                self._is_duoitheo = thietlap["is_duoitheo"]
            if "is_khongsudungnhieukynang" in thietlap:
                self._is_khongsudungnhieukynang = thietlap["is_khongsudungnhieukynang"]

            if "setdo1_goc" in thietlap:
                self._setdo1goc_map = thietlap["setdo1_goc"]
            if "setdo2_goc" in thietlap:
                self._setdo2goc_map = thietlap["setdo2_goc"]

            self._setdo1_map = {k: v for k, v in self._setdo1goc_map.items() if k not in self._setdo2goc_map}
            self._setdo2_map = {k: v for k, v in self._setdo2goc_map.items() if k not in self._setdo1goc_map}

    def them_tennhanvattodoitudong(self):
        idmuctieu = self.moitruong.get_idmuctieudangchichuot()
        if idmuctieu > 0 and self.moitruong.get_idloainhanvat(idmuctieu) == IDLOAINHANVAT_NGUOICHOI:
            tenhanvat = self.moitruong.get_tennhanvat(idmuctieu)
            if tenhanvat and tenhanvat not in self._tennhanvattodoitudongs:
                self._tennhanvattodoitudongs.add(tenhanvat)
                print(f"Danh sách Tổ đội: {list(self._tennhanvattodoitudongs)}")
                phatam(f"Thêm nhân vật tổ đội. Tổng {len(self._tennhanvattodoitudongs)}")

    def botoanbo_tennhanvattodoitudong(self):
        self._tennhanvattodoitudongs.clear()
        phatam("Bỏ toàn bộ danh sách tổ đội")

    def battat_is_duoitheo(self):
        self._is_duoitheo = not self._is_duoitheo
        if self._is_duoitheo:
            phatam("Bật tự động đuổi theo mục tiêu")
        else:
            phatam("Tắt tự động đuổi theo mục tiêu")

    def battat_is_khongsudungnhieukynang(self):
        self._is_khongsudungnhieukynang = not self._is_khongsudungnhieukynang
        if self._is_khongsudungnhieukynang:
            phatam("Bật chỉ dùng một kỹ năng")
        else:
            phatam("Tắt chỉ dùng một kỹ năng, cho phép đổi kỹ năng")

    def battat_phucsinhnhanh(self):
        self._is_phucsinhnhanh = not self._is_phucsinhnhanh

        if self._is_phucsinhnhanh:
            phatam("Bật phục sinh nhanh")
        else:
            phatam("Tắt phục sinh nhanh, nhường cho auto in-game xử lý")

    def battat_is_giukhoangcach(self):
        self._is_giukhoangcach = not self._is_giukhoangcach
        if self._is_giukhoangcach:
            phatam("Bật tự động giữ khoảng cách")
        else:
            phatam("Tắt tự động giữ khoảng cách")
    def battat_is_tudongvutvatpham(self):
        self._is_tudongvutvatpham = not self._is_tudongvutvatpham

        if self._is_tudongvutvatpham:
            phatam("Bật tự động vứt rác tại chỗ")
        else:
            phatam("Tắt tự động vứt rác tại chỗ")

    def battat_is_tudongmuavatphamkytrancac(self):
        self._is_tudongmuavatphamkytrancac = not self._is_tudongmuavatphamkytrancac

        if self._is_tudongmuavatphamkytrancac:
            phatam("Bật tự động mua vật phẩm kỳ trân các")
        else:
            phatam("Tắt tự động mua vật phẩm kỳ trân các")

    def battat_tudongfarm(self):
        self._is_tudongfarm = not self._is_tudongfarm

        if self._is_tudongfarm:
            if self.moitruong.get_is_khuvuccothetancong():
                self._idbandotudongfarm = self.moitruong.get_idbandohientai()
                self._toadoxtudongfarm, self._toadoytudongfarm = self.moitruong.get_toado()
                print(f"Đã lưu tọa độ Farm: Map {self._idbandotudongfarm} - {self._toadoxtudongfarm}:{self._toadoytudongfarm}")

            phatam("Bật tự động Farm và Bán rác")

        else:
            phatam("Tắt tự động Farm và Bán rác")

    def battat_tudongdanhtheosautruongnhom(self):
        self._is_tudongdanhtheosautruongnhom = not self._is_tudongdanhtheosautruongnhom

        if self._is_tudongdanhtheosautruongnhom:
            phatam("Bật tự động đánh theo sau trưởng nhóm")
        else:
            phatam("Tắt tự động đánh theo sau trưởng nhóm")

    def battat_is_tudongdoisetdo(self):
        self._is_tudongdoisetdo = not self._is_tudongdoisetdo

        if self._is_tudongdoisetdo:
            phatam("Bật tự động đổi sét đồ")
        else:
            phatam("Tắt tự động đổi sét đồ")

    def battat_is_sudungkynangtoadochichuot(self):
        self._is_sudungkynangtoadochichuot = not self._is_sudungkynangtoadochichuot

        if self._is_sudungkynangtoadochichuot:
            phatam("Bật tự động sử dụng kỹ năng tọa độ chỉ chuột")
        else:
            phatam("Tắt tự động sử dụng kỹ năng tọa độ chỉ chuột")

    def battat_is_uutientrieuhoithu(self):
        self._is_uutientrieuhoithu = not self._is_uutientrieuhoithu

        if self._is_uutientrieuhoithu:
            self._is_tudongtimkiemmuctieu = True
            phatam("Bật ưu tiên triệu hồi thú")
        else:
            phatam("Tắt ưu tiên triệu hồi thú")

    def battat_tudongmokhoa(self):
        self._is_tudongmokhoa = not self._is_tudongmokhoa

        if self._is_tudongmokhoa:
            phatam("Bật tự động mở khóa")
        else:
            phatam("Tắt tự động mở khóa")

    def battat_tudongbattathieuungbotro(self):
        self._is_tudongbattathieuungbotro = not self._is_tudongbattathieuungbotro

        if self._is_tudongbattathieuungbotro:
            phatam("Bật tự động bật / tắt hiệu ứng bổ trợ")
        else:
            phatam("Tắt tự động bật / tắt hiệu ứng bổ trợ")

    def battat_tudongsuavatpham(self):
        self._is_tudongsuavatpham = not self._is_tudongsuavatpham

        if self._is_tudongsuavatpham:
            phatam("Bật tự động sửa vật phẩm")
        else:
            phatam("Tắt tự động sửa vật phẩm")

    def bat_is_chidanhnguoichoivatrieuhoithu(self):
        if not self._is_chidanhnguoichoivatrieuhoithu:
            self._is_chidanhnguoichoivatrieuhoithu = True
            self._is_tudongtimkiemmuctieu = True
            phatam("Bật chỉ đánh người chơi và triệu hồi thú")

    def tat_is_chidanhnguoichoivatrieuhoithu(self):
        if self._is_chidanhnguoichoivatrieuhoithu:
            self._is_chidanhnguoichoivatrieuhoithu = False
            phatam("Tắt chỉ đánh người chơi và triệu hồi thú")

    def battat_tudongtimkiemmuctieu(self):
        self._is_tudongtimkiemmuctieu = not self._is_tudongtimkiemmuctieu

        if self._is_tudongtimkiemmuctieu:
            phatam("Bật tự động tìm kiếm mục tiêu")
        else:
            phatam("Tắt tự động tìm kiếm mục tiêu")

    def battat_is_khongdanhcungbang(self):
        self._is_khongdanhcungbang = not self._is_khongdanhcungbang

        if self._is_khongdanhcungbang:
            phatam("Bật không đánh cùng bang")
            self._is_tudongtimkiemmuctieu = True
        else:
            phatam("Tắt không đánh cùng bang")

    def them_tennhanvattancong(self):
        print("them_tennhanvattancong")
        idmuctieudangchichuot = self.moitruong.get_idmuctieudangchichuot()
        tennhanvattancong = self.moitruong.get_tennhanvat(idmuctieudangchichuot)
        if tennhanvattancong and tennhanvattancong not in self._tennhanvattancongs:
            self._tennhanvattancongs.add(tennhanvattancong)

            if self._tennhanvattancongs:
                print("Danh sách nhân vật tấn công: {}".format(self._tennhanvattancongs))
                phatam("Thêm tên nhân vật tấn công. Tổng cộng {}".format(len(self._tennhanvattancongs)))

    def them_tennhanvatkhongtancong(self):
        idmuctieudangchichuot = self.moitruong.get_idmuctieudangchichuot()
        tennhanvatkhongtancong = self.moitruong.get_tennhanvat(idmuctieudangchichuot)
        if tennhanvatkhongtancong and tennhanvatkhongtancong not in self._tennhanvatkhongtancongs:
            self._tennhanvatkhongtancongs.add(tennhanvatkhongtancong)

            if self._tennhanvatkhongtancongs:
                print("Danh sách nhân vật không tấn công: {}".format(self._tennhanvatkhongtancongs))
                phatam("Thêm tên nhân vật không tấn công. Tổng cộng {}".format(len(self._tennhanvatkhongtancongs)))

    def botoanbo_tennhanvattancong(self):
        self._tennhanvattancongs.clear()

        phatam("Bỏ toàn bộ thiết lập tên nhân vật tấn công")

    def botoanbo_tennhanvatkhongtancong(self):
        self._tennhanvatkhongtancongs.clear()
        phatam("Bỏ toàn bộ thiết lập tên nhân vật không tấn công")
    
    def action_test(self):
        # for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
        #     vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
        #     if not vitrivatpham:
        #         continue
        #     idvatpham, idruong, vitrix, vitriy = vitrivatpham
        #     print("#{}: {}: {}".format(sothutuvatpham, (idvatpham, idruong, vitrix, vitriy), self.moitruong.get_thongtinvatpham_display(idvatpham)))

        print(self.moitruong.get_hieuungbotros())

    def _taochukyvatpham(self, idvatpham):
        tenvatpham = self.moitruong.get_tenvatpham(idvatpham)
        if not tenvatpham:
            return None

        thuoctinh_map = self.moitruong.get_thuoctinhvatpham_map(idvatpham)
        thuoctinh_str = str(sorted(thuoctinh_map.items())) if thuoctinh_map else "KhongCoChiSo"

        return f"{tenvatpham}___{thuoctinh_str}"

    def luusetdo(self, sttset):
        setdo_map = {}
        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong == IDVITRIRUONG_TRANGBI:
                chuky = self._taochukyvatpham(idvatpham)
                tenvatpham = self.moitruong.get_tenvatpham(idvatpham)
                if chuky and tenvatpham:
                    setdo_map[chuky] = tenvatpham

        if sttset == 1:
            self._setdo1goc_map = setdo_map
        elif sttset == 2:
            self._setdo2goc_map = setdo_map

        self._setdo1_map = {k: v for k, v in self._setdo1goc_map.items() if k not in self._setdo2goc_map}
        self._setdo2_map = {k: v for k, v in self._setdo2goc_map.items() if k not in self._setdo1goc_map}

        if sttset == 1:
            print(f"Sét đồ 1 đã lưu (sau khi lọc trùng): {self._setdo1_map}")
            phatam(f"Đã lưu sét đồ 1. Cần đổi {len(self._setdo1_map)} món")
        elif sttset == 2:
            print(f"Sét đồ 2 đã lưu (sau khi lọc trùng): {self._setdo2_map}")
            phatam(f"Đã lưu sét đồ 2. Cần đổi {len(self._setdo2_map)} món")

    def _macsetdo(self, setdo_map):
        if not setdo_map:
            return

        chukyhanhtrangcanmacs = list(setdo_map.keys())

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong == IDVITRIRUONG_HANHTRANG:
                chukyhanhtrang = self._taochukyvatpham(idvatpham)

                if chukyhanhtrang and chukyhanhtrang in chukyhanhtrangcanmacs:
                    self.moitruong.action_sudungvatpham(sothutuvatpham, delay = 0.05)
                    chukyhanhtrangcanmacs.remove(chukyhanhtrang)
                    time.sleep(0.05)

                    if not chukyhanhtrangcanmacs:
                        break

    def action_mua1thancauphu(self):
        print("Mua 1 thần cẩu phù")
        if self.get_is_dusoluongtoithieu(TIENDONG, 2):
            self.moitruong.action_muavatphamkytrancac(IDTABVATPHAMKYTRANCAC_BIENPHU, 12, 1)

    def get_is_hanhtrangday(self):
        return self.get_tongsovatphamhanhtrang() >= 35 or self.moitruong.get_trongluongtoida() - self.get_tongtrongluongvatpham() <= 25

    def get_tongsovatphamhanhtrang(self):
        tongsovatphamhanhtrang = 0

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong != IDVITRIRUONG_HANHTRANG:
                continue

            tongsovatphamhanhtrang += 1

        return tongsovatphamhanhtrang

    def action_tudongfarm(self):
        yeucaudichuyenmoi = None
        try:
            if not self._is_tudongfarm:
                return

            if self._idbandotudongfarm == 0:
                return

            if self.moitruong.get_idbandohientai() != self._idbandotudongfarm:
                self._is_dadichuyentoivitrifarm = False
            elif self.moitruong.get_khoangcachdiem(1, self._toadoxtudongfarm, self._toadoytudongfarm) <= 300:
                self._is_dadichuyentoivitrifarm = True

            if self.get_is_hanhtrangday() and not self._is_dangxulybanrac:
                self._is_dangxulybanrac = True

            if self._is_dangxulybanrac:
                tenbandohientai = self.moitruong.get_tenbandohientai()

                if tenbandohientai in TOADODAIPHU_MAP:
                    toadodaiphu = TOADODAIPHU_MAP.get(tenbandohientai)
                    if self.moitruong.get_khoangcachdiem(1, *toadodaiphu) > 300:
                        yeucaudichuyenmoi = {
                            "loaidichuyen": "tudongtimduong",
                            "toadodich": toadodaiphu
                        }
                    else:
                        yeucaudichuyenmoi = {
                            "loaidichuyen": "dungim"
                        }
                        is_ok = self.action_bantoanbovatpham()
                        if is_ok:
                            self._is_dangxulybanrac = False
                        if not self.get_is_hanhtrangday():
                            self._is_dadichuyentoivitrifarm = False
                else:
                    pass

            else:
                if not self._is_dadichuyentoivitrifarm:
                    if self.moitruong.get_idbandohientai() != self._idbandotudongfarm:
                        yeucaudichuyenmoi = {
                            "loaidichuyen": "tudongtimduongxuyenbando",
                            "idbando": self._idbandotudongfarm,
                            "x": self._toadoxtudongfarm,
                            "y": self._toadoytudongfarm
                        }
                    else:
                        yeucaudichuyenmoi = {
                            "loaidichuyen": "tudongtimduong",
                            "toadodich": (self._toadoxtudongfarm, self._toadoytudongfarm)
                        }
        finally:
            self._yeucaudichuyenfarm = yeucaudichuyenmoi

    def action_bantoanbovatpham(self):
        idnhanvat = self.action_timkiemnhanvat(tennhanvat = "Đại phu", khoangcach = 800)

        if idnhanvat < 0:
            if self.moitruong.get_tenbandohientai() in TOADODAIPHU_MAP and self.moitruong.get_khoangcachdiem(1, *TOADODAIPHU_MAP[self.moitruong.get_tenbandohientai()]) < 600:
                print("{} Không tìm thấy Đại phu".format(self.moitruong.get_tennhanvat()))
            time.sleep(1.)
            return False

        if self.moitruong.get_khoangcach(idnhanvat) > 300:
            self.moitruong.action_dichuyengiukhoangcachtoida(idnhanvat, 0)
            time.sleep(1.)
            return False

        self.moitruong.action_doithoai(idnhanvat, delay = 0.)
        time.sleep(1.)

        if self.moitruong.get_is_dangdoithoaixacnhan():
            self.moitruong.action_xacnhandoithoai(delay = 0.)
            time.sleep(1.)
        else:
            phatam("Đối thoại thất bại")
            return False

        if not self.moitruong.get_is_dangmocuahang():
            phatam("Cửa hàng chưa mở")
            return False

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong != IDVITRIRUONG_HANHTRANG:
                continue

            tenvatpham = self.moitruong.get_tenvatpham(idvatpham)
            if not tenvatpham or tenvatpham in VATPHAMKHONGBANs:
                continue

            loaivatpham = self.moitruong.get_loaivatpham(idvatpham)

            if not loaivatpham:
                continue

            phamchat, danhmucvattutieuhao, danhmuctrangbi, _ = loaivatpham

            is_danduoc = (danhmucvattutieuhao == IDDANHMUCVATTUTIEUHAO_DANDUOC)
            is_trangbi = (danhmuctrangbi in DANHMUCTRANGBI_MAP)

            if not is_danduoc and not is_trangbi and tenvatpham != "Hàn Thiết Thạch":
                continue

            if is_trangbi and self.moitruong.get_capdovatpham(idvatpham) != 10:
                if phamchat != IDPHAMCHATVATPHAM_TRANGLAM:
                    continue

                if danhmuctrangbi in DANHMUCTRANGBI_MAP:
                    thuoctinh_map = self.moitruong.get_thuoctinhvatpham_map(idvatpham)
                    idhephaivatpham = self.moitruong.get_idhephaivatpham(idvatpham)
                    if danhmuctrangbi in (IDDANHMUCTRANGBI_VUKHI, IDDANHMUCTRANGBI_PHIPHONG):
                        if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 20 or thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUBUAPHAP, 0) >= 20:
                            continue
                        if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10 and thuoctinh_map.get(IDTHUOCTINHVATPHAM_DANHTAPTRUNG, 0) >= 10:
                            continue

                    if danhmuctrangbi == IDDANHMUCTRANGBI_AO:
                        if thuoctinh_map.get(IDTHUOCTINHVATPHAM_GIAMTRUNGTHUONG, 0) >= 15:
                            continue

                    if danhmuctrangbi == IDDANHMUCTRANGBI_VUKHI:
                        if idhephaivatpham == IDHEPHAI_DINHAN and thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10:
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_PHIPHONG:
                        if idhephaivatpham == IDHEPHAI_DINHAN and ((thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10 or thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) >= 5) or thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 20):
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_AO:
                        if idhephaivatpham == IDHEPHAI_DINHAN and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOISINHLUC, 0) >= 5:
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_DAI:
                        if idhephaivatpham == -1 and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) >= 5:
                            continue

            self.moitruong.action_banvatpham(sothutuvatpham, delay = 0.)
            time.sleep(0.25)

        self.moitruong.action_dongcuahang(delay = 0.)

        return True

    def action_tudongsuavatpham(self):
        if not self._is_tudongsuavatpham:
            return

        if time.time() - self._thoidiemkiemtrasuavatphamgannhat < 1.:
            return

        self._thoidiemkiemtrasuavatphamgannhat = time.time()

        self.action_suatoanbovatpham()

    def action_suatoanbovatpham(self):
        for i in range(SOLUONGVATPHAMTOIDA):
            idvatpham = self.moitruong.get_idvatpham(i)
            if idvatpham <= 0:
                continue
            dobenhientai = self.moitruong.get_dobenhientaivatpham(idvatpham)
            if dobenhientai < 0:
                continue
            dobentoida = self.moitruong.get_dobentoidavatpham(idvatpham)
            if dobentoida < 0:
                continue

            if dobenhientai * 100 / dobentoida <= 50:
                self.moitruong.action_suavatpham(idvatpham, delay = 0.)
                time.sleep(0.25)

    def action_timkiemnhanvat(self, tennhanvat = None, tenchunhan = None, khoangcach = KHOANGCACHTOIDATIMKIEMMUCTIEU):
        if not tennhanvat and not tenchunhan:
            return -1

        idnhanvat = 0

        while True:
            idnhanvat = self.moitruong.get_idnhanvattieptheo(idnhanvat)
            if idnhanvat <= 0:
                break
            if not self.moitruong.get_is_nhanvattontai(idnhanvat):
                continue
            if self.moitruong.get_khoangcach(idnhanvat) >= khoangcach:
                continue
            if tennhanvat:
                tennhanvatxemxet = self.moitruong.get_tennhanvat(idnhanvat)
                if not tennhanvatxemxet or tennhanvatxemxet.strip().lower() != tennhanvat.strip().lower():
                    continue
            if tenchunhan:
                tenchunhanxemxet = self.moitruong.get_tenchunhan()
                if not tenchunhanxemxet or tenchunhanxemxet.strip().lower() != tenchunhan.strip().lower():
                    continue
            return idnhanvat
        return -1

    def action_timkiemvatpham(self, tenvatpham):
        if not tenvatpham:
            return -1

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong != IDVITRIRUONG_HANHTRANG:
                continue

            tenvatphamxemxet = self.moitruong.get_tenvatpham(idvatpham)
            if tenvatphamxemxet and tenvatphamxemxet.strip().lower() == tenvatpham.strip().lower():
                return sothutuvatpham

        return -1

    def action_tudongbattathieuungbotro(self):
        if not self._is_tudongbattathieuungbotro:
            return

        if self.moitruong.get_is_khuvuccothetancong():
            if self.moitruong.get_idhephai() == IDHEPHAI_DINHAN:
                if not self.moitruong.get_is_datrieuhoithu() and not self.moitruong.get_is_dangtudongtimduong():
                    self._thoidiembathieuungbotrogannhat = time.time()
                    for idhieuungbotro in (IDHIEUUNGBOTRO_THANTIENTAN, IDHIEUUNGBOTRO_DAOTRAMTAN, IDHIEUUNGBOTRO_DAOHUYENTAN, IDHIEUUNGBOTRO_DAOTINHTAN):
                        self.moitruong.action_bathieuungbotro(idhieuungbotro)
                else:
                    if time.time() - self._thoidiembathieuungbotrogannhat > 1.5:
                        for idhieuungbotro in (IDHIEUUNGBOTRO_THANTIENTAN, IDHIEUUNGBOTRO_DAOTRAMTAN, IDHIEUUNGBOTRO_DAOHUYENTAN, IDHIEUUNGBOTRO_DAOTINHTAN): self.moitruong.action_tathieuungbotro(idhieuungbotro)
                return

            idmuctieu = self.moitruong.get_idmuctieutancong()
            if idmuctieu > 0 and (self.moitruong.get_idloainhanvat(idmuctieu) in (IDLOAINHANVAT_NGUOICHOI, IDLOAINHANVAT_TRIEUHOITHU) or self.moitruong.get_is_boss(
                    idmuctieu) or self.moitruong.get_is_quaixanh(idmuctieu)):
                self._thoidiembathieuungbotrogannhat = time.time()
                for idhieuungbotro in (IDHIEUUNGBOTRO_THANTIENTAN, IDHIEUUNGBOTRO_DAOTRAMTAN, IDHIEUUNGBOTRO_DAOHUYENTAN, IDHIEUUNGBOTRO_DAOTINHTAN):
                    self.moitruong.action_bathieuungbotro(idhieuungbotro)
            elif time.time() - self._thoidiembathieuungbotrogannhat > 30.:
                for idhieuungbotro in (IDHIEUUNGBOTRO_THANTIENTAN, IDHIEUUNGBOTRO_DAOTRAMTAN, IDHIEUUNGBOTRO_DAOHUYENTAN, IDHIEUUNGBOTRO_DAOTINHTAN):
                    self.moitruong.action_tathieuungbotro(idhieuungbotro)
        else:
            for idhieuungbotro in (IDHIEUUNGBOTRO_THANTIENTAN, IDHIEUUNGBOTRO_DAOTRAMTAN, IDHIEUUNGBOTRO_DAOHUYENTAN, IDHIEUUNGBOTRO_DAOTINHTAN):
                self.moitruong.action_tathieuungbotro(idhieuungbotro)

    def get_tongtrongluongvatpham(self):
        tongtrongluongvatpham = 0
        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue
            idvatpham, vitriruong, _, _ = vitrivatpham
            if vitriruong != IDVITRIRUONG_HANHTRANG:
                continue
            trongluongvatpham = self.moitruong.get_trongluongvatpham(idvatpham)
            tongtrongluongvatpham += trongluongvatpham

        return tongtrongluongvatpham

    def action_lammoitrangthaitactu(self):
        if self.moitruong.get_idtrangthainhanvat() != IDTRANGTHAINHANVAT_DUNGIM or not self.moitruong.get_is_dangtudongtimduong():
            self._thoidiemnhanvattudongtimduongdungimgannhat = time.time()
        if self.moitruong.get_idtrangthainhanvat() != IDTRANGTHAINHANVAT_DUNGIM:
            self._thoidiemnhanvatdungimgannhat = time.time()

        tenbandohientai = self.moitruong.get_tenbandohientai()
        if tenbandohientai != self._tenbandohientai:
            self._thoidiemthaydoibandogannhat = time.time()
            if self._tenbandohientai:
                self.moitruong.set_idtabkytrancac(-1)

        self._tenbandohientai = tenbandohientai

        phantramsinhluchientai = self.moitruong.get_phantramsinhluchientai()
        self._phantramsinhlucmatdi = self._phantramsinhluchientai - phantramsinhluchientai
        self._phantramsinhluchientai = phantramsinhluchientai
        
        if self.moitruong.get_idhephai() == IDHEPHAI_DINHAN:
            self._idtrieuhoithu = self.action_timkiemnhanvat(tenchunhan = self.moitruong.get_tennhanvat(), khoangcach = 600)

        if not self.moitruong.get_is_tamngungtancong():
            self._thoidiemtamngungtanconggannhat = time.time()

    def action_kiemtraxulyloitudongtimduong(self):
        if self.moitruong.get_idtrangthainhanvat() == IDTRANGTHAINHANVAT_DUNGIM and time.time() - self._thoidiemnhanvattudongtimduongdungimgannhat > 2. and self.moitruong.get_is_dangtudongtimduong():
            self.moitruong.set_is_dangtudongtimduong(False)
            self._toadodichtudongtimduonggannhat = None

    def _kiemtrathoamandieukientancong(self, idnhanvat):
        if not self.moitruong.get_is_nhanvattontai(idnhanvat):
            return False

        if self._tennhanvattancongs and self.moitruong.get_tennhanvat(idnhanvat) not in self._tennhanvattancongs:
            return False

        if self._tennhanvatkhongtancongs and self.moitruong.get_tennhanvat(idnhanvat) in self._tennhanvatkhongtancongs:
            return False

        if self._is_chidanhnguoichoivatrieuhoithu and self.moitruong.get_idloainhanvat(idnhanvat) not in (IDLOAINHANVAT_NGUOICHOI, IDLOAINHANVAT_TRIEUHOITHU):
            return False

        if self.moitruong.get_is_tranhboss() and self.moitruong.get_is_boss(idnhanvat):
            return False

        if not self.moitruong.get_is_cothetancong(idnhanvat):
            return False

        if self._is_khongdanhcungbang and self.moitruong.get_idbandohientai() != IDBANDO_CHIENTRUONG and self.moitruong.get_is_chungbang(idnhanvat):
            return False

        return True
    
    def _sosanhmuctieuuutien(self, idnhanvata, idnhanvatb, toadocosox, toadocosoy):
        if idnhanvatb <= 0:
            return True
        
        khoangcacha = self.moitruong.get_khoangcachdiem(idnhanvata, toadocosox, toadocosoy)
        khoangcachb = self.moitruong.get_khoangcachdiem(idnhanvatb, toadocosox, toadocosoy)

        if self._is_uutientrieuhoithu:
            if khoangcacha <= 650:
                idloainhanvata = self.moitruong.get_idloainhanvat(idnhanvata)
                idloainhanvatb = self.moitruong.get_idloainhanvat(idnhanvatb)
                if idloainhanvata == IDLOAINHANVAT_TRIEUHOITHU and idloainhanvatb != IDLOAINHANVAT_TRIEUHOITHU:
                    return True
                if idloainhanvatb == IDLOAINHANVAT_TRIEUHOITHU and idloainhanvata != IDLOAINHANVAT_TRIEUHOITHU:
                    return False

        if khoangcacha < khoangcachb:
            return True
        
        return False

    def action_tudongtimkiemmuctieu(self):
        if not self._is_tudongtimkiemmuctieu:
            self.moitruong.action_tatvohieuhoathietlapmuctieutancong()
            self.moitruong.action_tatvohieuhoathietlapmuctieudangchon()
            return

        self.moitruong.action_vohieuhoathietlapmuctieutancong()
        self.moitruong.action_vohieuhoathietlapmuctieudangchon()
        self.moitruong.set_iddoituongtudanh(IDDOITUONGTUDANH_MUCTIEUDANGCHON)

        khoangcachtoida = min(KHOANGCACHTOIDATIMKIEMMUCTIEU,  self.moitruong.get_phamvitimkiemmuctieu())

        if self._is_tudongdanhtheosautruongnhom and self.moitruong.get_idtodoi() > 0 and not self.moitruong.get_is_truongnhom():
            toadocosox, toadocosoy = self.moitruong.get_toadotruongnhom()
            if toadocosox <= 0 or toadocosoy <= 0:
                toadocosox, toadocosoy = self.moitruong.get_toado()
        else:
            toadocosox, toadocosoy = self.moitruong.get_toado()

        idungvienso1 = self.moitruong.get_idmuctieutancong()

        if idungvienso1 > 0:
            khoangcach = self.moitruong.get_khoangcachdiem(idungvienso1, toadocosox, toadocosoy)
            if khoangcach >= khoangcachtoida or not self._kiemtrathoamandieukientancong(idungvienso1):
                idungvienso1 = 0

        idnhanvatxemxet = 0
        while True:
            idnhanvatxemxet = self.moitruong.get_idnhanvattieptheo(idnhanvatxemxet)
            if idnhanvatxemxet <= 0:
                break

            if idnhanvatxemxet == 1 or idnhanvatxemxet == idungvienso1:
                continue

            khoangcach = self.moitruong.get_khoangcachdiem(idnhanvatxemxet, toadocosox, toadocosoy)

            if khoangcach >= khoangcachtoida:
                continue

            if not self._kiemtrathoamandieukientancong(idnhanvatxemxet):
                continue

            if self._sosanhmuctieuuutien(idnhanvatxemxet, idungvienso1, toadocosox, toadocosoy):
                idungvienso1 = idnhanvatxemxet

        idmuctieudangchon = self.moitruong.get_idmuctieudangchon()
        idmuctieutancong = self.moitruong.get_idmuctieutancong()
        if idungvienso1 != idmuctieudangchon or idungvienso1 != idmuctieutancong:
            if idungvienso1 > 0:
                self.moitruong.set_idmuctieu(idungvienso1)
            elif idmuctieudangchon > 0 or idmuctieutancong > 0:
                self.moitruong.set_idmuctieu(0)

    def action_batpk(self):
        if self.moitruong.get_idmaupk() != IDMAUPK_DO:
            self.moitruong.action_doimaupk(IDMAUPK_DO)
            sothutuvatpham = self.action_timkiemvatpham(QUANAMTHUY)
            if sothutuvatpham == -1:
                if time.time() - self._thoidiemthongbaohetquanamthuygannhat > 5.:
                    phatam("Không tìm thấy {}".format(QUANAMTHUY))
                    self._thoidiemthongbaohetquanamthuygannhat = time.time()
                return

    def action_tatpk(self):
        if self.moitruong.get_idmaupk() != IDMAUPK_XANH:
            self.moitruong.action_doimaupk(IDMAUPK_XANH)
        if self.moitruong.get_diempk() > 0:
            self.action_sudungvatpham(QUANAMTHUY, delay = 0.)

    def action_sudungvatpham(self, tenvatpham, delay = 0.25):
        sothutuvatpham = self.action_timkiemvatpham(tenvatpham)
        if sothutuvatpham == -1:
            if tenvatpham == QUANAMTHUY:
                if time.time() - self._thoidiemthongbaohetquanamthuygannhat > 5.:
                    phatam("Không tìm thấy {}".format(tenvatpham))
                    self._thoidiemthongbaohetquanamthuygannhat = time.time()
            return False

        return self.moitruong.action_sudungvatpham(sothutuvatpham, delay = delay)

    def action_tudongsudungvatpham(self):
        if self.moitruong.get_is_nhanvatdachet():
            return

        diempk = self.moitruong.get_diempk()
        phantramsinhluchientai = self.moitruong.get_phantramsinhluchientai()

        if diempk > 0:
            if diempk >= 8 or (diempk >= 5 and phantramsinhluchientai <= 70) or (diempk >= 3 and phantramsinhluchientai <= 60) or phantramsinhluchientai <= 50 or self._phantramsinhlucmatdi >= 20:
                if self.action_sudungvatpham(QUANAMTHUY, delay = 0.05):
                    time.sleep(0.05)
                    return

        if self.moitruong.get_idbienthannhanvat() >= 0:
            self._thoidiemyeucaubienthan = time.time()

        if self.moitruong.get_is_khuvuccothetancong() and time.time() - self._thoidiemyeucaubienthan > 2.5 and self.moitruong.get_idbienthannhanvat() < 0 and self.moitruong.get_is_dangbatauto():
            if self.action_sudungvatpham(BIENPHUs[random.randint(0, len(BIENPHUs) - 1)], delay = 1.):
                return

        hieuungbotros = self.moitruong.get_hieuungbotros()
        if IDHIEUUNGBOTRO_BUFFTHUONGCHU1 not in hieuungbotros and IDHIEUUNGBOTRO_BUFFTHUONGCHU2 not in hieuungbotros:
            if self.action_sudungvatpham(BUFFTHUONGCHU, delay = 0.25):
                return

        for tenvatpham in [THANCAUPHU, THANTIENTAN, NIETBANCHU, ]:
            if self.action_sudungvatpham(tenvatpham, delay = 0.25):
                return

    def action_tudongmokhoa(self):
        if not self._is_tudongmokhoa:
            return
        if not self.moitruong.get_is_dangkhoa():
            return
        self.moitruong.action_mokhoa("1")

    def action_tudongdanhtheosautruongnhom(self):
        yeucaudichuyenmoi = None
        try:
            if not self._is_tudongdanhtheosautruongnhom:
                return
            if self._is_dangxulybanrac:
                return
            if not self.moitruong.get_is_dangbatauto():
                return

            if self.moitruong.get_idtodoi() > 0 and not self.moitruong.get_is_truongnhom():
                xtruongnhom, ytruongnhom = self.moitruong.get_toadotruongnhom()

                if xtruongnhom > 0 and ytruongnhom > 0:
                    khoangcach = self.moitruong.get_khoangcachdiem(1, xtruongnhom, ytruongnhom)
                    khoangcachtheosau = self.moitruong.get_khoangcachtheosau()
                    if khoangcach >= khoangcachtheosau:
                        if time.time() - self._thoidiemkiemtrabiket > 1.5:
                            x_hientai, y_hientai = self.moitruong.get_toado()
                            x_cu, y_cu = self._toadokiemtrabiket
                            khoangcachdadi = math.hypot(x_hientai - x_cu, y_hientai - y_cu)
                            if khoangcachdadi < 300:
                                self._is_dangbiket = True
                            else:
                                self._is_dangbiket = False

                            self._toadokiemtrabiket = (x_hientai, y_hientai)
                            self._thoidiemkiemtrabiket = time.time()

                        if khoangcach >= KHOANGCACHTOIDATIMKIEMMUCTIEU or self._is_dangbiket:
                            loaidichuyen = "tudongtimduong"
                        else:
                            loaidichuyen = "dichuyengiukhoangcachtoidadiem"

                        yeucaudichuyenmoi = {
                            "loaidichuyen": loaidichuyen,
                            "toadodich": (xtruongnhom, ytruongnhom),
                            "khoangcach": random.randint(100, 150) if khoangcach >= 1200 else max(khoangcachtheosau - random.randint(100, 150), 0),
                        }
        finally:
            self._yeucaudichuyentheosautruongnhom = yeucaudichuyenmoi

    def action_xulydichuyenuutien(self):
        if self.moitruong.get_is_dangdoithoaixacnhan() or self.moitruong.get_is_dangmocuahang():
            self.moitruong.set_is_duoitheo(False)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
            return

        if self.moitruong.get_idtrangthaiclickchuot() == IDTRANGTHAICLICKCHUOT_CHUOTTRAI:
            return

        yeucauduocchon = None
        is_quaxatruongnhom = False

        if self._yeucaudichuyentheosautruongnhom and "toadodich" in self._yeucaudichuyentheosautruongnhom:
            toadox, toadoy = self._yeucaudichuyentheosautruongnhom["toadodich"]
            khoangcach = self.moitruong.get_khoangcachdiem(1, toadox, toadoy)
            if khoangcach > 900:
                is_quaxatruongnhom = True

        if not self._is_duoitheo:
            if is_quaxatruongnhom:
                yeucauduocchon = self._yeucaudichuyentheosautruongnhom
            elif self._yeucaudichuyentheosautruongnhom:
                yeucauduocchon = self._yeucaudichuyentheosautruongnhom
        else:
            if is_quaxatruongnhom:
                yeucauduocchon = self._yeucaudichuyentheosautruongnhom
            elif self._yeucaudichuyentancong:
                yeucauduocchon = self._yeucaudichuyentancong
            elif self._yeucaudichuyenfarm:
                yeucauduocchon = self._yeucaudichuyenfarm
            elif self._yeucaudichuyentheosautruongnhom:
                yeucauduocchon = self._yeucaudichuyentheosautruongnhom

        if yeucauduocchon:
            self.moitruong.set_is_duoitheo(False)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)

            loaidichuyen = yeucauduocchon.get("loaidichuyen")

            if loaidichuyen == "dichuyengiukhoangcachtoithieu" or (yeucauduocchon == self._yeucaudichuyentheosautruongnhom and is_quaxatruongnhom):
                self.moitruong.set_is_tamngungtancong(True)
            else:
                self.moitruong.set_is_tamngungtancong(False)

            if loaidichuyen == "dungim":
                pass
            elif loaidichuyen == "tudongtimduongxuyenbando":
                idbando = yeucauduocchon.get("idbando")
                x = yeucauduocchon.get("x")
                y = yeucauduocchon.get("y")
                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduongxuyenbando(idbando, x, y)
            elif loaidichuyen == "tudongtimduong":
                toadodich = yeucauduocchon.get("toadodich")
                toadox, toadoy = toadodich
                is_dangtudongtimduong = self.moitruong.get_is_dangtudongtimduong()
                is_cancapnhatduongdi = False
                if not is_dangtudongtimduong:
                    is_cancapnhatduongdi = True
                elif self._toadodichtudongtimduonggannhat:
                    toadocux, toadocuy = self._toadodichtudongtimduonggannhat
                    khoangcachchenhlech = math.hypot(toadox - toadocux, toadoy - toadocuy)
                    if khoangcachchenhlech > 600 and (time.time() - self._thoidiemtudongtimduonggannhat) > 4.5:
                        is_cancapnhatduongdi = True
                else:
                    is_cancapnhatduongdi = True

                if is_cancapnhatduongdi:
                    self.moitruong.action_tudongtimduong(toadox, toadoy)
                    self._toadodichtudongtimduonggannhat = (toadox, toadoy)
            elif loaidichuyen == "dichuyengiukhoangcachtoidadiem":
                self.moitruong.action_dichuyengiukhoangcachtoidadiem(*yeucauduocchon.get("toadodich"), khoangcachtoida = yeucauduocchon.get("khoangcach"))
            elif loaidichuyen == "dichuyengiukhoangcachtoida":
                self.moitruong.action_dichuyengiukhoangcachtoida(yeucauduocchon.get("idmuctieu"), khoangcachtoida = yeucauduocchon.get("khoangcach"))
            elif loaidichuyen == "dichuyengiukhoangcachtoithieu":
                self.moitruong.action_dichuyengiukhoangcachtoithieu(yeucauduocchon.get("idmuctieu"), khoangcachtoithieu = yeucauduocchon.get("khoangcach"))
        else:
            self.moitruong.set_is_tamngungtancong(False)
            if self._is_dangxulybanrac:
                self.moitruong.set_is_duoitheo(False)
                self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
            else:
                if not self._is_duoitheo:
                    self.moitruong.set_is_duoitheo(False)
                    self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
                elif self.moitruong.get_idhephai() in (IDHEPHAI_GIAPSI, IDHEPHAI_DINHAN, IDHEPHAI_VUSI):
                    self.moitruong.set_is_duoitheo(True)
                else:
                    self.moitruong.set_is_duoitheo(False)
                if self._is_duoitheo and (not self._is_tudongdanhtheosautruongnhom or self.moitruong.get_idtodoi() <= 0 or not self.moitruong.get_is_truongnhomcungbando()):
                    self.moitruong.set_is_dichuyenhoatdongquanhphamvi(True)
                else:
                    self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)

    def action_xulytancong(self):
        yeucaudichuyenmoi = None
        try:
            if self.moitruong.get_idhephai() == IDHEPHAI_DINHAN:
                is_datrieuhoithu = self.moitruong.get_is_datrieuhoithu()
                is_vohieuhoa_o3 = True

                if not is_datrieuhoithu:
                    danhsachhieuungbotros = (IDHIEUUNGBOTRO_THANTIENTAN, IDHIEUUNGBOTRO_DAOTRAMTAN, IDHIEUUNGBOTRO_DAOHUYENTAN, IDHIEUUNGBOTRO_DAOTINHTAN)

                    is_cohieuungnhungchuabat = False
                    is_dabatitnhat1hieuungbotro = False

                    for idhieuung in danhsachhieuungbotros:
                        if self.moitruong.get_is_cohieuungbotro(idhieuung):
                            if self.moitruong.get_is_hieuungbotrodangbat(idhieuung):
                                is_dabatitnhat1hieuungbotro = True
                                break
                            else:
                                is_cohieuungnhungchuabat = True

                    if is_dabatitnhat1hieuungbotro or not is_cohieuungnhungchuabat:
                        is_vohieuhoa_o3 = False

                self.moitruong.set_is_vohieuhoakynangbotro3(is_vohieuhoa_o3)

                if is_datrieuhoithu and self._idtrieuhoithu > 0 and self.moitruong.get_khoangcach(self._idtrieuhoithu) < 800 and (self.moitruong.get_sinhluctoida(self._idtrieuhoithu) - self.moitruong.get_sinhluchientai(self._idtrieuhoithu) >= 200):
                    self.moitruong.set_idkynangbotro4(IDKYNANG_BOTAMCHU)
                else:
                    self.moitruong.set_idkynangbotro4(0)

            elif self.moitruong.get_idhephai() == IDHEPHAI_GIAPSI:
                is_cothesudungkynang = self.moitruong.get_is_dangbatauto() and self.moitruong.get_is_khuvuccothetancong() and self.moitruong.get_idtrangthaiclickchuot() != IDTRANGTHAICLICKCHUOT_CHUOTTRAI and not self.moitruong.get_is_dangtudongtimduong()
                if is_cothesudungkynang:
                    idkynang1 = IDKYNANG_LACDIATRAM
                    idmuctieu = self.moitruong.get_idmuctieutancong()
                    if idmuctieu > 0:
                        khoangcachmuctieu = self.moitruong.get_khoangcach(idmuctieu)
                        khoangcachmuctieusaptoi = self.moitruong.get_khoangcachsaptoi(idmuctieu)

                        is_muctieudangdichuyen = self.moitruong.get_idtrangthainhanvat(idmuctieu) == IDTRANGTHAINHANVAT_DICHUYEN
                        is_muctieuchaydi = is_muctieudangdichuyen and khoangcachmuctieusaptoi > khoangcachmuctieu and khoangcachmuctieu > 150

                        if not is_muctieudangdichuyen or self.moitruong.get_idloainhanvat(idmuctieu) != IDLOAINHANVAT_NGUOICHOI:
                            idkynang1 = 0
                    elif self._is_sudungkynangtoadochichuot:
                        self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_KHUYNHTHANHNHATKICH, 0)

                    self.moitruong.set_idkynang1(idkynang1)

            elif self.moitruong.get_idhephai() == IDHEPHAI_DAOSI:
                if self.moitruong.get_phantramkhanghoa() < self.moitruong.get_phantramkhanghoatoida():
                    self.moitruong.set_idkynangbotro4(IDKYNANG_LOIPHONGGIAP)
                else:
                    self.moitruong.set_idkynangbotro4(0)

                is_cothesudungkynang = self.moitruong.get_is_dangbatauto() and self.moitruong.get_is_khuvuccothetancong() and self.moitruong.get_idtrangthaiclickchuot() != IDTRANGTHAICLICKCHUOT_CHUOTTRAI and not self.moitruong.get_is_dangtudongtimduong()
                is_cothesudungkynangbotro = self.moitruong.get_is_dangbatauto() and not self.moitruong.get_is_khuvuccothetancong() and self.moitruong.get_idtrangthaiclickchuot() != IDTRANGTHAICLICKCHUOT_CHUOTTRAI and not self.moitruong.get_is_dangtudongtimduong()
                is_phudau = False
                if is_cothesudungkynang:
                    idmuctieu = self.moitruong.get_idmuctieutancong()
                    if idmuctieu > 0:
                        khoangcachmuctieu = self.moitruong.get_khoangcach(idmuctieu)
                        khoangcachmuctieusaptoi = self.moitruong.get_khoangcachsaptoi(idmuctieu)

                        if is_phudau and not self._is_duoitheo:
                            if 500 < khoangcachmuctieu <= 750:
                                danhsachkynang = [IDKYNANG_TAMMUOICHANHOA] if self._is_khongsudungnhieukynang else [IDKYNANG_TAMMUOICHANHOA, IDKYNANG_BANGPHONGVANLY, IDKYNANG_THAPPHUONGLIETHOA, IDKYNANG_LOIDONGCUUTHIEN, IDKYNANG_BANGPHONGBAO]

                                for idkynang in danhsachkynang:
                                    if self.moitruong.get_is_kynangsansang(idkynang):
                                        self.moitruong.action_sudungkynangphudau(idmuctieu, idkynang, random.randint(450, 475) if idkynang != IDKYNANG_BANGPHONGBAO else random.randint(350, 375))
                                        break
                                return

                            elif khoangcachmuctieu <= 500:
                                if not self._is_khongsudungnhieukynang:
                                    if self.moitruong.get_is_kynangsansang(IDKYNANG_TAMMUOICHANHOA):
                                        self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)
                                    elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGVANLY):
                                        self.moitruong.set_idkynang1(IDKYNANG_BANGPHONGVANLY)
                                    elif self.moitruong.get_is_kynangsansang(IDKYNANG_THAPPHUONGLIETHOA):
                                        self.moitruong.set_idkynang1(IDKYNANG_THAPPHUONGLIETHOA)
                                    elif self.moitruong.get_is_kynangsansang(IDKYNANG_LOIDONGCUUTHIEN):
                                        self.moitruong.set_idkynang1(IDKYNANG_LOIDONGCUUTHIEN)
                                    elif khoangcachmuctieu < 400 and self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGBAO):
                                        self.moitruong.set_idkynang1(IDKYNANG_BANGPHONGBAO)
                                    else:
                                        self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)
                                else:
                                    self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)

                            return

                        yeucaudichuyenmoi = {"loaidichuyen": "dungim"}

                        if self._is_giukhoangcach:
                            is_nguoichoicangiukhoangcach = (self.moitruong.get_idloainhanvat(idmuctieu) == IDLOAINHANVAT_NGUOICHOI and self.moitruong.get_idhephai(idmuctieu) in (IDHEPHAI_GIAPSI, IDHEPHAI_DINHAN))
                            is_boss = self.moitruong.get_is_boss(idmuctieu)
                            khoangcachantoan = 300 if is_nguoichoicangiukhoangcach else 450 if is_boss else 2000
                            if (is_nguoichoicangiukhoangcach or is_boss) and khoangcachmuctieu < khoangcachantoan:
                                is_cokynangsansang = False
                                for idkynang in (IDKYNANG_TAMMUOICHANHOA, IDKYNANG_THAPPHUONGLIETHOA, IDKYNANG_LOIDONGCUUTHIEN, ):
                                    if self.moitruong.get_is_kynangsansang(idkynang):
                                        is_cokynangsansang = True
                                        break

                                if not is_cokynangsansang:
                                    yeucaudichuyenmoi = {
                                        "loaidichuyen": "dichuyengiukhoangcachtoithieu",
                                        "idmuctieu": idmuctieu,
                                        "khoangcach": khoangcachantoan + 50
                                    }
                                    self._yeucaudichuyentancong = yeucaudichuyenmoi
                                    return

                        idtrangthainhanvatmuctieu = self.moitruong.get_idtrangthainhanvat(idmuctieu)
                        is_muctieudungim = idtrangthainhanvatmuctieu in (IDTRANGTHAINHANVAT_DUNGIM, IDTRANGTHAINHANVAT_TANCONG, IDTRANGTHAINHANVAT_TRONGTHUONG)
                        is_muctieutiepcan = idtrangthainhanvatmuctieu == IDTRANGTHAINHANVAT_DICHUYEN and khoangcachmuctieusaptoi < khoangcachmuctieu

                        if is_phudau:
                            khoangcachphudau = 750 if is_muctieutiepcan else 650 if is_muctieudungim else 550

                            if khoangcachmuctieu > khoangcachphudau:
                                yeucaudichuyenmoi = {
                                    "loaidichuyen": "dichuyengiukhoangcachtoida",
                                    "idmuctieu": idmuctieu,
                                    "khoangcach": khoangcachphudau - random.randint(100, 150)
                                }
                                self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)
                                return

                            if 500 < khoangcachmuctieu < khoangcachphudau:
                                if self.moitruong.get_is_kynangsansang(IDKYNANG_TAMMUOICHANHOA):
                                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_TAMMUOICHANHOA, random.randint(450, 475))
                                    return
                                if is_muctieutiepcan and self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGVANLY):
                                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_BANGPHONGVANLY, random.randint(450, 475))
                                    return

                        if khoangcachmuctieu > 500:
                            yeucaudichuyenmoi = {
                                "loaidichuyen": "dichuyengiukhoangcachtoida",
                                "idmuctieu": idmuctieu,
                                "khoangcach": khoangcachmuctieu - random.randint(100, 150) if is_muctieutiepcan else khoangcachmuctieu - random.randint(200, 300)
                            }
                            return

                        if not self._is_khongsudungnhieukynang:
                            if self.moitruong.get_is_kynangsansang(IDKYNANG_TAMMUOICHANHOA):
                                self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)
                            elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGVANLY):
                                self.moitruong.set_idkynang1(IDKYNANG_BANGPHONGVANLY)
                            elif self.moitruong.get_is_kynangsansang(IDKYNANG_THAPPHUONGLIETHOA):
                                self.moitruong.set_idkynang1(IDKYNANG_THAPPHUONGLIETHOA)
                            elif self.moitruong.get_is_kynangsansang(IDKYNANG_LOIDONGCUUTHIEN):
                                self.moitruong.set_idkynang1(IDKYNANG_LOIDONGCUUTHIEN)
                            elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGBAO):
                                if khoangcachmuctieu < 400:
                                    self.moitruong.set_idkynang1(IDKYNANG_BANGPHONGBAO)
                                else:
                                    self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)
                                if 400 <= khoangcachmuctieu <= 500 and is_cothesudungkynang:
                                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_BANGPHONGBAO, random.randint(350, 375))

                    elif self._is_sudungkynangtoadochichuot:
                        if self.moitruong.get_idbandohientai() == IDBANDO_NGOCHUCUNG10NAMTRUOC:
                            if not self.moitruong.get_is_cohieuungbotro(IDHIEUUNGBOTRO_CHUCDUNGCHANKHI):
                                self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_CHUCDUNGCHANKHI, random.randint(450, 475))
                            elif self.moitruong.get_idkynangtaytrai() == IDKYNANG_THIETMABANGQUA:
                                self.moitruong.action_sudungkynangtoadochichuot2(IDKYNANG_TINHTHONGBANGHE, random.randint(450, 475))
                            else:
                                self.moitruong.action_sudungkynangtoadochichuot2(IDKYNANG_TINHTHONGHOAHE, random.randint(450, 475))
                        else:
                            if self.moitruong.get_is_kynangsansang(IDKYNANG_TAMMUOICHANHOA):
                                self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_TAMMUOICHANHOA, random.randint(450, 475))
                            if self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGVANLY):
                                self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_BANGPHONGVANLY, random.randint(450, 475))
                            if self.moitruong.get_is_kynangsansang(IDKYNANG_THAPPHUONGLIETHOA):
                                self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_THAPPHUONGLIETHOA, random.randint(450, 475))
                            if self.moitruong.get_is_kynangsansang(IDKYNANG_LOIDONGCUUTHIEN):
                                self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_LOIDONGCUUTHIEN, random.randint(450, 475))
                            if self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGBAO):
                                self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_BANGPHONGBAO, random.randint(350, 375))
                # elif is_cothesudungkynangbotro:
                #     if self.moitruong.get_is_kynangsansang(IDKYNANG_CHUCDUNGCHANKHI) and not self.moitruong.get_is_cohieuungbotro(IDHIEUUNGBOTRO_CHUCDUNGCHANKHI):
                #         self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_CHUCDUNGCHANKHI, random.randint(450, 475))
                #     elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGCOTUYETCOT) and not self.moitruong.get_is_cohieuungbotro(IDHIEUUNGBOTRO_BANGCOTUYETCOT):
                #         self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_BANGCOTUYETCOT, random.randint(450, 475))
                #     elif self.moitruong.get_is_kynangsansang(IDKYNANG_LOIPHONGGIAP) and not self.moitruong.get_is_cohieuungbotro(IDHIEUUNGBOTRO_LOIPHONGGIAP):
                #         self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_LOIPHONGGIAP, random.randint(450, 475))

            elif self.moitruong.get_idhephai() == IDHEPHAI_VUSI:
                is_cothesudungkynang = self.moitruong.get_is_dangbatauto() and self.moitruong.get_is_khuvuccothetancong() and self.moitruong.get_idtrangthaiclickchuot() != IDTRANGTHAICLICKCHUOT_CHUOTTRAI and not self.moitruong.get_is_dangtudongtimduong()
                is_phudau = False
                if is_cothesudungkynang:
                    idmuctieu = self.moitruong.get_idmuctieutancong()
                    if idmuctieu > 0:
                        khoangcachmuctieu = self.moitruong.get_khoangcach(idmuctieu)
                        khoangcachmuctieusaptoi = self.moitruong.get_khoangcachsaptoi(idmuctieu)

                        if is_phudau and not self._is_duoitheo:
                            if 500 < khoangcachmuctieu <= 900:
                                danhsachkynang = [IDKYNANG_XASAT] if self._is_khongsudungnhieukynang else [IDKYNANG_XASAT, IDKYNANG_BACHBOXUYENDUONG, ]

                                for idkynang in danhsachkynang:
                                    if self.moitruong.get_is_kynangsansang(idkynang):
                                        self.moitruong.action_sudungkynangphudau(idmuctieu, idkynang, random.randint(450, 475))
                                        break
                                return

                            elif khoangcachmuctieu <= 500:
                                if not self._is_khongsudungnhieukynang:
                                    if self.moitruong.get_is_kynangsansang(IDKYNANG_XASAT):
                                        self.moitruong.set_idkynang1(IDKYNANG_XASAT)
                                    elif self.moitruong.get_is_kynangsansang(IDKYNANG_BACHBOXUYENDUONG):
                                        self.moitruong.set_idkynang1(IDKYNANG_BACHBOXUYENDUONG)
                                else:
                                    self.moitruong.set_idkynang1(IDKYNANG_XASAT)
                            return

                        yeucaudichuyenmoi = {"loaidichuyen": "dungim"}

                        if self._is_giukhoangcach:
                            is_nguoichoicangiukhoangcach = (self.moitruong.get_idloainhanvat(idmuctieu) == IDLOAINHANVAT_NGUOICHOI and self.moitruong.get_idhephai(idmuctieu) in (IDHEPHAI_GIAPSI, IDHEPHAI_DINHAN))
                            is_boss = self.moitruong.get_is_boss(idmuctieu)
                            khoangcachantoan = 300 if is_nguoichoicangiukhoangcach else 450 if is_boss else 2000
                            if (is_nguoichoicangiukhoangcach or is_boss) and khoangcachmuctieu < khoangcachantoan:
                                is_cokynangsansang = False
                                for idkynang in (IDKYNANG_XASAT, IDKYNANG_BACHBOXUYENDUONG, ):
                                    if self.moitruong.get_is_kynangsansang(idkynang):
                                        is_cokynangsansang = True
                                        break

                                if not is_cokynangsansang:
                                    yeucaudichuyenmoi = {
                                        "loaidichuyen": "dichuyengiukhoangcachtoithieu",
                                        "idmuctieu": idmuctieu,
                                        "khoangcach": khoangcachantoan + 50
                                    }
                                    self._yeucaudichuyentancong = yeucaudichuyenmoi
                                    return

                        is_muctieudangdichuyen = self.moitruong.get_idtrangthainhanvat(idmuctieu) == IDTRANGTHAINHANVAT_DICHUYEN
                        is_muctieutiepcan = is_muctieudangdichuyen and khoangcachmuctieusaptoi < khoangcachmuctieu

                        if is_phudau:
                            khoangcachphudau = 900

                            if khoangcachmuctieu > khoangcachphudau:
                                yeucaudichuyenmoi = {
                                    "loaidichuyen": "dichuyengiukhoangcachtoida",
                                    "idmuctieu": idmuctieu,
                                    "khoangcach": khoangcachphudau - random.randint(100, 150)
                                }
                                self.moitruong.set_idkynang1(IDKYNANG_XASAT)
                                return

                            if 500 < khoangcachmuctieu < khoangcachphudau:
                                if self.moitruong.get_is_kynangsansang(IDKYNANG_XASAT):
                                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_XASAT, random.randint(450, 475))
                                    return
                                elif self.moitruong.get_is_kynangsansang(IDKYNANG_BACHBOXUYENDUONG):
                                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_BACHBOXUYENDUONG, random.randint(450, 475))
                                    return

                        if khoangcachmuctieu > 500:
                            yeucaudichuyenmoi = {
                                "loaidichuyen": "dichuyengiukhoangcachtoida",
                                "idmuctieu": idmuctieu,
                                "khoangcach": khoangcachmuctieu - random.randint(100, 150) if is_muctieutiepcan else khoangcachmuctieu - random.randint(200, 300)
                            }
                            return

                        if not self._is_khongsudungnhieukynang:
                            if self.moitruong.get_is_kynangsansang(IDKYNANG_XASAT):
                                self.moitruong.set_idkynang1(IDKYNANG_XASAT)
                            elif self.moitruong.get_is_kynangsansang(IDKYNANG_BACHBOXUYENDUONG):
                                self.moitruong.set_idkynang1(IDKYNANG_BACHBOXUYENDUONG)

                    elif self._is_sudungkynangtoadochichuot:
                        if self.moitruong.get_is_kynangsansang(IDKYNANG_XASAT):
                            self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_XASAT, random.randint(450, 475))
                        if self.moitruong.get_is_kynangsansang(IDKYNANG_BACHBOXUYENDUONG):
                            self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_BACHBOXUYENDUONG, random.randint(450, 475))
        finally:
            self._yeucaudichuyentancong = yeucaudichuyenmoi

    def action_tudongdoisetdo(self):
        if not self._is_tudongdoisetdo:
            return

        if self.moitruong.get_idhephai() in (IDHEPHAI_DAOSI, IDHEPHAI_VUSI, IDHEPHAI_GIAPSI):
            if self.moitruong.get_is_khuvuccothetancong() and (not self.moitruong.get_is_tamngungtancong() or time.time() - self._thoidiemtamngungtanconggannhat < 0.25) and not self.moitruong.get_is_dangtudongtimduong():
                if self._setdo1_map:
                    self._macsetdo(self._setdo1_map)
            else:
                if self._setdo2_map:
                    self._macsetdo(self._setdo2_map)

    def action_tudongvutvatpham(self):
        if not self._is_tudongvutvatpham:
            return False

        if not self.moitruong.get_is_khuvuccothetancong():
            return False

        if time.time() - self._thoidiemvutvatphamgannhat < 1.0:
            return False

        vitriracs = []
        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong != IDVITRIRUONG_HANHTRANG:
                continue

            tenvatpham = self.moitruong.get_tenvatpham(idvatpham)
            if not tenvatpham or tenvatpham in VATPHAMKHONGBANs:
                continue

            loaivatpham = self.moitruong.get_loaivatpham(idvatpham)
            if not loaivatpham:
                continue

            phamchat, danhmucvattutieuhao, danhmuctrangbi, _ = loaivatpham

            if danhmuctrangbi not in DANHMUCTRANGBI_MAP:
                continue

            if danhmuctrangbi == IDDANHMUCTRANGBI_THUCUOI:
                continue

            if phamchat != IDPHAMCHATVATPHAM_TRANGLAM:
                continue

            dobentoida = self.moitruong.get_dobentoidavatpham(idvatpham)
            if dobentoida <= 0:
                continue

            thuoctinh_map = self.moitruong.get_thuoctinhvatpham_map(idvatpham)

            if danhmuctrangbi in (IDDANHMUCTRANGBI_VUKHI, IDDANHMUCTRANGBI_PHIPHONG):
                if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 20 or thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUBUAPHAP, 0) >= 20:
                    continue
                if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10 and thuoctinh_map.get(IDTHUOCTINHVATPHAM_DANHTAPTRUNG, 0) >= 10:
                    continue

            if danhmuctrangbi == IDDANHMUCTRANGBI_AO:
                if thuoctinh_map.get(IDTHUOCTINHVATPHAM_GIAMTRUNGTHUONG, 0) >= 15:
                    continue

            vitriracs.append(sothutuvatpham)

        soluongractoithieudevut = 5

        if len(vitriracs) >= soluongractoithieudevut:
            self._is_dangdondeprac = True
        elif len(vitriracs) == 0:
            self._is_dangdondeprac = False

        if self._is_dangdondeprac and len(vitriracs) > 0:
            vitricanvut = vitriracs[0]
            is_thanhcong = self.moitruong.action_vutvatpham(vitricanvut)

            if is_thanhcong:
                self._thoidiemvutvatphamgannhat = time.time()
                return True

        return False

    def get_is_dusoluongtoithieu(self, tenvatpham, soluongtoithieu):
        tongsoluong = 0
        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong not in (IDVITRIRUONG_HANHTRANG, IDVITRIRUONG_DANGCAMTRENTAY):
                continue

            tenvatphamxemxet = self.moitruong.get_tenvatpham(idvatpham)
            if tenvatphamxemxet == tenvatpham:
                tongsoluong += self.moitruong.get_soluongvatpham(idvatpham)
                if tongsoluong >= soluongtoithieu:
                    return True

        return False

    def action_tudongmuavatpham(self):
        if not self._is_tudongmuavatphamkytrancac:
            return False

        if self.moitruong.get_idmaupk() == IDMAUPK_DO or self.moitruong.get_diempk() > 0:
            if not self.get_is_dusoluongtoithieu(QUANAMTHUY, 1):
                if self.get_is_dusoluongtoithieu(TIENDONG, 2):
                    is_muathanhcong = self.moitruong.action_muavatphamkytrancac(IDTABVATPHAMKYTRANCAC_DUOCLIEU, 10, 1)
                    if is_muathanhcong:
                        return True
                    return False

        hieuungbotros = self.moitruong.get_hieuungbotros()
        if IDHIEUUNGBOTRO_NIETBANCHU not in hieuungbotros:
            if not self.get_is_dusoluongtoithieu(NIETBANCHU, 1):
                if self.get_is_dusoluongtoithieu(TIENDONG, 6):
                    is_muathanhcong = self.moitruong.action_muavatphamkytrancac(IDTABVATPHAMKYTRANCAC_GIOITHIEU, 24, 1)
                    if is_muathanhcong:
                        return True
                    return False

        if self._is_tudongbattathieuungbotro:
            if not ({IDHIEUUNGBOTRO_THANTIENTAN, IDHIEUUNGBOTRO_DAOTRAMTAN, IDHIEUUNGBOTRO_DAOHUYENTAN, IDHIEUUNGBOTRO_DAOTINHTAN} & set(hieuungbotros)):
                if not self.get_is_dusoluongtoithieu(THANTIENTAN, 1):
                    if self.get_is_dusoluongtoithieu(TIENDONG, 9):
                        is_muathanhcong = self.moitruong.action_muavatphamkytrancac(IDTABVATPHAMKYTRANCAC_DUOCLIEU, 23, 1, delay = 2.5)
                        if is_muathanhcong:
                            return True
                        return False

        if not self.get_is_dusoluongtoithieu(THANHLO, 1):
            if self.get_is_dusoluongtoithieu(TIENDONG, 8):
                is_muathanhcong = self.moitruong.action_muavatphamkytrancac(IDTABVATPHAMKYTRANCAC_DUOCLIEU, 21, 1, delay = 2.5)
                if is_muathanhcong:
                    return True
                return False

        if not self.get_is_dusoluongtoithieu(CHANKHI, 1):
            if self.get_is_dusoluongtoithieu(TIENDONG, 8):
                is_muathanhcong = self.moitruong.action_muavatphamkytrancac(IDTABVATPHAMKYTRANCAC_DUOCLIEU, 22, 1, delay = 2.5)
                if is_muathanhcong:
                    return True
                return False

        self.moitruong.action_tatvohieuhoapopuptabkytrancac()

        return False

    def action_tudongphucsinh(self):
        if not self._is_phucsinhnhanh:
            return

        if not self.moitruong.get_is_dangbatauto() and not self.moitruong.get_is_dangtudongtimduong():
            return

        is_tudongphucsinh = self.moitruong.get_is_tudongphucsinh()

        if not is_tudongphucsinh and self.moitruong.get_idbandohientai() == IDBANDO_CHIENTRUONG:
            self.moitruong.action_phucsinh(TUYCHONPHUCSINH_VETHANH)

        if not is_tudongphucsinh:
            return

        if self.moitruong.get_is_nhanvatdachet():
            self.moitruong.action_phucsinh()

    def action_dongbotoadohientai(self, delay = 0.25):
        if time.time() - self._thoidiemdongbotoadohientaigannhat < delay:
            return False

        return False

        if self.moitruong.get_idtrangthainhanvat() != IDTRANGTHAINHANVAT_TANCONG:
           return False

        self._thoidiemdongbotoadohientaigannhat = time.time()
        toadox, toadoy = self.moitruong.get_toado()

        return self.moitruong.action_dichuyen2(toadox, toadoy, delay = 0.)

    def action_tudongmoitodoi(self):
        if not self._tennhanvattodoitudongs:
            return
        idtodoi = self.moitruong.get_idtodoi()
        if idtodoi > 0 and not self.moitruong.get_is_truongnhom():
            return
        tenthanhvientrongdois = self.moitruong.get_tenthanhviendoinhoms()
        ungviens = []
        for tenungvien in self._tennhanvattodoitudongs:
            if tenungvien and tenungvien in tenthanhvientrongdois:
                continue
            thoidiemgannhat = self._thoidiemmoitodoigannhat_map.get(tenungvien, 0.)
            if time.time() - thoidiemgannhat > 2.5:
                idnhanvat_ungvien = self.action_timkiemnhanvat(tennhanvat = tenungvien, khoangcach = 800)
                if idnhanvat_ungvien > 0:
                    dbid_hientai = self.moitruong.get_dbidnhanvat(idnhanvat_ungvien)
                    if dbid_hientai > 0:
                        ungviens.append((dbid_hientai, tenungvien, thoidiemgannhat))
        if not ungviens:
            return
        ungviens.sort(key = lambda x: x[2])
        dbidnhanvatduocchon, tennhanvatduocchon, _ = ungviens[0]
        if self.moitruong.action_moitodoi(dbidnhanvatduocchon, delay = 0.25):
            self._thoidiemmoitodoigannhat_map[tennhanvatduocchon] = time.time()