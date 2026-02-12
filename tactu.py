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
            if idvatpham <= 0:
                continue
            thongtin = self.moitruong.get_thongtinvatpham_display(idvatpham)
            if thongtin:
                print(thongtin)

    def action_vebanrac(self):
        if self.moitruong.get_is_khuvuccothetancong():
            tenbandohientai = self.moitruong.get_tenbandohientai()
            if self._tenbandotruockhivebanrac != tenbandohientai:
                self._tenbandotruockhivebanrac = tenbandohientai

            if tenbandohientai in (BANDO_CULOC, BANDO_DUHON):
                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduong(*TOADODIEMCHUYENTIEP_MAP[tenbandohientai, BANDO_XIVUUMO])
                time.sleep(2.)
            elif tenbandohientai in (BANDO_CHANNUICONLON,):
                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduong(*TOADODIEMCHUYENTIEP_MAP[tenbandohientai, BANDO_NGOCHUCUNG])
                time.sleep(2.)
            else:
                vitrivatpham = self.action_timkiemvatpham(HOITHANHPHUSIEUCAP)
                if not vitrivatpham:
                    phatam("Không tìm thấy {}".format(HOITHANHPHUSIEUCAP))
                    return


                time.sleep(2.)

                idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
                self.moitruong.action_sudungvatphamhanhtrang(idvatpham, vitrix, vitriy, delay = 0.)

                time.sleep(2.)
        else:
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
                self.moitruong.action_suavatpham(idvatpham, delay = 0.)
                time.sleep(0.25)

    def action_bantoanbovatpham(self):
        idnhanvat = self.action_timkiemnhanvat(tennhanvat = "Đại phu", khoangcach = 800)
        if idnhanvat < 0:
            tenbandohientai = self.moitruong.get_tenbandohientai()
            if tenbandohientai in TOADODAIPHU_MAP:
                if not self.moitruong.get_is_dangtudongtimduong():
                    self.moitruong.action_tudongtimduong(*TOADODAIPHU_MAP.get(tenbandohientai))
            else:
                phatam("Không tìm thấy Đại phu")
            return False

        if self.moitruong.get_khoangcach(idnhanvat) > 300:
            self.moitruong.action_dichuyengiukhoangcachtoithieu(idnhanvat, 0)
            time.sleep(2.)
            return False

        self.moitruong.action_doithoai(idnhanvat, delay = 0.)
        time.sleep(2.)

        if not self.moitruong.get_is_dangdoithoai():
            phatam("Đối thoại thất bại")
            return False

        if self.moitruong.get_idhephai() == IDHEPHAI_DAOSI and self.moitruong.get_tenbandohientai() == BANDO_NGOCHUCUNG\
                or self.moitruong.get_idhephai() == IDHEPHAI_DINHAN and self.moitruong.get_tenbandohientai() == BANDO_XIVUUMO\
                or self.moitruong.get_idhephai() == IDHEPHAI_GIAPSI and self.moitruong.get_tenbandohientai() == BANDO_SUNGTHANHDOANH:
            self.moitruong.action_luachondoithoai(1, delay = 0.)
            time.sleep(2.)
        else:
            self.moitruong.action_xacnhandoithoai(delay = 0.)
            time.sleep(2.)

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

            self.moitruong.action_banvatpham(sothutuvatpham, delay = 0.)
            time.sleep(0.25)

        self.moitruong.action_dongcuahang(delay = 0.)

        return True

    def get_is_hanhtrangday(self):
        return self.get_tongsovatphamhanhtrang() >= 35 or self.get_tongtrongluongvatpham() >= 185

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

        if self.get_is_hanhtrangday():
            self.action_vebanrac()
        elif not self.moitruong.get_is_khuvuccothetancong() and not self.moitruong.get_is_dangtudongtimduong():
            tukhoadiemchuyentiep = (self.moitruong.get_tenbandohientai(), self._tenbandotruockhivebanrac or self.moitruong.get_tenbandohientai())
            if tukhoadiemchuyentiep in TOADODIEMCHUYENTIEP_MAP:
                self.moitruong.action_tudongtimduong(*TOADODIEMCHUYENTIEP_MAP[tukhoadiemchuyentiep])

    def action_tudongsuavatpham(self):
        if not self._is_tudongsuavatpham:
            return

        if time.time() - self._thoidiemkiemtrasuavatphamgannhat < 1.:
            return

        self._thoidiemkiemtrasuavatphamgannhat = time.time()

        self.action_suatoanbovatpham()

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
            if vitriruong not in (IDVITRIRUONG_HANHTRANG, IDVITRIRUONG_TRANGBI):
                continue
            tongtrongluongvatpham += self.moitruong.get_trongluongvatpham(idvatpham)
        return tongtrongluongvatpham

    def action_lammoitrangthaitactu(self):
        if self.moitruong.get_idtrangthainhanvat() != IDTRANGTHAINHANVAT_DUNGIM:
            self._thoidiemnhanvatdungimgannhat = time.time()

    def action_kiemtraxulyloitudongtimduong(self):
        if self.moitruong.get_idtrangthainhanvat() == IDTRANGTHAINHANVAT_DUNGIM and time.time() - self._thoidiemnhanvatdungimgannhat > 2. and self.moitruong.get_is_dangtudongtimduong():
            self.moitruong.set_is_dangtudongtimduong(False)