import ctypes

import pymem
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

from hangso import *
from tienich import *

# Inspect từ Tên nhân vật - 0xBC9
OFFSET_DIACHICOSONHANVAT = 0x4BA7C0 + 0x000
OFFSET_DIACHICOSOMOINHANVAT = 0x8294

# Inspect từ ID vị trí rương = 1 khi cầm vật phẩm lên và đặt xuống hành trang là 3
# Lấy địa chỉ tìm được - 4 sẽ ra ID vật phẩm, Lấy địa chỉ - ID vật phẩm * 0x10 sẽ ra OFFSET_DIACHICOSOVITRIVATPHAM
OFFSET_DIACHICOSOVITRIVATPHAM = 0x49F1D4 + 0x000
OFFSET_DIACHICOSOVITRIMOIVATPHAM = 0x10

# Inspect từ Hàm bán đồ
OFFSET_DIACHICOSOTHONGTINVATPHAM = 0x2BBD60 + 0x000
OFFSET_DIACHICOSOMOIVATPHAM = 0x778
#
OFFSET_DIACHICOSOTHONGTINVATPHAMDUOIDAT = 0x2CA5100 + 0x000
OFFSET_DIACHICOSOMOIVATPHAMDUOIDAT = 0x3F4

# Inspect từ Tọa độ X, Y của thành viên thay đổi
OFFSET_DIACHICOSOTHONGTINTHANHVIENDOINHOM = 0x2CA4E84 + 0x000
OFFSET_DIACHICOSOMOITHANHVIENDOINHOM = 0x30


class MoiTruong:
    def __init__(self, idcuaso):
        self._thoidiemboquamuctieumaucaogannhat = 0.
        self._thoidiemdichuyengiukhoangcachtoithieu = 0.
        self._thoidiemtudongtimduonggannhat = 0.
        self._thoidiemtudongtimduongxuyenbandogannhat = 0.
        self._thoidiembanvatphamgannhat = 0.
        self._thoidiemsudungvatphamgannhat = 0.
        self._thoidiemdichuyengannhat = 0.
        self._thoidiemsuavatphamgannhat = 0.
        self._thoidiembattathieuungbotrogannhat_map = {}
        self._thoidiemnhatvatphamgannhat = 0.
        self._thoidiemsudungphimtatgannhat = 0.

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

        kichthuoccuaso = win32gui.GetWindowRect(self.idcuaso)
        if not kichthuoccuaso:
            raise Exception("Lấy kích thước cửa sổ game không thành công")

        self.kichthuoccuasogame = kichthuoccuaso[2] - kichthuoccuaso[0], kichthuoccuaso[3] - kichthuoccuaso[1]

        self.diachihambanvatpham = 0
        self.diachihamsudungvatpham = 0
        self.diachihamtudongtimduong = 0
        self.diachihamtudongtimduongxuyenbando = 0
        self.diachihamdichuyen = 0
        self.diachihamsuavatpham = 0
        self.diachihambattathieuungbotro = 0
        self.diachihamboquamuctieumaucao = 0
        self.diachihamnhatvatpham = 0
        self.diachihamsudungphimtat = 0

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

    def __del__(self):
        def safe_free(diachi):
            try:
                if diachi and hasattr(self, "tientrinh"):
                    self.tientrinh.free(diachi)
            except:
                pass

        cac_ten_thuoc_tinh = [
            "diachihambanvatpham",
            "diachihamsudungvatpham",
            "diachihamtudongtimduong",
            "diachihamtudongtimduongxuyenbando",
            "diachihamdichuyen",
            "diachihambattathieuungbotro",
            "diachihamboquamuctieumaucao",
            "diachihamnhatvatpham",
            "diachihamdoimaupk",
            "diachihammokhoa",
            "diachihamsudungphimtat",

            "diachihamdongcuahang",
            "diachihamdoithoai",
            "diachihamxacnhandoithoai",
        ]

        for ten_thuoc_tinh in cac_ten_thuoc_tinh:
            if hasattr(self, ten_thuoc_tinh):
                diachi = getattr(self, ten_thuoc_tinh)
                safe_free(diachi)

    def get_is_dangmatketnoi(self):
        return not self.get_is_nhanvattontai()

    def get_is_cuasogametontai(self):
        return win32gui.IsWindow(self.idcuaso)

    def get_is_cuasogamekichhoat(self):
        return win32gui.GetForegroundWindow() == self.idcuaso

    def get_is_nhanvattontai(self, idnhanvat = 1):
        # 0x18 dò bằng cách cho mục tiêu ra đủ xa đến mức tọa độ của nó không thay đổi nữa
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x4 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT) == idnhanvat and read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x18 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT) > 0 and read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x7E8 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT) >= 0

    def get_tennhanvat(self, idnhanvat = 1):
        return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xBC9 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_sinhluchientai(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x7FC + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_sinhluctoida(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x800 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_phantramkhanghoa(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x904 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_phantramkhanghoatoida(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x918 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_diempk(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xD5C + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_phantramsinhluchientai(self, idnhanvat = 1):
        sinhluctoida = self.get_sinhluctoida(idnhanvat)
        if not sinhluctoida:
            return 0
        return int(self.get_sinhluchientai(idnhanvat) * 100. / sinhluctoida)

    def get_toado(self, idnhanvat = 1):
        diachinhanvat = self.diachigame + OFFSET_DIACHICOSONHANVAT + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT
        toadoluoix = read_int(self.tientrinh, diachinhanvat + 0x0ACC)
        toadoluoiy = read_int(self.tientrinh, diachinhanvat + 0x0AD0)
        offsetx = read_int(self.tientrinh, diachinhanvat + 0x0AD8)
        offsety = read_int(self.tientrinh, diachinhanvat + 0x0ADC)

        idbando = read_int(self.tientrinh, diachinhanvat + 0x07E4)
        idkhuvuc = read_int(self.tientrinh, diachinhanvat + 0x07E8)

        diachibando = self.diachigame + 0x2CA3960 + 0x000 + (idbando * 172)
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
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x1028 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT),
            read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x102C + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)
        )

    def get_toadoclick(self):
        toadox, toadoy = self.get_toado()
        return (
            toadox + read_int(self.tientrinh, self.diachigame + 0x2AD2E4) - int(self.kichthuoccuasogame[0] / 2),
            toadoy + int(read_int(self.tientrinh, self.diachigame + 0x2AD2E8) - int(self.kichthuoccuasogame[1] / 2)) * 2
        )

    def get_tocdodichuyen(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x934 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_tocdoxuatchieuvukhi(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x948 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_tocdoxuatchieubuaphap(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x94C + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_is_nhanvatdachet(self, idnhanvat = 1):
        return self.get_idtrangthainhanvat(idnhanvat) == IDTRANGTHAINHANVAT_DACHET

    def get_idloainhanvat(self, idnhanvat = 1):
        return read_short_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x20 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_idtrangthainhanvat(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xB4 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_is_bidongbang(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x64 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT) > 0

    def get_idhephai(self, idnhanvat = 1):
        return read_short_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x21 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_idmaupk(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xAC + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_capdonhanvat(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x1C + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_tenchunhan(self, idnhanvat = 1):
        return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xBE9 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_tenbang(self, idnhanvat = 1):
        if self.get_idloainhanvat(idnhanvat) in (IDLOAINHANVAT_TRIEUHOITHU, 8):
            idchunhan = self.get_idchunhan(idnhanvat)
            if not idchunhan:
                return False
            return self.get_tenbang(idchunhan)
        return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xB75 + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_idtodoi(self, idnhanvat = 1):
        if self.get_idloainhanvat(idnhanvat) == IDLOAINHANVAT_TRIEUHOITHU:
            idchunhan = self.get_idchunhan(idnhanvat)
            if not idchunhan:
                return -1
            return self.get_idtodoi(idchunhan)
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xB2C + idnhanvat * OFFSET_DIACHICOSOMOINHANVAT)

    def get_idkynang(self, iddiachikynang):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSONHANVAT + 0xC0 + 0x24 * iddiachikynang + 1 * OFFSET_DIACHICOSOMOINHANVAT)

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

    def get_idchunhan(self, idnhanvat = 1):
        tenchunhan = self.get_tenchunhan(idnhanvat)
        if not tenchunhan:
            return -1
        idchunhan = self._idchunhan_map.get(tenchunhan, False)
        if idchunhan and self.get_tennhanvat(idchunhan) == tenchunhan and self.get_is_nhanvattontai(idchunhan):
            return idchunhan
        else:
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
            return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINTHANHVIENDOINHOM) == self.get_tennhanvat()
        return False

    def get_toadotruongnhom(self):
        if self.get_idtodoi() > 0:
            return (
                read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINTHANHVIENDOINHOM + 0x28),
                read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINTHANHVIENDOINHOM + 0x2C)
            )
        return -1, -1

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

    def get_capdovatpham(self, idvatpham):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x68 + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM)

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
        return read_short_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + 0x4EC + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM) * self.get_soluongvatpham(idvatpham)

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

    def get_idhephaivatpham(self, idvatpham):
        if idvatpham < 0 or idvatpham >= SOLUONGVATPHAMTOIDA:
            return -1

        for offset in range(5 * 0x14, 0xFE, 0x14):
            x = self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM + offset
            if read_int(self.tientrinh, x) == 0x25:
                return read_int(self.tientrinh, x + 4)
        return -1

    def get_is_vatphamduoidattontai(self, idvatphamduoidat):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAMDUOIDAT + 0xC + idvatphamduoidat * OFFSET_DIACHICOSOMOIVATPHAMDUOIDAT) == idvatphamduoidat

    def get_tenvatphamduoidat(self, idvatphamduoidat):
        return read_string(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAMDUOIDAT + 0x44 + idvatphamduoidat * OFFSET_DIACHICOSOMOIVATPHAMDUOIDAT)

    def get_tuchatvatphamduoidat(self, idvatphamduoidat):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAMDUOIDAT + 0x98 + idvatphamduoidat * OFFSET_DIACHICOSOMOIVATPHAMDUOIDAT)

    def get_is_thucuoiduoidat(self, idvatphamduoidat):
        return read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAMDUOIDAT + 0x170 + idvatphamduoidat * OFFSET_DIACHICOSOMOIVATPHAMDUOIDAT) == 38

    def get_khoangcachvatphamduoidat(self, idvatphamduoidat, default = 1000):
        x = read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAMDUOIDAT + 0x2AC + idvatphamduoidat * OFFSET_DIACHICOSOMOIVATPHAMDUOIDAT)
        y = read_int(self.tientrinh, self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAMDUOIDAT + 0x2B0 + idvatphamduoidat * OFFSET_DIACHICOSOMOIVATPHAMDUOIDAT)

        return round(math.dist(
            self.get_toado(),
            (x, y),
        ))

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

    def get_donghothoigian(self):
        return read_int(self.tientrinh, self.diachigame + 0x29E4328 + 0x000)

    def get_is_kynangsansang(self, idkynang):
        if not self.get_is_dahockynang(idkynang):
            return False

        thoidiemhoiphuckynang = self.get_thoidiemhoiphuckynang(idkynang)
        return not thoidiemhoiphuckynang or thoidiemhoiphuckynang < self.get_donghothoigian()

    def get_is_khuvuccothetancong(self):
        return read_int(self.tientrinh, self.diachigame + 0x29F0424 + 0x000) > 0

    def get_is_dangbatauto(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A47A8 + 0x000)

    def get_is_dangtudongtimduong(self):
        return read_int(self.tientrinh, self.diachigame + 0x49F0E4 + 0x000) > 0

    def set_is_dangtudongtimduong(self, is_dangtudongtimduong):
        if self.get_is_dangtudongtimduong() != is_dangtudongtimduong:
            write_int(self.tientrinh, self.diachigame + 0x49F0E4 + 0x000, 1 if is_dangtudongtimduong else 0)

    def get_idmauvatphamnhat(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A3EB4 + 0x000)

    def get_iddoituongtudanh(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A4530 + 0x000)

    def set_iddoituongtudanh(self, iddoituongtudanh):
        if self.get_iddoituongtudanh() != iddoituongtudanh:
            write_int(self.tientrinh, self.diachigame + 0x4A4530 + 0x000, iddoituongtudanh)

    def get_tennguoidanhtheosau(self):
        return read_string(self.tientrinh, self.diachigame + 0x4A3EC4 + 0x000)

    def get_khoangcachtheosau(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A3EE4 + 0x000)

    def get_is_theosau(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A3EC0 + 0x000)

    def set_is_theosau(self, is_theosau):
        if self.get_is_theosau() != is_theosau:
            write_int(self.tientrinh, self.diachigame + 0x4A3EC0 + 0x000, 1 if is_theosau else 0)

    def get_phamvitimkiemmuctieu(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A37F4 + 0x000)

    def get_idtrangthaiclickchuot(self):
        return read_int(self.tientrinh, self.diachigame + 0x2B2F84 + 0x000)

    def get_is_dangmocuahang(self):
        return read_int(self.tientrinh, self.diachigame + 0x2B2BEC + 0x000)

    def get_is_dangdoithoaixacnhan(self):
        return read_int(self.tientrinh, self.diachigame + 0x2B1170 + 0x000)

    def get_is_tamngungtancong(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A3788 + 0x000)

    def get_is_datrieuhoithu(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A47A4 + 0x000)

    def get_trongluongtoida(self):
        return read_int(self.tientrinh, self.diachigame + 0x4C3460 + 0x000)

    def get_is_duoitheo(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A4534 + 0x000) > 0

    def set_is_duoitheo(self, is_duoitheo):
        if self.get_is_duoitheo() != is_duoitheo:
            write_int(self.tientrinh, self.diachigame + 0x4A4534 + 0x000, 1 if is_duoitheo else 0)

    def get_is_tranhboss(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A3810 + 0x000) > 0

    def get_is_boss(self, idnhanvat = 1):
        return self.get_idloainhanvat(idnhanvat) == IDLOAINHANVAT_QUAIVAT and self.get_sinhluctoida(idnhanvat) >= 2000 * self.get_capdonhanvat(idnhanvat)

    def get_idkynang1(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A3814 + 0x000)

    def set_idkynang1(self, idkynang1):
        if self.get_idkynang1() != idkynang1:
            write_int(self.tientrinh, self.diachigame + 0x4A3814 + 0x000, idkynang1)

    def get_idkynanghotro4(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A3808 + 0x000)

    def set_idkynangbotro4(self, idkynangbotro):
        if self.get_idkynanghotro4() != idkynangbotro:
            write_int(self.tientrinh, self.diachigame + 0x4A3808 + 0x000, idkynangbotro)

    def get_is_dichuyenhoatdongquanhphamvi(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A4538 + 0x000) > 0

    def set_is_dichuyenhoatdongquanhphamvi(self, is_dichuyenhoatdongquanhphamvi):
        if self.get_is_dichuyenhoatdongquanhphamvi() != is_dichuyenhoatdongquanhphamvi:
            write_int(self.tientrinh, self.diachigame + 0x4A4538 + 0x000, 1 if is_dichuyenhoatdongquanhphamvi else 0)

    def get_is_dangkhoa(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A48B4 + 0x000) > 0

    def get_idbandohientai(self):
        return read_int(self.tientrinh, self.diachigame + 0x29AAC54 + 0x000)

    def get_tenbandohientai(self):
        return read_string(self.tientrinh, self.diachigame + 0x29AAC04 + 0x000)

    def get_is_tudongnhatvatpham(self):
        return read_int(self.tientrinh, self.diachigame + 0x4A3EAC + 0x000)

    def get_idmuctieudangchichuot(self):
        return read_int(self.tientrinh, self.diachigame + 0x49F0A8 + 0x000)

    def get_idmuctieudangchon(self):
        # Tìm theo hàm vô hiệu hóa
        return read_int(self.tientrinh, self.diachigame + 0x4A48C8 + 0x000)

    def set_idmuctieudangchon(self, idmuctieudangchon):
        if self.get_idmuctieudangchon() != idmuctieudangchon:
            write_int(self.tientrinh, self.diachigame + 0x4A48C8 + 0x000, idmuctieudangchon)

    def get_idmuctieutancong(self):
        #Tìm theo hàm vô hiệu hóa
        return read_int(self.tientrinh, self.diachigame + 0x4A382C + 0x000)

    def set_idmuctieutancong(self, idmuctieutancong):
        if self.get_idmuctieutancong() != idmuctieutancong:
            write_int(self.tientrinh, self.diachigame + 0x4A382C + 0x000, idmuctieutancong)

    def get_idmuctieudangkhoa(self):
        return read_int(self.tientrinh, self.diachigame + 0x4C36C4 + 0x000)

    def set_idmuctieudangkhoa(self, idmuctieudangkhoa):
        if self.get_idmuctieudangkhoa() != idmuctieudangkhoa:
            write_int(self.tientrinh, self.diachigame + 0x4C36C4 + 0x000, idmuctieudangkhoa)

    def set_idmuctieu(self, idnhanvat):
        self.set_idmuctieudangchon(idnhanvat)
        self.set_idmuctieutancong(idnhanvat)

        idmuctieudangkhoa = self.get_idmuctieudangkhoa()
        if idmuctieudangkhoa and idmuctieudangkhoa != idnhanvat:
            self.set_idmuctieudangkhoa(0)

    def get_idnhanvattieptheo(self, idnhanvat = 1):
        diachicosonhanvattieptheo = read_int(self.tientrinh, self.diachigame + 0x2A08E08 + 0x000)
        idnhanvattieptheo = read_int(self.tientrinh, diachicosonhanvattieptheo + 0x4 + 0x8 * idnhanvat)
        if idnhanvattieptheo > SOLUONGNHANVATTOIDA or idnhanvattieptheo < 0:
            return -1
        return idnhanvattieptheo

    def action_vohieuhoagiamxuatchieukhithaydo(self):
        diachixuatchieuvukhi = self.diachigame + OFFSET_DIACHICOSONHANVAT + OFFSET_DIACHICOSOMOINHANVAT + 0x948
        diachixuatchieubuaphap = self.diachigame + OFFSET_DIACHICOSONHANVAT + OFFSET_DIACHICOSOMOINHANVAT + 0x94C

        if read_int(self.tientrinh, self.diachigame + 0x128005 + 0x2) != diachixuatchieuvukhi:
            write_int(self.tientrinh, self.diachigame + 0x128005 + 0x2, diachixuatchieuvukhi)

        if read_int(self.tientrinh, self.diachigame + 0x128011 + 0x2) != diachixuatchieubuaphap:
            write_int(self.tientrinh, self.diachigame + 0x128011 + 0x2, diachixuatchieubuaphap)

    def action_vohieuhoathietlapmuctieudangchon(self):
        if read_bytes(self.tientrinh, self.diachigame + 0x1ABA87, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x1ABA87, bytes.fromhex("90 90 90909090"), 6)

        if read_bytes(self.tientrinh, self.diachigame + 0x11908F, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x11908F, bytes.fromhex("90 90 90909090 90909090"), 10)

    def action_tatvohieuhoathietlapmuctieudangchon(self):
        if read_bytes(self.tientrinh, self.diachigame + 0x1ABA87, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x1ABA87, bytes.fromhex("89 0D"), 2)
            write_int(self.tientrinh, self.diachigame + 0x1ABA87 + 0x2, self.diachigame + 0x4A48C8 + 0x000)

        if read_bytes(self.tientrinh, self.diachigame + 0x11908F, 1) != bytes.fromhex("C7"):
            write_bytes(self.tientrinh, self.diachigame + 0x11908F, bytes.fromhex("C7 05"), 10)
            write_int(self.tientrinh, self.diachigame + 0x11908F + 0x2, self.diachigame + 0x4A48C8 + 0x000)
            write_int(self.tientrinh, self.diachigame + 0x11908F + 0x6, 0)

    def action_vohieuhoathietlapmuctieutancong(self):
        if read_bytes(self.tientrinh, self.diachigame + 0x1AC21D, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AC21D, bytes.fromhex("90 90 90909090"), 6)

        if read_bytes(self.tientrinh, self.diachigame + 0x1AC719, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AC719, bytes.fromhex("90 90 90909090"), 6)

        # Lúc theo sau
        if read_bytes(self.tientrinh, self.diachigame + 0x1AB734, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AB734, bytes.fromhex("90 90 90909090"), 6)

        # Lúc ngoài phạm vi điểm di chuyển xunh quanh
        if read_bytes(self.tientrinh, self.diachigame + 0x1AB70A, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AB70A, bytes.fromhex("90 90 90909090"), 6)
        if read_bytes(self.tientrinh, self.diachigame + 0x1AC743, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AC743, bytes.fromhex("90 90 90909090"), 6)

    def action_tatvohieuhoathietlapmuctieutancong(self):
        if read_bytes(self.tientrinh, self.diachigame + 0x1AC21D, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AC21D, bytes.fromhex("89 AE AC000000"), 6)

        if read_bytes(self.tientrinh, self.diachigame + 0x1AC719, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AC719, bytes.fromhex("89 BE AC000000"), 6)

        # Lúc theo sau
        if read_bytes(self.tientrinh, self.diachigame + 0x1AB734, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AB734, bytes.fromhex("89 AE AC000000"), 6)

        # Lúc ngoài phạm vi điểm di chuyển xunh quanh
        if read_bytes(self.tientrinh, self.diachigame + 0x1AB70A, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AB70A, bytes.fromhex("89 AE AC000000"), 6)
        if read_bytes(self.tientrinh, self.diachigame + 0x1AC743, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x1AC743, bytes.fromhex("89 AE AC000000"), 6)

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

            mov ecx, {hex(self.diachigame + 0x49F090 + 0x000)}
            push ebx

            mov ebp, {hex(self.diachigame + 0x122530)}
            call ebp

            ret
        """
        encoding, _ = ks.asm(asm_code)
        self.tientrinh.write_bytes(self.diachihamsudungvatpham, bytes(encoding), len(encoding))

    def action_sudungvatpham(self, idvatpham, vitrix, vitriy, delay = 0.25):
        if not self.diachihamsudungvatpham:
            self.khoitaohamsudungvatpham()

        if time.time() - self._thoidiemsudungvatphamgannhat < delay:
            return False

        self._thoidiemsudungvatphamgannhat = time.time()

        diachidulieu = self.diachihamsudungvatpham + 0x40
        write_int(self.tientrinh, diachidulieu, idvatpham)
        write_int(self.tientrinh, diachidulieu + 0x4, vitrix)
        write_int(self.tientrinh, diachidulieu + 0x8, vitriy)
        self.tientrinh.start_thread(self.diachihamsudungvatpham)
        return True

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

            mov ecx, {hex(self.diachigame + 0x49F090 + 0x000)}

            mov eax, {hex(self.diachigame + 0x11FB10)}
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

    def khoitaohamtudongtimduongxuyenbando(self):
        if self.diachihamtudongtimduongxuyenbando:
            return

        self.diachihamtudongtimduongxuyenbando = self.tientrinh.allocate(256)

        diachidulieu = self.diachihamtudongtimduongxuyenbando + 0x40
        write_bytes(self.tientrinh, diachidulieu + 16, b"\x00" * 4, 4)
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov ecx, {self.diachigame + 0x2B2E88 + 0x000}

            push dword ptr [{diachidulieu}]
            push {diachidulieu + 16}
            push dword ptr [{diachidulieu + 8}]
            push dword ptr [{diachidulieu + 4}]
            push dword ptr [{diachidulieu + 12}]

            mov eax, {self.diachigame + 0x119F30}
            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)

        write_bytes(self.tientrinh, self.diachihamtudongtimduongxuyenbando, bytes(encoding), len(encoding))

    def action_tudongtimduongxuyenbando(self, idbando, toadox, toadoy, tennpc = "", mode = IDCHEDOTIMDUONG_CHUYENTIEP_HOITHANH, delay = 1.0):
        if not self.diachihamtudongtimduongxuyenbando:
            self.khoitaohamtudongtimduongxuyenbando()

        if time.time() - self._thoidiemtudongtimduongxuyenbandogannhat < delay:
            return False

        self._thoidiemtudongtimduongxuyenbandogannhat = time.time()

        diachidulieu = self.diachihamtudongtimduongxuyenbando + 0x40

        write_int(self.tientrinh, diachidulieu, mode)
        write_int(self.tientrinh, diachidulieu + 4, int(round(toadox / 32)))
        write_int(self.tientrinh, diachidulieu + 8, int(round(toadoy / 32)))
        write_int(self.tientrinh, diachidulieu + 12, idbando)

        if tennpc:
            npc_bytes = Unicode_to_TCVN3(tennpc)
            npc_bytes = npc_bytes[:63] + b"\x00"
            write_bytes(self.tientrinh, diachidulieu + 16, npc_bytes, len(npc_bytes))
        else:
            write_bytes(self.tientrinh, diachidulieu + 16, b"\x00", 1)

        self.tientrinh.start_thread(self.diachihamtudongtimduongxuyenbando)
        return True

    def khoitaohamdichuyen(self):
        if self.diachihamdichuyen: return
        self.diachihamdichuyen = self.tientrinh.allocate(256)

        diachidulieu = self.diachihamdichuyen + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov esi, {hex(self.diachigame + OFFSET_DIACHICOSONHANVAT + OFFSET_DIACHICOSOMOINHANVAT)}
            mov edi, dword ptr [{diachidulieu}]
            mov edx, dword ptr [{diachidulieu + 4}]
            mov ebx, 0

            push ebx
            push edx
            push edi
            
            mov ecx, esi
            mov eax, {hex(self.diachigame + 0x12C8E0)}
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

        x1, y1 = self.get_toado()
        x2, y2 = self.get_toado(idnhanvat2)

        D = math.dist((x1, y1), (x2, y2))

        if D > khoangcachtoithieu:
            tile = khoangcachtoithieu / D

            xmoi = int(x2 - tile * (x2 - x1))
            ymoi = int(y2 - tile * (y2 - y1))

            return self.action_dichuyen(xmoi, ymoi, delay = delay)

        return False

    def action_dichuyengiukhoangcachtoithieudiem(self, toadox, toadoy, khoangcachtoithieu, delay = 0.25):
        if time.time() - self._thoidiemdichuyengiukhoangcachtoithieu < delay:
            return False

        self._thoidiemdichuyengiukhoangcachtoithieu = time.time()

        x1, y1 = self.get_toado()
        x2 = toadox
        y2 = toadoy

        D = math.dist((x1, y1), (x2, y2))

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
            mov eax, {hex(self.diachigame + 0x192D10)}
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

        self._thoidiemsuavatphamgannhat = time.time()

        if read_int(self.tientrinh, self.diachigame + 0x2CA3518 + 0x000 + 0x4) == 0:
            return False

        dobenhientai = self.get_dobenhientaivatpham(idvatpham)
        dobentoida = self.get_dobentoidavatpham(idvatpham)

        if dobentoida == -1 or dobenhientai >= dobentoida or dobenhientai < 0:
            return False

        diachicosothongtinvatpham = self.diachigame + OFFSET_DIACHICOSOTHONGTINVATPHAM + idvatpham * OFFSET_DIACHICOSOMOIVATPHAM
        val_param = read_int(self.tientrinh, diachicosothongtinvatpham + 0x10C)
        global_factor = read_int(self.tientrinh, self.diachigame + 0x2CA3518 + 0x000)

        product = (val_param * global_factor) * 0x51EB851F
        edx_val = (product >> 32) & 0xFFFFFFFF
        if edx_val & 0x80000000: edx_val -= 0x100000000

        scaled_unit = (edx_val >> 5) + ((edx_val >> 5 >> 31) & 1)
        final_price = (scaled_unit * (dobentoida - dobenhientai)) // dobentoida

        factor_addr = self.diachigame + (0x2CA3518 + 0x000 + 0x10 if dobenhientai == 0 else 0x2CA3518 + 0x000 + 0xC)
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
        if self.diachihambattathieuungbotro:
            return
        self.diachihambattathieuungbotro = self.tientrinh.allocate(256)

        diachidulieu = self.diachihambattathieuungbotro + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov edx, dword ptr [{hex(diachidulieu)}]
            mov ecx, 00000000

            push ecx
            push edx
            mov eax, {hex(self.diachigame + 0x192E40)}
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

    def khoitaohamboquamuctieumaucao(self):
        if self.diachihamboquamuctieumaucao:
            return
        self.diachihamboquamuctieumaucao = self.tientrinh.allocate(256)

        diachidulieu = self.diachihamboquamuctieumaucao + 0x40
        write_int(self.tientrinh, diachidulieu, 0)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        offset_capdo = self.diachigame + OFFSET_DIACHICOSONHANVAT + 0x1C

        asm_code = f"""
            cmp [eax+{hex(self.diachigame + 0x4BA7C0 + 0x800 + 0x000)}], ebp
            jng {hex(self.diachigame + 0x1AB734)}

            cmp dword ptr [{hex(diachidulieu)}], 1
            jne boqualogicboquamuctieumaucao

            mov ecx, dword ptr [eax+{hex(offset_capdo)}]
            imul ecx, ecx, 2000
            cmp [eax+{hex(self.diachigame + 0x4BA7C0 + 0x800 + 0x000)}], ecx
            jnl {hex(self.diachigame + 0x1AB734)}

            boqualogicboquamuctieumaucao:
            jmp {hex(self.diachigame + 0x1AB52C + 0xC)}
        """

        encoding, _ = ks.asm(asm_code, addr = self.diachihamboquamuctieumaucao)
        write_bytes(self.tientrinh, self.diachihamboquamuctieumaucao, bytes(encoding), len(encoding))
        write_bytes(self.tientrinh, self.diachigame + 0x1AB52C, b"\xE9" + (self.diachihamboquamuctieumaucao - (self.diachigame + 0x1AB52C) - 5).to_bytes(4, byteorder = sys.byteorder, signed = True) + (b"\x90" * 7), 12)

    def action_thietlapboquamuctieumaucao(self, is_boquamuctieumaucao: bool, delay = 0.5):
        if not self.diachihamboquamuctieumaucao:
            self.khoitaohamboquamuctieumaucao()

        if time.time() - self._thoidiemboquamuctieumaucaogannhat < delay:
            return False

        self._thoidiemboquamuctieumaucaogannhat = time.time()

        diachidulieu = self.diachihamboquamuctieumaucao + 0x40
        trangthaihientai = read_int(self.tientrinh, diachidulieu)
        trangthaimoi = 1 if is_boquamuctieumaucao else 0

        if trangthaihientai != trangthaimoi:
            write_int(self.tientrinh, diachidulieu, trangthaimoi)

        return True

    def khoitaohamnhatvatpham(self):
        if self.diachihamnhatvatpham:
            return

        self.diachihamnhatvatpham = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov ecx, dword ptr [{self.diachihamnhatvatpham + 0x40}]
            push ecx
            mov esi, {self.diachigame + 0x49F090 + 0x000}
            mov ecx,esi
            mov eax, {self.diachigame + 0x122690}
            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamnhatvatpham, bytes(encoding), len(encoding))

    def action_nhatvatpham(self, idvatphamduoidat, delay = 0.02):
        if not self.diachihamnhatvatpham:
            self.khoitaohamnhatvatpham()

        if time.time() - self._thoidiemnhatvatphamgannhat < delay:
            return False

        self._thoidiemnhatvatphamgannhat = time.time()

        diachidulieu = self.diachihamnhatvatpham + 0x40
        write_int(self.tientrinh, diachidulieu, idvatphamduoidat)

        self.tientrinh.start_thread(self.diachihamnhatvatpham)
        return True

    def khoitaohamdoimaupk(self):
        if self.diachihamdoimaupk:
            return
        self.diachihamdoimaupk = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov eax, dword ptr [{self.diachihamdoimaupk + 0x40}]
            push eax
            mov ecx, {hex(self.diachigame + 0x4A3728)}
            mov edx, {hex(self.diachigame + 0x1BAE80)}
            call edx
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdoimaupk, bytes(encoding), len(encoding))

    def action_doimaupk(self, idmaupk):
        if not self.diachihamdoimaupk:
            self.khoitaohamdoimaupk()

        diachidulieu = self.diachihamdoimaupk + 0x40
        write_int(self.tientrinh, diachidulieu, idmaupk - 8)

        self.tientrinh.start_thread(self.diachihamdoimaupk)
        return True

    def khoitaohammokhoa(self):
        if self.diachihammokhoa:
            return
        self.diachihammokhoa = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        diachidulieu = self.diachihammokhoa + 0x40

        asm_code = f"""
            push {hex(diachidulieu)}
            push 03
            mov ecx, {hex(self.diachigame + 0x49F090 + 0x000)}
            mov eax, {hex(self.diachigame + 0x1206F0)}
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
        self.diachihamsudungkynangtoado = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamsudungkynangtoado + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            push dword ptr [{hex(diachidulieu + 8)}]
            push dword ptr [{hex(diachidulieu + 4)}]
            push dword ptr [{hex(diachidulieu)}]
            mov ecx, {hex(self.diachigame + OFFSET_DIACHICOSONHANVAT + OFFSET_DIACHICOSOMOINHANVAT)}
            mov eax, {hex(self.diachigame + 0x12CB20)}
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

    def khoitaohamsudungphimtat(self):
        if self.diachihamsudungphimtat:
            return

        self.diachihamsudungphimtat = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamsudungphimtat + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov eax, dword ptr [{hex(diachidulieu)}]
            mov ebx, 0x32
            mov edx, eax
            push edx
            push {hex(1)}
            push edx

            mov ecx, {hex(self.diachigame + 0xB90D0)}
            call ecx

            add esp, 0x0C
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamsudungphimtat, bytes(encoding), len(encoding))

    def action_sudungphimtat(self, vitriphimtat, delay = 0.5):
        if not self.diachihamsudungphimtat:
            self.khoitaohamsudungphimtat()

        if time.time() - self._thoidiemsudungphimtatgannhat < delay:
            return False

        self._thoidiemsudungphimtatgannhat = time.time()

        diachidulieu = self.diachihamsudungphimtat + 0x40

        write_int(self.tientrinh, diachidulieu, vitriphimtat - 1)

        self.tientrinh.start_thread(self.diachihamsudungphimtat)

        return True

    def khoitaohambanvatpham(self):
        if self.diachihambanvatpham: return
        self.diachihambanvatpham = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov ebx, dword ptr [{self.diachihambanvatpham + 0x40}]
            mov ecx, dword ptr [{self.diachihambanvatpham + 0x40 + 0x4}]
            mov edx, dword ptr [{self.diachihambanvatpham + 0x40 + 0x8}]
            push edx
            mov eax, {self.diachigame + 0x192E90}
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

    def khoitaohamdoithoai(self):
        if self.diachihamdoithoai: return
        self.diachihamdoithoai = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov ebx, dword ptr [{self.diachihamdoithoai + 0x40}]
            push ebx
            mov ecx, {self.diachigame + 0x49F090 + 0x000} 
            mov eax, {self.diachigame + 0x1219E0} 
            call eax
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamdoithoai, bytes(encoding), len(encoding))

    def action_doithoai(self, idnhanvat, delay = 0.5):
        print("action_doithoai")
        if not self.diachihamdoithoai:
            self.khoitaohamdoithoai()

        if idnhanvat <= 0:
            return False

        if time.time() - self._thoidiemdoithoaigannhat < delay:
            return False

        self._thoidiemdoithoaigannhat = time.time()

        diachidulieu = self.diachihamdoithoai + 0x40
        write_int(self.tientrinh, diachidulieu, idnhanvat)
        self.tientrinh.start_thread(self.diachihamdoithoai)
        return True

    def khoitaohamxacnhandoithoai(self):
        if self.diachihamxacnhandoithoai: return
        self.diachihamxacnhandoithoai = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            push 01
            mov ebx, {hex(self.diachigame + 0x756E0)}
            call ebx
            add esp, 04

            push 00
            push 00
            push 0x0A
            mov edx, dword ptr [{hex(self.diachigame + 0x2B2E88 + 0x000)}]
            mov eax, dword ptr [edx]
            mov ecx, dword ptr [{hex(self.diachigame + 0x2B2E88 + 0x000)}]
            mov edx, dword ptr [eax + 0x04]
            call edx
            ret
        """
        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamxacnhandoithoai, bytes(encoding), len(encoding))

    def action_xacnhandoithoai(self, delay = 0.25):
        print("action_xacnhandoithoai")
        if not self.diachihamxacnhandoithoai:
            self.khoitaohamxacnhandoithoai()

        if time.time() - self._thoidiemxacnhandoithoaigannhat < delay:
            return False

        self._thoidiemxacnhandoithoaigannhat = time.time()
        self.tientrinh.start_thread(self.diachihamxacnhandoithoai)
        return True

    def khoitaohamdongcuahang(self):
        #Dò bằng cách xem hàm nào sửa cái Is đang mở cửa hàng về 0
        if self.diachihamdongcuahang:
            return
        self.diachihamdongcuahang = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov eax, {self.diachigame + 0xF0770}
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

        self._thoidiemdongcuahanggannhat = time.time()

        self.tientrinh.start_thread(self.diachihamdongcuahang)
        return True
