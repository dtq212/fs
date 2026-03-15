import frida
import sys
import re

TCVN3TAB = "µ¸¶·¹¨»¾¼½Æ©ÇÊÈÉË®ÌÐÎÏÑªÒÕÓÔÖ×ÝØÜÞßãáâä«åèæçé¬êíëìîïóñòô­õøö÷ùúýûüþ¡¢§£¤¥¦Ù"
UNICODETAB = "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵĂÂĐÊÔƠƯ "
replaces_dict = dict(zip(list(TCVN3TAB), list(UNICODETAB)))
r_regex = re.compile("|".join(list(TCVN3TAB)))


def TCVN3_to_unicode(tcvn3str):
    return r_regex.sub(lambda m: replaces_dict[m.group(0)], tcvn3str)


js_code = """
function scanOnce() {
    var targetIds = [];
    var targetNamesBytes = [];

    try {
        // 1. Đọc Base Mảng từ con trỏ tĩnh 0x04D2F9F8
        var staticPtr = ptr("0x04D2F9F8"); 
        var baseAddr = staticPtr.readPointer();

        if (baseAddr.isNull()) return;

        var currentId = 0; 
        var visited = [];
        var count = 0;

        // Bắt đầu từ Next ID của ID 0 (nằm tại Base + 4)
        var nextId = baseAddr.add(4).readU32();

        // Vòng lặp kết thúc khi nextId <= 0 [Cấu trúc Linked List chuẩn]
        while (nextId > 0 && nextId <= 1024) {
            if (visited.indexOf(nextId) !== -1) break;
            visited.push(nextId);

            currentId = nextId;

            try {
                // Sử dụng base 0x93800008 ông vừa tìm
                var infoBaseAddr = ptr("0x93800008").add(currentId * 0xD5AC);

                // Kiểm tra Map (+0x38)
                var isInMap = infoBaseAddr.add(0x38).readU32(); 

                if (isInMap !== 0) {
                    var nameAddr = infoBaseAddr.add(0xB2D);
                    var rawBytes = nameAddr.readByteArray(32);
                    var u8Array = new Uint8Array(rawBytes);
                    var nameBytesArray = [];

                    for(var b = 0; b < u8Array.length; b++) {
                        if(u8Array[b] === 0) break;
                        nameBytesArray.push(u8Array[b]);
                    }

                    targetIds.push(currentId);
                    targetNamesBytes.push(nameBytesArray);
                    count++;
                }

                // Nhảy sang ID tiếp theo (Base + currentId*8 + 4)
                nextId = baseAddr.add(currentId * 8).add(4).readU32();

            } catch(e) {
                break; 
            }
        }

        send({type: 'result', ids: targetIds, names: targetNamesBytes});

    } catch (e) {
        // Lỗi tĩnh
    }
}

setInterval(scanOnce, 1000);
"""

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        if payload['type'] == 'result':
            ids = payload['ids']
            names_raw = payload['names']

            print(f"\n[*] Đang quét... (Tìm thấy {len(ids)} thực thể)")
            for i in range(len(ids)):
                raw_bytes = bytes(names_raw[i])
                raw_str = raw_bytes.decode('latin-1', errors = 'ignore')
                ten_chuan = TCVN3_to_unicode(raw_str)
                # Dọn rác mã màu (hàm slugify/clean của ông)
                ten_chuan = re.sub(r'\x1b\[[0-9;]*[mK]', '', ten_chuan)
                ten_chuan = re.sub(r'\x1b.[a-zA-Z0-9]?', '', ten_chuan).strip()

                print(f"   [+] ID: {ids[i]:<4} | Tên: {ten_chuan}")
            print("-" * 40)


try:
    device = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
    front_app = device.get_frontmost_application()

    if not front_app:
        print("[!] Không tìm thấy ứng dụng đang chạy.")
        sys.exit()

    print(f"[*] Đang attach vào: {front_app.identifier} (PID: {front_app.pid})")
    session = device.attach(front_app.pid)

    script = session.create_script(js_code)
    script.on('message', on_message)
    script.load()

    print("[*] Tool đang chạy... Quét mỗi 1s. Ctrl+C để dừng.")
    sys.stdin.read()
except Exception as e:
    print(f"[!] Lỗi: {e}")