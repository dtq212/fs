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

    def action_vebanrac(self):
        vitrivatpham = self.moitruong.action_timkiemvatpham(HOITHANHPHUSIEUCAP)
        if not vitrivatpham:
            phatam("Không tìm thấy {}".format(HOITHANHPHUSIEUCAP))
            return
        idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
        self.moitruong.action_sudungvatphamhanhtrang(idvatpham, vitrix, vitriy)

        time.sleep(5.)

        self.action_bantoanbovatpham()

    def action_bantoanbovatpham(self):
        idnhanvat = self.moitruong.action_timkiemnhanvat(tennhanvat = "Đại phu")
        if idnhanvat < 0:
            phatam("Không tìm thấy Đại phu")
            return
        self.moitruong.action_doithoai(idnhanvat)
        time.sleep(0.5)

        if not self.moitruong.get_is_dangdoithoai():
            phatam("Đối thoại thất bại")
            return

        self.moitruong.action_luachondoithoai(1)
        time.sleep(0.5)

        if not self.moitruong.get_is_dangmocuahang():
            phatam("Cửa hàng chưa mở")

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
            time.sleep(0.25)

        self.moitruong.action_dongcuahang()

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

        return tongsovatphamhanhtrang >= 35
