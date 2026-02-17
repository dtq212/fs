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

        self._idbandotudongfarm = 0
        self._toadoxtudongfarm = 0
        self._toadoytudongfarm = 0

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
            "is_uutiennguoichoi": self._is_uutiennguoichoi,
            "is_tudongtimkiemmuctieu": self._is_tudongtimkiemmuctieu,
            "is_khongdanhcungbang": self._is_khongdanhcungbang,
            "is_chidanhnguoichoivatrieuhoithu": self._is_chidanhnguoichoivatrieuhoithu,
            "tennhanvattancongs": self._tennhanvattancongs,
            "tennhanvatkhongtancongs": self._tennhanvatkhongtancongs,
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
                self._is_uutiennguoichoi = thietlap["is_uutiennguoichoi"]

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

    def battat_tudongfarmvabanrac(self):
        self._is_tudongfarmvabanrac = not self._is_tudongfarmvabanrac

        if self._is_tudongfarmvabanrac and self.moitruong.get_is_khuvuccothetancong():
            self._idbandotudongfarm = self.moitruong.get_idbandohientai()
            self._toadoxtudongfarm = self.moitruong.get_toadox()
            self._toadoytudongfarm = self.moitruong.get_toadoy()
            
            phatam("Bật tự động Farm và Bán rác")
            print(f"Đã lưu tọa độ Farm: Map {self._idbandotudongfarm} - {self._toadoxtudongfarm}:{self._toadoytudongfarm}")
        else:
            phatam("Tắt tự động Farm và Bán rác")

    def battat_tudongdanhtheosautruongnhom(self):
        self._is_tudongdanhtheosautruongnhom = not self._is_tudongdanhtheosautruongnhom

        if self._is_tudongdanhtheosautruongnhom:
            phatam("Bật tự động đánh theo sau trưởng nhóm")
        else:
            phatam("Tắt tự động đánh theo sau trưởng nhóm")

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
        # self.moitruong.action_tudongtimduongxuyenbando(21, 54929, 94496, "Hoàng Thiên Hóa")
        self.action_tudongnhatvatpham()

        # for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
        #     vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
        #     if not vitrivatpham:
        #         continue
        #
        #     idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
        #     if vitriruong != IDVITRIRUONG_HANHTRANG:
        #         continue
        #     print("Tên vật phẩm: {}, Thuộc tính: {}".format(self.moitruong.get_tenvatpham(idvatpham), self.moitruong.get_thongtinvatpham_display(idvatpham)))


        print("ID bản đồ hiện tại: {}".format(self.moitruong.get_idbandohientai()))
        print("Tọa độ hiện tại: {} / {}".format(self.moitruong.get_toadox(), self.moitruong.get_toadoy()))

    def action_tudongtimduongtoidaiphu(self):
        tenbandohientai = self.moitruong.get_tenbandohientai()
        if tenbandohientai in TOADODAIPHU_MAP:
            if not self.moitruong.get_is_dangtudongtimduong():
                self.moitruong.action_tudongtimduong(*TOADODAIPHU_MAP.get(tenbandohientai))
                time.sleep(1.)
        else:
            if tenbandohientai in (BANDO_CULOC, BANDO_DUHON):
                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduong(*TOADODIEMCHUYENTIEP_MAP[tenbandohientai, BANDO_XIVUUMO])
                time.sleep(1.)
            elif tenbandohientai in (BANDO_CHANNUICONLON,):
                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduong(*TOADODIEMCHUYENTIEP_MAP[tenbandohientai, BANDO_NGOCHUCUNG])
                time.sleep(1.)
            elif self.moitruong.get_is_khuvuccothetancong():
                vitrivatpham = self.action_timkiemvatpham(HOITHANHPHUSIEUCAP)
                if not vitrivatpham:
                    phatam("Không tìm thấy {}".format(HOITHANHPHUSIEUCAP))
                    return

                time.sleep(1.)

                idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
                self.moitruong.action_sudungvatphamhanhtrang(idvatpham, vitrix, vitriy, delay = 0.)

                time.sleep(1.)
            else:
                phatam("Chưa thiết lập tọa độ Đại phu cho bản đồ {}".format(tenbandohientai))
                time.sleep(1.)

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
                    if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 20 or thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUBUAPHAP, 0) >= 20:
                        continue
                    if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10 or thuoctinh_map.get(IDTHUOCTINHVATPHAM_DANHTAPTRUNG, 0) >= 10:
                        continue

                    if danhmuctrangbi == IDDANHMUCTRANGBI_PHIPHONG:
                        if ("Báo Thần" in tenvatpham or "Hổ Đầu" in tenvatpham) and thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10 and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) >= 8:
                            continue
                    elif danhmuctrangbi in (IDDANHMUCTRANGBI_NON, IDDANHMUCTRANGBI_AO):
                        if ("Báo Thần" in tenvatpham or "Hổ Đầu" in tenvatpham) and (thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) > 0 or thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOISINHLUC, 0) >= 8):
                            continue
                    else:
                        if "Ngạo Cốt" not in tenvatpham and "Huyền Mộc" not in tenvatpham and "Kiêu Dũng" not in tenvatpham and "Yêu Đái" not in tenvatpham and "Cân" not in tenvatpham and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) >= 8:
                            continue
                    

            self.moitruong.action_banvatpham(sothutuvatpham, delay=0.)
            time.sleep(0.25)

        self.moitruong.action_dongcuahang(delay = 0.)

        return True

    def get_is_hanhtrangday(self):
        return self.get_tongsovatphamhanhtrang() >= 35 or self.get_tongtrongluongvatpham() >= 175

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

        if self.get_is_hanhtrangday() and not self._is_dangxulybanrac:
            self._is_dangxulybanrac = True

        if self._is_dangxulybanrac:
            tenbandohientai = self.moitruong.get_tenbandohientai()

            if tenbandohientai in TOADODAIPHU_MAP:
                toadodaiphu = TOADODAIPHU_MAP.get(tenbandohientai)
                if self.moitruong.get_khoangcachdiem(1, *toadodaiphu) > 300:
                    self._yeucaudichuyenfarmvabanrac = {
                        "loaidichuyen": "trongbando",
                        "toadodich": toadodaiphu
                    }
                else:
                    is_dabanxonghet = self.action_bantoanbovatpham()
                    if is_dabanxonghet:
                        self._is_dangxulybanrac = False
            else:
                pass

        else:
            if self.moitruong.get_idbandohientai() != self._idbandotudongfarm:
                self._yeucaudichuyenfarmvabanrac = {
                    "loaidichuyen": "xuyenbando",
                    "idbando": self._idbandotudongfarm,
                    "x": self._toadoxtudongfarm,
                    "y": self._toadoytudongfarm
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

    def action_timkiemnhanvat(self, tennhanvat, khoangcach = 2000):
        if not tennhanvat:
            return -1
        for idnhanvat in range(SOLUONGNHANVATTOIDA):
            if not self.moitruong.get_is_nhanvattontai(idnhanvat):
                continue
            tennhanvatxemxet = self.moitruong.get_tennhanvat(idnhanvat)
            if tennhanvatxemxet and tennhanvatxemxet.strip().lower() == tennhanvat.strip().lower() and self.moitruong.get_khoangcach(idnhanvat) < khoangcach:
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
            self.moitruong.action_bathieuungbotro(IDHIEUUNGBOTRO_DAOTRAMTAN)
        else:
            self.moitruong.action_tathieuungbotro(IDHIEUUNGBOTRO_DAOTRAMTAN)

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
        pass

    def action_tatpk(self):
        pass

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

    def action_tudongdanhtheosautruongnhom(self):
        self._yeucaudichuyentheosautruongnhom = None

        if not self._is_tudongdanhtheosautruongnhom:
            return

        if self._is_dangxulybanrac:
            return

        if self.moitruong.get_idtodoi() > 0:
            xtruongnhom = self.moitruong.get_toadoxtruongnhom()
            ytruongnhom = self.moitruong.get_toadoytruongnhom()

            if xtruongnhom > 0 and ytruongnhom > 0:
                if self.moitruong.get_khoangcachdiem(1, xtruongnhom, ytruongnhom) >= self.moitruong.get_khoangcachtheosau():
                    self._yeucaudichuyentheosautruongnhom = {
                        "loaidichuyen": "trongbando",
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

            if loaidichuyen == "xuyenbando":
                idbando = yeucauduocchon.get("idbando")
                x = yeucauduocchon.get("x")
                y = yeucauduocchon.get("y")

                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduongxuyenbando(idbando, x, y)

            elif loaidichuyen == "trongbando":
                toadodich = yeucauduocchon.get("toadodich")
                toadox, toadoy = toadodich

                khoangcach = self.moitruong.get_khoangcachdiem(1, toadox, toadoy)
                NGUONGANTOAN = 800

                if khoangcach > NGUONGANTOAN:
                    if not self.moitruong.get_is_dangtudongtimduong():
                        self.moitruong.action_tudongtimduong(toadox, toadoy)
                else:
                    if self.moitruong.get_is_dangtudongtimduong():
                        pass
                    self.moitruong.action_dichuyengiukhoangcachtoithieudiem(toadox, toadoy, 0)
        else:
            if self._is_dangxulybanrac:
                self.moitruong.set_is_duoitheo(False)
                self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
            else:
                self.moitruong.set_is_duoitheo(True)
                self.moitruong.set_is_dichuyenhoatdongquanhphamvi(True)
