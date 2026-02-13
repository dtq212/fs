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
        self.moitruong = moitruong
        self._is_tudongvebanrac = True
        self._is_tudongsuavatpham = True
        self._is_tudongbattathieuungbotro = True
        self._tenbandotruockhivebanrac = False

        self._thoidiemkiemtravebanracgannhat = 0.
        self._thoidiemkiemtrasuavatphamgannhat = 0.

        self._thoidiemnhanvatdungimgannhat = 0.
        self._thoidiemnhanvattudongtimduongdungimgannhat = 0.

        self._tenbandohientai = False
        self._thoidiemthaydoibandogannhat = 0.

        self._is_dangxulybanrac = False

    def __del__(self):
        try:
            pass
        except (pymem.exception.PymemError, pymem.exception.WinAPIError):
            pass

    def luuthietlap(self, idnguoichoi):
        thietlap = {
            
        }
        util_luuthietlap(str(idnguoichoi), thietlap)

    def taithietlap(self, idnguoichoi):
        thietlap = util_taithietlap(str(idnguoichoi))
        if thietlap:
            pass

    def battat_tudongvebanrac(self):
        self._is_tudongvebanrac = not self._is_tudongvebanrac

        if self._is_tudongvebanrac:
            phatam("Bật tự động về bán rác")
        else:
            phatam("Tắt tự động về bán rác")

    def battat_tudongsuavatpham(self):
        self._is_tudongsuavatpham = not self._is_tudongsuavatpham

        if self._is_tudongsuavatpham:
            phatam("Bật tự động sửa vật phẩm")
        else:
            phatam("Tắt tự động sửa vật phẩm")

    def action_test(self):
        data = []
        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue
            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
            if vitriruong != IDVITRIRUONG_HANHTRANG:
                continue
            trongluongvatpham = self.moitruong.get_trongluongvatpham(idvatpham)

            data.append((vitrix, vitriy, self.moitruong.get_tenvatpham(idvatpham), trongluongvatpham))

        print(data.sort())

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
            idnhanvat = self.action_timkiemnhanvat(tennhanvat = "Đại Phu", khoangcach = 800)

        if idnhanvat < 0:
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

            if self.moitruong.get_tenvatpham(idvatpham) in VATPHAMKHONGBANs:
                continue

            loaivatpham = self.moitruong.get_loaivatpham(idvatpham)

            if not loaivatpham:
                continue

            phamchat, _, danhmuctrangbi, _ = loaivatpham

            if danhmuctrangbi in DANHMUCTRANGBI_MAP and phamchat != IDPHAMCHATVATPHAM_TRANGLAM:
                continue

            if danhmuctrangbi == IDDANHMUCTRANGBI_VUKHI:
                thuoctinh_map = self.moitruong.get_thuoctinhvatpham_map(idvatpham)
                if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 20 or thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUBUAPHAP, 0) >= 20:
                    continue

            self.moitruong.action_banvatpham(sothutuvatpham, delay = 0.)
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

    def action_tudongvebanrac(self):
        if not self._is_tudongvebanrac:
            return

        if time.time() - self._thoidiemkiemtravebanracgannhat < 1.:
            return
        self._thoidiemkiemtravebanracgannhat = time.time()

        tenbandohientai = self.moitruong.get_tenbandohientai()
        is_khuvuccothetancong = self.moitruong.get_is_khuvuccothetancong()

        if self._is_dangxulybanrac:
            self.moitruong.set_is_duoitheo(False)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
        else:
            self.moitruong.set_is_duoitheo(True)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(True)

        if self.get_is_hanhtrangday() and not self._is_dangxulybanrac:
            self._is_dangxulybanrac = True
            if is_khuvuccothetancong:
                self._tenbandotruockhivebanrac = tenbandohientai

        if self._is_dangxulybanrac:
            self.action_tudongtimduongtoidaiphu()

            if not self.moitruong.get_is_dangtudongtimduong():
                is_dabanxonghet = self.action_bantoanbovatpham()
                if is_dabanxonghet:
                    self._is_dangxulybanrac = False
        else:
            if not self.moitruong.get_is_dangtudongtimduong():
                tenbandotruockhivebanrac = self._tenbandotruockhivebanrac
                if not tenbandotruockhivebanrac:
                    tenbandotruockhivebanrac = tenbandohientai

                tukhoadiemchuyentiep = (tenbandohientai, tenbandotruockhivebanrac)

                if tukhoadiemchuyentiep in TOADODIEMCHUYENTIEP_MAP:
                    self.moitruong.action_tudongtimduong(*TOADODIEMCHUYENTIEP_MAP[tukhoadiemchuyentiep])

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
            if tennhanvatxemxet and tennhanvatxemxet == tennhanvat and self.moitruong.get_khoangcach(idnhanvat) < khoangcach:
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
            if tenvatphamxemxet and tenvatphamxemxet == tenvatpham:
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