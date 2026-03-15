import frida
import sys

TARGET_VALUE = 53
PATTERN = "35 00 00 00"
MAX_ENTITIES = 1024
MIN_HOPS = 5

js_code = f"""
rpc.exports = {{
    scanrange: function() {{
        console.log("[*] Đang quét Mảng ID, Check Map và Đọc Tên (Bản x86_64)...");

        var NPC_SIZE = 0xD5F0;     
        var OFFSET_EXIST = 0x44;   
        var OFFSET_NAME = 0xB65;   

        var NODE_SIZE = 8;         
        var NEXT_ID_OFFSET = 4;    

        var moduleCocos = Process.findModuleByName("libcocos2dcpp.so");

        // ĐÃ THÊM 0x ĐỂ FIX LỖI "EXPECTED A POINTER"
        var npcArrayBase = ptr("0x00007FF4CA000008"); 

        if (moduleCocos) {{
            // Giải mã Con trỏ
            var globalPointerAddr = moduleCocos.base.add(0x11B0F20);
            npcArrayBase = globalPointerAddr.readPointer();
            console.log("[+] Đã tự động giải mã Con trỏ NPC Array Base: " + npcArrayBase);
        }} else {{
            console.log("[-] Không tìm thấy module, xài Base cứng: " + npcArrayBase);
        }}

        var ranges = Process.enumerateRanges('rw-');
        var found = 0;

        ranges.forEach(function(range) {{
            try {{
                var matches = Memory.scanSync(range.base, range.size, "{PATTERN}");

                matches.forEach(function(match) {{
                    var addr = match.address; 
                    var baseAddr = addr.sub({TARGET_VALUE} * NODE_SIZE);

                    var currentId = 0; 
                    var visited = [];
                    var hops = 0;
                    var hasTarget = false;
                    var logData = []; 
                    var isValid = true;

                    while (hops < 150) {{ 
                        try {{
                            var blockAddr = baseAddr.add(currentId * NODE_SIZE);
                            var nextId = blockAddr.add(NEXT_ID_OFFSET).readU32();

                            if (nextId < 0 || nextId > {MAX_ENTITIES}) {{
                                isValid = false; break;
                            }}

                            if (nextId > 0 && visited.indexOf(nextId) !== -1) {{
                                isValid = false; break;
                            }}

                            logData.push({{ current: currentId, next: nextId }});

                            if (currentId === {TARGET_VALUE} || nextId === {TARGET_VALUE}) {{
                                hasTarget = true;
                            }}

                            visited.push(currentId);
                            currentId = nextId;
                            hops++;

                            if (currentId === 0) {{
                                break; 
                            }}
                        }} catch(e) {{
                            isValid = false; break;
                        }}
                    }}

                    if (isValid && hasTarget && hops >= {MIN_HOPS}) {{
                        console.log("\\n[+] BINGO! TÌM THẤY MẢNG CHUẨN (CÓ " + hops + " NHÂN VẬT):");
                        console.log("    Địa chỉ Gốc mảng quản lý ID: " + baseAddr);

                        for (var i = 0; i < logData.length; i++) {{
                            var cId = logData[i].current;
                            var nId = logData[i].next;
                            var charName = "[Lính Canh / Trống]"; 

                            if (cId > 0) {{
                                try {{
                                    var entityAddr = npcArrayBase.add(cId * NPC_SIZE);
                                    var mapCheckAddr = entityAddr.add(OFFSET_EXIST);
                                    var isInMap = mapCheckAddr.readU32(); 

                                    if (isInMap === 0) {{ 
                                         charName = "[KHÔNG NẰM TRONG BẢN ĐỒ]";
                                    }} else {{
                                        try {{
                                            var nameAddr = entityAddr.add(OFFSET_NAME);
                                            charName = nameAddr.readCString();
                                            if (!charName || charName.trim() === "") {{
                                                charName = "[Chuỗi rỗng]";
                                            }}
                                        }} catch (eName) {{
                                            charName = "[Lỗi đọc tên]";
                                        }}
                                    }}
                                }} catch(eMap) {{
                                    charName = "[Lỗi check map]";
                                }}
                            }}

                            var isTarget = (cId === {TARGET_VALUE}) ? " <--- [TARGET]" : "";
                            console.log("    [Hop " + i + "] ID: " + cId + " (" + charName + ") ---> Next ID: " + nId + isTarget);
                        }}
                        console.log("---------------------------------------------------");
                        found++;
                    }}
                }});
            }} catch (e1) {{
            }}
        }});

        console.log("\\n[!] Hoàn tất. Tìm thấy " + found + " mảng hợp lệ.");
    }}
}};
"""

try:
    device = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
    front_app = device.get_frontmost_application()

    if not front_app:
        print("[!] Không tìm thấy ứng dụng. Bật game lên đã ông ơi!")
        sys.exit()

    print(f"[*] Đang móc vào: {front_app.identifier} (PID: {front_app.pid})")
    session = device.attach(front_app.pid)

    script = session.create_script(js_code)
    script.load()
    script.exports_sync.scanrange()

    print("[*] Quét xong! Bấm Ctrl+C để thoát...")
    sys.stdin.read()
except Exception as e:
    print(f"[!] Lỗi: {e}")