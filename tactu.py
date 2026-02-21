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
        self._is_uutienmuctieusinhluc = False
        self._is_uutientrieuhoithu = False
        self._is_uutienboss = False
        self._is_uutiennguoichoi = True
        self._is_tudongtimkiemmuctieu = False
        self._is_khongdanhcungbang = False
        self._is_chidanhnguoichoivatrieuhoithu = False
        self._tennhanvattancongs = set()
        self._tennhanvatkhongtancongs = set()

        self.moitruong = moitruong
        
        self._is_tudongfarmvabanrac = False
        self._is_tudongsuavatpham = True
        self._is_tudongbattathieuungbotro = True
        self._is_tudongboquamuctieumaucao = True
        self._is_tudongmokhoa = False

        self._idbandotudongfarm = 0
        self._toadoxtudongfarm = 0
        self._toadoytudongfarm = 0
        self._is_dadichuyentoivitrifarm = False

        self._thoidiemkiemtrasuavatphamgannhat = 0.

        self._thoidiemnhanvatdungimgannhat = 0.
        self._thoidiemnhanvattudongtimduongdungimgannhat = 0.

        self._tenbandohientai = False
        self._thoidiemthaydoibandogannhat = 0.

        self._is_dangxulybanrac = False

        self._thoidiemtudongnhatdogannhat = 0.

        self._yeucaudichuyentheosautruongnhom = None
        self._yeucaudichuyenfarmvabanrac = None

        self._idmuctieuduphong = 0
        
        self._is_tudongtaypk = True
        self._idtrieuhoithu = -1

        self._yeucautatduoitheo = False

    def __del__(self):
        try:
            self.moitruong.action_tatvohieuhoathietlapmuctieutancong()
            self.moitruong.action_tatvohieuhoathietlapmuctieudangchon()
        except (pymem.exception.PymemError, pymem.exception.WinAPIError):
            pass

    def luuthietlap(self, tennhanvat):
        if not tennhanvat:
            return
            
        thietlap = {
            "is_danhtheosautruongnhom": self._is_tudongdanhtheosautruongnhom,
            "is_tudongfarmvabanrac": self._is_tudongfarmvabanrac,
            "is_tudongsuavatpham": self._is_tudongsuavatpham,
            "is_tudongbattathieuungbotro": self._is_tudongbattathieuungbotro,
            "is_tudongboquamuctieumaucao": self._is_tudongboquamuctieumaucao,
            "idbandotudongfarm": self._idbandotudongfarm,
            "toadoxtudongfarm": self._toadoxtudongfarm,
            "toadoytudongfarm": self._toadoytudongfarm,

            "is_uutienmuctieusinhluc": self._is_uutienmuctieusinhluc,
            "is_uutientrieuhoithu": self._is_uutientrieuhoithu,
            "is_uutienboss": self._is_uutienboss,
            "is_uutiennguoichoi": False,
            "is_tudongtimkiemmuctieu": self._is_tudongtimkiemmuctieu,
            "is_khongdanhcungbang": self._is_khongdanhcungbang,
            "is_chidanhnguoichoivatrieuhoithu": self._is_chidanhnguoichoivatrieuhoithu,
            "tennhanvattancongs": self._tennhanvattancongs,
            "tennhanvatkhongtancongs": self._tennhanvatkhongtancongs,
            "is_tudongmokhoa": self._is_tudongmokhoa,
        }

        util_luuthietlap(str(tennhanvat), thietlap)

    def taithietlap(self, tennhanvat):
        if not tennhanvat:
            return

        thietlap = util_taithietlap(str(tennhanvat))
        if thietlap:
            if "is_danhtheosautruongnhom" in thietlap:
                self._is_tudongdanhtheosautruongnhom = thietlap["is_danhtheosautruongnhom"]

            if "is_tudongfarmvabanrac" in thietlap:
                self._is_tudongfarmvabanrac = thietlap["is_tudongfarmvabanrac"]

            if "is_tudongsuavatpham" in thietlap:
                self._is_tudongsuavatpham = thietlap["is_tudongsuavatpham"]

            if "is_tudongbattathieuungbotro" in thietlap:
                self._is_tudongbattathieuungbotro = thietlap["is_tudongbattathieuungbotro"]

            if "is_tudongboquamuctieumaucao" in thietlap:
                self._is_tudongboquamuctieumaucao = thietlap["is_tudongboquamuctieumaucao"]
            
            if "idbandotudongfarm" in thietlap:
                self._idbandotudongfarm = thietlap["idbandotudongfarm"]
            
            if "toadoxtudongfarm" in thietlap:
                self._toadoxtudongfarm = thietlap["toadoxtudongfarm"]
            
            if "toadoytudongfarm" in thietlap:
                self._toadoytudongfarm = thietlap["toadoytudongfarm"]

            if "is_uutienmuctieusinhluc" in thietlap:
                self._is_uutienmuctieusinhluc = thietlap["is_uutienmuctieusinhluc"]

            if "is_uutientrieuhoithu" in thietlap:
                self._is_uutientrieuhoithu = thietlap["is_uutientrieuhoithu"]

            if "is_uutienboss" in thietlap:
                self._is_uutienboss = thietlap["is_uutienboss"]

            if "is_uutiennguoichoi" in thietlap:
                self._is_uutiennguoichoi = False

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

            if "is_tudongmokhoa" in thietlap:
                self._is_tudongmokhoa = thietlap["is_tudongmokhoa"]

    def battat_tudongfarmvabanrac(self):
        self._is_tudongfarmvabanrac = not self._is_tudongfarmvabanrac

        if self._is_tudongfarmvabanrac:
            if self.moitruong.get_is_khuvuccothetancong():
                self._idbandotudongfarm = self.moitruong.get_idbandohientai()
                self._toadoxtudongfarm = self.moitruong.get_toadox()
                self._toadoytudongfarm = self.moitruong.get_toadoy()
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
        hieuungbotros = self.moitruong.get_hieuungbotros()
        for hieuungbotro in hieuungbotros:
            print("Hiệu ứng bổ trợ: {} {}".format(hieuungbotro, self.moitruong.get_is_hieuungbotrodangbat(hieuungbotro)))
        print("ID bản đồ hiện tại: {}".format(self.moitruong.get_idbandohientai()))
        print("Tọa độ hiện tại: {}, {}".format(self.moitruong.get_toadox(), self.moitruong.get_toadoy()))

    def action_bantoanbovatpham(self):
        idnhanvat = self.action_timkiemnhanvat(tennhanvat = "Đại phu", khoangcach = 800)

        if idnhanvat < 0:
            if self.moitruong.get_tenbandohientai() in TOADODAIPHU_MAP and self.moitruong.get_khoangcachdiem(1, *TOADODAIPHU_MAP[self.moitruong.get_tenbandohientai()]) < 600:
                print("{} Không tìm thấy Đại phu".format(self.moitruong.get_tennhanvat()))
            time.sleep(1.)
            return False

        if self.moitruong.get_khoangcach(idnhanvat) > 300:
            self.moitruong.action_dichuyengiukhoangcachtoithieu(idnhanvat, 0)
            time.sleep(1.)
            return False

        self.moitruong.action_doithoai(idnhanvat, delay = 0.)
        time.sleep(1.)

        if self.moitruong.get_is_dangdoithoailuachon():
            if self.moitruong.get_tenbandohientai() in (BANDO_XIVUUMO, BANDO_SUNGTHANHDOANH, BANDO_NGOCHUCUNG):
                self.moitruong.action_luachondoithoai(1, delay = 0.)
            else:
                self.moitruong.action_luachondoithoai(0, delay = 0.)
            time.sleep(1.)
        elif self.moitruong.get_is_dangdoithoaixacnhan():
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

            if vitriy < 1:
                continue
            
            tenvatpham = self.moitruong.get_tenvatpham(idvatpham)
            if tenvatpham in VATPHAMKHONGBANs:
                continue

            loaivatpham = self.moitruong.get_loaivatpham(idvatpham)

            if not loaivatpham:
                continue

            phamchat, danhmucvattutieuhao, danhmuctrangbi, _ = loaivatpham

            is_danduoc = (danhmucvattutieuhao == IDDANHMUCVATTUTIEUHAO_DANDUOC)
            is_trangbi = (danhmuctrangbi in DANHMUCTRANGBI_MAP)

            if not is_danduoc and not is_trangbi:
                continue

            if is_trangbi:
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
                    if danhmuctrangbi == IDDANHMUCTRANGBI_VUKHI:
                        if idhephaivatpham == IDHEPHAI_DINHAN and thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10:
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_PHIPHONG:
                        if idhephaivatpham == IDHEPHAI_DINHAN and ((thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10 and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) >= 5) or thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 20):
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_AO:
                        if idhephaivatpham == IDHEPHAI_DINHAN and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOISINHLUC, 0) >= 10:
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_DAI:
                        if idhephaivatpham == -1 and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) >= 10:
                            continue
                    

            self.moitruong.action_banvatpham(sothutuvatpham, delay=0.)
            time.sleep(0.25)

        self.moitruong.action_dongcuahang(delay = 0.)

        return True

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

    def action_tudongfarmvabanrac(self):
        self._yeucaudichuyenfarmvabanrac = None

        if not self._is_tudongfarmvabanrac:
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
                    self._yeucaudichuyenfarmvabanrac = {
                        "loaidichuyen": "tudongtimduong",
                        "toadodich": toadodaiphu
                    }
                else:
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
                    self._yeucaudichuyenfarmvabanrac = {
                        "loaidichuyen": "tudongtimduong_xuyenbando",
                        "idbando": self._idbandotudongfarm,
                        "x": self._toadoxtudongfarm,
                        "y": self._toadoytudongfarm
                    }
                else:
                    self._yeucaudichuyenfarmvabanrac = {
                        "loaidichuyen": "tudongtimduong",
                        "toadodich": (self._toadoxtudongfarm, self._toadoytudongfarm)
                    }

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

            if dobenhientai < dobentoida:
                self.moitruong.action_suavatpham(idvatpham, delay = 0.)
                time.sleep(0.25)

    def action_timkiemnhanvat(self, tennhanvat = None, tenchunhan = None, khoangcach = 2000):
        if not tennhanvat and not tenchunhan:
            return -1

        for idnhanvat in range(SOLUONGNHANVATTOIDA):
            if not self.moitruong.get_is_nhanvattontai(idnhanvat):
                continue
            if self.moitruong.get_khoangcach(idnhanvat) > khoangcach:
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
            return False

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue
            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
            tenvatphamxemxet = self.moitruong.get_tenvatpham(idvatpham)
            if tenvatphamxemxet and tenvatphamxemxet.strip().lower() == tenvatpham.strip().lower():
                return vitrivatpham
        return False

    def action_tudongbattathieuungbotro(self):
        if not self._is_tudongbattathieuungbotro:
            return

        if self.moitruong.get_is_khuvuccothetancong():
            if self.moitruong.get_idhephai() == IDHEPHAI_DINHAN:
                if not self.moitruong.get_is_datrieuhoithu() and not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_bathieuungbotro(IDHIEUUNGBOTRO_THANTIENTAN)
                else:
                    self.moitruong.action_tathieuungbotro(IDHIEUUNGBOTRO_THANTIENTAN)
        else:
            self.moitruong.action_tathieuungbotro(IDHIEUUNGBOTRO_THANTIENTAN)

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
        self._tenbandohientai = tenbandohientai

        phantramsinhluchientai = self.moitruong.get_phantramsinhluchientai()
        self._phantramsinhlucmatdi = self._phantramsinhluchientai - phantramsinhluchientai
        self._phantramsinhluchientai = phantramsinhluchientai
        
        if self.moitruong.get_idhephai() == IDHEPHAI_DINHAN:
            self._idtrieuhoithu = self.action_timkiemnhanvat(tenchunhan = self.moitruong.get_tennhanvat())

    def action_kiemtraxulyloitudongtimduong(self):
        if self.moitruong.get_idtrangthainhanvat() == IDTRANGTHAINHANVAT_DUNGIM and time.time() - self._thoidiemnhanvattudongtimduongdungimgannhat > 2. and self.moitruong.get_is_dangtudongtimduong():
            self.moitruong.set_is_dangtudongtimduong(False)

    def action_tudongboquamuctieumaucao(self):
        if not self._is_tudongboquamuctieumaucao:
            return
        
        self.moitruong.action_boquamuctieumaucao(20000 if self.moitruong.get_is_tranhboss() else 999999999)

    def _kiemtrathoamandieukientancong(self, idnhanvat):
        if not self.moitruong.get_is_nhanvattontai(idnhanvat):
            return False

        if self._tennhanvattancongs and self.moitruong.get_tennhanvat(idnhanvat) not in self._tennhanvattancongs:
            return False

        if self._is_chidanhnguoichoivatrieuhoithu and self.moitruong.get_idloainhanvat(idnhanvat) not in (IDLOAINHANVAT_NGUOICHOI, IDLOAINHANVAT_TRIEUHOITHU):
            return False

        if self.moitruong.get_is_tranhboss() and self.moitruong.get_is_boss(idnhanvat):
            return False

        if not self.moitruong.get_is_cothetancong(idnhanvat):
            return False

        if self._is_khongdanhcungbang and self.moitruong.get_is_chungbang(idnhanvat):
            return False

        return True
    
    def _sosanhmuctieuuutien(self, idnhanvata, idnhanvatb, toadocosox, toadocosoy):
        if idnhanvatb <= 0:
            return True
        
        khoangcacha = self.moitruong.get_khoangcachdiem(idnhanvata, toadocosox, toadocosoy)
        khoangcachb = self.moitruong.get_khoangcachdiem(idnhanvatb, toadocosox, toadocosoy)
        
        if self._is_uutienmuctieusinhluc:
            if khoangcacha <= 800:
                sinhluchientaia = self.moitruong.get_sinhluchientai(idnhanvata)
                sinhluchientaib = self.moitruong.get_sinhluchientai(idnhanvatb)
                if sinhluchientaia < sinhluchientaib - 30:
                    return True
                if sinhluchientaib < sinhluchientaia - 30:
                    return False
        
        if self._is_uutientrieuhoithu:
            if khoangcacha <= 800:
                idloainhanvata = self.moitruong.get_idloainhanvat(idnhanvata)
                idloainhanvatb = self.moitruong.get_idloainhanvat(idnhanvatb)
                if idloainhanvata == IDLOAINHANVAT_TRIEUHOITHU and idloainhanvatb != IDLOAINHANVAT_TRIEUHOITHU:
                    return True
                if idloainhanvatb == IDLOAINHANVAT_TRIEUHOITHU and idloainhanvata != IDLOAINHANVAT_TRIEUHOITHU:
                    return False

        if self._is_uutiennguoichoi:
            idloainhanvata = self.moitruong.get_idloainhanvat(idnhanvata)
            idloainhanvatb = self.moitruong.get_idloainhanvat(idnhanvatb)
            if idloainhanvata == IDLOAINHANVAT_NGUOICHOI and idloainhanvatb != IDLOAINHANVAT_NGUOICHOI:
                return True
            if idloainhanvatb == IDLOAINHANVAT_NGUOICHOI and idloainhanvata != IDLOAINHANVAT_NGUOICHOI:
                return False

        if self._is_uutienboss:
             is_bossa = self.moitruong.get_is_boss(idnhanvata)
             is_bossb = self.moitruong.get_is_boss(idnhanvatb)
             if is_bossa and not is_bossb:
                 return True
             if is_bossb and not is_bossa:
                 return False

        if khoangcacha < khoangcachb - 30:
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

        khoangcachtoida = self.moitruong.get_phamvitimkiemmuctieu()

        toadocosox = self.moitruong.get_toadoxtruongnhom()
        if toadocosox <= 0:
            toadocosox = self.moitruong.get_toadox()

        toadocosoy = self.moitruong.get_toadoytruongnhom()
        if toadocosoy <= 0:
            toadocosoy = self.moitruong.get_toadoy()

        idungvienso1 = self.moitruong.get_idmuctieudangchon()
        idungvienso2 = self._idmuctieuduphong

        if idungvienso1 > 0:
            khoangcach = self.moitruong.get_khoangcachdiem(idungvienso1, toadocosox, toadocosoy)
            if khoangcach >= khoangcachtoida or not self._kiemtrathoamandieukientancong(idungvienso1):
                idungvienso1 = 0

        if idungvienso2 > 0:
            khoangcach = self.moitruong.get_khoangcachdiem(idungvienso2, toadocosox, toadocosoy)
            if khoangcach >= khoangcachtoida or not self._kiemtrathoamandieukientancong(idungvienso2):
                idungvienso2 = 0

        if self._sosanhmuctieuuutien(idungvienso2, idungvienso1, toadocosox, toadocosoy):
            idungvienso1, idungvienso2 = idungvienso2, idungvienso1

        idnhanvatxemxet = 0
        for _ in range(SOLUONGNHANVATTOIDA):
            idnhanvatxemxet = self.moitruong.get_idnhanvattieptheo(idnhanvatxemxet)
            if idnhanvatxemxet <= 0:
                break

            if idnhanvatxemxet == idungvienso1 or idnhanvatxemxet == idungvienso2:
                continue

            khoangcach = self.moitruong.get_khoangcachdiem(idnhanvatxemxet, toadocosox, toadocosoy)
            if khoangcach >= khoangcachtoida:
                continue

            if not self._kiemtrathoamandieukientancong(idnhanvatxemxet):
                continue

            if self._sosanhmuctieuuutien(idnhanvatxemxet, idungvienso1, toadocosox, toadocosoy):
                idungvienso2 = idungvienso1
                idungvienso1 = idnhanvatxemxet

            elif self._sosanhmuctieuuutien(idnhanvatxemxet, idungvienso2, toadocosox, toadocosoy):
                idungvienso2 = idnhanvatxemxet

        self._idmuctieuduphong = idungvienso2

        idmuctieudangchon = self.moitruong.get_idmuctieudangchon()

        if idungvienso1 != idmuctieudangchon:
            if idungvienso1 > 0:
                self.moitruong.set_idmuctieu(idungvienso1)
            elif idmuctieudangchon > 0:
                self.moitruong.set_idmuctieu(0)

    def action_batpk(self):
        if self.moitruong.get_idmaupk() != IDMAUPK_DO:
            self.moitruong.action_doimaupk(IDMAUPK_DO)
            vitrivatpham = self.action_timkiemvatpham(QUANAMTHUY)
            if not vitrivatpham:
                phatam("Không tìm thấy {}".format(QUANAMTHUY))
                return

    def action_tatpk(self):
        if self.moitruong.get_idmaupk() != IDMAUPK_XANH:
            self.moitruong.action_doimaupk(IDMAUPK_XANH)
        if self.moitruong.get_diempk() > 0:
            self.action_sudungquanamthuy()

    def action_sudungquanamthuy(self):
        vitrivatpham = self.action_timkiemvatpham(QUANAMTHUY)
        if not vitrivatpham:
            phatam("Không tìm thấy {}".format(QUANAMTHUY))
            return
        idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
        self.moitruong.action_sudungvatphamhanhtrang(idvatpham, vitrix, vitriy, delay = 0.)

    def action_tudongtaypk(self):
        if not self._is_tudongtaypk:
            return
        
        diempk = self.moitruong.get_diempk()
        phantramsinhluchientai = self.moitruong.get_phantramsinhluchientai()

        if diempk > 0:
            if diempk >= 8 or (diempk >= 5 and phantramsinhluchientai <= 70) or (diempk >= 3 and phantramsinhluchientai <= 60) or phantramsinhluchientai <= 50 or self._phantramsinhlucmatdi >= 20:
                self.action_sudungquanamthuy()
    
    def action_tudongnhatvatpham(self):
        if not self.moitruong.get_is_tudongnhatvatpham():
            return
        
        self._thoidiemtudongnhatdogannhat = time.time()

        if self.get_is_hanhtrangday():
            return

        for idvatphamduoidat in range(SOLUONGVATPHAMTOIDADUOIDAT):
            if self.moitruong.get_is_vatphamduoidattontai(idvatphamduoidat):
                is_nhatvatpham = False
                if self.moitruong.get_idmauvatphamnhat() == IDMAUTUCHATVATPHAMNHAT_TRANG:
                    if self.moitruong.get_tuchatvatphamduoidat(idvatphamduoidat) >= IDTUCHATVATPHAMDUOIDAT_TRANG:
                        is_nhatvatpham = True
                elif self.moitruong.get_idmauvatphamnhat() == IDMAUTUCHATVATPHAMNHAT_LAM:
                    if self.moitruong.get_tuchatvatphamduoidat(idvatphamduoidat) >= IDTUCHATVATPHAMDUOIDAT_LAM:
                        is_nhatvatpham = True
                elif self.moitruong.get_idmauvatphamnhat() == IDMAUTUCHATVATPHAMNHAT_LUC:
                    if self.moitruong.get_tuchatvatphamduoidat(idvatphamduoidat) >= IDTUCHATVATPHAMDUOIDAT_LUC:
                        is_nhatvatpham = True

                if not is_nhatvatpham and self.moitruong.get_is_thucuoiduoidat(idvatphamduoidat):
                    is_nhatvatpham = True

                if not is_nhatvatpham:
                    if self.moitruong.get_tenvatphamduoidat(idvatphamduoidat) in (TENVATPHAM_LAMBAOTHACH, TENVATPHAM_MANHHONGTHUYTINH, TENVATPHAM_HONGTHUYTINH, TENVATPHAM_HONGBAOTHACH):
                        is_nhatvatpham = True

                if is_nhatvatpham and self.moitruong.get_khoangcachvatphamduoidat(idvatphamduoidat) < 400:
                    self.moitruong.action_nhatvatpham(idvatphamduoidat)
                    time.sleep(0.02)

    def action_tudongmokhoa(self):
        if not self._is_tudongmokhoa:
            return
        if not self.moitruong.get_is_dangkhoa():
            return
        self.moitruong.action_mokhoa("1")

    def action_tudongdanhtheosautruongnhom(self):
        self._yeucaudichuyentheosautruongnhom = None

        if not self._is_tudongdanhtheosautruongnhom:
            return

        if self._is_dangxulybanrac:
            return

        if self.moitruong.get_idtodoi() > 0 and not self.moitruong.get_is_truongnhom():
            xtruongnhom = self.moitruong.get_toadoxtruongnhom()
            ytruongnhom = self.moitruong.get_toadoytruongnhom()

            if xtruongnhom > 0 and ytruongnhom > 0:
                khoangcach = self.moitruong.get_khoangcachdiem(1, xtruongnhom, ytruongnhom)

                if khoangcach >= self.moitruong.get_khoangcachtheosau():
                    if khoangcach >= 2000 or self.moitruong.get_is_dangtudongtimduong():
                        loaidichuyen = "tudongtimduong"
                    else:
                        loaidichuyen = "dichuyengiukhoangcachtoithieudiem"

                    self._yeucaudichuyentheosautruongnhom = {
                        "loaidichuyen": loaidichuyen,
                        "toadodich": (xtruongnhom, ytruongnhom)
                    }

    def action_xulydichuyenuutien(self):
        if self.moitruong.get_is_dangdoithoailuachon() or self.moitruong.get_is_dangmocuahang():
            self.moitruong.set_is_duoitheo(False)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
            return

        if self.moitruong.get_idtrangthaiclickchuot() == IDTRANGTHAICLICKCHUOT_CHUOTTRAI:
            return

        yeucauduocchon = None
        if self._yeucaudichuyenfarmvabanrac:
            yeucauduocchon = self._yeucaudichuyenfarmvabanrac
        elif self._yeucaudichuyentheosautruongnhom:
            yeucauduocchon = self._yeucaudichuyentheosautruongnhom

        if yeucauduocchon:
            self.moitruong.set_is_duoitheo(False)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)

            loaidichuyen = yeucauduocchon.get("loaidichuyen")

            if loaidichuyen == "tudongtimduong_xuyenbando":
                idbando = yeucauduocchon.get("idbando")
                x = yeucauduocchon.get("x")
                y = yeucauduocchon.get("y")

                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduongxuyenbando(idbando, x, y)

            elif loaidichuyen == "tudongtimduong":
                toadodich = yeucauduocchon.get("toadodich")
                toadox, toadoy = toadodich

                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduong(toadox, toadoy)

            elif loaidichuyen == "dichuyengiukhoangcachtoithieudiem":
                toadodich = yeucauduocchon.get("toadodich")
                toadox, toadoy = toadodich

                self.moitruong.action_dichuyengiukhoangcachtoithieudiem(toadox, toadoy, 0)

        else:
            if self._is_dangxulybanrac:
                self.moitruong.set_is_duoitheo(False)
                self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
            else:
                if self._yeucautatduoitheo:
                    self.moitruong.set_is_duoitheo(False)
                    self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
                else:
                    self.moitruong.set_is_duoitheo(True)
                    if not self._is_tudongdanhtheosautruongnhom or self.moitruong.get_idtodoi() <= 0 or not self.moitruong.get_is_truongnhomcungbando():
                        self.moitruong.set_is_dichuyenhoatdongquanhphamvi(True)
                    else:
                        self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)

    def action_xulytancong(self):
        self._yeucautatduoitheo = False
        if self.moitruong.get_idhephai() == IDHEPHAI_DINHAN:
            if self._idtrieuhoithu > 0 and self.moitruong.get_khoangcach(self._idtrieuhoithu) and (self.moitruong.get_sinhluctoida(self._idtrieuhoithu) - self.moitruong.get_sinhluchientai(self._idtrieuhoithu) >= 200):
                self.moitruong.set_idkynangbotro3(IDKYNANG_BOTAMCHU)

        elif self.moitruong.get_idhephai() == IDHEPHAI_DAOSI:
            is_cothesudungkynang = self.moitruong.get_is_dangbatauto() and self.moitruong.get_idtrangthaiclickchuot() != IDTRANGTHAICLICKCHUOT_CHUOTTRAI
            idmuctieu = self.moitruong.get_idmuctieudangchon()
            if idmuctieu <= 0:
                return
            khoangcachmuctieu = self.moitruong.get_khoangcach(idmuctieu)
            if khoangcachmuctieu >= 650:
                self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)
                return
            self._yeucautatduoitheo = True if is_cothesudungkynang else False
            if 500 <= khoangcachmuctieu < 650 and is_cothesudungkynang:
                if self.moitruong.get_is_kynangsansang(IDKYNANG_TAMMUOICHANHOA):
                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_TAMMUOICHANHOA, random.randint(450, 475))
                    return
                elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGVANLY):
                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_BANGPHONGVANLY, random.randint(450, 475))
                    return
                elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGBAO):
                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_BANGPHONGBAO, random.randint(350, 375))
                    return
            if self.moitruong.get_is_kynangsansang(IDKYNANG_TAMMUOICHANHOA):
                self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)
            elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGVANLY):
                self.moitruong.set_idkynang1(IDKYNANG_BANGPHONGVANLY)
            elif self.moitruong.get_is_kynangsansang(IDKYNANG_THAPPHUONGLIETHOA):
                self.moitruong.set_idkynang1(IDKYNANG_THAPPHUONGLIETHOA)
            elif self.moitruong.get_is_kynangsansang(IDKYNANG_LOIDONGCUUTHIEN):
                self.moitruong.set_idkynang1(IDKYNANG_LOIDONGCUUTHIEN)
            elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGBAO):
                self.moitruong.set_idkynang1(IDKYNANG_BANGPHONGBAO)
                if 400 <= khoangcachmuctieu < 500 and is_cothesudungkynang:
                    self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_BANGPHONGBAO, random.randint(350, 375))