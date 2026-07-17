import math
import os
import pickle
import re
import sys
import threading

import gtts
import pygame
import unicodedata

import win32gui
import win32con
import time
import pywintypes

def to_hex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

def read_boolean(process, address):
    return process.read_bool(address)


def write_boolean(process, address, value):
    process.write_bool(address, value)


def read_int(process, address):
    return process.read_int(address)


def write_int(process, address, value):
    process.write_int(address, value)


def read_short_int(process, address, n_bytes = 1):
    return int.from_bytes(process.read_bytes(address, n_bytes), sys.byteorder)


def write_short_int(process, address, value, n_bytes = 1):
    process.write_bytes(address, value.to_bytes(n_bytes, sys.byteorder), n_bytes)


def read_bytes(process, address, n_bytes):
    return process.read_bytes(address, n_bytes)


def write_bytes(process, address, value, n_bytes):
    return process.write_bytes(address, value, n_bytes)


def read_string(process, address, max_length = 2048):
    try:
        buffer = process.read_bytes(address, max_length)
        null_index = buffer.find(b"\x00")
        if null_index != -1:
            buffer = buffer[:null_index]
        raw_text = buffer.decode("latin-1", errors = "ignore")
        converted_text = TCVN3_to_unicode(raw_text)
        clean_text = re.sub(r'\x1b\[[0-9;]*[mK]', '', converted_text)
        clean_text = re.sub(r'\x1b.[a-zA-Z0-9]?', '', clean_text)

        return clean_text.strip()
    except Exception:
        return ""

def write_string(process, address, value):
    return process.write_string(address, value)

def slugify(value, allow_unicode = False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

def _phatam(noidung, is_block):
    try:
        print(f"phatam (thread): {noidung}")
        tenfile = slugify(noidung)

        duongdanthumucamthanh = os.path.join(os.getcwd(), "_internal", "amthanh")

        if not os.path.exists(duongdanthumucamthanh):
            os.makedirs(duongdanthumucamthanh, exist_ok = True)

        file_path = os.path.join(duongdanthumucamthanh, "{}.mp3".format(tenfile))

        if not os.path.exists(file_path):
            try:
                gtts.gTTS(noidung, lang = "vi").save(file_path)
            except Exception as e_save:
                print(f"Lỗi khi lưu file âm thanh: {e_save}")
                return
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            if is_block:
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
        except Exception as e_play:
            print(f"Lỗi phát âm thanh: {e_play}")

    except Exception as err:
        print("Phát âm lỗi tổng quát: {}".format(err))

def phatam(noidung, is_block = True):
    t = threading.Thread(target = _phatam, args = (noidung, is_block), daemon = True)
    t.start()

def luuthietlap(tennhanvat, thietlap):
    tenfile = slugify(tennhanvat)

    try:
        thumuc = os.path.join(".", "_internal", "thietlap")
        if not os.path.exists(thumuc):
            os.makedirs(thumuc)
        with open(os.path.join(thumuc, str(tenfile)), "wb") as file:
            pickle.dump(thietlap, file)

    except Exception as err:
        print(err)


def taithietlap(tennhanvat):
    tenfile = slugify(tennhanvat)
    filepath = os.path.join(".", "_internal", "thietlap", str(tenfile))

    try:
        if os.path.exists(filepath):
            with open(filepath, "rb") as file:
                return pickle.load(file)
    except Exception as err:
        print(err)


def tinhkhoangcach(x1, y1, x2, y2):
    return round(math.dist((x1, y1), (x2, y2), ))

TCVN3TAB = "µ¸¶·¹¨»¾¼½Æ©ÇÊÈÉË®ÌÐÎÏÑªÒÕÓÔÖ×ÝØÜÞßãáâä«åèæçé¬êíëìîïóñòô­õøö÷ùúýûüþ¡¢§£¤¥¦Ù"
TCVN3TAB = [ch for ch in TCVN3TAB]

UNICODETAB = "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵĂÂĐÊÔƠƯ "
UNICODETAB = [ch for ch in UNICODETAB]

r = re.compile("|".join(TCVN3TAB))
replaces_dict = dict(zip(TCVN3TAB, UNICODETAB))


def TCVN3_to_unicode(tcvn3str):
    return r.sub(lambda m: replaces_dict[m.group(0)], tcvn3str)

UNICODE_TO_TCVN3_MAP = dict(zip(UNICODETAB, TCVN3TAB))
if ' ' in UNICODE_TO_TCVN3_MAP:
    del UNICODE_TO_TCVN3_MAP[' ']

def Unicode_to_TCVN3(unicode_str):
    if not unicode_str:
        return b""
    
    result = bytearray()
    for char in unicode_str:
        if ord(char) < 128:
            result.append(ord(char))
            continue
            
        tcvn_char = UNICODE_TO_TCVN3_MAP.get(char)
        
        if tcvn_char:
            try:
                result.extend(tcvn_char.encode('latin-1'))
            except UnicodeEncodeError:
                result.extend(b'?')
        else:
            try:
                result.extend(char.encode('mbcs'))
            except:
                result.extend(b'?')
            
    return bytes(result)

def make_lparam(x, y):
    return (y << 16) | (x & 0xFFFF)

def taopatterntuaob(aob_string):
    pattern = b""
    for byte_str in aob_string.split():
        if byte_str == "?" or byte_str == "??":
            pattern += b"."
        else:
            b = bytes.fromhex(byte_str)
            if b in b".^$*+?{}[]\\|()":
                pattern += b"\\" + b
            else:
                pattern += b
    return pattern

class BackgroundInput:
    @staticmethod
    def _safe_post_message(hwnd, msg, wparam, lparam):
        """Hàm gửi tin nhắn an toàn, tự động bỏ qua nếu cửa sổ đã bị tắt"""
        try:
            win32gui.PostMessage(hwnd, msg, wparam, lparam)
        except pywintypes.error as e:
            # Mã lỗi 1400: Invalid window handle (Cửa sổ đã đóng)
            if e.winerror == 1400:
                return
            # Nếu là lỗi khác thì vẫn báo
            raise e

    @staticmethod
    def click(hwnd, x, y, delay=0.1):
        """Click chuột trái ngầm"""
        lparam = make_lparam(x, y)
        BackgroundInput._safe_post_message(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        time.sleep(0.05)
        BackgroundInput._safe_post_message(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
        time.sleep(delay)

    @staticmethod
    def right_click(hwnd, x, y, delay=0.1):
        """Click chuột phải ngầm"""
        lparam = make_lparam(x, y)
        BackgroundInput._safe_post_message(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lparam)
        time.sleep(0.05)
        BackgroundInput._safe_post_message(hwnd, win32con.WM_RBUTTONUP, 0, lparam)
        time.sleep(delay)

    @staticmethod
    def press_key(hwnd, key_code, delay=0.1):
        """Nhấn một phím ngầm"""
        BackgroundInput._safe_post_message(hwnd, win32con.WM_KEYDOWN, key_code, 0)
        time.sleep(0.05)
        BackgroundInput._safe_post_message(hwnd, win32con.WM_KEYUP, key_code, 0)
        time.sleep(delay)

    @staticmethod
    def type_text(hwnd, text, delay=0.05):
        """Gõ văn bản ngầm"""
        for char in text:
            BackgroundInput._safe_post_message(hwnd, win32con.WM_CHAR, ord(char), 0)
            time.sleep(delay)

    @staticmethod
    def press_combo(hwnd, modifier, key, delay=0.1):
        """Nhấn tổ hợp phím (Ví dụ Shift + Tab)"""
        BackgroundInput._safe_post_message(hwnd, win32con.WM_KEYDOWN, modifier, 0)
        time.sleep(0.05)
        BackgroundInput._safe_post_message(hwnd, win32con.WM_KEYDOWN, key, 0)
        time.sleep(0.05)
        BackgroundInput._safe_post_message(hwnd, win32con.WM_KEYUP, key, 0)
        time.sleep(0.05)
        BackgroundInput._safe_post_message(hwnd, win32con.WM_KEYUP, modifier, 0)
        time.sleep(delay)