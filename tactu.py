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

        self._thoidiemkiemtravebanracgannhat = 0.
        self._thoidiemkiemtrasuavatphamgannhat = 0.

        self._thoidiemnhanvatdungimgannhat = 0.
        self._thoidiemnhanvattudongtimduongdungimgannhat = 0.

        self._tenbandohientai = False
        self._thoidiemthaydoibandogannhat = 0.

        self._is_dangxulybanrac = False

        self._thoidiemtudongnhatdogannhat = 0.

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

                    if danhmuctrangbi == IDDANHMUCTRANGBI_PHIPHONG:
                        if ("Báo Thần" in tenvatpham or "Hổ Đầu" in tenvatpham) and thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10 and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) > 0:
                            continue
                    elif danhmuctrangbi in (IDDANHMUCTRANGBI_NON, IDDANHMUCTRANGBI_AO):
                        if ("Báo Thần" in tenvatpham or "Hổ Đầu" in tenvatpham) and (thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) > 0 or thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOISINHLUC, 0) > 0):
                            continue
                    else:
                        if "Ngạo Cốt" not in tenvatpham and "Huyền Mộc" not in tenvatpham and "Kiêu Dũng" not in tenvatpham and "Yêu Đái" not in tenvatpham and "Cân" not in tenvatpham and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) > 0:
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
        if not self._is_tudongfarmvabanrac:
            return

        if time.time() - self._thoidiemkiemtravebanracgannhat < 1.:
            return
        self._thoidiemkiemtravebanracgannhat = time.time()

        if self._idbandotudongfarm == 0:
            return

        is_khuvuccothetancong = self.moitruong.get_is_khuvuccothetancong()

        if self.get_is_hanhtrangday() and not self._is_dangxulybanrac:
            self._is_dangxulybanrac = True

        if self._is_dangxulybanrac:
            self.moitruong.set_is_duoitheo(False)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)

            self.action_tudongtimduongtoidaiphu()

            if not self.moitruong.get_is_dangtudongtimduong():
                is_dabanxonghet = self.action_bantoanbovatpham()
                if is_dabanxonghet:
                    self._is_dangxulybanrac = False
        else:
            self.moitruong.set_is_duoitheo(True)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(True)

            idbandohientai = self.moitruong.get_idbandohientai()
            
            if idbandohientai != self._idbandotudongfarm:
                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduongxuyenbando(
                        self._idbandotudongfarm, 
                        self._toadoxtudongfarm, 
                        self._toadoytudongfarm
                    )

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

    def action_tudongtimkiemmuctieu(self):
        if not self._is_tudongtimkiemmuctieu:
            self.moitruong.action_tatvohieuhoathietlapmuctieutancong()
            self.moitruong.action_tatvohieuhoathietlapmuctieudangchon()
            return
        self.moitruong.action_vohieuhoathietlapmuctieutancong()
        self.moitruong.action_vohieuhoathietlapmuctieudangchon()

        self.moitruong.set_iddoituongtudanh(IDDOITUONGTUDANH_MUCTIEUDANGCHON)

        khoangcachtoida = self.moitruong.get_phamvitimkiemmuctieu()

        idmuctieudangchon = self.moitruong.get_idmuctieudangchon()
        if idmuctieudangchon:
            if self._tennhanvattancongs and self.moitruong.get_tennhanvat(idmuctieudangchon) not in self._tennhanvattancongs:
                idmuctieudangchon = 0
            elif self._is_chidanhnguoichoivatrieuhoithu and self.moitruong.get_idloainhanvat(idmuctieudangchon) not in (IDLOAINHANVAT_NGUOICHOI, IDLOAINHANVAT_TRIEUHOITHU):
                idmuctieudangchon = 0
            elif self.moitruong.get_is_tranhboss() and self.moitruong.get_is_boss(idmuctieudangchon):
                idmuctieudangchon = 0
            elif not self.moitruong.get_is_cothetancong(idmuctieudangchon):
                idmuctieudangchon = 0
            elif self._is_khongdanhcungbang and self.moitruong.get_is_chungbang(idmuctieudangchon):
                idmuctieudangchon = 0

        self.moitruong.set_idmuctieu(idmuctieudangchon)

        idnhanvatxemxet = 0

        for _ in range(SOLUONGNHANVATTOIDA):
            idnhanvatxemxet = self.moitruong.get_idnhanvattieptheo(idnhanvatxemxet)
            if not idnhanvatxemxet:
                break

            idmuctieudangchon = self.moitruong.get_idmuctieudangchon()
            if idnhanvatxemxet == idmuctieudangchon:
                continue

            if not self.moitruong.get_is_nhanvattontai(idnhanvatxemxet):
                continue

            khoangcachmuctieuxemxet = self.moitruong.get_khoangcach(idnhanvatxemxet)
            if khoangcachmuctieuxemxet >= khoangcachtoida:
                continue

            if self._tennhanvattancongs and self.moitruong.get_tennhanvat(idnhanvatxemxet) not in self._tennhanvattancongs:
                continue

            if self._is_chidanhnguoichoivatrieuhoithu and self.moitruong.get_idloainhanvat(idnhanvatxemxet) not in (IDLOAINHANVAT_NGUOICHOI, IDLOAINHANVAT_TRIEUHOITHU):
                continue

            if self.moitruong.get_is_tranhboss() and self.moitruong.get_is_boss(idnhanvatxemxet):
                continue

            if not self.moitruong.get_is_cothetancong(idnhanvatxemxet):
                continue

            if self._is_khongdanhcungbang and self.moitruong.get_is_chungbang(idnhanvatxemxet):
                continue

            if not idmuctieudangchon:
                self.moitruong.set_idmuctieu(idnhanvatxemxet)
            else:
                if self._is_uutienmuctieusinhluc:
                    if khoangcachmuctieuxemxet <= 800:
                        sinhlucconlaimuctieuxemxet = self.moitruong.get_sinhluchientai(idnhanvatxemxet)
                        sinhlucconlaimuctieu = self.moitruong.get_sinhluchientai(idmuctieudangchon)
                        if sinhlucconlaimuctieuxemxet >= sinhlucconlaimuctieu - 30:
                            continue

                if self._is_uutientrieuhoithu:
                    if khoangcachmuctieuxemxet <= 800:
                        if self.moitruong.get_idloainhanvat(idnhanvatxemxet) != IDLOAINHANVAT_TRIEUHOITHU:
                            if self.moitruong.get_idloainhanvat(idmuctieudangchon) == IDLOAINHANVAT_TRIEUHOITHU:
                                continue
                        elif self.moitruong.get_idloainhanvat(idmuctieudangchon) != IDLOAINHANVAT_TRIEUHOITHU:
                            self.moitruong.set_idmuctieu(idnhanvatxemxet)
                            continue
                        elif khoangcachmuctieuxemxet < self.moitruong.get_khoangcach(idmuctieudangchon) - 30:
                            self.moitruong.set_idmuctieu(idnhanvatxemxet)
                            continue

                if self._is_uutiennguoichoi:
                    if self.moitruong.get_idloainhanvat(idnhanvatxemxet) != 1:
                        if self.moitruong.get_idloainhanvat(idmuctieudangchon) == 1:
                            continue
                    elif self.moitruong.get_idloainhanvat(idmuctieudangchon) != 1:
                        self.moitruong.set_idmuctieu(idnhanvatxemxet)
                        continue
                    elif khoangcachmuctieuxemxet < self.moitruong.get_khoangcach(idmuctieudangchon) - 30:
                        self.moitruong.set_idmuctieu(idnhanvatxemxet)
                        continue

                if self._is_uutienboss:
                    if not self.moitruong.get_is_boss(idnhanvatxemxet):
                        if self.moitruong.get_is_boss(idmuctieudangchon):
                            continue
                    elif not self.moitruong.get_is_boss(idmuctieudangchon):
                        self.moitruong.set_idmuctieu(idnhanvatxemxet)
                        continue
                    elif khoangcachmuctieuxemxet < self.moitruong.get_khoangcach(idmuctieudangchon) - 30:
                        self.moitruong.set_idmuctieu(idnhanvatxemxet)
                        continue

                if khoangcachmuctieuxemxet < self.moitruong.get_khoangcach(idmuctieudangchon) - 30:
                    self.moitruong.set_idmuctieu(idnhanvatxemxet)
                    continue

    def action_batpk(self):
        pass

    def action_tatpk(self):
        pass

    def action_tudongnhatvatpham(self, delay = 0.1):
        if not self.moitruong.get_is_tudongnhatvatpham():
            return
        if time.time() - self._thoidiemtudongnhatdogannhat < delay:
            return
        self._thoidiemtudongnhatdogannhat = time.time()
        for idvatphamduoidat in range(SOLUONGVATPHAMTOIDADUOIDAT):
            if self.moitruong.get_is_vatphamduoidattontai(idvatphamduoidat):
                is_nhatvatpham = False
                if self.moitruong.get_tuchatvatphamduoidat(idvatphamduoidat) >= IDTUCHATVATPHAMDUOIDAT_LUC:
                    is_nhatvatpham = True
                if self.moitruong.get_is_thucuoiduoidat(idvatphamduoidat):
                    is_nhatvatpham = True
                if not is_nhatvatpham:
                    if self.moitruong.get_tenvatphamduoidat(idvatphamduoidat) in (TENVATPHAM_LAMBAOTHACH, TENVATPHAM_MANHHONGTHUYTINH, TENVATPHAM_HONGTHUYTINH, TENVATPHAM_HONGBAOTHACH):
                        is_nhatvatpham = True
                if is_nhatvatpham and self.moitruong.get_khoangcachvatphamduoidat(idvatphamduoidat) < 400:
                    self.moitruong.action_nhatvatpham(idvatphamduoidat)
                    time.sleep(0.02)
