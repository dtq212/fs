import socket
import time
import re


class AutoFarmMobile:
    def __init__(self):
        self.SOLUONGVITRIVATPHAMTOIDA = 512
        TCVN3TAB = "µ¸¶·¹¨»¾¼½Æ©ÇÊÈÉË®ÌÐÎÏÑªÒÕÓÔÖ×ÝØÜÞßãáâä«åèæçé¬êíëìîïóñòô­õøö÷ùúýûüþ¡¢§£¤¥¦Ù"
        UNICODETAB = "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵĂÂĐÊÔƠƯ "
        self.replaces_dict = dict(zip(list(TCVN3TAB), list(UNICODETAB)))
        self.r_regex = re.compile("|".join(list(TCVN3TAB)))

    def tcvn3_to_unicode(self, tcvn3str):
        return self.r_regex.sub(lambda m: self.replaces_dict[m.group(0)], tcvn3str)

    def _gui_lenh_socket(self, cmd):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(0.5)
            client.connect(("127.0.0.1", 5000))
            client.sendall(cmd.encode('utf-8'))
            response = client.recv(1024).decode('latin-1', errors = 'ignore')
            client.close()
            return response
        except Exception:
            return None

    def get_vitrivatpham(self, sothutuvatpham):
        if sothutuvatpham < 0 or sothutuvatpham > self.SOLUONGVITRIVATPHAMTOIDA:
            return False

        resp = self._gui_lenh_socket(f"getpos,{sothutuvatpham}")
        if not resp or resp == "0,0,0,0":
            return False

        parts = resp.split(',')
        if len(parts) == 4:
            vitri = (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
            if vitri == (0, 0, 0, 0):
                return False
            return vitri
        return False

    def get_tenvatpham(self, idvatpham):
        raw_str = self._gui_lenh_socket(f"getname,{idvatpham}")
        if not raw_str or raw_str == "EMPTY":
            return None

        ten_chuan = self.tcvn3_to_unicode(raw_str)
        ten_chuan = re.sub(r'\x1b\[[0-9;]*[mK]', '', ten_chuan)
        ten_chuan = re.sub(r'\x1b.[a-zA-Z0-9]?', '', ten_chuan).strip()
        return ten_chuan

    def action_timkiemvatpham(self, tenvatpham):
        if not tenvatpham:
            return False

        print(f"[*] Đang tìm kiếm '{tenvatpham}'...")
        for sothutuvatpham in range(self.SOLUONGVITRIVATPHAMTOIDA):
            vitrivatpham = self.get_vitrivatpham(sothutuvatpham)

            if not vitrivatpham:
                continue

            idvatpham, vitriruong, vitrix, vitriy = vitrivatpham

            tenvatphamxemxet = self.get_tenvatpham(idvatpham)

            if tenvatphamxemxet:
                print(f"   [Debug] Slot {sothutuvatpham:<3} | ID: {idvatpham:<4} | Tên đang xét: '{tenvatphamxemxet}'")

            if tenvatphamxemxet and tenvatphamxemxet.strip().lower() == tenvatpham.strip().lower():
                print(f"[+] Bingo! Tìm thấy '{tenvatpham}' tại ID: {idvatpham} | Rương: {vitriruong} | X: {vitrix}, Y: {vitriy}")
                return vitrivatpham

        return False

    def action_sudungvatphamhanhtrang(self, idvatpham, vitriruong, vitrix, vitriy):
        print(f"[*] Đang thực thi lệnh uống thuốc...")
        resp = self._gui_lenh_socket(f"useitem,{idvatpham},{vitriruong},{vitrix},{vitriy}")
        return resp == "OK"


if __name__ == "__main__":
    auto = AutoFarmMobile()
    ketqua_timkiem = auto.action_timkiemvatpham("Tiểu Hồng đơn")
    if ketqua_timkiem:
        id_vp, ruong, x, y = ketqua_timkiem
        thanh_cong = auto.action_sudungvatphamhanhtrang(id_vp, ruong, x, y)
        if thanh_cong:
            print("[+] Đã sử dụng Tiểu Hồng đơn thành công!")
    else:
        print("[-] Hết sạch Tiểu Hồng đơn rồi đại hiệp!")