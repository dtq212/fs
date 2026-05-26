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
        self._tennhanvattancongs = set()
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
        
        self._is_tudongtaypk = True
        self._idtrieuhoithu = -1

        self._yeucaudichuyentancong = None
        self._thoidiembathieuungbotrogannhat = 0.
        self._is_sudungkynangtoadochichuot = False

        self._is_tudongdoithucuoi = False

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
            "is_tudongsuavatpham": self._is_tudongsuavatpham,
            "is_tudongbattathieuungbotro": self._is_tudongbattathieuungbotro,

            "is_uutientrieuhoithu": self._is_uutientrieuhoithu,
            "is_tudongtimkiemmuctieu": self._is_tudongtimkiemmuctieu,
            "is_khongdanhcungbang": self._is_khongdanhcungbang,
            "is_chidanhnguoichoivatrieuhoithu": self._is_chidanhnguoichoivatrieuhoithu,
            "tennhanvattancongs": self._tennhanvattancongs,
            "tennhanvatkhongtancongs": self._tennhanvatkhongtancongs,
            "is_tudongmokhoa": self._is_tudongmokhoa,
            "is_tudongdoithucuoi": self._is_tudongdoithucuoi,

            "is_tudongfarm": self._is_tudongfarm,
            "is_tudongvutvatpham": self._is_tudongvutvatpham,
            "idbandotudongfarm": self._idbandotudongfarm,
            "toadoxtudongfarm": self._toadoxtudongfarm,
            "toadoytudongfarm": self._toadoytudongfarm,
        }

        util_luuthietlap(str(tennhanvat), thietlap)

    def taithietlap(self, tennhanvat):
        if not tennhanvat:
            return

        thietlap = util_taithietlap(str(tennhanvat))
        if thietlap:
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

            if "is_tudongmokhoa" in thietlap:
                self._is_tudongmokhoa = thietlap["is_tudongmokhoa"]

            if "is_tudongdoithucuoi" in thietlap:
                self._is_tudongdoithucuoi = thietlap["is_tudongdoithucuoi"]

            if "is_tudongfarm" in thietlap:
                self._is_tudongfarm = thietlap["is_tudongfarm"]

            if "is_tudongvutvatpham" in thietlap:
                self._is_tudongvutvatpham = thietlap["is_tudongvutvatpham"]

            if "idbandotudongfarm" in thietlap:
                self._idbandotudongfarm = thietlap["idbandotudongfarm"]

            if "toadoxtudongfarm" in thietlap:
                self._toadoxtudongfarm = thietlap["toadoxtudongfarm"]

            if "toadoytudongfarm" in thietlap:
                self._toadoytudongfarm = thietlap["toadoytudongfarm"]

    def battat_is_tudongvutvatpham(self):
        self._is_tudongvutvatpham = not self._is_tudongvutvatpham

        if self._is_tudongvutvatpham:
            phatam("Bật tự động vứt rác tại chỗ")
        else:
            phatam("Tắt tự động vứt rác tại chỗ")

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

    def battat_is_tudongdoithucuoi(self):
        self._is_tudongdoithucuoi = not self._is_tudongdoithucuoi

        if self._is_tudongdoithucuoi:
            phatam("Bật tự động đổi thú cưỡi")
        else:
            phatam("Tắt tự động đổi thú cưỡi")

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

        print("toado: {}".format(self.moitruong.get_toado()))

        tenvatpham_canvut = "Mảnh Hồng thủy tinh"
        print(f"--- BẮT ĐẦU TEST VỨT VẬT PHẨM: {tenvatpham_canvut} ---")

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.moitruong.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            if vitriruong != IDVITRIRUONG_HANHTRANG:
                continue

            tenvatphamxemxet = self.moitruong.get_tenvatpham(idvatpham)

            if tenvatphamxemxet and tenvatphamxemxet.strip().lower() == tenvatpham_canvut.lower():
                print(f"[+] Đã tìm thấy '{tenvatphamxemxet}' tại ô index số {sothutuvatpham} (ID: {idvatpham}).")
                print(f"[+] Tiến hành gửi lệnh vứt...")

                ketqua = self.moitruong.action_vutvatpham(sothutuvatpham)

                if ketqua:
                    print("[OK] Lệnh vứt đã được gửi thẳng vào memory (Bypass UI thành công)!")
                    return True
                else:
                    print("[FAIL] Lệnh vứt thất bại (Có thể do delay hoặc packet buffer chưa sẵn sàng).")
                    return False

        print(f"[-] Không tìm thấy '{tenvatpham_canvut}' trong hành trang để test.")
        return False

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
            self.moitruong.action_dichuyengiukhoangcachtoithieu(idnhanvat, 0)
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

            # if vitriy < 1:
            #     continue

            tenvatpham = self.moitruong.get_tenvatpham(idvatpham)
            if not tenvatpham or tenvatpham in VATPHAMKHONGBANs:
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

            if dobenhientai < dobentoida:
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
            for idhieuungbotro in (IDHIEUUNGBOTRO_THANTIENTAN, IDHIEUUNGBOTRO_DAOTRAMTAN, IDHIEUUNGBOTRO_DAOTINHTAN, IDHIEUUNGBOTRO_DAOTINHTAN):
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

    def action_tudongboquaboss(self):
        self.moitruong.action_thietlapboquaboss(True if self.moitruong.get_is_tranhboss() else False)

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

        if self._is_khongdanhcungbang and self.moitruong.get_is_chungbang(idnhanvat):
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
            vitrivatpham = self.action_timkiemvatpham(QUANAMTHUY)
            if not vitrivatpham:
                if time.time() - self._thoidiemthongbaohetquanamthuygannhat > 5.:
                    phatam("Không tìm thấy {}".format(QUANAMTHUY))
                    self._thoidiemthongbaohetquanamthuygannhat = time.time()
                return

    def action_tatpk(self):
        if self.moitruong.get_idmaupk() != IDMAUPK_XANH:
            self.moitruong.action_doimaupk(IDMAUPK_XANH)
        if self.moitruong.get_diempk() > 0:
            self.action_sudungquanamthuy()

    def action_sudungquanamthuy(self):
        vitrivatpham = self.action_timkiemvatpham(QUANAMTHUY)
        if not vitrivatpham:
            if time.time() - self._thoidiemthongbaohetquanamthuygannhat > 5.:
                phatam("Không tìm thấy {}".format(QUANAMTHUY))
                self._thoidiemthongbaohetquanamthuygannhat = time.time()
            return
        idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
        self.moitruong.action_sudungvatpham(idvatpham, vitrix, vitriy, delay = 0.)

    def action_tudongtaypk(self):
        if not self._is_tudongtaypk:
            return
        
        if self.moitruong.get_is_nhanvatdachet():
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
                if self.moitruong.get_tuchatvatphamduoidat(idvatphamduoidat) == IDTUCHATVATPHAMDUOIDAT_LUC:
                    is_nhatvatpham = True

                if not is_nhatvatpham and self.moitruong.get_is_thucuoiduoidat(idvatphamduoidat):
                    is_nhatvatpham = True

                if not is_nhatvatpham:
                    if self.moitruong.get_tenvatphamduoidat(idvatphamduoidat) in (TENVATPHAM_LAMBAOTHACH, TENVATPHAM_MANHHONGTHUYTINH, TENVATPHAM_HONGTHUYTINH, TENVATPHAM_HONGBAOTHACH):
                        is_nhatvatpham = True

                if is_nhatvatpham and self.moitruong.get_khoangcachvatphamduoidat(idvatphamduoidat) < 400:
                    self.moitruong.action_nhatvatpham(idvatphamduoidat)
                    time.sleep(0.02)

        for sothutuvatp in range(SOLUONGVATPHAMTOIDADUOIDAT):
            if self.moitruong.get_is_vatphamduoidattontai(idvatphamduoidat):
                is_nhatvatpham = False
                if self.moitruong.get_tuchatvatphamduoidat(idvatphamduoidat) == IDTUCHATVATPHAMDUOIDAT_LUC:
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

                    if khoangcach >= self.moitruong.get_khoangcachtheosau():
                        if khoangcach >= 2000 or self.moitruong.get_is_dangtudongtimduong():
                            loaidichuyen = "tudongtimduong"
                        else:
                            loaidichuyen = "dichuyengiukhoangcachtoithieudiem"

                        yeucaudichuyenmoi = {
                            "loaidichuyen": loaidichuyen,
                            "toadodich": (xtruongnhom, ytruongnhom)
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
        if self._yeucaudichuyentancong:
            yeucauduocchon = self._yeucaudichuyentancong
        elif self._yeucaudichuyenfarm:
            yeucauduocchon = self._yeucaudichuyenfarm
        elif self._yeucaudichuyentheosautruongnhom:
            yeucauduocchon = self._yeucaudichuyentheosautruongnhom

        if yeucauduocchon:
            self.moitruong.set_is_duoitheo(False)
            self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)

            loaidichuyen = yeucauduocchon.get("loaidichuyen")
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
                    if khoangcachchenhlech > 300:
                        is_cancapnhatduongdi = True
                else:
                    is_cancapnhatduongdi = True

                if is_cancapnhatduongdi:
                    self.moitruong.action_tudongtimduong(toadox, toadoy)
                    self._toadodichtudongtimduonggannhat = (toadox, toadoy)

            elif loaidichuyen == "dichuyengiukhoangcachtoithieudiem":
                toadodich = yeucauduocchon.get("toadodich")
                toadox, toadoy = toadodich
                self.moitruong.action_dichuyengiukhoangcachtoithieudiem(toadox, toadoy, 0)
            elif loaidichuyen == "dichuyengiukhoangcachtoithieu":
                self.moitruong.action_dichuyengiukhoangcachtoithieu(yeucauduocchon.get("idmuctieu"), yeucauduocchon.get("khoangcach"))
        else:
            if self._is_dangxulybanrac:
                self.moitruong.set_is_duoitheo(False)
                self.moitruong.set_is_dichuyenhoatdongquanhphamvi(False)
            else:
                self.moitruong.set_is_duoitheo(True)
                if not self._is_tudongdanhtheosautruongnhom or self.moitruong.get_idtodoi() <= 0 or not self.moitruong.get_is_truongnhomcungbando():
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

                if is_datrieuhoithu and self._idtrieuhoithu > 0 and self.moitruong.get_khoangcach(
                        self._idtrieuhoithu) < 800 and (
                        self.moitruong.get_sinhluctoida(self._idtrieuhoithu) - self.moitruong.get_sinhluchientai(
                    self._idtrieuhoithu) >= 200):
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

                if is_cothesudungkynang:
                    idmuctieu = self.moitruong.get_idmuctieutancong()
                    if idmuctieu > 0:
                        khoangcachmuctieu = self.moitruong.get_khoangcach(idmuctieu)
                        khoangcachmuctieusaptoi = self.moitruong.get_khoangcachsaptoi(idmuctieu)

                        yeucaudichuyenmoi = {"loaidichuyen": "dungim"}

                        is_muctieudangdichuyen = self.moitruong.get_idtrangthainhanvat(idmuctieu) == IDTRANGTHAINHANVAT_DICHUYEN
                        is_muctieutiepcan = is_muctieudangdichuyen and khoangcachmuctieusaptoi < khoangcachmuctieu

                        # khoangcachphudau = 850 if is_muctieutiepcan else 650
                        khoangcachphudau = 500

                        if khoangcachmuctieu > khoangcachphudau:
                            yeucaudichuyenmoi = {
                                "loaidichuyen": "dichuyengiukhoangcachtoithieu",
                                "idmuctieu": idmuctieu,
                                "khoangcach": khoangcachphudau - 5
                            }
                            self.moitruong.set_idkynang1(IDKYNANG_TAMMUOICHANHOA)
                            return

                        if 500 < khoangcachmuctieu < khoangcachphudau:
                            if self.moitruong.get_is_kynangsansang(IDKYNANG_TAMMUOICHANHOA):
                                self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_TAMMUOICHANHOA, random.randint(450, 475))
                                return
                            elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGBAO):
                                self.moitruong.action_sudungkynangphudau(idmuctieu, IDKYNANG_BANGPHONGBAO, random.randint(350, 375))
                                return

                        if khoangcachmuctieu > 500:
                            yeucaudichuyenmoi = {
                                "loaidichuyen": "dichuyengiukhoangcachtoithieu",
                                "idmuctieu": idmuctieu,
                                "khoangcach": 495
                            }
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

                    elif self._is_sudungkynangtoadochichuot:
                        if self.moitruong.get_is_kynangsansang(IDKYNANG_TAMMUOICHANHOA):
                            self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_TAMMUOICHANHOA, random.randint(450, 475))
                        elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGVANLY):
                            self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_BANGPHONGVANLY, random.randint(450, 475))
                        elif self.moitruong.get_is_kynangsansang(IDKYNANG_THAPPHUONGLIETHOA):
                            self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_THAPPHUONGLIETHOA, random.randint(450, 475))
                        elif self.moitruong.get_is_kynangsansang(IDKYNANG_LOIDONGCUUTHIEN):
                            self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_LOIDONGCUUTHIEN, random.randint(450, 475))
                        elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGPHONGBAO):
                            self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_BANGPHONGBAO, random.randint(350, 375))
                elif is_cothesudungkynangbotro:
                    if self.moitruong.get_is_kynangsansang(IDKYNANG_CHUCDUNGCHANKHI) and not self.moitruong.get_is_cohieuungbotro(IDHIEUUNGBOTRO_CHUCDUNGCHANKHI):
                        self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_CHUCDUNGCHANKHI, random.randint(450, 475))
                    elif self.moitruong.get_is_kynangsansang(IDKYNANG_BANGCOTUYETCOT) and not self.moitruong.get_is_cohieuungbotro(IDHIEUUNGBOTRO_BANGCOTUYETCOT):
                        self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_BANGCOTUYETCOT, random.randint(450, 475))
                    elif self.moitruong.get_is_kynangsansang(IDKYNANG_LOIPHONGGIAP) and not self.moitruong.get_is_cohieuungbotro(IDHIEUUNGBOTRO_LOIPHONGGIAP):
                        self.moitruong.action_sudungkynangtoadochichuot(IDKYNANG_LOIPHONGGIAP, random.randint(450, 475))
        finally:
            self._yeucaudichuyentancong = yeucaudichuyenmoi

    def action_tudongdoithucuoi(self):
        if not self._is_tudongdoithucuoi:
            return

        if self.moitruong.get_idhephai() == IDHEPHAI_DAOSI:
            if self.moitruong.get_is_khuvuccothetancong() and (not self.moitruong.get_is_tamngungtancong() or time.time() - self._thoidiemtamngungtanconggannhat < 0.25) and not self.moitruong.get_is_dangtudongtimduong():
                self.moitruong.action_sudungphimtat(2)
            else:
                self.moitruong.action_sudungphimtat(3)
        elif self.moitruong.get_idhephai() == IDHEPHAI_GIAPSI:
            if self.moitruong.get_is_khuvuccothetancong() and (not self.moitruong.get_is_tamngungtancong() or time.time() - self._thoidiemtamngungtanconggannhat < 0.25) and not self.moitruong.get_is_dangtudongtimduong():
                self.moitruong.action_sudungphimtat(2)
            else:
                self.moitruong.action_sudungphimtat(3)

    def action_tudongvutvatpham(self):
        if not self._is_tudongvutvatpham:
            return False

        if time.time() - self._thoidiemvutvatphamgannhat < 0.25:
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

            if not is_danduoc and not is_trangbi:
                continue

            if is_trangbi:
                if phamchat != IDPHAMCHATVATPHAM_TRANGLAM:
                    continue

                if danhmuctrangbi in DANHMUCTRANGBI_MAP:
                    thuoctinh_map = self.moitruong.get_thuoctinhvatpham_map(idvatpham)
                    idhephaivatpham = self.moitruong.get_idhephaivatpham(idvatpham)

                    if danhmuctrangbi in (IDDANHMUCTRANGBI_VUKHI, IDDANHMUCTRANGBI_PHIPHONG):
                        if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 20 or thuoctinh_map.get(
                                IDTHUOCTINHVATPHAM_XUATCHIEUBUAPHAP, 0) >= 20:
                            continue
                        if thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 10 and thuoctinh_map.get(
                                IDTHUOCTINHVATPHAM_DANHTAPTRUNG, 0) >= 10:
                            continue

                    if danhmuctrangbi == IDDANHMUCTRANGBI_AO:
                        if thuoctinh_map.get(IDTHUOCTINHVATPHAM_GIAMTRUNGTHUONG, 0) >= 15:
                            continue

                    if danhmuctrangbi == IDDANHMUCTRANGBI_VUKHI:
                        if idhephaivatpham == IDHEPHAI_DINHAN and thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI,
                                                                                    0) >= 10:
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_PHIPHONG:
                        if idhephaivatpham == IDHEPHAI_DINHAN and ((thuoctinh_map.get(IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI,
                                                                                      0) >= 10 or thuoctinh_map.get(
                                IDTHUOCTINHVATPHAM_HOINOILUC, 0) >= 5) or thuoctinh_map.get(
                                IDTHUOCTINHVATPHAM_XUATCHIEUVUKHI, 0) >= 20):
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_AO:
                        if idhephaivatpham == IDHEPHAI_DINHAN and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOISINHLUC,
                                                                                    0) >= 5:
                            continue
                    elif danhmuctrangbi == IDDANHMUCTRANGBI_DAI:
                        if idhephaivatpham == -1 and thuoctinh_map.get(IDTHUOCTINHVATPHAM_HOINOILUC, 0) >= 5:
                            continue

            is_thanhcong = self.moitruong.action_vutvatpham(sothutuvatpham)

            if is_thanhcong:
                self._thoidiemvutvatphamgannhat = time.time()
                return True

        return False