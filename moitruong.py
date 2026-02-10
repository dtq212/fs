import ctypes

import pymem
import win32gui
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

from hangso import *
from tienich import *

OFFSET_DIACHICOSONHANVAT = 0x3B0CD0
OFFSET_DIACHICOSOMOINHANVAT = 0x8294

#ĐỊA CHỈ CƠ SỞ THÔNG TIN VẬT PHẨM
#Moi bằng id vị trí rương = 1 khi cầm vật phẩm lên và đặt xuống hành trang là 3
OFFSET_DIACHICOSOVITRIVATPHAM = 0x3956B4
OFFSET_DIACHICOSOVITRIMOIVATPHAM = 0x10

#Moi từ địa chỉ số lượng hàng và cột tối đa trong hành trang (Tìm kiếm theo byte array 05 00 00 00 0E 00 00 00 rồi trừ cho 0x8
OFFSET_DIACHICOSOIDVATPHAMHANHTRANG = 0x395778
#Moi ở hàm sửa đồ
OFFSET_DIACHICOSOTHONGTINVATPHAM = 0x2A049C #lea edi,[esi+CoreClient.dll+OFFSET_DIACHICOSOTHONGTINVATPHAM] # game.g_NpcSetting
OFFSET_DIACHICOSOMOIVATPHAM = 0x73C

class MoiTruong:
    def __init__(self, idcuaso):
        self.idcuaso = idcuaso
        idtientrinh = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(self.idcuaso, ctypes.byref(idtientrinh))
        idtientrinh = idtientrinh.value

        self.tientrinh = pymem.Pymem()
        self.tientrinh.open_process_from_id(idtientrinh)

        gamemodule = pymem.process.module_from_name(self.tientrinh.process_handle, "Game.exe")
        if not gamemodule:
            raise Exception("Tìm không thấy module Game.exe. Có vẻ cửa sổ Game không phải cửa sổ Game Phong thần. Vui lòng thử lại")
        self.diachigame = gamemodule.lpBaseOfDll

        self.diachihambanvatpham = self.tientrinh.allocate(1024)
        self.khoitaohambanvatpham()

        self.diachihammocuahang = self.tientrinh.allocate(1024)
        self.khoitaohammocuahang()

        self.diachihamdongcuahang = self.tientrinh.allocate(1024)
        self.khoitaohamdongcuahang()

        self.diachihamdoithoai = self.tientrinh.allocate(1024)
        self.khoitaohamdoithoai()

        self.diachihamluachondoithoai = self.tientrinh.allocate(1024)
        self.khoitaohamluachondoithoai()

        self.diachihamsudungvatpham = self.tientrinh.allocate(1024)
        self.khoitaohamsudungvatpham()

    def __del__(self):
        def safe_free(diachi):
            try:
                if diachi and hasattr(self, "tientrinh"):
                    self.tientrinh.free(diachi)
            except:
                pass

        diachicangiaiphongs = [
            "diachihambanvatpham",
            "diachihammocuahang",
            "diachihamdongcuahang",
            "diachihamdoithoai",
            "diachihamluachondoithoai",
            "diachihamsudungvatpham",
        ]

        for diachicangiaiphong in diachicangiaiphongs:
            safe_free(diachicangiaiphong)

    def get_is_nhanvattontai(self, idnhanvat = 1):
        if read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x4 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT) != idnhanvat:
            return False
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT) >= 0

    def get_tennhanvat(self, idnhanvat = 1):
        return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xBC9 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_is_dangmatketnoi(self):
        return not self.get_is_nhanvattontai()

    def get_is_cuasogametontai(self):
        return win32gui.IsWindow(self.idcuaso)

    def get_is_cuasogamekichhoat(self):
        return win32gui.GetForegroundWindow() == self.idcuaso

    def get_soohanhtrangmoihang(self):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOIDVATPHAMHANHTRANG + 0x8)

    def get_sohanghanhtrang(self):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOIDVATPHAMHANHTRANG + 0xC)

    def get_soohanhtrangtoida(self):
        return self.get_sohanghanhtrang() * self.get_soohanhtrangmoihang() * SOHANHTRANGTOIDA

    def get_idvatpham(self, sothutuvatpham):
        if sothutuvatpham <= 0 or sothutuvatpham > SOLUONGVITRIVATPHAMTOIDA:
            return -1

        idvatpham = read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM)

        if idvatpham > SOLUONGVATPHAMTOIDA or idvatpham < 0:
            return -1

        return idvatpham

    def get_vitrivatpham(self, sothutuvatpham):
        if sothutuvatpham <= 0 or sothutuvatpham > SOLUONGVITRIVATPHAMTOIDA:
            return False

        vitrivatpham = (
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM), #ID vật phẩm
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + 0x4 + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM), #Vị trí rương
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + 0x8 + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM), #Vị trí X
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + 0xC + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM), #Vị trí Y
        )

        if vitrivatpham == (0, 0, 0, 0):
            return False

        return vitrivatpham

    def get_soluongvatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x82A4 + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)

    def get_tenvatpham(self, idvatpham):
        return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x7EFC + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)

    def get_dbidvatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x8438 + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)

    def khoitaohambanvatpham(self):
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov ebx, dword ptr [{self.diachihambanvatpham + 0x40}]
            mov ecx, dword ptr [{self.diachihambanvatpham + 0x40 + 0x4}]
            mov edx, dword ptr [{self.diachihambanvatpham + 0x40 + 0x8}]
            push edx
            mov eax, {self.diachigame + 0x1811E0}
            call eax
            add esp, 4
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihambanvatpham, bytes(encoding), len(encoding))

    def get_is_dangmocuahang(self):
        return read_int(self.tientrinh, self.diachigame + 0x29F4FC) > 0

    def action_banvatpham(self, sothutuvatpham):
        print("action_banvatpham: {}".format(sothutuvatpham))
        idvatpham = self.get_idvatpham(sothutuvatpham)

        if idvatpham <= 0:
            return

        if not self.get_is_dangmocuahang():
            return

        dbidvatpham = self.get_dbidvatpham(idvatpham)

        diachidulieuhambanvatpham = self.diachihambanvatpham + 0x40
        write_int(self.tientrinh, diachidulieuhambanvatpham, idvatpham * 0x73C)
        write_int(self.tientrinh, diachidulieuhambanvatpham + 4, idvatpham)
        write_int(self.tientrinh, diachidulieuhambanvatpham + 8, dbidvatpham)

        self.tientrinh.start_thread(self.diachihambanvatpham)

    def khoitaohammocuahang(self):
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push 03
            push {0x6FF178}
            mov ecx,{self.diachigame + 0x395560}
            mov eax, {self.diachigame + 0x10F280}
            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihammocuahang, bytes(encoding), len(encoding))

    def action_mocuahang(self):
        print("action_mocuahang")
        self.tientrinh.start_thread(self.diachihammocuahang)

    def khoitaohamdongcuahang(self):
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov eax, {self.diachigame + 0xE3C30}
            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdongcuahang, bytes(encoding), len(encoding))

    def action_dongcuahang(self):
        print("action_dongcuahang")
        self.tientrinh.start_thread(self.diachihamdongcuahang)

    def khoitaohamdoithoai(self):
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov ebx, dword ptr [{self.diachihamdoithoai + 0x40}]
            push ebx
            mov ecx, {self.diachigame + 0x395560}
            mov eax, {self.diachigame + 0x1100B0}
            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdoithoai, bytes(encoding), len(encoding))

    def action_doithoai(self, idnhanvat):
        print("action_doithoai: {}".format(idnhanvat))
        if idnhanvat <= 0:
            return

        diachidulieu = self.diachihamdoithoai + 0x40
        write_int(self.tientrinh, diachidulieu, idnhanvat)
        self.tientrinh.start_thread(self.diachihamdoithoai)

    def get_is_dangdoithoai(self):
        return read_int(self.tientrinh, self.diachigame + 0x29F0C0) > 0

    def khoitaohamluachondoithoai(self):
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push 01
            mov eax, {self.diachigame + 0xC9450}
            call eax
            add esp, 04
            
            mov eax, dword ptr [{self.diachihamluachondoithoai + 0x40}]
            push eax
            push 0x00
            push 0x09

            mov ecx, dword ptr [{self.diachigame + 0x29F794}]
            mov edx, dword ptr [ecx]
            mov ecx, dword ptr [{self.diachigame + 0x29F794}]
            mov eax, dword ptr [edx + 0x04]

            mov ebx, {self.diachigame + 0x10AE00}
            call ebx
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamluachondoithoai, bytes(encoding), len(encoding))

    def action_luachondoithoai(self, idluachon):
        print("action_luachondoithoai: {}".format(idluachon))
        diachidulieu = self.diachihamluachondoithoai + 0x40
        write_int(self.tientrinh, diachidulieu, idluachon)
        self.tientrinh.start_thread(self.diachihamluachondoithoai)

    def khoitaohamsudungvatpham(self):
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov ebx, dword ptr [{self.diachihamsudungvatpham + 0x40}]
            mov eax, dword ptr [{self.diachihamsudungvatpham + 0x40 + 0x4}]
            mov ecx, dword ptr [{self.diachihamsudungvatpham + 0x40 + 0x8}]
            mov esi, {VITRIRUONGHANHTRANG}
            mov edx, 0
            
            push edx
            push ecx
            push eax
            push esi

            mov ecx, {hex(self.diachigame + 0x395560)}
            push ebx

            mov ebp, {hex(self.diachigame + 0x110BE0)}
            call ebp
            
            ret
        """

        encoding, _ = ks.asm(asm_code)
        self.tientrinh.write_bytes(self.diachihamsudungvatpham, bytes(encoding), len(encoding))

    def action_sudungvatphamhanhtrang(self, idvatpham, vitrix, vitriy):
        diachidulieu = self.diachihamsudungvatpham + 0x40
        self.tientrinh.write_int(diachidulieu, idvatpham)
        self.tientrinh.write_int(diachidulieu + 0x4, vitrix)
        self.tientrinh.write_int(diachidulieu + 0x8, vitriy)
        self.tientrinh.start_thread(self.diachihamsudungvatpham)

    def action_timkiemnhanvat(self, tennhanvat):
        if not tennhanvat:
            return -1
        for idnhanvat in range(SOLUONGNHANVATTOIDA):
            if not self.get_is_nhanvattontai(idnhanvat):
                continue
            tennhanvatxemxet = self.get_tennhanvat(idnhanvat)
            if tennhanvatxemxet and tennhanvatxemxet.strip() == tennhanvat.strip():
                return idnhanvat
        return -1

    def action_timkiemvatpham(self, tenvatpham):
        if not tenvatpham:
            return False

        for sothutuvatpham in range(SOLUONGVATPHAMTOIDA):
            vitrivatpham = self.get_vitrivatpham(sothutuvatpham)
            if not vitrivatpham:
                continue
            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham
            tenvatphamxemxet = self.get_tenvatpham(idvatpham)
            if tenvatphamxemxet and tenvatphamxemxet.strip() == tenvatpham.strip():
                return vitrivatpham
        return False

    def get_tenbandohientai(self):
        return read_string(self.tientrinh, self.diachigame + 0x28A1114)
