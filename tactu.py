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

        self._tenbandotruockhivebanrac = False

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

    def action_vebanrac(self):
        if self.moitruong.get_tenbandohientai() not in TRONGTHANHs:
            vitrivatpham = self.moitruong.action_timkiemvatpham(HOITHANHPHUSIEUCAP)
            if not vitrivatpham:
                phatam("Không tìm thấy {}".format(HOITHANHPHUSIEUCAP))
                return

            if self._tenbandotruockhivebanrac != self.moitruong.get_tenbandohientai():
                self._tenbandotruockhivebanrac = self.moitruong.get_tenbandohientai()

            time.sleep(1.)

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
            self.moitruong.action_sudungvatphamhanhtrang(idvatpham, vitrix, vitriy)

            time.sleep(1.)

        self.action_bantoanbovatpham()

        time.sleep(1.)

    def action_bantoanbovatpham(self):
        idnhanvat = self.moitruong.action_timkiemnhanvat(tennhanvat = "Đại phu")
        if idnhanvat < 0:
            phatam("Không tìm thấy Đại phu")
            return False

        if self.moitruong.get_khoangcach(idnhanvat) > 450:
            self.moitruong.action_dichuyengiukhoangcachtoithieu(idnhanvat, 0)
            time.sleep(1.0)
            return False

        self.moitruong.action_doithoai(idnhanvat)
        time.sleep(1.0)

        if not self.moitruong.get_is_dangdoithoai():
            phatam("Đối thoại thất bại")
            return False

        self.moitruong.action_luachondoithoai(1)
        time.sleep(1.0)

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

            self.moitruong.action_banvatpham(sothutuvatpham)
            time.sleep(0.5)

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

        print("{}: tongsovatphamhanhtrang: {}".format(self.moitruong.get_tennhanvat(), tongsovatphamhanhtrang))

        return tongsovatphamhanhtrang >= 35

    def action_tudongvebanrac(self):
        if not self._is_tudongvebanrac:
            return

        if self.get_is_hanhtrangday():
            self.action_vebanrac()
        elif self.moitruong.get_tenbandohientai() in TRONGTHANHs:
            tukhoadiemchuyentiep = (self.moitruong.get_tenbandohientai(), self._tenbandotruockhivebanrac or self.moitruong.get_tenbandohientai())
            if tukhoadiemchuyentiep in DIEMCHUYENTIEP_MAP:
                self.moitruong.action_dichuyen(*DIEMCHUYENTIEP_MAP.get(tukhoadiemchuyentiep))