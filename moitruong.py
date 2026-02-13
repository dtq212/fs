import ctypes
import time

import pymem
import win32gui
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

from hangso import *
from tienich import *

# Inspect từ Tên nhân vật - 0xBC5
OFFSET_DIACHICOSONHANVAT = 0x3BA980
OFFSET_DIACHICOSOMOINHANVAT = 0x8294

# Inspect từ ID vị trí rương = 1 khi cầm vật phẩm lên và đặt xuống hành trang là 3
# Lấy địa chỉ tìm được - 4 sẽ ra ID vật phẩm, Lấy địa chỉ - ID vật phẩm * 0x10 sẽ ra OFFSET_DIACHICOSOVITRIVATPHAM
OFFSET_DIACHICOSOVITRIVATPHAM = 0x39F354
OFFSET_DIACHICOSOVITRIMOIVATPHAM = 0x10

# Inspect từ Hàm bán đồ
OFFSET_DIACHICOSOTHONGTINVATPHAM = 0x2AA728
OFFSET_DIACHICOSOMOIVATPHAM = 0x778

class MoiTruong:
    def __init__(self, idcuaso):
        self._thoidiemdichuyengiukhoangcachtoithieu = 0.
        self._thoidiemtudongtimduonggannhat = 0.
        self._thoidiembanvatphamgannhat = 0.
        self._thoidiemmocuahanggannhat = 0.
        self._thoidiemdongcuahanggannhat = 0.
        self._thoidiemdoithoaigannhat = 0.
        self._thoidiemluachondoithoaigannhat = 0.
        self._thoidiemsudungvatphamgannhat = 0.
        self._thoidiemdichuyengannhat = 0.
        self._thoidiemsuavatphamgannhat = 0.
        self._thoidiemxacnhandoithoaigannhat = 0.
        self._thoidiembattathieuungbotrogannhat_map = {}

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

        self.diachihambanvatpham = 0
        self.diachihamdongcuahang = 0
        self.diachihamdoithoai = 0
        self.diachihamluachondoithoai = 0
        self.diachihamsudungvatpham = 0
        self.diachihamtudongtimduong = 0
        self.diachihamdichuyen = 0
        self.diachihamsuavatpham = 0
        self.diachihambattathieuungbotro = 0
        self.diachihamxacnhandoithoai = 0

    def __del__(self):
        def safe_free(diachi):
            try:
                if diachi and hasattr(self, "tientrinh"):
                    self.tientrinh.free(diachi)
            except:
                pass

        diachicangiaiphongs = [
            self.diachihambanvatpham,
            self.diachihamdongcuahang,
            self.diachihamdoithoai,
            self.diachihamluachondoithoai,
            self.diachihamsudungvatpham,
            self.diachihamtudongtimduong,
            self.diachihamdichuyen,
            self.diachihambattathieuungbotro,
            self.diachihamxacnhandoithoai,
        ]

        for diachi in diachicangiaiphongs:
            safe_free(diachi)

    def get_is_dangmatketnoi(self):
        return not self.get_is_nhanvattontai()

    def get_is_cuasogametontai(self):
        return win32gui.IsWindow(self.idcuaso)

    def get_is_cuasogamekichhoat(self):
        return win32gui.GetForegroundWindow() == self.idcuaso

    def get_is_nhanvattontai(self, idnhanvat = 1):
        if read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x4 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT) != idnhanvat:
            return False
        return self.get_dbidnhanvat(idnhanvat) >= 0

    def get_dbidnhanvat(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_tennhanvat(self, idnhanvat = 1):
        return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xBC9 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_sinhluchientai(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x7FC + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_sinhluctoida(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x800 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_toadox(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x2520 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_toadoy(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x2524 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_toadoxsaptoi(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x1028 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_toadoysaptoi(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x102C + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_is_nhanvatdachet(self, idnhanvat = 1):
        return self.get_idtrangthainhanvat(idnhanvat) == IDTRANGTHAINHANVAT_DACHET

    def get_idloainhanvat(self, idnhanvat = 1):
        return read_short_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x20 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_idtrangthainhanvat(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xB4 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_idhephai(self, idnhanvat = 1):
        return read_short_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x21 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_idmaupk(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xAC + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_idkynang(self, iddiachikynang):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xC0 + 0x24 * iddiachikynang + 1 * OFFSET_DIACHICOSOMOINHANVAT)

    def get_iddiachikynang(self, idkynang):
        iddiachikynang_map = IDDIACHIKYNANG_MAP.get(self.get_idhephai(), 0)
        if not iddiachikynang_map:
            return 0
        iddiachikynang = iddiachikynang_map.get(idkynang, 0)
        if not iddiachikynang:
            return 0
        return iddiachikynang

    def get_capdokynang(self, idkynang):
        if idkynang > SOLUONGKYNANGTOIDA or idkynang < 0:
            return 0
        iddiachikynang = self.get_iddiachikynang(idkynang)
        if not iddiachikynang:
            return 0
        return read_short_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xC4 + 0x24 * iddiachikynang + 1 * OFFSET_DIACHICOSOMOINHANVAT)

    def get_is_dahockynang(self, idkynang):
        capdokynang = self.get_capdokynang(idkynang)
        return capdokynang > 0

    def get_thoidiemhoiphuckynang(self, idkynang, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xB4 + 0x24 * idkynang + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_diachicosohieuungbotro(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x98 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_diachihieuungbotro(self, idhieuungbotro, idnhanvat = 1):
        diachicosohieuungbotro = self.get_diachicosohieuungbotro(idnhanvat)
        diachihieuungbotrotieptheo = diachicosohieuungbotro
        while diachihieuungbotrotieptheo:
            idhieuungbotroxemxet = read_int(self.tientrinh, diachihieuungbotrotieptheo + 0xC)
            if idhieuungbotroxemxet == idhieuungbotro:
                return diachihieuungbotrotieptheo
            diachihieuungbotrotieptheo = read_int(self.tientrinh, diachihieuungbotrotieptheo + 0x4)
        return False

    def get_is_hieuungbotrodangbat(self, idkynangbotro, idnhanvat = 1):
        diachihieuungbotro = self.get_diachihieuungbotro(idkynangbotro, idnhanvat)
        return diachihieuungbotro and read_short_int(self.tientrinh, diachihieuungbotro + 0x1C) != 1

    def get_is_cohieuungbotro(self, idhieuungbotro, idnhanvat = 1):
        diachihieuungbotro = self.get_diachihieuungbotro(idhieuungbotro, idnhanvat)
        if not diachihieuungbotro:
            return False
        return True

    def get_hieuungbotros(self, idnhanvat = 1):
        diachicosohieuungbotro = self.get_diachicosohieuungbotro(idnhanvat)
        diachihieuungbotrotieptheo = diachicosohieuungbotro
        hieuungbotros = []
        while diachihieuungbotrotieptheo:
            idhieuungbotroxemxet = read_int(self.tientrinh, diachihieuungbotrotieptheo + 0xC)
            hieuungbotros.append(idhieuungbotroxemxet)
            diachihieuungbotrotieptheo = read_int(self.tientrinh, diachihieuungbotrotieptheo + 0x4)
        return hieuungbotros

    def get_donghothoigian(self):
        return read_int(self.tientrinh, self.diachigame + 0x28E44E8) # 0x28DA838

    def get_is_kynangsansang(self, idkynang):
        if not self.get_is_dahockynang(idkynang):
            return False

        thoidiemhoiphuckynang = self.get_thoidiemhoiphuckynang(idkynang)
        return not thoidiemhoiphuckynang or thoidiemhoiphuckynang < self.get_donghothoigian()

    def get_is_khuvuccothetancong(self):
        return read_int(self.tientrinh, self.diachigame + 0x28F05E4) > 0

    def get_idmuctieudangchon(self):
        return read_int(self.tientrinh, self.diachigame + 0x3A4A34)

    def set_idmuctieudangchon(self, idmuctieudangchon):
        if self.get_idmuctieudangchon() != idmuctieudangchon:
            write_int(self.tientrinh, self.diachigame + 0x3A4A34, idmuctieudangchon)

    def get_idmuctieutancong(self):
        return read_int(self.tientrinh, self.diachigame + 0x3C3C1C)

    def set_idmuctieutancong(self, idmuctieutancong):
        if self.get_idmuctieutancong() != idmuctieutancong:
            write_int(self.tientrinh, self.diachigame + 0x3C3C1C, idmuctieutancong)

    def get_is_dangmocuahang(self):
        return read_int(self.tientrinh, self.diachigame + 0x2A19AC) > 0

    def get_is_dangdoithoailuachon(self):
        return read_int(self.tientrinh, self.diachigame + 0x2A08A0) > 0

    def get_is_dangdoithoaixacnhan(self):
        return read_int(self.tientrinh, self.diachigame + 0x29FFF0) > 0

    def get_is_dangtudongtimduong(self):
        return read_int(self.tientrinh, self.diachigame + 0x39F264) > 0

    def set_is_dangtudongtimduong(self, is_dangtudongtimduong):
        if self.get_is_dangtudongtimduong() != is_dangtudongtimduong:
            write_int(self.tientrinh, self.diachigame + 0x39F264, 1 if is_dangtudongtimduong else 0)

    def get_is_duoitheo(self):
        return read_int(self.tientrinh, self.diachigame + 0x3A46A0) > 0

    def set_is_duoitheo(self, is_duoitheo):
        if self.get_is_duoitheo() != is_duoitheo:
            write_int(self.tientrinh, self.diachigame + 0x3A46A0, 1 if is_duoitheo else 0)

    def get_is_dichuyenhoatdongquanhphamvi(self):
        return read_int(self.tientrinh, self.diachigame + 0x3A46A4) > 0

    def set_is_dichuyenhoatdongquanhphamvi(self, is_dichuyenhoatdongquanhphamvi):
        if self.get_is_dichuyenhoatdongquanhphamvi() != is_dichuyenhoatdongquanhphamvi:
            write_int(self.tientrinh, self.diachigame + 0x3A46A4, 1 if is_dichuyenhoatdongquanhphamvi else 0)

    def get_is_phimcachtudanh(self):
        return read_int(self.tientrinh, self.diachigame + 0x3A390C) > 0

    def set_is_phimcachtudanh(self, is_phimcachtudanh):
        if self.get_is_phimcachtudanh() != is_phimcachtudanh:
            write_int(self.tientrinh, self.diachigame + 0x3A390C, 1 if is_phimcachtudanh else 0)

    def get_tenbandohientai(self):
        return read_string(self.tientrinh, self.diachigame + 0x28AADC4)

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
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM),  # ID vật phẩm
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + 0x4 + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM),  # Vị trí rương
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + 0x8 + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM),  # Vị trí X
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOVITRIVATPHAM + 0xC + sothutuvatpham * OFFSET_DIACHICOSOVITRIMOIVATPHAM),  # Vị trí Y
        )

        if vitrivatpham == (0, 0, 0, 0):
            return False

        return vitrivatpham

    def get_soluongvatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x4C8 + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)

    def get_tenvatpham(self, idvatpham):
        return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x120 + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)

    def get_dbidvatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x698 + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)

    def get_loaivatpham(self, idvatpham):
        if idvatpham <= 0 or idvatpham > SOLUONGVATPHAMTOIDA:
            return False

        diachicosothongtinvatpham = self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM

        phamchat = read_short_int(self.tientrinh, diachicosothongtinvatpham + 0xFC, 1)
        danhmucvattutieuhao = read_short_int(self.tientrinh, diachicosothongtinvatpham + 0xFE, 2)
        danhmuctrangbi = read_int(self.tientrinh, diachicosothongtinvatpham + 0x100)
        loaihinh = read_short_int(self.tientrinh, diachicosothongtinvatpham + 0x108, 1)

        return phamchat, danhmucvattutieuhao, danhmuctrangbi, loaihinh

    def get_thuoctinhvatpham_map(self, idvatpham):
        if idvatpham <= 0 or idvatpham > SOLUONGVATPHAMTOIDA:
            return []

        diachicosothongtinvatpham = self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM

        thuoctinhvatpham_map = {}

        for i in range(16):
            diachicosothongtinthuoctinhvatpham = diachicosothongtinvatpham + 0x51C + (i * 0x14)

            idthuoctinh = read_int(self.tientrinh, diachicosothongtinthuoctinhvatpham)

            if idthuoctinh <= 0 or idthuoctinh:
                continue

            thuoctinhvatpham_map[idthuoctinh] = read_int(self.tientrinh, diachicosothongtinthuoctinhvatpham + 0x4)

        return thuoctinhvatpham_map

    def get_thongtinvatpham_display(self, idvatpham):
        loaivatpham = self.get_loaivatpham(idvatpham)
        if not loaivatpham:
            return None

        phamchat, danhmucvattutieuhao, danhmuctrangbi, loaihinh = loaivatpham

        tenphamchat = PHAMCHATVATPHAM_MAP.get(phamchat, f"Lạ({phamchat})")
        tendanhmuctrangbi = DANHMUCTRANGBI_MAP.get(danhmuctrangbi, "Vật phẩm khác")

        return {
            "Tên": self.get_tenvatpham(idvatpham),
            "Số lượng": self.get_soluongvatpham(idvatpham),
            "Độ bền": f"{self.get_dobenhientaivatpham(idvatpham)}/{self.get_dobentoidavatpham(idvatpham)}",
            "Danh mục trang bị": tendanhmuctrangbi,
            "Phẩm chất": tenphamchat,
            "DBID": self.get_dbidvatpham(idvatpham),
            "Danh mục vật tư tiêu hao": danhmucvattutieuhao,
            "Loại hình": loaihinh,
            "Trọng lượng": self.get_trongluongvatpham(idvatpham),
            "Thuộc tính": self.get_thuoctinhvatpham_map(idvatpham),
        }

    def get_trongluongvatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x4EC + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM) * self.get_soluongvatpham(idvatpham)

    def get_dobenhientaivatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x69C + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)

    def get_dobentoidavatpham(self, idvatpham):
        if idvatpham <= 0 or idvatpham > SOLUONGVATPHAMTOIDA:
            return -1

        if int.from_bytes(read_bytes(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0xFE + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM, 2), sys.byteorder) != 0:
            return -1

        for i in range(5):
            x = self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM + (i * 0x14)
            if read_int(self.tientrinh, x) == 0x1F:
                dobentoida = read_int(self.tientrinh, x + 4)
                return dobentoida if dobentoida > 0 else -1

        return -1

    def get_khoangcach(self, idnhanvat2, idnhanvat1 = 1):
        x1 = self.get_toadox(idnhanvat1)
        y1 = self.get_toadoy(idnhanvat1)

        x2 = self.get_toadox(idnhanvat2)
        y2 = self.get_toadoy(idnhanvat2)

        khoangcach = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return int(khoangcach)

    def get_khoangcachdiem(self, idnhanvat2, toadox1, toadoy1):
        x2 = self.get_toadox(idnhanvat2)
        y2 = self.get_toadoy(idnhanvat2)

        khoangcach = ((x2 - toadox1) ** 2 + (y2 - toadoy1) ** 2) ** 0.5
        return int(khoangcach)

    def khoitaohambanvatpham(self):
        if self.diachihambanvatpham: return
        self.diachihambanvatpham = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov ebx, dword ptr [{self.diachihambanvatpham + 0x40}]
            mov ecx, dword ptr [{self.diachihambanvatpham + 0x40 + 0x4}]
            mov edx, dword ptr [{self.diachihambanvatpham + 0x40 + 0x8}]
            push edx
            mov eax, {self.diachigame + 0x1829A0}
            call eax
            add esp, 4
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihambanvatpham, bytes(encoding), len(encoding))

    def action_banvatpham(self, sothutuvatpham, delay = 0.25):
        if not self.diachihambanvatpham:
            self.khoitaohambanvatpham()

        if time.time() - self._thoidiembanvatphamgannhat < delay:
            return False
        print("{}: action_banvatpham".format(self.get_tennhanvat()))
        self._thoidiembanvatphamgannhat = time.time()

        idvatpham = self.get_idvatpham(sothutuvatpham)
        if idvatpham <= 0 or not self.get_is_dangmocuahang():
            return False

        dbidvatpham = self.get_dbidvatpham(idvatpham)
        diachidulieuhambanvatpham = self.diachihambanvatpham + 0x40
        write_int(self.tientrinh, diachidulieuhambanvatpham, idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)
        write_int(self.tientrinh, diachidulieuhambanvatpham + 4, idvatpham)
        write_int(self.tientrinh, diachidulieuhambanvatpham + 8, dbidvatpham)
        self.tientrinh.start_thread(self.diachihambanvatpham)
        return True

    #Inspect hàm nào sửa giá trị biến Đang mở cửa hàng về 0
    def khoitaohamdongcuahang(self):
        if self.diachihamdongcuahang: return
        self.diachihamdongcuahang = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov eax, {self.diachigame + 0xE51D0}
            call eax
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdongcuahang, bytes(encoding), len(encoding))

    def action_dongcuahang(self, delay = 0.5):
        if not self.diachihamdongcuahang:
            self.khoitaohamdongcuahang()

        if time.time() - self._thoidiemdongcuahanggannhat < delay:
            return False
        print("{}: action_dongcuahang".format(self.get_tennhanvat()))
        self._thoidiemdongcuahanggannhat = time.time()

        self.tientrinh.start_thread(self.diachihamdongcuahang)
        return True

    #Inspect click khương tử nha lúc trẻ Request thứ 2
    def khoitaohamdoithoai(self):
        if self.diachihamdoithoai: return
        self.diachihamdoithoai = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov ebx, dword ptr [{self.diachihamdoithoai + 0x40}]
            push ebx
            mov ecx, {self.diachigame + 0x39F210}
            mov eax, {self.diachigame + 0x111760}
            call eax
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdoithoai, bytes(encoding), len(encoding))

    def action_doithoai(self, idnhanvat, delay = 0.5):
        if not self.diachihamdoithoai:
            self.khoitaohamdoithoai()

        if idnhanvat <= 0:
            return False

        if time.time() - self._thoidiemdoithoaigannhat < delay:
            return False
        print("{}: action_doithoai".format(self.get_tennhanvat()))
        self._thoidiemdoithoaigannhat = time.time()

        diachidulieu = self.diachihamdoithoai + 0x40
        write_int(self.tientrinh, diachidulieu, idnhanvat)
        self.tientrinh.start_thread(self.diachihamdoithoai)
        return True

    def khoitaohamluachondoithoai(self):
        if self.diachihamluachondoithoai: return
        self.diachihamluachondoithoai = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            push 01
            mov eax, {self.diachigame + 0xCA290}
            call eax
            add esp, 04

            mov eax, dword ptr [{self.diachihamluachondoithoai + 0x40}]
            push eax
            push 0x00
            push 0x09

            mov ecx, dword ptr [{self.diachigame + 0x2A1C44}]
            mov edx, dword ptr [ecx]
            mov ecx, dword ptr [{self.diachigame + 0x2A1C44}]
            mov eax, dword ptr [edx + 0x04]
            
            call eax
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamluachondoithoai, bytes(encoding), len(encoding))

    def action_luachondoithoai(self, idluachon, delay = 0.25):
        if not self.diachihamluachondoithoai:
            self.khoitaohamluachondoithoai()

        if time.time() - self._thoidiemluachondoithoaigannhat < delay:
            return False
        print("{}: action_luachondoithoai".format(self.get_tennhanvat()))
        self._thoidiemluachondoithoaigannhat = time.time()

        diachidulieu = self.diachihamluachondoithoai + 0x40
        write_int(self.tientrinh, diachidulieu, idluachon)
        self.tientrinh.start_thread(self.diachihamluachondoithoai)
        return True

    def khoitaohamxacnhandoithoai(self):
        if self.diachihamxacnhandoithoai: return
        self.diachihamxacnhandoithoai = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            push 01
            mov ebx, {hex(self.diachigame + 0x80F30)}
            call ebx
            add esp, 04

            push 00
            push 00
            push 0x0A
            mov edx, dword ptr [{hex(self.diachigame + 0x2A1C44)}]
            mov eax, dword ptr [edx]
            mov ecx, dword ptr [{hex(self.diachigame + 0x2A1C44)}]
            mov edx, dword ptr [eax + 0x04]
            call edx
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamxacnhandoithoai, bytes(encoding), len(encoding))

    def action_xacnhandoithoai(self, delay = 0.25):
        if not self.diachihamxacnhandoithoai:
            self.khoitaohamxacnhandoithoai()

        if time.time() - self._thoidiemxacnhandoithoaigannhat < delay:
            return False
        print("{}: action_xacnhandoithoai".format(self.get_tennhanvat()))

        self._thoidiemxacnhandoithoaigannhat = time.time()
        self.tientrinh.start_thread(self.diachihamxacnhandoithoai)
        return True

    def khoitaohamsudungvatpham(self):
        if self.diachihamsudungvatpham: return
        self.diachihamsudungvatpham = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov ebx, dword ptr [{self.diachihamsudungvatpham + 0x40}]
            mov eax, dword ptr [{self.diachihamsudungvatpham + 0x40 + 0x4}]
            mov ecx, dword ptr [{self.diachihamsudungvatpham + 0x40 + 0x8}]
            mov esi, {IDVITRIRUONG_HANHTRANG}
            mov edx, 0

            push edx
            push ecx
            push eax
            push esi

            mov ecx, {hex(self.diachigame + 0x39F210)}
            push ebx

            mov ebp, {hex(self.diachigame + 0x1122B0)}
            call ebp

            ret
        """
        encoding, _ = ks.asm(asm_code)
        self.tientrinh.write_bytes(self.diachihamsudungvatpham, bytes(encoding), len(encoding))

    def action_sudungvatphamhanhtrang(self, idvatpham, vitrix, vitriy, delay = 0.25):
        if not self.diachihamsudungvatpham:
            self.khoitaohamsudungvatpham()

        if time.time() - self._thoidiemsudungvatphamgannhat < delay:
            return False
        print("{}: action_sudungvatphamhanhtrang".format(self.get_tennhanvat()))
        self._thoidiemsudungvatphamgannhat = time.time()

        diachidulieu = self.diachihamsudungvatpham + 0x40
        write_int(self.tientrinh, diachidulieu, idvatpham)
        write_int(self.tientrinh, diachidulieu + 0x4, vitrix)
        write_int(self.tientrinh, diachidulieu + 0x8, vitriy)
        self.tientrinh.start_thread(self.diachihamsudungvatpham)
        return True

    #Inspect hàm nào write biến Đang tự động tìm đường = 1
    def khoitaohamtudongtimduong(self):
        if self.diachihamtudongtimduong: return
        self.diachihamtudongtimduong = self.tientrinh.allocate(256)

        diachidulieu = self.diachihamtudongtimduong + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov esi, dword ptr [{diachidulieu}]
            mov edi, dword ptr [{diachidulieu + 4}]

            push 01
            push edi
            push esi

            mov ecx, {hex(self.diachigame + 0x39F210)}

            mov eax, {hex(self.diachigame + 0x10F8B0)}
            call eax

            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamtudongtimduong, bytes(encoding), len(encoding))

    def action_tudongtimduong(self, toadox, toadoy, delay = 1.):
        if not self.diachihamtudongtimduong:
            self.khoitaohamtudongtimduong()

        if time.time() - self._thoidiemtudongtimduonggannhat < delay:
            return False

        print("{}: action_tudongtimduong".format(self.get_tennhanvat()))
        self._thoidiemtudongtimduonggannhat = time.time()

        toadobandonhox = int(toadox / 256)
        toadobandonhoy = int(toadoy / 512)

        diachidulieu = self.diachihamtudongtimduong + 0x40

        write_int(self.tientrinh, diachidulieu, toadobandonhox * 16 + 8)
        write_int(self.tientrinh, diachidulieu + 4, toadobandonhoy * 16 + 8)

        self.tientrinh.start_thread(self.diachihamtudongtimduong)
        return True

    def khoitaohamdichuyen(self):
        if self.diachihamdichuyen: return
        self.diachihamdichuyen = self.tientrinh.allocate(256)

        diachidulieu = self.diachihamdichuyen + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov esi, {hex(self.diachigame + 0x3C2C14)}
            mov edi, dword ptr [{diachidulieu}]
            mov edx, dword ptr [{diachidulieu + 4}]
            mov ebx, 0

            push ebx
            push edx
            push edi
            mov ecx, esi
            mov eax, {hex(self.diachigame + 0x11C4A0)}
            call eax
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdichuyen, bytes(encoding), len(encoding))

    def action_dichuyen(self, toadox, toadoy, delay = 0.25):
        if not self.diachihamdichuyen:
            self.khoitaohamdichuyen()

        if time.time() - self._thoidiemdichuyengannhat < delay:
            return False
        print("{}: action_dichuyen".format(self.get_tennhanvat()))
        self._thoidiemdichuyengannhat = time.time()

        diachidulieu = self.diachihamdichuyen + 0x40
        write_int(self.tientrinh, diachidulieu, toadox)
        write_int(self.tientrinh, diachidulieu + 4, toadoy)
        self.tientrinh.start_thread(self.diachihamdichuyen)
        return True

    def action_dichuyengiukhoangcachtoithieu(self, idnhanvat2, khoangcachtoithieu, delay = 0.25):
        if not self.get_is_nhanvattontai(idnhanvat2):
            return False

        if time.time() - self._thoidiemdichuyengiukhoangcachtoithieu < delay:
            return False

        self._thoidiemdichuyengiukhoangcachtoithieu = time.time()

        x1 = self.get_toadox(1)
        y1 = self.get_toadoy(1)
        x2 = self.get_toadox(idnhanvat2)
        y2 = self.get_toadoy(idnhanvat2)

        D = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        if D > khoangcachtoithieu:
            tile = khoangcachtoithieu / D

            xmoi = int(x2 - tile * (x2 - x1))
            ymoi = int(y2 - tile * (y2 - y1))

            return self.action_dichuyen(xmoi, ymoi, delay = delay)

        return False

    def khoitaohamsuavatpham(self):
        if self.diachihamsuavatpham: return
        self.diachihamsuavatpham = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        diachidulieu = self.diachihamsuavatpham + 0x40

        asm_code = f"""
            mov ebx, dword ptr [{diachidulieu}]
            mov ebp, dword ptr [{diachidulieu + 0x4}]
            mov edi, dword ptr [{diachidulieu + 0x8}]
            mov ecx, dword ptr [{diachidulieu + 0xC}]
            mov esi, 1

            push ecx
            mov eax, {hex(self.diachigame + 0x182820)}
            call eax
            add esp, 4
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamsuavatpham, bytes(encoding), len(encoding))

    def action_suavatpham(self, idvatpham, delay = 0.25):
        if not self.diachihamsuavatpham:
            self.khoitaohamsuavatpham()

        if time.time() - self._thoidiemsuavatphamgannhat < delay:
            return False
        print("{}: action_suavatpham".format(self.get_tennhanvat()))
        self._thoidiemsuavatphamgannhat = time.time()

        if read_int(self.tientrinh, self.diachigame + 0x2BA36DC) == 0:
            return False

        dobenhientai = self.get_dobenhientaivatpham(idvatpham)
        dobentoida = self.get_dobentoidavatpham(idvatpham)

        if dobentoida == -1 or dobenhientai >= dobentoida or dobenhientai < 0:
            return False

        diachicosothongtinvatpham = self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM
        val_param = read_int(self.tientrinh, diachicosothongtinvatpham + 0x10C)
        global_factor = read_int(self.tientrinh, self.diachigame + 0x2BA36D8)

        product = (val_param * global_factor) * 0x51EB851F
        edx_val = (product >> 32) & 0xFFFFFFFF
        if edx_val & 0x80000000: edx_val -= 0x100000000

        scaled_unit = (edx_val >> 5) + ((edx_val >> 5 >> 31) & 1)
        final_price = (scaled_unit * (dobentoida - dobenhientai)) // dobentoida

        factor_addr = self.diachigame + (0x2BA36E8 if dobenhientai == 0 else 0x2BA36E4)
        final_price *= read_int(self.tientrinh, factor_addr)

        dbid = self.get_dbidvatpham(idvatpham)
        diachidulieu = self.diachihamsuavatpham + 0x40

        write_int(self.tientrinh, diachidulieu, int(final_price))
        write_int(self.tientrinh, diachidulieu + 0x4, dobenhientai)
        write_int(self.tientrinh, diachidulieu + 0x8, idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)
        write_int(self.tientrinh, diachidulieu + 0xC, dbid)

        self.tientrinh.start_thread(self.diachihamsuavatpham)
        return True

    def khoitaohambattathieuungbotro(self):
        if self.diachihambattathieuungbotro: return
        self.diachihambattathieuungbotro = self.tientrinh.allocate(256)

        diachidulieu = self.diachihambattathieuungbotro + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov edx, dword ptr [{hex(diachidulieu)}]
            mov ecx, 00000000

            push ecx
            push edx
            mov eax, {hex(self.diachigame + 0x182950)}
            call eax
            add esp, 8
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihambattathieuungbotro, bytes(encoding), len(encoding))

    def action_bathieuungbotro(self, idhieuungbotro, delay = 0.5):
        if self.get_is_cohieuungbotro(idhieuungbotro) and not self.get_is_hieuungbotrodangbat(idhieuungbotro):
            self.action_battathieuungbotro(idhieuungbotro, delay = delay)

    def action_tathieuungbotro(self, idhieuungbotro, delay = 0.5):
        if self.get_is_cohieuungbotro(idhieuungbotro) and self.get_is_hieuungbotrodangbat(idhieuungbotro):
            self.action_battathieuungbotro(idhieuungbotro, delay = delay)

    def action_battathieuungbotro(self, idhieuungbotro, delay = 0.5):
        if not self.diachihambattathieuungbotro:
            self.khoitaohambattathieuungbotro()

        if time.time() - self._thoidiembattathieuungbotrogannhat_map.get(idhieuungbotro, 0.) < delay:
            return False

        print("{}: action_battathieuungbotro".format(self.get_tennhanvat()))

        self._thoidiembattathieuungbotrogannhat_map[idhieuungbotro] = time.time()

        diachidulieu = self.diachihambattathieuungbotro + 0x40

        write_int(self.tientrinh, diachidulieu, idhieuungbotro)

        self.tientrinh.start_thread(self.diachihambattathieuungbotro)

        return True

    def action_themmuctieuvaodanhsachden(self, idnhanvat):
        if idnhanvat <= 0:
            return False

        diachibatdaudanhsachden = self.diachigame + 0x3A3900 + 0x174

        for i in range(50):
            diachinhanvatdanhsachden = diachibatdaudanhsachden + (i * 4)
            idnhanvatdangxemxet = read_int(self.tientrinh, diachinhanvatdanhsachden)
            if idnhanvatdangxemxet == idnhanvat:
                return True
            if idnhanvatdangxemxet == 0:
                write_int(self.tientrinh, diachinhanvatdanhsachden, idnhanvat)
                return True

        return False