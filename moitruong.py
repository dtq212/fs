import ctypes

import pymem
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

from hangso import *
from tienich import *


class MoiTruong:
    def __init__(self, idcuaso):
        self._thoidiemnhanloimoitodoigannhat = 0.
        self._thoidiemmoitodoigannhat = 0.
        self.diachihammoitodoi = 0
        self.diachihamnhanloimoitodoi = 0
        self._thoidiemphucsinhgannhat = 0.
        self.diachihamphucsinh = 0
        self.diachihamsudungkynangtoado2 = 0
        self._thoidiemboquabossgannhat = 0.
        self._thoidiemvohieuhoakynangbotro3gannhat = 0.
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
        #
        self.offsetdiachicosothongtinvatphamduoidat = 0
        self.offsetdiachicosomoivatphamduoidat = 0

        # Inspect từ Tọa độ X, Y của thành viên thay đổi
        self.offsetdiachicosothongtinthanhviendoinhom = 0
        self.offsetdiachicosomoithanhviendoinhom = 0

        # #1 biến nào đó mà + FE0 thì phải đấy
        self.offsetdiachicosonhanvattieptheo = 0

        self.diachihambanvatpham = 0
        self.diachihamsudungvatpham = 0
        self.diachihamtudongtimduong = 0
        self.diachihamtudongtimduongxuyenbando = 0
        self.diachihamdichuyen = 0
        self.diachihamsuavatpham = 0
        self.diachihambattathieuungbotro = 0
        self.diachihamnhatvatpham = 0
        self.diachihamsudungphimtat = 0
        self.diachihamvohieuhoakynangbotro3 = 0
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
        self.offsetdiachidongho = 0
        self.offsetdiachiidbandohientai = 0
        self.offsetdiachitenbandohientai = 0

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
            "diachihamtudongtimduongxuyenbando",
            "diachihamdichuyen",
            "diachihambattathieuungbotro",
            "diachihamnhatvatpham",
            "diachihamdoimaupk",
            "diachihammokhoa",
            "diachihamsudungphimtat",

            "diachihamdongcuahang",
            "diachihamdoithoai",
            "diachihamxacnhandoithoai",
            "diachihamvohieuhoakynangbotro3",
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

    def get_toadoclick(self):
        toadox, toadoy = self.get_toado()
        return (
            toadox + read_int(self.tientrinh, self.diachigame + 0x260F44) - int(self.kichthuoccuasogame[0] / 2),
            toadoy + int(read_int(self.tientrinh, self.diachigame + 0x260F48) - int(self.kichthuoccuasogame[1] / 2)) * 2
        )

    def get_tocdodichuyen(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x934 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_trihoanxuatchieuvukhi(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x948 + idnhanvat * self.offsetdiachicosomoinhanvat)

    def get_trihoanxuatchieubuaphap(self, idnhanvat = 1):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x94C + idnhanvat * self.offsetdiachicosomoinhanvat)

    def set_trihoanxuatchieubuaphap(self, trihoanxuatchieubuaphap, idnhanvat = 1):
        if trihoanxuatchieubuaphap != self.get_trihoanxuatchieubuaphap(idnhanvat):
            return write_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + 0x94C + idnhanvat * self.offsetdiachicosomoinhanvat, trihoanxuatchieubuaphap)

    def get_is_nhanvatdachet(self, idnhanvat = 1):
        return self.get_idtrangthainhanvat(idnhanvat) == IDTRANGTHAINHANVAT_DACHET

    def get_idloainhanvat(self, idnhanvat = 1):
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
        if self.get_idloainhanvat(idnhanvat) == IDLOAINHANVAT_TRIEUHOITHU:
            idchunhan = self.get_idchunhan(idnhanvat)
            if not idchunhan:
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
        if idnhanvat <= 1 or not self.get_is_nhanvattontai(idnhanvat) or self.get_is_nhanvatdachet( idnhanvat) or self.get_sinhluctoida(idnhanvat) <= 0:
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
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + sothutuvatpham * self.offsetdiachicosovitrimoivatpham), # ID vật phẩm
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + 0x4 + sothutuvatpham * self.offsetdiachicosovitrimoivatpham), # Vị trí rương
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + 0x8 + sothutuvatpham * self.offsetdiachicosovitrimoivatpham), # Vị trí X
            read_int(self.tientrinh, self.diachigame + self.offsetdiachicosovitrivatpham + 0xC + sothutuvatpham * self.offsetdiachicosovitrimoivatpham), # Vị trí Y
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

    def get_dbidvatphamduoidat(self, idvatphamduoidat):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatphamduoidat + idvatphamduoidat * self.offsetdiachicosomoivatphamduoidat)

    def get_is_vatphamduoidattontai(self, idvatphamduoidat):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatphamduoidat + 0xC + idvatphamduoidat * self.offsetdiachicosomoivatphamduoidat) == idvatphamduoidat

    def get_tenvatphamduoidat(self, idvatphamduoidat):
        return read_string(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatphamduoidat + 0x44 + idvatphamduoidat * self.offsetdiachicosomoivatphamduoidat)

    def get_tuchatvatphamduoidat(self, idvatphamduoidat):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatphamduoidat + 0x98 + idvatphamduoidat * self.offsetdiachicosomoivatphamduoidat)

    def get_is_thucuoiduoidat(self, idvatphamduoidat):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatphamduoidat + 0x170 + idvatphamduoidat * self.offsetdiachicosomoivatphamduoidat) == 38

    def get_khoangcachvatphamduoidat(self, idvatphamduoidat, default = 1000):
        x = read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatphamduoidat + 0x2AC + idvatphamduoidat * self.offsetdiachicosomoivatphamduoidat)
        y = read_int(self.tientrinh, self.diachigame + self.offsetdiachicosothongtinvatphamduoidat + 0x2B0 + idvatphamduoidat * self.offsetdiachicosomoivatphamduoidat)

        return round(math.dist(self.get_toado(), (x, y),))

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
        #game.g_SubWorldSet
        if not self.offsetdiachidongho:
            return 0
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachidongho)

    def get_is_khuvuccothetancong(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachidongho + 0x8 + 0xC0F4) > 0

    def get_idbandohientai(self):
        if not self.offsetdiachiidbandohientai:
            return -1
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachiidbandohientai)

    def get_tenbandohientai(self):
        if not self.offsetdiachitenbandohientai:
            return ""
        return read_string(self.tientrinh, self.diachigame + self.offsetdiachitenbandohientai)

    def get_is_dangbatauto(self):
        return read_int(self.tientrinh, self.diachigame + 0x458498)

    def get_is_dangtudongtimduong(self):
        return read_int(self.tientrinh, self.diachigame + 0x452DBC) > 0

    def set_is_dangtudongtimduong(self, is_dangtudongtimduong):
        if self.get_is_dangtudongtimduong() != is_dangtudongtimduong:
            write_int(self.tientrinh, self.diachigame + 0x452DBC, 1 if is_dangtudongtimduong else 0)

    def get_idmauvatphamnhat(self):
        return read_int(self.tientrinh, self.diachigame + 0x457B84)

    def get_phantramsinhluchoiphuc(self):
        return read_int(self.tientrinh, self.diachigame + 0x457474)

    def get_phantramnoiluchoiphuc(self):
        return read_int(self.tientrinh, self.diachigame + 0x457478)

    def get_iddoituongtudanh(self):
        return read_int(self.tientrinh, self.diachigame + 0x458200)

    def set_iddoituongtudanh(self, iddoituongtudanh):
        if self.get_iddoituongtudanh() != iddoituongtudanh:
            write_int(self.tientrinh, self.diachigame + 0x458200, iddoituongtudanh)

    def get_tennguoidanhtheosau(self):
        return read_string(self.tientrinh, self.diachigame + 0x457B94)

    def get_khoangcachtheosau(self):
        return read_int(self.tientrinh, self.diachigame + 0x457BB4)

    def get_idtabkytrancac(self):
        return read_int(self.tientrinh, self.diachigame + 0x456118)

    def get_is_theosau(self):
        return read_int(self.tientrinh, self.diachigame + 0x457B90)

    def set_is_theosau(self, is_theosau):
        if self.get_is_theosau() != is_theosau:
            write_int(self.tientrinh, self.diachigame + 0x457B90, 1 if is_theosau else 0)

    def get_phamvitimkiemmuctieu(self):
        return read_int(self.tientrinh, self.diachigame + 0x4574C4)

    def get_idtrangthaiclickchuot(self):
        return read_int(self.tientrinh, self.diachigame + 0x266BE4)

    def get_is_dangmocuahang(self):
        return read_int(self.tientrinh, self.diachigame + 0x26684C) > 0

    def get_is_dangdoithoaixacnhan(self):
        return read_int(self.tientrinh, self.diachigame + 0x263E3C) > 0

    def get_is_tamngungtancong(self):
        return read_int(self.tientrinh, self.diachigame + 0x457458)

    def set_is_tamngungtancong(self, is_tamngungtancong):
        if self.get_is_tamngungtancong() != is_tamngungtancong:
            write_int(self.tientrinh, self.diachigame + 0x457458, 1 if is_tamngungtancong else 0)

    def get_is_datrieuhoithu(self):
        return read_int(self.tientrinh, self.diachigame + 0x458494)

    def get_is_duoitheo(self):
        return read_int(self.tientrinh, self.diachigame + 0x458204) > 0

    def set_is_duoitheo(self, is_duoitheo):
        if self.get_is_duoitheo() != is_duoitheo:
            write_int(self.tientrinh, self.diachigame + 0x458204, 1 if is_duoitheo else 0)

    def get_is_tranhboss(self):
        return read_int(self.tientrinh, self.diachigame + 0x4574E0) > 0

    def get_is_boss(self, idnhanvat = 1):
        if self.get_idloainhanvat(idnhanvat) != IDLOAINHANVAT_QUAIVAT:
            return
        capdonhanvat = self.get_capdonhanvat(idnhanvat)
        sinhluctoida = self.get_sinhluctoida(idnhanvat)
        if capdonhanvat <= 55:
            return sinhluctoida >= 2000 * capdonhanvat
        elif capdonhanvat <= 75:
            return sinhluctoida > 50_000
        elif capdonhanvat <= 75:
            return sinhluctoida > 100_000

    def get_is_quaixanh(self, idnhanvat = 1):
        return self.get_idloainhanvat(idnhanvat) == IDLOAINHANVAT_QUAIVAT and self.get_tocdodichuyen(idnhanvat) > TOCDODICHUYENQUAITHUONG

    def get_idkynangtaytrai(self):
        return read_int(self.tientrinh, self.diachigame + 0x452D68)

    def get_idkynang1(self):
        return read_int(self.tientrinh, self.diachigame + 0x4574E4)

    def set_idkynang1(self, idkynang1):
        if self.get_idkynang1() != idkynang1:
            write_int(self.tientrinh, self.diachigame + 0x4574E4, idkynang1)

    def get_idkynanghotro1(self):
        return read_int(self.tientrinh, self.diachigame + 0x4574CC)

    def set_idkynangbotro1(self, idkynangbotro):
        if self.get_idkynanghotro1() != idkynangbotro:
            write_int(self.tientrinh, self.diachigame + 0x4574CC, idkynangbotro)

    def get_idkynanghotro2(self):
        return read_int(self.tientrinh, self.diachigame + 0x4574D0)

    def set_idkynangbotro2(self, idkynangbotro):
        if self.get_idkynanghotro2() != idkynangbotro:
            write_int(self.tientrinh, self.diachigame + 0x4574D0, idkynangbotro)

    def get_idkynanghotro3(self):
        return read_int(self.tientrinh, self.diachigame + 0x4574D4)

    def set_idkynangbotro3(self, idkynangbotro):
        if self.get_idkynanghotro3() != idkynangbotro:
            write_int(self.tientrinh, self.diachigame + 0x4574D4, idkynangbotro)

    def get_idkynanghotro4(self):
        return read_int(self.tientrinh, self.diachigame + 0x4574D8)

    def set_idkynangbotro4(self, idkynangbotro):
        if self.get_idkynanghotro4() != idkynangbotro:
            write_int(self.tientrinh, self.diachigame + 0x4574D8, idkynangbotro)

    def get_is_tudongphucsinh(self):
        return read_int(self.tientrinh, self.diachigame + 0x458490)

    def get_is_dichuyenhoatdongquanhphamvi(self):
        return read_int(self.tientrinh, self.diachigame + 0x458228) > 0

    def set_is_dichuyenhoatdongquanhphamvi(self, is_dichuyenhoatdongquanhphamvi):
        if self.get_is_dichuyenhoatdongquanhphamvi() != is_dichuyenhoatdongquanhphamvi:
            write_int(self.tientrinh, self.diachigame + 0x458228, 1 if is_dichuyenhoatdongquanhphamvi else 0)

    def get_is_dangkhoa(self):
        return read_int(self.tientrinh, self.diachigame + 0x4585A4) > 0

    def get_is_tudongnhatvatpham(self):
        return read_int(self.tientrinh, self.diachigame + 0x457B7C)

    def get_idmuctieudangchichuot(self):
        return read_int(self.tientrinh, self.diachigame + 0x452D80)

    def get_idmuctieudangkhoa(self):
        return read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat + 0xC70)

    def set_idmuctieudangkhoa(self, idmuctieudangkhoa):
        if self.get_idmuctieudangkhoa() != idmuctieudangkhoa:
            write_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat + 0xC70, idmuctieudangkhoa)

    def get_idmuctieudangchon(self):
        # Tìm theo hàm vô hiệu hóa
        return read_int(self.tientrinh, self.diachigame + 0x4585B8)

    def set_idmuctieudangchon(self, idmuctieudangchon):
        if self.get_idmuctieudangchon() != idmuctieudangchon:
            write_int(self.tientrinh, self.diachigame + 0x4585B8, idmuctieudangchon)

    def get_idmuctieutancong(self):
        # Tìm theo hàm vô hiệu hóa
        return read_int(self.tientrinh, self.diachigame + 0x4574FC)

    def set_idmuctieutancong(self, idmuctieutancong):
        if self.get_idmuctieutancong() != idmuctieutancong:
            write_int(self.tientrinh, self.diachigame + 0x4574FC, idmuctieutancong)

    def set_idmuctieu(self, idnhanvat):
        self.set_idmuctieudangchon(idnhanvat)
        self.set_idmuctieutancong(idnhanvat)

        idmuctieudangkhoa = self.get_idmuctieudangkhoa()
        if idmuctieudangkhoa and idmuctieudangkhoa != idnhanvat:
            self.set_idmuctieudangkhoa(0)

    def get_idnhanvattieptheo(self, idnhanvat = 1):
        diachicosonhanvattieptheo = read_int(self.tientrinh, self.diachigame + self.offsetdiachicosonhanvattieptheo) #1 biến nào đó mà + FE0 thì phải đấy
        idnhanvattieptheo = read_int(self.tientrinh, diachicosonhanvattieptheo + 0x4 + 0x8 * idnhanvat)
        if idnhanvattieptheo > SOLUONGNHANVATTOIDA or idnhanvattieptheo < 0:
            return -1
        return idnhanvattieptheo

    def action_tatvohieuhoapopuptabkytrancac(self):
        diachi = self.diachigame + 0x3AF8
        if read_bytes(self.tientrinh, self.diachigame + 0x3AF8, 1) != bytes.fromhex("E8"):
            write_bytes(self.tientrinh, diachi, b'\xE8\xD3\xBD\x06\x00', 5)

    def action_vohieuhoapopuptabkytrancac(self):
        diachi = self.diachigame + 0x3AF8
        if read_bytes(self.tientrinh, self.diachigame + 0x3AF8, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, diachi, b'\x90\x90\x90\x90\x90', 5)

    def action_vohieuhoagiamxuatchieukhithaydo(self):
        diachixuatchieuvukhi = self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat + 0x948
        diachixuatchieubuaphap = self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat + 0x94C

        if read_int(self.tientrinh, self.diachigame + 0x129945 + 0x2) != diachixuatchieuvukhi:
            write_int(self.tientrinh, self.diachigame + 0x129945 + 0x2, diachixuatchieuvukhi)

        if read_int(self.tientrinh, self.diachigame + 0x129951 + 0x2) != diachixuatchieubuaphap:
            write_int(self.tientrinh, self.diachigame + 0x129951 + 0x2, diachixuatchieubuaphap)

    def action_tatvohieuhoathietlapmuctieudangchon(self):
        if read_bytes(self.tientrinh, self.diachigame + 0x16AB57, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x16AB57, bytes.fromhex("89 0D"), 2)
            write_int(self.tientrinh, self.diachigame + 0x16AB57 + 0x2, self.diachigame + 0x4585B8)

        if read_bytes(self.tientrinh, self.diachigame + 0x11AADF, 1) != bytes.fromhex("C7"):
            write_bytes(self.tientrinh, self.diachigame + 0x11AADF, bytes.fromhex("C7 05"), 10)
            write_int(self.tientrinh, self.diachigame + 0x11AADF + 0x2, self.diachigame + 0x4585B8)
            write_int(self.tientrinh, self.diachigame + 0x11AADF + 0x6, 0)

    def action_vohieuhoathietlapmuctieudangchon(self):
        if read_bytes(self.tientrinh, self.diachigame + 0x16AB57, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x16AB57, bytes.fromhex("90 90 90909090"), 6)

        if read_bytes(self.tientrinh, self.diachigame + 0x11AADF, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x11AADF, bytes.fromhex("90 90 90909090 90909090"), 10)

    def action_tatvohieuhoathietlapmuctieutancong(self):
        #Auto ingame tự chọn quái
        if read_bytes(self.tientrinh, self.diachigame + 0x16B7D9, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x16B7D9, bytes.fromhex("89 BE AC000000"), 6)

        #Lúc dí chuột
        if read_bytes(self.tientrinh, self.diachigame + 0x16B2DD, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x16B2DD, bytes.fromhex("89 AE AC000000"), 6)

        # Lúc theo lại gần mục tiêu theo sau cái là chỗ này bắt đầu chạy
        if read_bytes(self.tientrinh, self.diachigame + 0x16B5A6, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x16B5A6, bytes.fromhex("89 AE AC000000"), 6)

        # Lúc ngoài phạm vi điểm di chuyển xunh quanh + Lúc ngoài phạm vi tìm kiếm
        if read_bytes(self.tientrinh, self.diachigame + 0x16A801, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x16A801, bytes.fromhex("89 AE AC000000"), 6)
        if read_bytes(self.tientrinh, self.diachigame + 0x16B803, 1) != bytes.fromhex("89"):
            write_bytes(self.tientrinh, self.diachigame + 0x16B803, bytes.fromhex("89 AE AC000000"), 6)

    def action_vohieuhoathietlapmuctieutancong(self):
        #Auto ingame tự chọn quái
        if read_bytes(self.tientrinh, self.diachigame + 0x16B7D9, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x16B7D9, bytes.fromhex("90 90 90909090"), 6)

        #Lúc dí chuột
        if read_bytes(self.tientrinh, self.diachigame + 0x16B2DD, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x16B2DD, bytes.fromhex("90 90 90909090"), 6)

        # Lúc theo lại gần mục tiêu theo sau cái là chỗ này bắt đầu chạy
        if read_bytes(self.tientrinh, self.diachigame + 0x16B5A6, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x16B5A6, bytes.fromhex("90 90 90909090"), 6)

        # Lúc ngoài phạm vi điểm di chuyển xunh quanh + Lúc ngoài phạm vi tìm kiếm
        if read_bytes(self.tientrinh, self.diachigame + 0x16A801, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x16A801, bytes.fromhex("90 90 90909090"), 6)

        if read_bytes(self.tientrinh, self.diachigame + 0x16B803, 1) != bytes.fromhex("90"):
            write_bytes(self.tientrinh, self.diachigame + 0x16B803, bytes.fromhex("90 90 90909090"), 6)

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

        aob_ham = "56 6A 00 6A 01 6A 01 8B F1 E8 ?? ?? ?? ?? 8B C8 E8 ?? ?? ?? ?? 8B 44 24 0C 6A 01 6A 00 6A 01 6A 01 50"
        diachi_scan_ham = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_ham)
        )
        if diachi_scan_ham:
            diachi_ham = diachi_scan_ham
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hàm tự động tìm đường: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm tự động tìm đường! Hủy bỏ khởi tạo.")
            return

        aob_doituong = "8B 87 ?? ?? ?? ?? 8B 8F ?? ?? ?? ?? 6A 01 03 C9 50 51 B9 ?? ?? ?? ?? 89 2F E8"
        diachi_scan_obj = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_doituong)
        )
        if diachi_scan_obj:
            diachi_doituong = read_int(self.tientrinh, diachi_scan_obj + 19)
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Đối tượng UI tìm đường: {hex(diachi_doituong - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Đối tượng UI tìm đường! Hủy bỏ khởi tạo.")
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

            mov ecx, {hex(diachi_doituong)}

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

    def khoitaohamtudongtimduongxuyenbando(self):
        if self.diachihamtudongtimduongxuyenbando:
            return

        aob_ham = "8B 44 24 04 85 C0 75 10 B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? 83 C8 FF C2 14 00 89 44 24 04 B9 ?? ?? ?? ?? E9 ?? ?? ?? ??"
        diachi_scan_ham = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_ham)
        )

        if diachi_scan_ham:
            diachi_ham = diachi_scan_ham
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hàm tìm đường xuyên bản đồ: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm tìm đường xuyên bản đồ! Hủy bỏ khởi tạo.")
            return

        aob_doituong = "50 8B 0D ?? ?? ?? ?? 8B 11 8B 0D ?? ?? ?? ?? 8B 82 ?? ?? ?? ?? FF D0"
        diachi_scan_obj = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_doituong)
        )

        if diachi_scan_obj:
            diachi_doituong = read_int(self.tientrinh, diachi_scan_obj + 3)
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Đối tượng UI xuyên bản đồ: {hex(diachi_doituong - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Đối tượng UI xuyên bản đồ! Hủy bỏ khởi tạo.")
            return

        self.diachihamtudongtimduongxuyenbando = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamtudongtimduongxuyenbando + 0x40
        write_bytes(self.tientrinh, diachidulieu + 16, b"\x00" * 4, 4)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov ecx, {hex(diachi_doituong)}

            push dword ptr [{hex(diachidulieu)}]
            push {hex(diachidulieu + 16)}
            push dword ptr [{hex(diachidulieu + 8)}]
            push dword ptr [{hex(diachidulieu + 4)}]
            push dword ptr [{hex(diachidulieu + 12)}]

            mov eax, {hex(diachi_ham)}

            call eax
            ret
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamtudongtimduongxuyenbando, bytes(encoding), len(encoding))

    def action_tudongtimduongxuyenbando(self, idbando, toadox, toadoy, tennpc = "", mode = IDCHEDOTIMDUONG_TONGHOP, delay = 1.0):
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
        if self.diachihamdichuyen:
            return


        aob = "A1 ?? ?? ?? ?? 3B 05 ?? ?? ?? ?? 57 8B F9 0F 8D ?? ?? ?? ?? 8B 8F ?? ?? ?? ?? 83 F9 05 0F 84 ?? ?? ?? ??"
        diachi_scan_ham = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if diachi_scan_ham:
            diachi_ham = diachi_scan_ham
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hàm di chuyển: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm di chuyển! Hủy bỏ khởi tạo.")
            return

        self.diachihamdichuyen = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamdichuyen + 0x40
        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov esi, {hex(self.diachigame + self.offsetdiachicosonhanvat + self.offsetdiachicosomoinhanvat)}
            mov edi, dword ptr [{hex(diachidulieu)}]
            mov edx, dword ptr [{hex(diachidulieu + 4)}]
            mov ebx, 0

            push ebx
            push edx
            push edi

            mov ecx, esi

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

    def khoitaohamdichuyen2(self):
        if self.diachihamdichuyen2:
            return

        self.diachihamdichuyen2 = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamdichuyen2 + 0x80

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 16                     

            mov eax, dword ptr [{hex(diachidulieu)}]
            mov ecx, dword ptr [{hex(diachidulieu + 4)}]

            mov byte ptr [ebp - 12], 0x4C
            mov dword ptr [ebp - 11], eax
            mov dword ptr [ebp - 7], ecx

            mov dword ptr [ebp - 4], 9        

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
        write_bytes(self.tientrinh, self.diachihamdichuyen2, bytes(encoding), len(encoding))

    def action_dichuyen2(self, toadox, toadoy, delay = 0.05):
        if not self.diachihamdichuyen2:
            self.khoitaohamdichuyen2()

        if time.time() - self._thoidiemdichuyengannhat < delay:
            return False

        self._thoidiemdichuyengannhat = time.time()

        diachidulieu = self.diachihamdichuyen2 + 0x80
        write_int(self.tientrinh, diachidulieu, toadox)
        write_int(self.tientrinh, diachidulieu + 4, toadoy)

        self.tientrinh.start_thread(self.diachihamdichuyen2)
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
            ret                           
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

        aob = "83 EC 08 8B 44 24 0C 8A 4C 24 10 89 44 24 01 A1 ?? ?? ?? ?? C6 04 24 65 88 4C 24 05 85 C0 74 ?? 8D 4C 24 10 51 8D 4C 24 04 C7 44 24 14 06 00 00 00"

        diachitimthay = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if diachitimthay:
            diachi_ham = diachitimthay
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hàm bật tắt hiệu ứng: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm bật tắt hiệu ứng! Hủy bỏ khởi tạo.")
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

    def khoitaohamvohieuhoakynangbotro3(self):
        if self.diachihamvohieuhoakynangbotro3:
            return

        import pymem.pattern

        aob = "85 C0 74 ?? 8B 06 8B 50 10 8B CE FF D2 83 F8 14 75 ?? 83 BD ?? ?? ?? ?? 00 EB ?? 8B 0D ?? ?? ?? ??"

        diachitimthay = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if diachitimthay:
            diachi_hook = diachitimthay + 33
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hook Vô hiệu hóa kỹ năng 3: {hex(diachi_hook - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Hook vô hiệu hóa kỹ năng 3! Hủy bỏ khởi tạo.")
            return

        diachi_return = diachi_hook + 8

        self.diachihamvohieuhoakynangbotro3 = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamvohieuhoakynangbotro3 + 0x40
        write_int(self.tientrinh, diachidulieu, 0)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            cmp edi, {self.diachigame + 0x4574D4}
            jne logic_goc
            cmp dword ptr [{hex(diachidulieu)}], 1
            jne logic_goc
            mov eax, 0
            jmp logic_phuchoi_imul
            logic_goc:
            mov eax, dword ptr [edi]
            logic_phuchoi_imul:
            imul ecx, ecx, 0x8294
            jmp {hex(diachi_return)}
        """

        encoding, _ = ks.asm(asm_code, addr = self.diachihamvohieuhoakynangbotro3)
        write_bytes(self.tientrinh, self.diachihamvohieuhoakynangbotro3, bytes(encoding), len(encoding))

        jump_offset = self.diachihamvohieuhoakynangbotro3 - diachi_hook - 5
        patch_bytes = b"\xE9" + jump_offset.to_bytes(4, byteorder = sys.byteorder, signed = True) + b"\x90\x90\x90"
        write_bytes(self.tientrinh, diachi_hook, patch_bytes, 8)

    def set_is_vohieuhoakynangbotro3(self, is_vohieuhoa: bool, delay = 0.5):
        if not self.diachihamvohieuhoakynangbotro3:
            self.khoitaohamvohieuhoakynangbotro3()

        if time.time() - self._thoidiemvohieuhoakynangbotro3gannhat < delay:
            return False

        self._thoidiemvohieuhoakynangbotro3gannhat = time.time()

        diachidulieu = self.diachihamvohieuhoakynangbotro3 + 0x40
        trangthaihientai = read_int(self.tientrinh, diachidulieu)
        trangthaimoi = 1 if is_vohieuhoa else 0

        if trangthaihientai != trangthaimoi:
            write_int(self.tientrinh, diachidulieu, trangthaimoi)

        return True

    def khoitaohamnhatvatpham(self):
        if self.diachihamnhatvatpham:
            return

        self.diachihamnhatvatpham = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamnhatvatpham + 0x80

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 24                     

            mov eax, dword ptr [{hex(diachidulieu)}]
            mov ebx, dword ptr [{hex(diachidulieu + 4)}]

            mov byte ptr [ebp - 20], 0x58
            mov dword ptr [ebp - 19], eax

            mov cx, bx
            mov word ptr [ebp - 15], cx      
            shr ebx, 16
            mov byte ptr [ebp - 13], bl      

            mov dword ptr [ebp - 4], 8        

            mov eax, dword ptr [{hex(self.diachigame + self.offsetdiachicosothuchiencaulenh)}]
            test eax, eax
            je ketthuc

            lea edx, [ebp - 4]
            push edx

            lea edx, [ebp - 20]
            push edx

            push eax

            lea ecx, [ebp - 20]

            mov edx, dword ptr [eax]
            mov edx, dword ptr [edx + 0x1C]
            call edx                        

            ketthuc:
            mov esp, ebp
            pop ebp
            ret 4                           
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamnhatvatpham, bytes(encoding), len(encoding))

    def action_nhatvatpham(self, idvatphamduoidat, delay = 0.05):
        if not self.diachihamnhatvatpham:
            self.khoitaohamnhatvatpham()

        if time.time() - self._thoidiemnhatvatphamgannhat < delay:
            return False

        dbidvatphamduoidat = self.get_dbidvatphamduoidat(idvatphamduoidat)
        if dbidvatphamduoidat <= 0:
            return False

        self._thoidiemnhatvatphamgannhat = time.time()

        diachidulieu = self.diachihamnhatvatpham + 0x80
        write_int(self.tientrinh, diachidulieu, dbidvatphamduoidat)
        write_bytes(self.tientrinh, diachidulieu + 4, bytes([0, 0, 0, 0]), 4)
        self.tientrinh.start_thread(self.diachihamnhatvatpham)

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
        aob_ham = "83 EC 2C A1 ?? ?? ?? ?? 33 C4 89 44 24 28 8B 44 24 34 85 C0 74 ?? 8A 4C 24 30 6A 20 50 8D 54 24 0E 52 C6 44 24 10 74 88 4C 24 11 FF 15 ?? ?? ?? ?? A1 ?? ?? ?? ?? 83 C4 0C 85 C0 74 ??"
        diachi_scan_ham = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_ham)
        )

        if diachi_scan_ham:
            diachi_ham = diachi_scan_ham
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hàm mở khóa: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm mở khóa! Hủy bỏ khởi tạo.")
            return

        aob_doituong = "85 DB 0F 84 ?? ?? ?? ?? 53 6A 03 B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? E9 ?? ?? ?? ?? 53 6A 09"
        diachi_scan_obj = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_doituong)
        )

        if diachi_scan_obj:
            diachi_doituong = read_int(self.tientrinh, diachi_scan_obj + 12)
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Đối tượng UI mở khóa: {hex(diachi_doituong - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Đối tượng UI mở khóa! Hủy bỏ khởi tạo.")
            return

        self.diachihammokhoa = self.tientrinh.allocate(256)
        diachidulieu = self.diachihammokhoa + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push {hex(diachidulieu)}
            push 03

            mov ecx, {hex(diachi_doituong)}

            mov eax, {hex(diachi_ham)}

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

        aob = "56 8B F1 8B 86 ?? ?? ?? ?? 83 F8 05 0F 84 ?? ?? ?? ?? 83 F8 04 0F 84 ?? ?? ?? ?? 8B 86 ?? ?? ?? ?? 83 F8 05 0F 84 ?? ?? ?? ?? 83 F8 06 0F 84 ?? ?? ?? ??"

        diachi_scan_ham = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if diachi_scan_ham:
            diachi_ham = diachi_scan_ham
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hàm sử dụng kỹ năng tọa độ: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm sử dụng kỹ năng tọa độ! Hủy bỏ khởi tạo.")
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

    def khoitaohamsudungkynangtoado2(self):
        if self.diachihamsudungkynangtoado2:
            return

        self.diachihamsudungkynangtoado2 = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamsudungkynangtoado2 + 0x80

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 32                     

            mov eax, dword ptr [{hex(diachidulieu)}]
            mov ebx, dword ptr [{hex(diachidulieu + 4)}]
            mov ecx, dword ptr [{hex(diachidulieu + 8)}]
            mov edx, dword ptr [{hex(diachidulieu + 12)}]
            mov esi, dword ptr [{hex(diachidulieu + 16)}]

            mov byte ptr [ebp - 28], 0x4D
            mov dword ptr [ebp - 27], esi
            mov dword ptr [ebp - 23], ebx
            mov dword ptr [ebp - 19], ecx
            mov dword ptr [ebp - 15], eax
            mov dword ptr [ebp - 11], edx

            mov dword ptr [ebp - 4], 21        

            mov eax, dword ptr [{hex(self.diachigame + self.offsetdiachicosothuchiencaulenh)}]
            test eax, eax
            je ketthuc

            lea edx, [ebp - 4]
            push edx

            lea edx, [ebp - 28]
            push edx

            push eax

            mov edx, dword ptr [eax]
            mov edx, dword ptr [edx + 0x1C]
            call edx                        

            ketthuc:
            mov esp, ebp
            pop ebp
            ret 4                           
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamsudungkynangtoado2, bytes(encoding), len(encoding))

    def action_sudungkynangtoado2(self, idkynang, toadox, toadoy, delay = 0.05):
        if not self.diachihamsudungkynangtoado2:
            self.khoitaohamsudungkynangtoado2()

        if time.time() - self._thoidiemsudungkynanggannhat_map.get(idkynang, 0.) < delay:
            return False

        toadox_hientai, toadoy_hientai = self.get_toado()

        self._thoidiemsudungkynanggannhat_map[idkynang] = time.time()

        diachidulieu = self.diachihamsudungkynangtoado2 + 0x80
        write_int(self.tientrinh, diachidulieu, toadox)  # Target X
        write_int(self.tientrinh, diachidulieu + 4, toadox_hientai)  # Current X
        write_int(self.tientrinh, diachidulieu + 8, toadoy_hientai)  # Current Y
        write_int(self.tientrinh, diachidulieu + 12, toadoy)  # Target Y
        write_int(self.tientrinh, diachidulieu + 16, idkynang)  # Skill ID

        self.tientrinh.start_thread(self.diachihamsudungkynangtoado2)
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

    def action_sudungkynangtoadochichuot2(self, idkynang, khoangcachtoida, delay = 0.05):
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

        return self.action_sudungkynangtoado2(idkynang, target_x, target_y, delay = delay)

    def khoitaohamsudungphimtat(self):
        if self.diachihamsudungphimtat:
            return

        aob = "55 8B EC 83 EC 44 E8 ?? ?? ?? ?? 85 C0 74 ?? E9 ?? ?? ?? ?? 83 3D ?? ?? ?? ?? 00 0F 84 ?? ?? ?? ?? 83 7D 08 00 0F 8C ?? ?? ?? ?? 83 7D 08 09 0F 8D ?? ?? ?? ??"

        diachi_scan_ham = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if diachi_scan_ham:
            diachi_ham = diachi_scan_ham
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hàm sử dụng phím tắt: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm sử dụng phím tắt! Hủy bỏ khởi tạo.")
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

            mov ecx, {hex(diachi_ham)}
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
        if self.diachihambanvatpham:
            return

        self.diachihambanvatpham = self.tientrinh.allocate(256)
        diachidulieu = self.diachihambanvatpham + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 16                     

            mov eax, dword ptr [{hex(diachidulieu)}]

            mov byte ptr [ebp - 12], 0x5A
            mov dword ptr [ebp - 11], eax

            mov dword ptr [ebp - 4], 5        

            mov eax, dword ptr [{hex(self.diachigame)} + {hex(self.offsetdiachicosothuchiencaulenh)}]
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
        write_bytes(self.tientrinh, self.diachihambanvatpham, bytes(encoding), len(encoding))

    def action_banvatpham(self, sothutuvatpham, delay = 0.25):
        if not self.diachihambanvatpham:
            self.khoitaohambanvatpham()

        if time.time() - self._thoidiembanvatphamgannhat < delay:
            return False

        idvatpham = self.get_idvatpham(sothutuvatpham)
        if idvatpham <= 0: # or not self.get_is_dangmocuahang():
            return False

        dbidvatpham = self.get_dbidvatpham(idvatpham)
        if dbidvatpham <= 0:
            return False

        self._thoidiembanvatphamgannhat = time.time()

        diachidulieu = self.diachihambanvatpham + 0x40
        write_int(self.tientrinh, diachidulieu, dbidvatpham)
        self.tientrinh.start_thread(self.diachihambanvatpham)

        return True

    def khoitaohamdoithoai(self):
        if self.diachihamdoithoai:
            return

        aob_ham = "83 EC 08 56 8B 74 24 10 57 8B F9 85 F6 7E ?? 8B C6 69 C0 ?? ?? ?? ?? 83 B8 ?? ?? ?? ?? 00 7E ?? 8B 80 ?? ?? ?? ?? 89 44 24 09 A1 ?? ?? ?? ?? C6 44 24 08 62 85 C0 74 ?? 8D 54 24 14"
        diachi_scan_ham = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_ham)
        )

        if diachi_scan_ham:
            diachi_ham = diachi_scan_ham
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Hàm đối thoại: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm đối thoại! Hủy bỏ khởi tạo.")
            return

        aob_doituong = "83 FD 10 0F 85 ?? ?? ?? ?? 8B 44 24 1C 3B 86 ?? ?? ?? ?? 7F ?? 53 B9 ?? ?? ?? ??"
        diachi_scan_obj = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob_doituong)
        )

        if diachi_scan_obj:
            diachi_doituong = read_int(self.tientrinh, diachi_scan_obj + 23)
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Đối tượng UI đối thoại: {hex(diachi_doituong - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Đối tượng UI đối thoại! Hủy bỏ khởi tạo.")
            return

        self.diachihamdoithoai = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamdoithoai + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            mov ebx, dword ptr [{hex(diachidulieu)}]
            push ebx

            mov ecx, {hex(diachi_doituong)} 

            mov eax, {hex(diachi_ham)} 

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

        self._thoidiemdoithoaigannhat = time.time()

        diachidulieu = self.diachihamdoithoai + 0x40
        write_int(self.tientrinh, diachidulieu, idnhanvat)
        self.tientrinh.start_thread(self.diachihamdoithoai)
        return True

    def khoitaohamxacnhandoithoai(self):
        if self.diachihamxacnhandoithoai:
            return
        aob = "6A 01 6A 00 6A 0A 8B 0D ?? ?? ?? ?? 8B 11 8B 0D ?? ?? ?? ?? 8B 42 04 FF D0 6A 01 E8 ?? ?? ?? ?? 83 C4 04 8B E5 5D"
        diachi_scan = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if diachi_scan:
            diachi_doituong = read_int(self.tientrinh, diachi_scan + 8)
            #print(f"[THÀNH CÔNG] Tự động tìm thấy Offset Đối tượng UI xác nhận đối thoại: {hex(diachi_doituong - self.diachigame)}")
            khoang_cach_call = read_int(self.tientrinh, diachi_scan + 28)
            diachi_ham = diachi_scan + 27 + 5 + khoang_cach_call
            #print(f"[THÀNH CÔNG] Tự động tính toán được Offset Hàm xác nhận đối thoại: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern hàm xác nhận đối thoại! Hủy bỏ khởi tạo.")
            return

        self.diachihamxacnhandoithoai = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            push 01
            mov ebx, {hex(diachi_ham)}

            call ebx
            add esp, 04

            push 00
            push 00
            push 0x0A
            mov edx, dword ptr [{hex(diachi_doituong)}]

            mov eax, dword ptr [edx]
            mov ecx, dword ptr [{hex(diachi_doituong)}]

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

        self._thoidiemxacnhandoithoaigannhat = time.time()
        self.tientrinh.start_thread(self.diachihamxacnhandoithoai)
        return True

    def khoitaohamdongcuahang(self):
        if self.diachihamdongcuahang:
            return

        aob = "8B 45 FC 05 ?? ?? ?? ?? 39 45 08 75 ?? E8 ?? ?? ?? ?? EB ?? 8B 4D FC 81 C1"

        diachi_scan = pymem.pattern.pattern_scan_module(
            self.tientrinh.process_handle,
            self.gamemodule,
            taopatterntuaob(aob)
        )

        if diachi_scan:
            khoang_cach_call = read_int(self.tientrinh, diachi_scan + 14)
            diachi_ham = diachi_scan + 13 + 5 + khoang_cach_call
            #print(f"[THÀNH CÔNG] Tự động tính toán được Offset Hàm đóng cửa hàng: {hex(diachi_ham - self.diachigame)}")
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Hàm đóng cửa hàng! Hủy bỏ khởi tạo.")
            return

        self.diachihamdongcuahang = self.tientrinh.allocate(256)

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        asm_code = f"""
            mov eax, {hex(diachi_ham)}
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

    def khoitaohamvutvatpham(self):
        if self.diachihamvutvatpham:
            return

        self.diachihamvutvatpham = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamvutvatpham + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 12                     

            mov eax, dword ptr [{hex(diachidulieu)}]

            mov byte ptr [ebp - 12], 0x5C
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
        write_bytes(self.tientrinh, self.diachihamvutvatpham, bytes(encoding), len(encoding))

    def action_vutvatpham(self, sothutuvatpham, delay = 0.25):
        if not self.diachihamvutvatpham:
            self.khoitaohamvutvatpham()

        if time.time() - self._thoidiemvutvatphamgannhat < delay:
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

        self._thoidiemvutvatphamgannhat = time.time()

        diachidulieu = self.diachihamvutvatpham + 0x40
        write_int(self.tientrinh, diachidulieu, dbid)

        self.tientrinh.start_thread(self.diachihamvutvatpham)
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
            mov ebx, ecx

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

    def action_motabkytrancac(self, vitritab, delay = 0.5):
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

    def action_muavatphamkytrancac(self, idtab, vitrivatpham, soluong, delay = 0.5):
        if not self.diachihammuavatphamkytrancac:
            self.khoitaohammuavatphamkytrancac()

        if time.time() - self._thoidiemmuakytrancacgannhat < delay:
            return False

        if self.get_idtabkytrancac() != idtab:
            vitritab = VITRITAB_MAP.get(idtab)
            if vitritab is not None:
                self.action_vohieuhoapopuptabkytrancac()
                self.action_motabkytrancac(vitritab)
            return False

        self.action_tatvohieuhoapopuptabkytrancac()

        self._thoidiemmuakytrancacgannhat = time.time()

        diachidulieu = self.diachihammuavatphamkytrancac + 0x80
        write_int(self.tientrinh, diachidulieu, idtab)
        write_int(self.tientrinh, diachidulieu + 4, vitrivatpham)
        write_int(self.tientrinh, diachidulieu + 8, soluong)

        print("action_muavatphamkytrancac: {}, {}, {}".format(idtab, vitrivatpham, soluong))

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

    def khoitaohammoitodoi(self):
        if self.diachihammoitodoi:
            return

        self.diachihammoitodoi = self.tientrinh.allocate(256)
        diachidulieu = self.diachihammoitodoi + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 16                     

            mov eax, dword ptr [{hex(diachidulieu)}]

            mov byte ptr [ebp - 12], 0x63
            mov dword ptr [ebp - 11], eax

            mov dword ptr [ebp - 4], 5        

            mov eax, dword ptr [{hex(self.diachigame)} + {hex(self.offsetdiachicosothuchiencaulenh)}]
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
            ret                           
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihammoitodoi, bytes(encoding), len(encoding))

    def action_moitodoi(self, dbidnhanvat, delay = 0.25):
        if not self.diachihammoitodoi:
            self.khoitaohammoitodoi()

        if time.time() - self._thoidiemmoitodoigannhat < delay:
            return False

        if dbidnhanvat <= 0:
            return False

        self._thoidiemmoitodoigannhat = time.time()

        diachidulieu = self.diachihammoitodoi + 0x40
        write_int(self.tientrinh, diachidulieu, dbidnhanvat)

        self.tientrinh.start_thread(self.diachihammoitodoi)

        return True

    def khoitaohamnhanloimoitodoi(self):
        if self.diachihamnhanloimoitodoi:
            return

        self.diachihamnhanloimoitodoi = self.tientrinh.allocate(256)
        diachidulieu = self.diachihamnhanloimoitodoi + 0x40

        ks = Ks(KS_ARCH_X86, KS_MODE_32)

        asm_code = f"""
            push ebp
            mov ebp, esp
            sub esp, 20                     

            mov eax, dword ptr [{hex(diachidulieu)}]
            mov ecx, dword ptr [{hex(diachidulieu + 4)}]

            mov byte ptr [ebp - 16], 0x66
            mov byte ptr [ebp - 15], cl
            mov dword ptr [ebp - 14], eax

            mov dword ptr [ebp - 4], 6        

            mov eax, dword ptr [{hex(self.diachigame)} + {hex(self.offsetdiachicosothuchiencaulenh)}]
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
            ret                           
        """

        encoding, _ = ks.asm(asm_code)
        write_bytes(self.tientrinh, self.diachihamnhanloimoitodoi, bytes(encoding), len(encoding))

    def action_nhanloimoitodoi(self, dbidnguoimoi, is_dongy = True, delay = 0.25):
        if not self.diachihamnhanloimoitodoi:
            self.khoitaohamnhanloimoitodoi()

        if time.time() - self._thoidiemnhanloimoitodoigannhat < delay:
            return False

        if dbidnguoimoi <= 0:
            return False

        self._thoidiemnhanloimoitodoigannhat = time.time()

        diachidulieu = self.diachihamnhanloimoitodoi + 0x40
        write_int(self.tientrinh, diachidulieu, dbidnguoimoi)
        write_int(self.tientrinh, diachidulieu + 4, 1 if is_dongy else 0)

        print("{}: {}".format(self.get_tennhanvat(), hex(self.diachihamnhanloimoitodoi)))

        self.tientrinh.start_thread(self.diachihamnhanloimoitodoi)
        return True

    def action_timkiemtoanbodiachiham(self):
        aob_nv = "A1 ?? ?? ?? ?? 69 C0 ?? ?? ?? ?? 83 EC ?? 57 8B 7C 24 ?? 8B 4F 01 3B 88 ?? ?? ?? ?? 0F 85"
        scan_nv = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_nv))
        if scan_nv:
            size_nv = read_int(self.tientrinh, scan_nv + 7)
            base_nv = read_int(self.tientrinh, scan_nv + 24) - self.diachigame
            self.offsetdiachicosonhanvat = base_nv
            self.offsetdiachicosomoinhanvat = size_nv
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset cơ sở nhân vật!")

        aob_bando = "8B 81 ?? ?? ?? ?? 52 8B 91 ?? ?? ?? ?? 50 8B 81 ?? ?? ?? ?? 8B 89 ?? ?? ?? ?? 69 C9 ?? ?? ?? ?? 52 50 81 C1"
        scan_bando = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_bando))

        if scan_bando:
            diachi_bando_tinh = read_int(self.tientrinh, scan_bando + 36)
            self.offsetdiachicosobando = diachi_bando_tinh - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset cơ sở mảng bản đồ!")

        aob_vtvp = "83 EC 0C 83 3D ?? ?? ?? ?? 00 75 ?? 8B 44 24 10 89 44 24 05 A1"
        scan_vtvp = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_vtvp))
        if scan_vtvp:
            diachi_goc = read_int(self.tientrinh, scan_vtvp + 5)
            base_vtvp = diachi_goc - self.diachigame + 0x8

            self.offsetdiachicosovitrivatpham = base_vtvp
            self.offsetdiachicosovitrimoivatpham = 0x10
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset vị trí vật phẩm!")

        aob_vpdd = "8B C8 69 C9 ?? ?? ?? ?? 83 B9 ?? ?? ?? ?? 00 7E ?? 39 B9 ?? ?? ?? ?? 74 ?? 50 8B CE"
        scan_vpdd = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_vpdd))
        if scan_vpdd:
            size_vpdd = read_int(self.tientrinh, scan_vpdd + 4)
            base_vpdd = read_int(self.tientrinh, scan_vpdd + 19) - self.diachigame

            self.offsetdiachicosomoivatphamduoidat = size_vpdd
            self.offsetdiachicosothongtinvatphamduoidat = base_vpdd
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset vật phẩm dưới đất!")

        aob_ttvp = "85 C0 74 ?? 57 8B 7C 24 ?? EB ?? 8D A4 24 ?? ?? ?? ?? 8B C8 69 C9 ?? ?? ?? ?? 39 B9 ?? ?? ?? ?? 74 ?? 50 8B CE"
        scan_ttvp = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_ttvp))

        if scan_ttvp:
            size_ttvp = read_int(self.tientrinh, scan_ttvp + 22)
            diachi_aob = read_int(self.tientrinh, scan_ttvp + 28)
            offset_dbid = 0x698
            base_ttvp = diachi_aob - self.diachigame - offset_dbid

            self.offsetdiachicosomoivatpham = size_ttvp
            self.offsetdiachicosothongtinvatpham = base_ttvp
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset thông tin vật phẩm mới!. Nhân vật: {}".format(self.get_tennhanvat()))

        aob_nhom = "8B 54 24 04 56 B8 ?? ?? ?? ?? 42 57 8B F8 8B F2 83 C0 ?? B9 ?? ?? ?? ??"
        scan_nhom = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_nhom))
        if scan_nhom:
            base_nhom = read_int(self.tientrinh, scan_nhom + 6) - self.diachigame
            size_nhom = read_bytes(self.tientrinh, scan_nhom + 18, 1)[0]

            self.offsetdiachicosothongtinthanhviendoinhom = base_nhom
            self.offsetdiachicosomoithanhviendoinhom = size_nhom
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset thông tin thành viên đội nhóm!")

        aob_nvtt = "8B 45 01 57 0F B6 7D 1B 50 B9 ?? ?? ?? ?? 89 7C 24 14 E8 ?? ?? ?? ?? 8B D8 89 5C 24 0C"
        scan_nvtt = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_nvtt))
        if scan_nvtt:
            base_nvtt = read_int(self.tientrinh, scan_nvtt + 10) - self.diachigame + 0xFE0
            self.offsetdiachicosonhanvattieptheo = base_nvtt
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset nhân vật tiếp theo!")

        aob_core = "FF 15 ?? ?? ?? ?? A1 ?? ?? ?? ?? 83 C4 0C 85 C0 74 ?? 8D 14 24"
        scan_core = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_core))
        if scan_core:
            base_core = read_int(self.tientrinh, scan_core + 7) - self.diachigame
            self.offsetdiachicosothuchiencaulenh = base_core
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Offset Core!")

        aob_dongho = "8B 01 8B 40 34 52 8D 54 24 ?? 52 FF D0 66 8B 44 24 ?? 66 85 C0 74 ?? 0F BF C8 A1 ?? ?? ?? ?? 99 F7 F9"
        scan_dongho = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_dongho))

        if scan_dongho:
            diachi_dongho_tinh = read_int(self.tientrinh, scan_dongho + 27)
            self.offsetdiachidongho = diachi_dongho_tinh - self.diachigame
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Đồng hồ thời gian!")

        aob_bandohientai = "B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? B8 01 00 00 00 C3"
        scan_bandohientai = pymem.pattern.pattern_scan_module(self.tientrinh.process_handle, self.gamemodule, taopatterntuaob(aob_bandohientai))

        if scan_bandohientai:
            diachi_cautruc_bando = read_int(self.tientrinh, scan_bandohientai + 11)
            offset_cautruc_bando = diachi_cautruc_bando - self.diachigame
            self.offsetdiachiidbandohientai = offset_cautruc_bando + 0x3314C
            self.offsetdiachitenbandohientai = offset_cautruc_bando + 0x330FC
        else:
            print("[LỖI NGHIÊM TRỌNG] Không tìm thấy Pattern Thông tin bản đồ hiện tại!")

        danhsachthuoctinh = dir(self)
        tongsoham = 0

        for tenthuoctinh in danhsachthuoctinh:
            if tenthuoctinh.startswith("khoitaoham") and callable(getattr(self, tenthuoctinh)):
                tongsoham += 1
                ham_khoi_tao = getattr(self, tenthuoctinh)
                try:
                    ham_khoi_tao()
                except Exception as e:
                    print(f"[LỖI NGOẠI LỆ CỦA PYTHON] Xảy ra lỗi khi chạy {tenthuoctinh}: {e}")
