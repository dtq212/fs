import ctypes

import pymem
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

from hangso import *
from tienich import *


class MoiTruong:

    def __init__(self, idcuaso):
        self._thoidiemdongkytrancacgannhat = 0.
        self._thoidiemphucsinhgannhat = 0.
        self.diachihamphucsinh = 0
        self.diachihamsudungkynangtoado2 = 0
        self._thoidiemboquabossgannhat = 0.
        self._thoidiemdichuyengiukhoangcachtoithieu = 0.
        self._thoidiemtudongtimduonggannhat = 0.
        self._thoidiembanvatphamgannhat = 0.
        self._thoidiemsudungvatphamgannhat = 0.
        self._thoidiemdichuyengannhat = 0.
        self._thoidiemsuavatphamgannhat = 0.
        self._thoidiembattathieuungbotrogannhat_map = {}

        self.idcuaso = idcuaso
        idtientrinh = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(self.idcuaso, ctypes.byref(idtientrinh))
        idtientrinh = idtientrinh.value

        self.tientrinh = pymem.Pymem()
        self.tientrinh.open_process_from_id(idtientrinh)

        self.gamemodule = pymem.process.module_from_name(self.tientrinh.process_handle, "Game.exe")
        if not self.gamemodule:
            raise Exception(
                "Tìm không thấy module Game.exe. Có vẻ cửa sổ Game không phải cửa sổ Game Phong thần. Vui lòng thử lại")
        self.diachigame = self.gamemodule.lpBaseOfDll

        kichthuoccuaso = win32gui.GetWindowRect(self.idcuaso)
        if not kichthuoccuaso:
            raise Exception("Lấy kích thước cửa sổ game không thành công")

        self.kichthuoccuasogame = kichthuoccuaso[2] - kichthuoccuaso[0], kichthuoccuaso[3] - kichthuoccuaso[1]

        # Inspect từ Tên nhân vật - 0xBC9
        self.offsetdiachicosonhanvat = 0
        self.offsetdiachicosomoinhanvat = 0

        # Inspect từ ID vị trí rương = 1 khi cầm vật phẩm lên và đặt xuống hành trang là 3
        # Lấy địa chỉ tìm được - 4 sẽ ra ID vật phẩm, Lấy địa chỉ - ID vật phẩm * 0x10 sẽ ra self.offsetdiachicosovitrivatpham
        # Lưu ý: Base từ 0
        self.offsetdiachicosovitrivatpham = 0
        self.offsetdiachicosovitrimoivatpham = 0

        # Inspect từ Hàm bán đồ mov edx,[ebx+game.g_NpcSetting+8474]
        # Để ý mà trừ 0x778 1 lần đi nhé, hôm nọ bị lỗi tính nhầm 1 lần
        # Lưu ý: Base từ 0
        self.offsetdiachicosothongtinvatpham = 0
        self.offsetdiachicosomoivatpham = 0

        # Inspect từ Tọa độ X, Y của thành viên thay đổi
        self.offsetdiachicosothongtinthanhviendoinhom = 0
        self.offsetdiachicosomoithanhviendoinhom = 0

        # #1 biến nào đó mà + FE0 thì phải đấy
        self.offsetdiachicosonhanvattieptheo = 0

        self.diachihamdongkytrancac = 0
        self.diachihambanvatpham = 0
        self.diachihamsudungvatpham = 0
        self.diachihamtudongtimduong = 0
        self.diachihamdichuyen = 0
        self.diachihamsuavatpham = 0
        self.diachihambattathieuungbotro = 0
        self.diachihamvutvatpham = 0
        self.diachihammuavatphamkytrancac = 0
        self.diachihammotabkytrancac = 0
        self._idchunhan_map = {}

        self.diachihamdoimaupk = 0
        self._thoidiemmokhoagannhat = 0.
        self.diachihammokhoa = 0

        self._thoidiemsudungkynanggannhat_map = {}
        self.diachihamsudungkynangtoado = 0

        self._thoidiemdongcuahanggannhat = 0.
        self._thoidiemdoithoaigannhat = 0.
        self._thoidiemxacnhandoithoaigannhat = 0.

        self.diachihamdongcuahang = 0
        self.diachihamdoithoai = 0
        self.diachihamxacnhandoithoai = 0
        self.diachihamdichuyen2 = 0

        self._thoidiemvutvatphamgannhat = 0.
        self._thoidiemmuakytrancacgannhat = 0.
        self._thoidiemmotabkytrancacgannhat = 0.

        self.offsetdiachicosothuchiencaulenh = 0
        self.offsetdiachicosobando = 0

        self.offsetdiachigiamxuatchieu1 = 0
        self.offsetdiachigiamxuatchieu2 = 0

        self.offsetdiachithietlapmuctieu_C705 = 0
        self.offsetdiachithietlapmuctieu_890D = 0

        self.offsetdiachithietlapmuctieutancong_ingame = 0
        self.offsetdiachithietlapmuctieutancong_ngoaiphamvi = 0
        self.offsetdiachithietlapmuctieutancong_dichuot = 0
        self.offsetdiachithietlapmuctieutancong_theolaitan = 0
        self.offsetdiachithietlapmuctieutancong_ngoaiphamvidichuyen = 0

        self.offsetdiachicosocauhinh = 0

        self.action_timkiemtoanbodiachiham()

    def __del__(self):
        def safe_free(diachi):
            try:
                if diachi and hasattr(self, "tientrinh"):
                    self.tientrinh.free(diachi)
            except:
                pass

        tenthuoctinhs = [
            "diachihambanvatpham",
            "diachihamsudungvatpham",
            "diachihamtudongtimduong",
            "diachihamdichuyen",
            "diachihambattathieuungbotro",
            "diachihamdoimaupk",
            "diachihammokhoa",

            "diachihamdongcuahang",
            "diachihamdoithoai",
            "diachihamxacnhandoithoai",
            "diachihamvutvatpham",
        ]

        for tenthuoctinh in tenthuoctinhs:
            if hasattr(self, tenthuoctinh):
                diachi = getattr(self, tenthuoctinh)
                safe_free(diachi)

    def get_is_dangmatketnoi(self):
        return not self.get_is_nhanvattontai()

    def get_is_cuasogametontai(self):
        return win32gui.IsWindow(self.idcuaso)

    def get_is_cuasogamekichhoat(self):
        return win32gui.GetForegroundWindow() == self.idcuaso

    def get_is_nhanvattontai(self, idnhanvat = 1):
        # 0x18 dò bằng cách cho mục tiêu ra đủ xa đến mức tọa độ của nó không thay đổi nữa
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x4 + idnhanvat * self.offsetdiachicosomoinhanvat) == idnhanvat and read_int(
            self.tientrinh,
            self.diachigame + self.offsetdiachicosonhanvat + 0x18 + idnhanvat * self.offsetdiachicosomoinhanvat) > 0 and read_int(
            self.tientrinh,
            self.diachigame + self.offsetdiachicosonhanvat + 0x7E8 + idnhanvat * self.offsetdiachicosomoinhanvat) >= 0

    def get_dbidnhanvat(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_tennhanvat(self, idnhanvat = 1):
        return read_string(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xBC9 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_sinhluchientai(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x7FC + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_sinhluctoida(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x800 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_noiluchientai(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x80C + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_noiluctoida(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x810 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_phantramkhanghoa(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x904 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_phantramkhanghoatoida(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x918 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_diempk(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xD5C + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_phantramsinhluchientai(self, idnhanvat = 1):
        sinhluctoida = self.get_sinhluctoida(idnhanvat)
        if not sinhluctoida:
            return 0
        return int(self.get_sinhluchientai(idnhanvat) * 100. / sinhluctoida)

    def get_phantramnoiluchientai(self, idnhanvat = 1):
        noiluctoida = self.get_noiluctoida(idnhanvat)
        if not noiluctoida:
            return 0
        return int(self.get_noiluchientai(idnhanvat) * 100. / noiluctoida)

    def get_toado(self, idnhanvat = 1):
        if not self.offsetdiachicosonhanvat or not self.offsetdiachicosobando:
            return -1, -1

        diachinhanvat = self.diachigame + self.offsetdiachicosonhanvat + idnhanvat * self.offsetdiachicosomoinhanvat

        toadoluoix = read_int(self.tientrinh, diachinhanvat + 0x0ACC)
        toadoluoiy = read_int(self.tientrinh, diachinhanvat + 0x0AD0)
        offsetx = read_int(self.tientrinh, diachinhanvat + 0x0AD8)
        offsety = read_int(self.tientrinh, diachinhanvat + 0x0ADC)

        idbando = read_int(self.tientrinh, diachinhanvat + 0x07E4)
        idkhuvuc = read_int(self.tientrinh, diachinhanvat + 0x07E8)

        diachibando = self.diachigame + self.offsetdiachicosobando + (idbando * 172)
        soluongkhuvuctoida = read_int(self.tientrinh, diachibando + 0x58)

        if idkhuvuc < 0 or idkhuvuc >= soluongkhuvuctoida:
            return -1, -1

        chieurongoluoi = read_int(self.tientrinh, diachibando + 0x64)
        chieucaooluoi = read_int(self.tientrinh, diachibando + 0x68)

        diachicosomangkhuvuc = read_int(self.tientrinh, diachibando + 0x28)
        diachikhuvuc = diachicosomangkhuvuc + (idkhuvuc * 204)

        toadogocx = read_int(self.tientrinh, diachikhuvuc + 0xA8)
        toadogocy = read_int(self.tientrinh, diachikhuvuc + 0xAC)

        toadox = (toadoluoix * chieurongoluoi) + toadogocx + (offsetx >> 10)
        toadoy = (toadoluoiy * chieucaooluoi) + toadogocy + (offsety >> 10)

        return toadox, toadoy

    def get_toadosaptoi(self, idnhanvat = 1):
        return (
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x1028 + idnhanvat * self.offsetdiachicosomoinhanvat),
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x102C + idnhanvat * self.offsetdiachicosomoinhanvat)
        )

    def get_tocdodichuyen(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x934 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_trihoanxuatchieuvukhi(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x948 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def set_trihoanxuatchieuvukhi(self, trihoanxuatchieuvukhi, idnhanvat = 1):
        if trihoanxuatchieuvukhi != self.get_trihoanxuatchieuvukhi(idnhanvat):
            return write_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x948 + idnhanvat * self.offsetdiachicosomoinhanvat, trihoanxuatchieuvukhi)

    def get_trihoanxuatchieubuaphap(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x94C + idnhanvat * self.offsetdiachicosomoinhanvat)

    def set_trihoanxuatchieubuaphap(self, trihoanxuatchieubuaphap, idnhanvat = 1):
        if trihoanxuatchieubuaphap != self.get_trihoanxuatchieubuaphap(idnhanvat):
            return write_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x94C + idnhanvat * self.offsetdiachicosomoinhanvat, trihoanxuatchieubuaphap)

    def get_is_nhanvatdachet(self, idnhanvat = 1):
        return self.get_idtrangthainhanvat(idnhanvat) == IDTRANGTHAINHANVAT_DACHET

    def get_idloainhanvat(self, idnhanvat = 1):
        if idnhanvat <= 0:
            return -1
        return read_short_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x20 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_idtrangthainhanvat(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xB4 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_is_bidongbang(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x64 + idnhanvat * self.offsetdiachicosomoinhanvat) > 0

    def get_idhephai(self, idnhanvat = 1):
        return read_short_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x21 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_idmaupk(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xAC + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_capdonhanvat(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x1C + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_idbienthannhanvat(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xB10 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_trongluongtoida(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat + 0xA0C)

    def get_tenchunhan(self, idnhanvat = 1):
        return read_string(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xBE9 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_tenbang(self, idnhanvat = 1):
        if self.get_idloainhanvat(idnhanvat) in (IDLOAINHANVAT_TRIEUHOITHU, 8):
            idchunhan = self.get_idchunhan(idnhanvat)
            if not idchunhan:
                return False
            return self.get_tenbang(idchunhan)
        return read_string(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xB75 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_idtodoi(self, idnhanvat = 1):
        if idnhanvat <= 0:
            return -1

        if self.get_idloainhanvat(idnhanvat) == IDLOAINHANVAT_TRIEUHOITHU:
            idchunhan = self.get_idchunhan(idnhanvat)
            if not idchunhan or idchunhan <= 0:
                return -1
            return self.get_idtodoi(idchunhan)

        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xB2C + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_idkynang(self, iddiachikynang):
        return read_short_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xC0 + 0x24 * iddiachikynang + 1 * self.offsetdiachicosomoinhanvat, 2)

    def get_iddiachikynang(self, idkynang):
        iddiachikynang_map = IDDIACHIKYNANG_MAP.get(self.get_idhephai(), 0)
        if not iddiachikynang_map:
            return -1
        iddiachikynang = iddiachikynang_map.get(idkynang, 0)
        if not iddiachikynang:
            return -1
        return iddiachikynang

    def get_capdokynang(self, idkynang):
        if idkynang > SOLUONGKYNANGTOIDA or idkynang < 0:
            return -1
        iddiachikynang = self.get_iddiachikynang(idkynang)
        if iddiachikynang <= 0:
            return -1
        return read_short_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xC4 + 0x24 * iddiachikynang + 1 * self.offsetdiachicosomoinhanvat)

    def get_is_dahockynang(self, idkynang):
        return self.get_capdokynang(idkynang) > 0

    def get_thoidiemhoiphuckynang(self, idkynang, idnhanvat = 1):
        if idkynang > SOLUONGKYNANGTOIDA or idkynang < 0:
            return -1
        iddiachikynang = self.get_iddiachikynang(idkynang)
        if iddiachikynang <= 0:
            return -1
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xD8 + 0x24 * iddiachikynang + idnhanvat * self.offsetdiachicosomoinhanvat)

    def set_thoidiemhoiphuckynang(self, idkynang, thoidiemhoiphuckynang = 0, idnhanvat = 1):
        if idkynang > SOLUONGKYNANGTOIDA or idkynang < 0:
            return False
        iddiachikynang = self.get_iddiachikynang(idkynang)
        if iddiachikynang <= 0:
            return False
        write_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0xD8 + 0x24 * iddiachikynang + idnhanvat * self.offsetdiachicosomoinhanvat, thoidiemhoiphuckynang)
        return True

    def get_diachicosohieuungbotro(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x98 + idnhanvat * self.offsetdiachicosomoinhanvat)

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

    def get_idchunhan(self, idnhanvat = 1):
        tenchunhan = self.get_tenchunhan(idnhanvat)
        if not tenchunhan:
            return -1
        idchunhan = self._idchunhan_map.get(tenchunhan, False)
        if idchunhan and idchunhan > 0 and self.get_tennhanvat(idchunhan) == tenchunhan and self.get_is_nhanvattontai(idchunhan):
            return idchunhan

        idnhanvatxemxet = 0
        while True:
            idnhanvatxemxet = self.get_idnhanvattieptheo(idnhanvatxemxet)
            if idnhanvatxemxet <= 0:
                break
            if not self.get_is_nhanvattontai(idnhanvatxemxet):
                continue
            if self.get_idloainhanvat(idnhanvatxemxet) != IDLOAINHANVAT_NGUOICHOI:
                continue
            if self.get_tennhanvat(idnhanvatxemxet) == tenchunhan:
                self._idchunhan_map[tenchunhan] = idnhanvatxemxet
                return idnhanvatxemxet

        return -1

    def get_is_truongnhom(self):
        if self.get_idtodoi() > 0:
            return read_string(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinthanhviendoinhom) == self.get_tennhanvat()
        return False

    def get_toadotruongnhom(self):
        if self.get_idtodoi() > 0:
            return (
                read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinthanhviendoinhom + 0x28),
                read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinthanhviendoinhom + 0x2C)
            )
        return -1, -1

    def get_tenthanhviendoinhoms(self):
        tenthanhviens = set()

        if self.get_idtodoi() <= 0:
            return tenthanhviens

        for sothutu in range(12):
            diachi = self.diachigame + self.offsetdiachicosothongtinthanhviendoinhom + (self.offsetdiachicosomoithanhviendoinhom * sothutu)
            tennhanvat = read_string(self.tientrinh, diachi)

            if tennhanvat:
                tenthanhviens.add(tennhanvat)

        return tenthanhviens

    def get_is_truongnhomcungbando(self):
        if self.get_idtodoi() <= 0:
            return False
        xtruongnhom, ytruongnhom = self.get_toadotruongnhom()
        return xtruongnhom > 0 and ytruongnhom > 0

    def get_is_chungtodoi(self, idnhanvat = 1):
        idtodoi1 = self.get_idtodoi()
        if idtodoi1 == -1:
            return False
        return idtodoi1 == self.get_idtodoi(idnhanvat)

    def get_is_chungbang(self, idnhanvat = 1):
        tenbang = self.get_tenbang()
        if not tenbang:
            return False
        return tenbang == self.get_tenbang(idnhanvat)

    def get_is_cothetancong(self, idnhanvat):
        if idnhanvat <= 1 or not self.get_is_nhanvattontai(idnhanvat) or self.get_is_nhanvatdachet(idnhanvat) or self.get_sinhluctoida(idnhanvat) <= 0:
            return False

        idloainhanvat = self.get_idloainhanvat(idnhanvat)
        if idloainhanvat not in (IDLOAINHANVAT_QUAIVAT, IDLOAINHANVAT_NGUOICHOI, IDLOAINHANVAT_TRIEUHOITHU):
            return False

        if idloainhanvat == IDLOAINHANVAT_TRIEUHOITHU:
            if self.get_tenchunhan(idnhanvat) == self.get_tennhanvat():
                return False
            elif self.get_khoangcach(idnhanvat) > 750 and not self.get_idchunhan(idnhanvat):
                return False

        maupk = self.get_idmaupk(idnhanvat)
        if not maupk:
            return False
        if maupk == 5:
            return True

        if self.get_is_chungtodoi(idnhanvat):
            return False

        maupk1 = self.get_idmaupk()
        if maupk1 == IDMAUPK_DO or maupk == IDMAUPK_DO:
            return True
        elif maupk1 == IDMAUPK_XANH or maupk == IDMAUPK_XANH:
            return False
        elif maupk1 != maupk:
            return True

        return False

    def get_idvatpham(self, sothutuvatpham):
        if sothutuvatpham <= 0 or sothutuvatpham > SOLUONGVITRIVATPHAMTOIDA:
            return -1

        idvatpham = read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + sothutuvatpham * self.offsetdiachicosovitrimoivatpham)

        if idvatpham > SOLUONGVATPHAMTOIDA or idvatpham < 0:
            return -1

        return idvatpham

    def get_vitrivatpham(self, sothutuvatpham):
        if sothutuvatpham <= 0 or sothutuvatpham > SOLUONGVITRIVATPHAMTOIDA:
            return False

        vitrivatpham = (
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + sothutuvatpham * self.offsetdiachicosovitrimoivatpham),  # ID vật phẩm
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + 0x4 + sothutuvatpham * self.offsetdiachicosovitrimoivatpham),  # Vị trí rương
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + 0x8 + sothutuvatpham * self.offsetdiachicosovitrimoivatpham),  # Vị trí X
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + 0xC + sothutuvatpham * self.offsetdiachicosovitrimoivatpham),  # Vị trí Y
        )

        if vitrivatpham == (0, 0, 0, 0):
            return False

        return vitrivatpham

    def get_soluongvatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatpham + 0x4C8 + idvatpham * self.offsetdiachicosomoivatpham)

    def get_tenvatpham(self, idvatpham):
        return read_string(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatpham + 0x120 + idvatpham * self.offsetdiachicosomoivatpham)

    def get_capdovatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatpham + 0x68 + idvatpham * self.offsetdiachicosomoivatpham)

    def get_dbidvatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatpham + 0x698 + idvatpham * self.offsetdiachicosomoivatpham)

    def get_loaivatpham(self, idvatpham):
        if idvatpham <= 0 or idvatpham > SOLUONGVATPHAMTOIDA:
            return False

        diachicosothongtinvatpham = self.diachigame + self.offsetdiachicosothongtinvatpham + idvatpham * self.offsetdiachicosomoivatpham

        phamchat = read_short_int(self.tientrinh, diachicosothongtinvatpham + 0xFC, 1)
        danhmucvattutieuhao = read_short_int(self.tientrinh, diachicosothongtinvatpham + 0xFE, 2)
        danhmuctrangbi = read_int(self.tientrinh, diachicosothongtinvatpham + 0x100)
        loaihinh = read_short_int(self.tientrinh, diachicosothongtinvatpham + 0x108, 1)

        return phamchat, danhmucvattutieuhao, danhmuctrangbi, loaihinh

    def get_thuoctinhvatpham_map(self, idvatpham):
        if idvatpham <= 0 or idvatpham > SOLUONGVATPHAMTOIDA:
            return []

        diachicosothongtinvatpham = self.diachigame + self.offsetdiachicosothongtinvatpham + idvatpham * self.offsetdiachicosomoivatpham

        thuoctinhvatpham_map = {}

        for i in range(16):
            diachicosothongtinthuoctinhvatpham = diachicosothongtinvatpham + 0x51C + (i * 0x14)

            idthuoctinh = read_int(self.tientrinh, diachicosothongtinthuoctinhvatpham)

            if idthuoctinh <= 0:
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
        return read_short_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatpham + 0x4EC + idvatpham * self.offsetdiachicosomoivatpham) * self.get_soluongvatpham(
            idvatpham)

    def get_dobenhientaivatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatpham + 0x69C + idvatpham * self.offsetdiachicosomoivatpham)

    def get_dobentoidavatpham(self, idvatpham):
        if idvatpham <= 0 or idvatpham > SOLUONGVATPHAMTOIDA:
            return -1

        if int.from_bytes(read_bytes(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatpham + 0xFE + idvatpham * self.offsetdiachicosomoivatpham, 2), sys.byteorder) != 0:
            return -1

        for i in range(5):
            x = self.diachigame + self.offsetdiachicosothongtinvatpham + idvatpham * self.offsetdiachicosomoivatpham + (i * 0x14)
            if read_int(self.tientrinh, x) == 0x1F:
                dobentoida = read_int(self.tientrinh, x + 4)
                return dobentoida if dobentoida > 0 else -1

        return -1

    def get_idhephaivatpham(self, idvatpham):
        if idvatpham < 0 or idvatpham >= SOLUONGVATPHAMTOIDA:
            return -1

        for offset in range(5 * 0x14, 0xFE, 0x14):
            x = self.diachigame + self.offsetdiachicosothongtinvatpham + idvatpham * self.offsetdiachicosomoivatpham + offset
            if read_int(self.tientrinh, x) == 0x25:
                return read_int(self.tientrinh, x + 4)
        return -1

    def get_khoangcach(self, idnhanvat2, idnhanvat1 = 1):
        return int(math.dist(self.get_toado(idnhanvat1), self.get_toado(idnhanvat2)))

    def get_khoangcachsaptoi(self, idnhanvat2, idnhanvat1 = 1, default = KHOANGCACHTOIDATIMKIEMMUCTIEU):
        if not idnhanvat2:
            return default

        x2, y2 = self.get_toadosaptoi(idnhanvat2)
        if x2 <= 0:
            return default

        x1, y1 = self.get_toado(idnhanvat1)

        return int(math.dist((x1, y1), (x2, y2)))

    def get_khoangcachdiem(self, idnhanvat, toadox, toadoy):
        x2, y2 = self.get_toado(idnhanvat)
        return int(math.dist((toadox, toadoy), (x2, y2)))

    def get_is_kynangsansang(self, idkynang):
        if not self.get_is_dahockynang(idkynang):
            return False

        thoidiemhoiphuckynang = self.get_thoidiemhoiphuckynang(idkynang)

        return not thoidiemhoiphuckynang or thoidiemhoiphuckynang < self.get_donghothoigian() - 5

    def get_donghothoigian(self):
        # game.g_SubWorldSet
        return read_int(self.tientrinh, self.diachigame + 0x7118D8)

    def get_is_khuvuccothetancong(self):
        return read_int(self.tientrinh, self.diachigame + 0x7118D8 + 0x8 + 0xC0F4) > 0

    def get_idbandohientai(self):
        return read_int(self.tientrinh, self.diachigame + 0x6D8204)

    def get_tenbandohientai(self):
        return read_string(self.tientrinh, self.diachigame + 0x6D81B4)

    def get_is_dangbatauto(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB370)

    def get_is_dangtudongtimduong(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0x5BCC) > 0

    def set_is_dangtudongtimduong(self, is_dangtudongtimduong):
        if self.get_is_dangtudongtimduong() != is_dangtudongtimduong:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0x5BCC, 1 if is_dangtudongtimduong else 0)

    def get_iddoituongtudanh(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB010)

    def set_iddoituongtudanh(self, iddoituongtudanh):
        if self.get_iddoituongtudanh() != iddoituongtudanh:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB010, iddoituongtudanh)

    def get_khoangcachtheosau(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA9C4)

    def get_idtabkytrancac(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0x8F28)

    def set_idtabkytrancac(self, idtab):
        if self.get_idtabkytrancac() != idtab:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0x8F28, idtab)

    def get_is_tiepcan(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2D0)

    def set_is_tiepcan(self, is_tiepcan):
        if self.get_is_tiepcan() != is_tiepcan:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2D0, 1 if is_tiepcan else 0)

    def get_is_theosau(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA9A0)

    def set_is_theosau(self, is_theosau):
        if self.get_is_theosau() != is_theosau:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA9A0, 1 if is_theosau else 0)

    def get_phamvitimkiemmuctieu(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2D4)

    def set_phamvitimkiemmuctieu(self, phamvi):
        if self.get_phamvitimkiemmuctieu() != phamvi:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2D4, phamvi)

    def get_is_tamngungtancong(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA268)

    def set_is_tamngungtancong(self, is_tamngungtancong):
        if self.get_is_tamngungtancong() != is_tamngungtancong:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA268, 1 if is_tamngungtancong else 0)

    def get_is_datrieuhoithu(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB36C)

    def get_is_duoitheo(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB014) > 0

    def set_is_duoitheo(self, is_duoitheo):
        if self.get_is_duoitheo() != is_duoitheo:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB014, 1 if is_duoitheo else 0)

    def get_is_tranhboss(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2F0) > 0

    def get_is_danhnguoichoi(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA998) > 0

    def set_is_danhnguoichoi(self, is_danhnguoichoi):
        if self.get_is_danhnguoichoi() != is_danhnguoichoi:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA998, 1 if is_danhnguoichoi else 0)

    def get_is_danhquai(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA99C) > 0

    def set_is_danhquai(self, is_danhquai):
        if self.get_is_danhquai() != is_danhquai:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA99C, 1 if is_danhquai else 0)

    def get_is_boss(self, idnhanvat = 1):
        if self.get_idloainhanvat(idnhanvat) != IDLOAINHANVAT_QUAIVAT:
            return
        capdonhanvat = self.get_capdonhanvat(idnhanvat)
        sinhluctoida = self.get_sinhluctoida(idnhanvat)
        if capdonhanvat <= 55:
            return sinhluctoida >= 2000 * capdonhanvat
        elif capdonhanvat <= 75:
            return sinhluctoida > 50_000
        else:
            return sinhluctoida > 100_000

    def get_is_quaixanh(self, idnhanvat = 1):
        return self.get_idloainhanvat(idnhanvat) == IDLOAINHANVAT_QUAIVAT and self.get_tocdodichuyen(idnhanvat) > TOCDODICHUYENQUAITHUONG

    def get_idkynangtaytrai(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0x5B78)

    def get_idkynang1(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2F4)

    def set_idkynang1(self, idkynang1):
        if self.get_idkynang1() != idkynang1:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2F4, idkynang1)

    def get_idkynanghotro4(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2E8)

    def set_idkynangbotro4(self, idkynangbotro):
        if self.get_idkynanghotro4() != idkynangbotro:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA2E8, idkynangbotro)

    def get_is_tudongphucsinh(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB368)

    def get_is_dichuyenhoatdongquanhphamvi(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB100) > 0

    def set_is_dichuyenhoatdongquanhphamvi(self, is_dichuyenhoatdongquanhphamvi):
        if self.get_is_dichuyenhoatdongquanhphamvi() != is_dichuyenhoatdongquanhphamvi:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB100, 1 if is_dichuyenhoatdongquanhphamvi else 0)

    def get_is_dangkhoa(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB47C) > 0

    def get_idmuctieudangchichuot(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0x5B90)

    def get_idmuctieudangkhoa(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat + 0xC70)

    def set_idmuctieudangkhoa(self, idmuctieudangkhoa):
        if self.get_idmuctieudangkhoa() != idmuctieudangkhoa:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat + 0xC70, idmuctieudangkhoa)

    def get_idmuctieudangchon(self):
        # Tìm theo hàm vô hiệu hóa
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB490)

    def set_idmuctieudangchon(self, idmuctieudangchon):
        if self.get_idmuctieudangchon() != idmuctieudangchon:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xB490, idmuctieudangchon)

    def get_idmuctieutancong(self):
        # Tìm theo hàm vô hiệu hóa
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA30C)

    def set_idmuctieutancong(self, idmuctieutancong):
        if self.get_idmuctieutancong() != idmuctieutancong:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosocauhinh + 0xA30C, idmuctieutancong)

    def set_idmuctieu(self, idnhanvat):
        self.set_idmuctieudangchon(idnhanvat)
        self.set_idmuctieutancong(idnhanvat)

        idmuctieudangkhoa = self.get_idmuctieudangkhoa()
        if idmuctieudangkhoa and idmuctieudangkhoa != idnhanvat:
            self.set_idmuctieudangkhoa(0)

    def get_idnhanvattieptheo(self, idnhanvat = 1):
        diachicosonhanvattieptheo = read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvattieptheo)  # 1 biến nào đó mà + FE0 thì phải đấy
        idnhanvattieptheo = read_int(self.tientrinh, diachicosonhanvattieptheo + 0x4 + 0x8 * idnhanvat)
        if idnhanvattieptheo > SOLUONGNHANVATTOIDA or idnhanvattieptheo < 0:
            return -1
        return idnhanvattieptheo

    def get_idtrangthaiclickchuot(self):
        return read_int(self.tientrinh, self.diachigame + 0x26E6F4)

    def get_toadoclick(self):
        toadox, toadoy = self.get_toado()
        return (
            toadox + read_int(self.tientrinh, self.diachigame + 0x2689F4) - int(self.kichthuoccuasogame[0] / 2),
            toadoy + int(read_int(self.tientrinh, self.diachigame + 0x2689F8) - int(self.kichthuoccuasogame[1] / 2)) * 2
        )

    def get_is_dangmokytrancac(self):
        return read_int(self.tientrinh, self.diachigame + 0x26B8D4)

    def khoitaohamsudungvatpham(self):
        if self.diachihamsudungvatpham:
            return

        self.diachihamsudungvatpham = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamsudungvatpham + 0x80

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 20                     

            mov eax, dword ptr [{hex(diachidulieu)}]
            mov ecx, dword ptr [{hex(diachidulieu + 4)}]

            mov byte ptr [ebp - 16], 0x57
            mov dword ptr [ebp - 15], eax
            mov dword ptr [ebp - 11], ecx

            mov dword ptr [ebp - 4], 9        

            mov eax, dword ptr [{hex(self.diachigame + self.offsetdiachicosothuchiencaulenh)}]
            test eax, eax
            je ketthuc

            lea edx, [ebp - 4]
            push edx

            lea edx, [ebp - 16]
            push edx

            push eax

            mov ecx, dword ptr [eax]
            mov edx, dword ptr [ecx + 0x1C]
            call edx                        

            ketthuc:
            mov esp, ebp
            pop ebp
            ret 4                           
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamsudungvatpham, bytes(encoding), len(encoding))

    def action_sudungvatpham(self, sothutuvatpham, delay = 0.2):
        if not self.diachihamsudungvatpham:
            self.khoitaohamsudungvatpham()

        if time.time() - self._thoidiemsudungvatphamgannhat < delay:
            return False

        vitrivatpham = self.get_vitrivatpham(sothutuvatpham)
        if not vitrivatpham:
            return False

        idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

        if vitriruong != IDVITRIRUONG_HANHTRANG:
            return False

        dbid = self.get_dbidvatpham(idvatpham)
        if dbid <= 0:
            return False

        self._thoidiemsudungvatphamgannhat = time.time()

        diachidulieu = self.diachihamsudungvatpham + 0x80
        write_int(self.tientrinh, diachidulieu, dbid)

        write_bytes(self.tientrinh, diachidulieu + 4, bytes([vitriruong, 0, vitrix, vitriy]), 4)

        self.tientrinh.start_thread(self.diachihamsudungvatpham)
        return True

    def khoitaohamtudongtimduong(self):
        if self.diachihamtudongtimduong:
            return

        aob = "8B 0D ?? ?? ?? ?? 6A 01 57 56 81 C1 ?? ?? ?? ?? E8 ?? ?? ?? ??"

        scan_diachi = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if scan_diachi:
            diachi_ptr_doituong = read_int(self.tientrinh, scan_diachi + 2)
            offset_doituong = read_int(self.tientrinh, scan_diachi + 12)
            diachi_lenh_call = scan_diachi + 16
            khoang_cach_call = read_int(self.tientrinh, diachi_lenh_call + 1)
            diachi_ham = diachi_lenh_call + 5 + khoang_cach_call
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Caller hàm tự động tìm đường! Hủy bỏ khởi tạo.")
            return

        self.diachihamtudongtimduong = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamtudongtimduong + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov esi, dword ptr [{hex(diachidulieu)}]
            mov edi, dword ptr [{hex(diachidulieu + 4)}]

            push 01
            push edi
            push esi

            mov ecx, dword ptr [{hex(diachi_ptr_doituong)}]
            add ecx, {hex(offset_doituong)}

            mov eax, {hex(diachi_ham)}
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

        self._thoidiemtudongtimduonggannhat = time.time()

        diachidulieu = self.diachihamtudongtimduong + 0x40

        write_int(self.tientrinh, diachidulieu, int(round(toadox / 16)))
        write_int(self.tientrinh, diachidulieu + 4, int(round(toadoy / 32)))

        self.tientrinh.start_thread(self.diachihamtudongtimduong)
        return True

    def khoitaohamdichuyen(self):
        if self.diachihamdichuyen:
            return

        aob = "53 52 8B 15 ?? ?? ?? ?? 57 8D 0C 16 E8 ?? ?? ?? ?? A1 ?? ?? ?? ?? C7 80 ?? ?? ?? ?? 00 00 00 00"
        diachi_scan_ham = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if not diachi_scan_ham:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm di chuyển! Hủy bỏ khởi tạo.")
            return

        ptr_array_base = read_int(self.tientrinh, diachi_scan_ham + 4)

        khoang_cach_call = read_int(self.tientrinh, diachi_scan_ham + 13)
        diachi_ham = diachi_scan_ham + 17 + khoang_cach_call

        self.diachihamdichuyen = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamdichuyen + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov edi, dword ptr [{hex(diachidulieu)}]
            mov eax, dword ptr [{hex(diachidulieu + 4)}]
            mov ebx, 0
            push ebx
            push eax
            mov edx, dword ptr [{hex(ptr_array_base)}]
            push edi
            mov ecx, {hex(self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat)} 
            mov eax, {hex(diachi_ham)} 
            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdichuyen, bytes(encoding), len(encoding))

    def action_dichuyen(self, toadox, toadoy, delay = 0.05):
        if not self.diachihamdichuyen:
            self.khoitaohamdichuyen()

        if time.time() - self._thoidiemdichuyengannhat < delay:
            return False

        self._thoidiemdichuyengannhat = time.time()

        diachidulieu = self.diachihamdichuyen + 0x40
        write_int(self.tientrinh, diachidulieu, toadox)
        write_int(self.tientrinh, diachidulieu + 4, toadoy)
        self.tientrinh.start_thread(self.diachihamdichuyen)
        return True

    def action_dichuyengiukhoangcachtoida(self, idnhanvat2, khoangcachtoida, buocditoithieu = 30, delay = 0.05):
        if not self.get_is_nhanvattontai(idnhanvat2):
            return False

        if time.time() - self._thoidiemdichuyengiukhoangcachtoithieu < delay:
            return False

        x1, y1 = self.get_toado()
        x2, y2 = self.get_toado(idnhanvat2)

        D = math.dist((x1, y1), (x2, y2))

        if D > khoangcachtoida:
            tile = khoangcachtoida / D

            xmoi = x2 - tile * (x2 - x1)
            ymoi = y2 - tile * (y2 - y1)

            buocdi = math.dist((x1, y1), (xmoi, ymoi))

            if 0 < buocdi < buocditoithieu:
                tilebuocdi = buocditoithieu / buocdi
                xmoi = x1 + tilebuocdi * (xmoi - x1)
                ymoi = y1 + tilebuocdi * (ymoi - y1)

            self._thoidiemdichuyengiukhoangcachtoithieu = time.time()
            return self.action_dichuyen(int(xmoi), int(ymoi), delay = delay)

        return False

    def action_dichuyengiukhoangcachtoidadiem(self, toadox, toadoy, khoangcachtoida, buocditoithieu = 30, delay = 0.05):
        if time.time() - self._thoidiemdichuyengiukhoangcachtoithieu < delay:
            return False

        x1, y1 = self.get_toado()
        x2 = toadox
        y2 = toadoy

        D = math.dist((x1, y1), (x2, y2))

        if D > khoangcachtoida:
            tile = khoangcachtoida / D

            xmoi = x2 - tile * (x2 - x1)
            ymoi = y2 - tile * (y2 - y1)

            buocdi = math.dist((x1, y1), (xmoi, ymoi))

            if 0 < buocdi < buocditoithieu:
                tilebuocdi = buocditoithieu / buocdi
                xmoi = x1 + tilebuocdi * (xmoi - x1)
                ymoi = y1 + tilebuocdi * (ymoi - y1)

            self._thoidiemdichuyengiukhoangcachtoithieu = time.time()
            return self.action_dichuyen(int(xmoi), int(ymoi), delay = delay)

        return False

    def action_dichuyengiukhoangcachtoithieu(self, idnhanvat2, khoangcachtoithieu, buocditoithieu = 30, delay = 0.05):
        if not self.get_is_nhanvattontai(idnhanvat2):
            return False

        if time.time() - self._thoidiemdichuyengiukhoangcachtoithieu < delay:
            return False

        x1, y1 = self.get_toado()
        x2, y2 = self.get_toado(idnhanvat2)

        D = math.dist((x1, y1), (x2, y2))

        if 0 < D < khoangcachtoithieu:
            tile = khoangcachtoithieu / D

            xmoi = x2 + tile * (x1 - x2)
            ymoi = y2 + tile * (y1 - y2)

            buocdi = math.dist((x1, y1), (xmoi, ymoi))

            if 0 < buocdi < buocditoithieu:
                tilebuocdi = buocditoithieu / buocdi
                xmoi = x1 + tilebuocdi * (xmoi - x1)
                ymoi = y1 + tilebuocdi * (ymoi - y1)

            self._thoidiemdichuyengiukhoangcachtoithieu = time.time()

            return self.action_dichuyen(int(xmoi), int(ymoi), delay = delay)

        return False

    def khoitaohamsuavatpham(self):
        if self.diachihamsuavatpham:
            return

        self.diachihamsuavatpham = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamsuavatpham + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 16                     

            mov eax, dword ptr [{hex(diachidulieu + 0xC)}]

            mov byte ptr [ebp - 12], 0x71
            mov dword ptr [ebp - 11], eax

            mov dword ptr [ebp - 4], 5

            mov eax, dword ptr [{hex(self.diachigame + self.offsetdiachicosothuchiencaulenh)}]
            test eax, eax
            je ketthuc

            lea edx, [ebp - 4]
            push edx

            lea edx, [ebp - 12]
            push edx

            push eax

            mov ecx, dword ptr [eax]
            mov edx, dword ptr [ecx + 0x1C]
            call edx

            ketthuc:
            mov esp, ebp
            pop ebp
            ret 4
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamsuavatpham, bytes(encoding), len(encoding))

    def action_suavatpham(self, idvatpham, delay = 0.25):
        if not self.diachihamsuavatpham:
            self.khoitaohamsuavatpham()

        if time.time() - self._thoidiemsuavatphamgannhat < delay:
            return False

        dobenhientai = self.get_dobenhientaivatpham(idvatpham)
        dobentoida = self.get_dobentoidavatpham(idvatpham)

        if dobentoida == -1 or dobenhientai >= dobentoida or dobenhientai < 0:
            return False

        dbid = self.get_dbidvatpham(idvatpham)
        if dbid <= 0:
            return False

        self._thoidiemsuavatphamgannhat = time.time()

        diachidulieu = self.diachihamsuavatpham + 0x40

        write_int(self.tientrinh, diachidulieu + 0xC, dbid)

        self.tientrinh.start_thread(self.diachihamsuavatpham)
        return True

    def khoitaohambattathieuungbotro(self):
        if self.diachihambattathieuungbotro:
            return

        aob = "53 E8 ?? ?? ?? ?? 85 C0 0F 84 ?? ?? ?? ?? 83 78 18 00 0F 84 ?? ?? ?? ?? 8B 4C 24 20 8B 50 0C 51 52 E8 ?? ?? ?? ?? 83 C4 08 E9 ?? ?? ?? ??"

        scan_diachi = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if scan_diachi:
            diachi_lenh_call = scan_diachi + 33
            khoang_cach_call = read_int(self.tientrinh, diachi_lenh_call + 1)
            diachi_ham = diachi_lenh_call + 5 + khoang_cach_call
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Caller Hàm bật tắt hiệu ứng bổ trợ! Hủy bỏ khởi tạo.")
            return

        self.diachihambattathieuungbotro = self.tientrinh.allocate(256)
        diachidulieu = self.diachihambattathieuungbotro + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov edx, dword ptr [{hex(diachidulieu)}]
            mov ecx, 00000000

            push ecx
            push edx
            mov eax, {hex(diachi_ham)}
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

        self._thoidiembattathieuungbotrogannhat_map[idhieuungbotro] = time.time()

        diachidulieu = self.diachihambattathieuungbotro + 0x40

        write_int(self.tientrinh, diachidulieu, idhieuungbotro)

        self.tientrinh.start_thread(self.diachihambattathieuungbotro)

        return True

    def khoitaohamdoimaupk(self):
        if self.diachihamdoimaupk:
            return

        self.diachihamdoimaupk = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamdoimaupk + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 16

            mov eax, dword ptr [{hex(diachidulieu)}]

            mov byte ptr [ebp - 12], 0x6D
            mov byte ptr [ebp - 11], al

            mov dword ptr [ebp - 4], 2

            mov eax, dword ptr [{hex(self.diachigame + self.offsetdiachicosothuchiencaulenh)}]
            test eax, eax
            je ketthuc

            lea edx, [ebp - 4]
            push edx

            lea edx, [ebp - 12]
            push edx

            push eax

            mov ecx, dword ptr [eax]
            mov edx, dword ptr [ecx + 0x1C]
            call edx                        

            add esp, 0x0C

            ketthuc:
            mov esp, ebp
            pop ebp
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdoimaupk, bytes(encoding), len(encoding))

    def action_doimaupk(self, idmaupk):
        if not self.diachihamdoimaupk:
            self.khoitaohamdoimaupk()

        self._thoidiemdoimaupkgannhat = time.time()

        diachidulieu = self.diachihamdoimaupk + 0x40
        write_int(self.tientrinh, diachidulieu, idmaupk - 8)

        self.tientrinh.start_thread(self.diachihamdoimaupk)
        return True

    def khoitaohammokhoa(self):
        if self.diachihammokhoa:
            return

        aob_wrapper_mokhoa = "53 6A 00 8B 0D ?? ?? ?? ?? 81 C1 ?? ?? ?? ?? E8 ?? ?? ?? ?? E9 ?? ?? ?? ?? 85 DB 0F 84 ?? ?? ?? ?? 53 6A 07 EB ?? 85 DB"
        scan_wrapper = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_wrapper_mokhoa)
        )

        if not scan_wrapper:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Wrapper Mở khóa! Hủy bỏ khởi tạo.")
            return

        diachi_ptr_cauhinh = read_int(self.tientrinh, scan_wrapper + 5)
        offset_cauhinh_mokhoa = read_int(self.tientrinh, scan_wrapper + 11)

        khoang_cach_call = read_int(self.tientrinh, scan_wrapper + 16)
        diachi_ham_mokhoa = scan_wrapper + 20 + khoang_cach_call

        self.diachihammokhoa = self.tientrinh.allocate(256)
        diachidulieu = self.diachihammokhoa + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push {hex(diachidulieu)}
            push 03

            mov ecx, dword ptr [{hex(diachi_ptr_cauhinh)}]
            add ecx, {hex(offset_cauhinh_mokhoa)}

            mov eax, {hex(diachi_ham_mokhoa)}
            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihammokhoa, bytes(encoding), len(encoding))

    def action_mokhoa(self, makhoa, delay = 0.5):
        if not self.diachihammokhoa:
            self.khoitaohammokhoa()

        if time.time() - self._thoidiemmokhoagannhat < delay:
            return False

        self._thoidiemmokhoagannhat = time.time()

        diachidulieu = self.diachihammokhoa + 0x40

        makhoa_bytes = str(makhoa).encode("ascii")[:31] + b"\x00"
        write_bytes(self.tientrinh, diachidulieu, makhoa_bytes, len(makhoa_bytes))

        self.tientrinh.start_thread(self.diachihammokhoa)
        return True

    def khoitaohamsudungkynangtoado(self):
        if self.diachihamsudungkynangtoado:
            return

        aob = "8B 8F ?? ?? ?? ?? 8B 15 ?? ?? ?? ?? 69 C9 ?? ?? ?? ?? 8B 84 11 ?? ?? ?? ?? 55 03 CA 6A FF 50 E8 ?? ?? ?? ??"

        scan_diachi = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if scan_diachi:
            diachi_lenh_call = scan_diachi + 31
            khoang_cach_call = read_int(self.tientrinh, diachi_lenh_call + 1)
            diachi_ham = diachi_lenh_call + 5 + khoang_cach_call
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern lấy địa chỉ hàm sử dụng kỹ năng tọa độ mới! Hủy bỏ khởi tạo.")
            return

        self.diachihamsudungkynangtoado = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamsudungkynangtoado + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push dword ptr [{hex(diachidulieu + 8)}]
            push dword ptr [{hex(diachidulieu + 4)}]
            push dword ptr [{hex(diachidulieu)}]
            mov ecx, {hex(self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat)}
            mov eax, {hex(diachi_ham)}
            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamsudungkynangtoado, bytes(encoding), len(encoding))

    def action_sudungkynangtoado(self, idkynang, toadox, toadoy, delay = 0.05):
        if not self.diachihamsudungkynangtoado:
            self.khoitaohamsudungkynangtoado()

        if time.time() - self._thoidiemsudungkynanggannhat_map.get(idkynang, 0.) < delay:
            return False

        self._thoidiemsudungkynanggannhat_map[idkynang] = time.time()

        diachidulieu = self.diachihamsudungkynangtoado + 0x40
        write_int(self.tientrinh, diachidulieu, idkynang)
        write_int(self.tientrinh, diachidulieu + 4, toadox)
        write_int(self.tientrinh, diachidulieu + 8, toadoy)

        self.tientrinh.start_thread(self.diachihamsudungkynangtoado)
        return True

    def action_sudungkynangphudau(self, idnhanvat, idkynang, khoangcachtoida, delay = 0.05):
        if time.time() - self._thoidiemsudungkynanggannhat_map.get(idkynang, 0.) < delay:
            return False

        x1, y1 = self.get_toado()
        x2, y2 = self.get_toado(idnhanvat)

        x2_saptoi, y2_saptoi = self.get_toadosaptoi(idnhanvat)
        idtrangthai = self.get_idtrangthainhanvat(idnhanvat)

        if idtrangthai == IDTRANGTHAINHANVAT_DICHUYEN and x2_saptoi > 0:
            deltax_vector = x2_saptoi - x2
            deltay_vector = y2_saptoi - y2

            khoangcachdukien = math.dist((x2, y2), (x2_saptoi, y2_saptoi))

            if khoangcachdukien > 0:
                is_bidongbang = self.get_is_bidongbang(idnhanvat)
                tocdo = self.get_tocdodichuyen(idnhanvat)
                offset_phudau = tocdo * 4 if is_bidongbang else tocdo * 9
                offset_phudau = min(offset_phudau, khoangcachdukien)

                x2 = x2 + (deltax_vector * offset_phudau / khoangcachdukien)
                y2 = y2 + (deltay_vector * offset_phudau / khoangcachdukien)

        deltax_final = x2 - x1
        deltay_final = y2 - y1
        khoangcachdendiemdon = math.dist((x1, y1), (x2, y2))

        target_x, target_y = x2, y2

        if khoangcachdendiemdon > khoangcachtoida:
            ratio = khoangcachtoida / max(khoangcachdendiemdon, 1)
            target_x = x1 + deltax_final * ratio
            target_y = y1 + deltay_final * ratio

        return self.action_sudungkynangtoado(idkynang, int(target_x), int(target_y), delay = delay)

    def action_sudungkynangtoadochichuot(self, idkynang, khoangcachtoida, delay = 0.05):
        if time.time() - self._thoidiemsudungkynanggannhat_map.get(idkynang, 0.) < delay:
            return False

        x1, y1 = self.get_toado()
        x2, y2 = self.get_toadoclick()

        deltax = x2 - x1
        deltay = y2 - y1

        khoangcach = max(round(math.sqrt(deltax ** 2 + deltay ** 2)), 1)

        if khoangcach > khoangcachtoida:
            deltax = deltax * khoangcachtoida / khoangcach
            deltay = deltay * khoangcachtoida / khoangcach

        target_x = int(x1 + deltax)
        target_y = int(y1 + deltay)

        return self.action_sudungkynangtoado(idkynang, target_x, target_y, delay = delay)

    def khoitaohamdongkytrancac(self):
        if self.diachihamdongkytrancac:
            return

        aob = "81 7D 08 00 01 00 00 75 12 83 7D 0C 1B 75 0A 6A 00 E8 ?? ?? ?? ?? 83 C4 04 EB 33"

        scan_diachi = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if scan_diachi:
            diachi_lenh_call = scan_diachi + 17
            khoang_cach_call = read_int(self.tientrinh, diachi_lenh_call + 1)
            diachi_ham = diachi_lenh_call + 5 + khoang_cach_call
        else:
            print("[LỖI] Không tìm thấy Pattern đóng KTC!")
            return

        self.diachihamdongkytrancac = self.tientrinh.allocate(256)
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push 0
            mov eax, {hex(diachi_ham)}
            call eax
            add esp, 4
            ret 4               
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdongkytrancac, bytes(encoding), len(encoding))

    def action_dongkytrancac(self, delay = 0.05):
        if not self.diachihamdongkytrancac:
            self.khoitaohamdongkytrancac()
        if time.time() - self._thoidiemdongkytrancacgannhat < delay:
            return False

        self._thoidiemdongkytrancacgannhat = time.time()
        self.tientrinh.start_thread(self.diachihamdongkytrancac)
        return True

    def khoitaohammotabkytrancac(self):
        if self.diachihammotabkytrancac:
            return

        self.diachihammotabkytrancac = self.tientrinh.allocate(256)
        diachidulieu = self.diachihammotabkytrancac + 0x80

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 16                     

            mov eax, dword ptr [{hex(diachidulieu)}]
            mov ecx, dword ptr [{hex(diachidulieu + 4)}]

            mov byte ptr [ebp - 12], 0x73
            mov byte ptr [ebp - 11], al
            mov dword ptr [ebp - 10], ecx

            mov dword ptr [ebp - 4], 6        

            mov eax, dword ptr [{hex(self.diachigame + self.offsetdiachicosothuchiencaulenh)}]
            test eax, eax
            je ketthuc

            lea edx, [ebp - 4]
            push edx

            lea edx, [ebp - 12]
            push edx

            push eax

            mov ecx, dword ptr [eax]
            mov edx, dword ptr [ecx + 0x1C]
            call edx                        

            add esp, 0x0C                   

            ketthuc:
            mov esp, ebp
            pop ebp
            ret 4                           
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihammotabkytrancac, bytes(encoding), len(encoding))

    def action_motabkytrancac(self, vitritab, delay = 0.05):
        if not self.diachihammotabkytrancac:
            self.khoitaohammotabkytrancac()

        if time.time() - self._thoidiemmotabkytrancacgannhat < delay:
            return False

        self._thoidiemmotabkytrancacgannhat = time.time()

        diachidulieu = self.diachihammotabkytrancac + 0x80
        write_int(self.tientrinh, diachidulieu, 3)
        write_int(self.tientrinh, diachidulieu + 4, vitritab)

        self.tientrinh.start_thread(self.diachihammotabkytrancac)
        return True

    def khoitaohammuavatphamkytrancac(self):
        if self.diachihammuavatphamkytrancac:
            return

        self.diachihammuavatphamkytrancac = self.tientrinh.allocate(256)
        diachidulieu = self.diachihammuavatphamkytrancac + 0x80

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 24                     

            mov eax, dword ptr [{hex(diachidulieu)}]
            mov ecx, dword ptr [{hex(diachidulieu + 4)}]
            mov edx, dword ptr [{hex(diachidulieu + 8)}]

            mov byte ptr [ebp - 20], 0x5B
            mov dword ptr [ebp - 19], eax
            mov dword ptr [ebp - 15], ecx
            mov dword ptr [ebp - 11], edx

            mov dword ptr [ebp - 4], 13        

            mov eax, dword ptr [{hex(self.diachigame + self.offsetdiachicosothuchiencaulenh)}]
            test eax, eax
            je ketthuc

            lea edx, [ebp - 4]
            push edx

            lea edx, [ebp - 20]
            push edx

            push eax

            mov ecx, dword ptr [eax]
            mov edx, dword ptr [ecx + 0x1C]
            call edx                        

            add esp, 0x0C                   

            ketthuc:
            mov esp, ebp
            pop ebp
            ret 4                           
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihammuavatphamkytrancac, bytes(encoding), len(encoding))

    def action_muavatphamkytrancac(self, idtab, vitrivatpham, soluong, delay = 0.05):
        if not self.diachihammuavatphamkytrancac:
            self.khoitaohammuavatphamkytrancac()

        if self.get_idtabkytrancac() != idtab:
            vitritab = VITRITAB_MAP.get(idtab)
            if vitritab is not None:
                self.action_motabkytrancac(vitritab)
            return False
        if self.get_is_dangmokytrancac():
            self.action_dongkytrancac()

        if time.time() - self._thoidiemmuakytrancacgannhat < delay:
            return False

        self._thoidiemmuakytrancacgannhat = time.time()

        diachidulieu = self.diachihammuavatphamkytrancac + 0x80
        write_int(self.tientrinh, diachidulieu, idtab)
        write_int(self.tientrinh, diachidulieu + 4, vitrivatpham)
        write_int(self.tientrinh, diachidulieu + 8, soluong)

        self.tientrinh.start_thread(self.diachihammuavatphamkytrancac)

        return True

    def khoitaohamphucsinh(self):
        if self.diachihamphucsinh:
            return

        self.diachihamphucsinh = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamphucsinh + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 16                     

            mov eax, dword ptr [{hex(diachidulieu)}]

            mov byte ptr [ebp - 12], 0x6B
            mov dword ptr [ebp - 11], eax

            mov dword ptr [ebp - 4], 5        

            mov eax, dword ptr [{hex(self.diachigame + self.offsetdiachicosothuchiencaulenh)}]
            test eax, eax
            je ketthuc

            lea edx, [ebp - 4]
            push edx

            lea edx, [ebp - 12]
            push edx

            push eax

            mov ecx, dword ptr [eax]
            mov edx, dword ptr [ecx + 0x1C]
            call edx                        

            add esp, 0x0C                   

            ketthuc:
            mov esp, ebp
            pop ebp
            ret 4                           
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamphucsinh, bytes(encoding), len(encoding))

    def action_phucsinh(self, tuychonphucsinh = TUYCHONPHUCSINH_PHUCSINH, delay = 0.05):
        if not self.diachihamphucsinh:
            self.khoitaohamphucsinh()

        if not self.get_is_nhanvatdachet():
            return False

        if time.time() - self._thoidiemphucsinhgannhat < delay:
            return False

        self._thoidiemphucsinhgannhat = time.time()

        diachidulieu = self.diachihamphucsinh + 0x40
        write_int(self.tientrinh, diachidulieu, tuychonphucsinh)

        self.tientrinh.start_thread(self.diachihamphucsinh)
        return True

    def action_timkiemtoanbodiachiham(self):
        aob_nv = "A1 ?? ?? ?? ?? 8B 15 ?? ?? ?? ?? 56 8B F1 8B 88 ?? ?? ?? ?? 69 C9 ?? ?? ?? ?? 8B 84 ?? ?? ?? ?? ?? 8B 0D ?? ?? ?? ?? 8B 15 ?? ?? ?? ?? 57 50 51 52"
        scan_nv = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_nv))

        if scan_nv:
            diachi_ptr = read_int(self.tientrinh, scan_nv + 7)
            diachi_thuc_te = read_int(self.tientrinh, diachi_ptr)

            self.offsetdiachicosonhanvat = diachi_thuc_te - self.diachigame
            self.offsetdiachicosomoinhanvat = read_int(self.tientrinh, scan_nv + 22)
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset cơ sở nhân vật!")

        aob_bando = "8B 44 24 08 8B 54 24 04 50 8B 81 ?? ?? ?? ?? 52 8B 91 ?? ?? ?? ?? 50 8B 81 ?? ?? ?? ?? 52 8B 91 ?? ?? ?? ?? 50 8B 81 ?? ?? ?? ?? 8B 89 ?? ?? ?? ?? 69 C9 ?? ?? ?? ?? 52 50 81 C1 ?? ?? ?? ??"
        scan_bando = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_bando))

        if scan_bando:
            diachi_bando_tinh = read_int(self.tientrinh, scan_bando + 59)
            self.offsetdiachicosobando = diachi_bando_tinh - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset cơ sở mảng bản đồ!")

        aob_vtvp = "56 57 8B 7C 24 0C 8B F1 85 FF 74 ?? 8A 07 3C 40 76 ?? 3C FD 73 ?? 0F B6 C8 83 3C 8E 00 74 ?? A1 ?? ?? ?? ?? 83 B8 ?? ?? ?? ?? 00 74 ?? 8D 88 ?? ?? ?? ?? E8 ?? ?? ?? ?? 0F B6 17 8B 04 96 57 8B CE FF D0"
        scan_vtvp = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_vtvp))

        if scan_vtvp:
            diachi_ptr = read_int(self.tientrinh, scan_vtvp + 32)
            diachi_thuc_te = read_int(self.tientrinh, diachi_ptr)
            offset_struct = read_int(self.tientrinh, scan_vtvp + 38)
            self.offsetdiachicosovitrivatpham = (diachi_thuc_te + offset_struct + 0x8) - self.diachigame
            self.offsetdiachicosovitrimoivatpham = 0x10
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset vị trí vật phẩm!")

        aob_ttvp = "69 FF ?? ?? ?? ?? 89 84 0F ?? ?? ?? ?? 0F B7 56 ?? A1 ?? ?? ?? ?? 89 94 07 ?? ?? ?? ?? 8B 4E ?? 8B 15 ?? ?? ?? ?? 89 8C 17 ?? ?? ?? ?? 8B 0D ?? ?? ?? ??"
        scan_ttvp = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_ttvp))

        if scan_ttvp:
            size_ttvp = read_int(self.tientrinh, scan_ttvp + 2)
            self.offsetdiachicosomoivatpham = size_ttvp
            diachi_ptr = read_int(self.tientrinh, scan_ttvp + 18)
            diachi_thuc_te = read_int(self.tientrinh, diachi_ptr)
            self.offsetdiachicosothongtinvatpham = diachi_thuc_te - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset thông tin vật phẩm!")

        aob_nhom = "A1 ?? ?? ?? ?? 83 B8 ?? ?? ?? ?? 00 74 ?? 8B 54 24 04 56 B8 ?? ?? ?? ?? 42 57 8D 9B 00 00 00 00 8B F8 8B F2 83 C0 ?? B9 ?? ?? ?? ?? 83 C2 ?? 3D ?? ?? ?? ?? F3 A5"
        scan_nhom = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_nhom))

        if scan_nhom:
            base_nhom = read_int(self.tientrinh, scan_nhom + 20) - self.diachigame
            self.offsetdiachicosothongtinthanhviendoinhom = base_nhom
            size_nhom = read_bytes(self.tientrinh, scan_nhom + 38, 1)[0]
            self.offsetdiachicosomoithanhviendoinhom = size_nhom
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset thông tin thành viên đội nhóm!")

        aob_cauhinh = "8B 15 ?? ?? ?? ?? 8B 8A ?? ?? ?? ?? 69 C9 ?? ?? ?? ?? 03 0D ?? ?? ?? ?? 50 E8 ?? ?? ?? ?? 8B D8 89 5C 24 ?? 85 DB"
        scan_cauhinh = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_cauhinh))

        if scan_cauhinh:
            diachi_ptr_cauhinh = read_int(self.tientrinh, scan_cauhinh + 2)
            diachi_thuc_te_cauhinh = read_int(self.tientrinh, diachi_ptr_cauhinh)
            self.offsetdiachicosocauhinh = diachi_thuc_te_cauhinh - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset cơ sở cấu hình (Auto/Settings)!")

        aob_nvtt = "8B 5C 24 2C 8B 43 01 57 0F B6 7B 1B 50 B9 ?? ?? ?? ?? 89 7C 24 14 E8 ?? ?? ?? ?? 89 44 24 1C 85 C0 0F 84 ?? ?? ?? ?? 56 8B F0 A1 ?? ?? ?? ?? 69 F6 ?? ?? ?? ??"
        scan_nvtt = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_nvtt))

        if scan_nvtt:
            base_g_subworldset = read_int(self.tientrinh, scan_nvtt + 14)
            self.offsetdiachicosonhanvattieptheo = (base_g_subworldset - self.diachigame) + 0xFE0
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset nhân vật tiếp theo!")

        aob_thuchiencaulenh = "51 8A 44 24 08 88 44 24 01 A1 ?? ?? ?? ?? C6 04 24 6D 85 C0 74 ?? 8D 54 24 08 52 8D 54 24 04 C7 44 24 0C 02 00 00 00 8B 08 52 50 8B 41 1C FF D0"
        scan_thuchiencaulenh = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_thuchiencaulenh))

        if scan_thuchiencaulenh:
            diachi_tinh_caulenh = read_int(self.tientrinh, scan_thuchiencaulenh + 10)
            self.offsetdiachicosothuchiencaulenh = diachi_tinh_caulenh - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Cơ sở thực hiện câu lệnh (Packet Sender)!")

        aob_giamxuatchieu = "89 91 40 09 00 00 8B 91 ?? ?? 00 00 89 91 44 09 00 00 8B 15 ?? ?? ?? ?? 89 91 48 09 00 00 8B 15 ?? ?? ?? ?? 89 91 4C 09 00 00 8B 91 ?? ?? 00 00"
        scan_giamxuatchieu = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_giamxuatchieu))

        if scan_giamxuatchieu:
            self.offsetdiachigiamxuatchieu1 = scan_giamxuatchieu + 18 - self.diachigame
            self.offsetdiachigiamxuatchieu2 = scan_giamxuatchieu + 30 - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset Giảm xuất chiêu khi thay đồ!")

        aob_muctieu_c780 = "2B C2 0F AF E9 8B C8 0F AF C8 03 E9 81 FD 00 00 08 00 7D ?? 53 52 8B 15 ?? ?? ?? ?? 57 8D 0C 16 E8 ?? ?? ?? ?? A1 ?? ?? ?? ?? C7 80 ?? ?? ?? ?? 00 00 00 00"
        scan_muctieu_c780 = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_muctieu_c780))

        if scan_muctieu_c780:
            self.offsetdiachithietlapmuctieu_C705 = scan_muctieu_c780 + 42 - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern C7 80 Thiết lập mục tiêu!")

        aob_muctieu_8988 = "A1 ?? ?? ?? ?? 8B 88 ?? ?? ?? ?? 8B 15 ?? ?? ?? ?? 69 C9 ?? ?? ?? ?? 83 BC 11 ?? ?? ?? ?? 00 75 ?? 83 BE ?? ?? ?? ?? 0A 57 0F 8D ?? ?? ?? ?? 81 BE ?? ?? ?? ?? E8 03 00 00 0F 8D ?? ?? ?? ?? 8B 8E ?? ?? ?? ?? 89 88 ?? ?? ?? ??"
        scan_muctieu_8988 = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_muctieu_8988))

        if scan_muctieu_8988:
            self.offsetdiachithietlapmuctieu_890D = scan_muctieu_8988 + 69 - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern 89 88 Thiết lập mục tiêu!")

        aob_muctieutancong = "8B 15 ?? ?? ?? ?? 8B CF 69 C9 ?? ?? ?? ?? 80 7C 11 ?? 01 75 ?? 33 C0 8D 8E ?? ?? ?? ?? 39 39 74 ?? 40 83 C1 04 83 F8 32 7C ?? 3B BE ?? ?? ?? ?? 74 ?? 89 BE ?? ?? ?? ?? 89 AE ?? ?? ?? ?? 89 AE ?? ?? ?? ?? 8B 86 ?? ?? ?? ?? 50 8B CE E8 ?? ?? ?? ?? 85 C0 0F 85 ?? ?? ?? ?? EB ?? 89 AE ?? ?? ?? ??"
        scan_muctieutancong = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_muctieutancong))

        if scan_muctieutancong:
            self.offsetdiachithietlapmuctieutancong_ingame = scan_muctieutancong + 50 - self.diachigame
            self.offsetdiachithietlapmuctieutancong_ngoaiphamvi = scan_muctieutancong + 92 - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Thiết lập mục tiêu tấn công!")

        aob_muctieutancong_dichuot = "55 39 5E 08 0F 84 ?? ?? ?? ?? 8B CE E8 ?? ?? ?? ?? 89 9E ?? ?? ?? ?? 89 9E ?? ?? ?? ?? 89 9E ?? ?? ?? ?? 89 9E ?? ?? ?? ?? 89 9E ?? ?? ?? ?? A1 ?? ?? ?? ?? 8B 88 ?? ?? ?? ?? 8B 15 ?? ?? ?? ?? 69 C9 ?? ?? ?? ??"
        scan_muctieutancong_dichuot = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_muctieutancong_dichuot))

        if scan_muctieutancong_dichuot:
            self.offsetdiachithietlapmuctieutancong_dichuot = scan_muctieutancong_dichuot + 17 - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Thiết lập mục tiêu tấn công lúc dí chuột!")

        aob_muctieutancong_theolaitan = "51 8B CF 69 C9 ?? ?? ?? ?? 03 0D ?? ?? ?? ?? 8D 54 24 18 52 E8 ?? ?? ?? ?? 8B 44 24 10 8B 4C 24 14 50 51 8B CE E8 ?? ?? ?? ?? 5D 33 C0 5F 89 86 ?? ?? ?? ??"
        scan_muctieutancong_theolaitan = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_muctieutancong_theolaitan))

        if scan_muctieutancong_theolaitan:
            self.offsetdiachithietlapmuctieutancong_theolaitan = scan_muctieutancong_theolaitan + 46 - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Thiết lập mục tiêu tấn công lúc theo lại gần!")

        aob_muctieutancong_ngoaiphamvidichuyen = "33 C0 5B 83 C4 14 C2 08 00 5F 89 AE ?? ?? ?? ?? 89 AE ?? ?? ?? ?? 89 AE ?? ?? ?? ?? 5E 5D B8 01 00 00 00 5B 83 C4 14 C2 08 00"
        scan_muctieutancong_ngoaiphamvidichuyen = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_muctieutancong_ngoaiphamvidichuyen))

        if scan_muctieutancong_ngoaiphamvidichuyen:
            self.offsetdiachithietlapmuctieutancong_ngoaiphamvidichuyen = scan_muctieutancong_ngoaiphamvidichuyen + 10 - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Thiết lập mục tiêu tấn công ngoài phạm vi di chuyển!")

        danhsachthuoctinh = dir(self)
        tongsoham = 0

        for tenthuoctinh in danhsachthuoctinh:
            if tenthuoctinh.startswith("khoitaoham") and callable(getattr(self, tenthuoctinh)):
                tongsoham += 1
                hamkhoitao = getattr(self, tenthuoctinh)
                try:
                    hamkhoitao()
                except Exception as e:
                    print(f"[LỖI NGOẠI LỆ CỦA PYTHON] Xảy ra lỗi khi chạy {tenthuoctinh}: {e}")
