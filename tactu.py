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
        self._tenbandotruockhivebanrac = False

        self._thoidiemkiemtravebanracgannhat = 0.
        self._thoidiemkiemtrasuavatphamgannhat = 0.

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
        for i in range(SOLUONGVATPHAMTOIDA):
            idvatpham = self.moitruong.get_idvatpham(i)
            thongtin = self.moitruong.get_thongtinvatpham_display(idvatpham)
            if thongtin:
                print(thongtin)

    def action_vebanrac(self):
        if self.moitruong.get_tenbandohientai() not in BANDOTRONGTHANHs:
            vitrivatpham = self.action_timkiemvatpham(HOITHANHPHUSIEUCAP)
            if not vitrivatpham:
                phatam("Không tìm thấy {}".format(HOITHANHPHUSIEUCAP))
                return

            if self._tenbandotruockhivebanrac != self.moitruong.get_tenbandohientai():
                self._tenbandotruockhivebanrac = self.moitruong.get_tenbandohientai()

            time.sleep(2.)

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
            self.moitruong.action_sudungvatphamhanhtrang(idvatpham, vitrix, vitriy)

            time.sleep(2.)

        self.action_bantoanbovatpham()

        time.sleep(2.)

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
                print("Sửa vật phẩm {}".format(self.moitruong.get_tenvatpham(idvatpham)))
                self.moitruong.action_suavatpham(idvatpham)

    def action_bantoanbovatpham(self):
        idnhanvat = self.action_timkiemnhanvat(tennhanvat = "Đại phu")
        if idnhanvat < 0:
            tenbandohientai = self.moitruong.get_tenbandohientai()
            if tenbandohientai in TOADODAIPHU_MAP:
                self.moitruong.action_dichuyen(*TOADODAIPHU_MAP.get(tenbandohientai))
            else:
                phatam("Không tìm thấy Đại phu")
            return False

        if self.moitruong.get_khoangcach(idnhanvat) > 450:
            self.moitruong.action_dichuyengiukhoangcachtoithieu(idnhanvat, 0)
            time.sleep(2.)
            return False

        self.moitruong.action_doithoai(idnhanvat)
        time.sleep(2.)

        if not self.moitruong.get_is_dangdoithoai():
            phatam("Đối thoại thất bại")
            return False

        self.moitruong.action_luachondoithoai(1)
        time.sleep(2.)

        if not self.moitruong.get_is_dangmocuahang():
            phatam("Cửa hàng chưa mở")
            return False

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong != VITRIRUONGHANHTRANG:
                continue

            if vitriy <= 1:
                continue

            if self.moitruong.get_tenvatpham(idvatpham) in VATPHAMKHONGBANs:
                continue

            loaivatpham = self.moitruong.get_loaivatpham(idvatpham)

            if not loaivatpham:
                continue

            phamchat, _, danhmuctrangbi, _ = loaivatpham

            if danhmuctrangbi not in DANHMUCTRANGBI_MAP or phamchat != PHAMCHATVATPHAM_TRANGLAM:
                continue

            self.moitruong.action_banvatpham(sothutuvatpham)
            time.sleep(0.25)

        self.moitruong.action_dongcuahang()

        return True

    def get_is_hanhtrangday(self):
        tongsovatphamhanhtrang = 0

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong != VITRIRUONGHANHTRANG:
                continue

            tongsovatphamhanhtrang += 1

        return tongsovatphamhanhtrang >= 30

    def action_tudongvebanrac(self):
        if not self._is_tudongvebanrac:
            return

        if time.time() - self._thoidiemkiemtravebanracgannhat < 1.:
            return

        self._thoidiemkiemtravebanracgannhat = time.time()

        if self.get_is_hanhtrangday():
            self.action_vebanrac()
        elif self.moitruong.get_tenbandohientai() in BANDOTRONGTHANHs:
            tukhoadiemchuyentiep = (self.moitruong.get_tenbandohientai(), self._tenbandotruockhivebanrac or self.moitruong.get_tenbandohientai())
            if tukhoadiemchuyentiep in TOADODIEMCHUYENTIEP_MAP:
                self.moitruong.action_dichuyen(*TOADODIEMCHUYENTIEP_MAP.get(tukhoadiemchuyentiep))

    def action_tudongsuavatpham(self):
        if not self._is_tudongsuavatpham:
            return

        if time.time() - self._thoidiemkiemtrasuavatphamgannhat < 1.:
            return

        self._thoidiemkiemtrasuavatphamgannhat = time.time()

        self.action_suatoanbovatpham()

    def action_timkiemnhanvat(self, tennhanvat, khoangcach = 2000):
        print("{}: action_timkiemnhanvat: {}".format(self.moitruong.get_tennhanvat(), tennhanvat))
        if not tennhanvat:
            return -1
        for idnhanvat in range(SOLUONGNHANVATTOIDA):
            if not self.moitruong.get_is_nhanvattontai(idnhanvat):
                continue
            tennhanvatxemxet = self.moitruong.get_tennhanvat(idnhanvat)
            if tennhanvatxemxet and tennhanvatxemxet.strip() == tennhanvat.strip() and self.moitruong.get_khoangcach(idnhanvat) < khoangcach:
                return idnhanvat
        return -1

    def action_timkiemvatpham(self, tenvatpham):
        print("{}: action_timkiemvatpham: {}".format(self.moitruong.get_tennhanvat(), tenvatpham))
        if not tenvatpham:
            return False

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue
            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
            tenvatphamxemxet = self.moitruong.get_tenvatpham(idvatpham)
            if tenvatphamxemxet and tenvatphamxemxet.strip() == tenvatpham.strip():
                return vitrivatpham
        return False
