import frida
import sys

TARGET_VALUE = 16
PATTERN = "10 00 00 00"
MAX_ENTITIES = 1024
MIN_HOPS = 5

js_code = f"""
rpc.exports = {{
    scanrange: function() {{
        console.log("[*] Đang quét Mảng, Check Map và Đọc Tên (Sử dụng C-String gốc)...");

        var ranges = Process.enumerateRanges('rw-');
        var found = 0;

        ranges.forEach(function(range) {{
            try {{
                var matches = Memory.scanSync(range.base, range.size, "{PATTERN}");

                matches.forEach(function(match) {{
                    var addr = match.address; 
                    var baseAddr = addr.sub({TARGET_VALUE} * 8);

                    var currentId = 0; 
                    var visited = [];
                    var hops = 0;
                    var hasTarget = false;
                    var logData = []; 
                    var isValid = true;

                    while (hops < 150) {{ 
                        try {{
                            var blockAddr = baseAddr.add(currentId * 8);
                            var nextId = blockAddr.add(4).readU32();

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

                    // --- IN KẾT QUẢ KÈM TÊN & KIỂM TRA MAP ---
                    if (isValid && hasTarget && hops >= {MIN_HOPS}) {{
                        console.log("\\n[+] BINGO! TÌM THẤY MẢNG CHUẨN (CÓ " + hops + " NHÂN VẬT):");
                        console.log("    Địa chỉ Gốc (diachicoso): " + baseAddr);

                        for (var i = 0; i < logData.length; i++) {{
                            var cId = logData[i].current;
                            var nId = logData[i].next;
                            var charName = "[Lính Canh / Trống]"; 

                            if (cId > 0) {{
                                try {{
                                    // KIỂM TRA MAP (Tại +0x38)
                                    var mapCheckAddr = ptr("0x96700008").add(cId * 0xD5AC).add(0x38);
                                    var isInMap = mapCheckAddr.readU32(); 

                                    if (isInMap === 0) {{ 
                                         charName = "[KHÔNG NẰM TRONG BẢN ĐỒ]";
                                    }} else {{
                                        // ĐỌC TÊN NẾU CÓ TRONG MAP (Tại +0xB2D)
                                        try {{
                                            var nameAddr = ptr("0x96700008").add(cId * 0xD5AC).add(0xB2D);
                                            // Dùng readCString để đọc thô mảng byte trên Android
                                            charName = nameAddr.readCString();
                                            if (!charName || charName.trim() === "") {{
                                                charName = "[Chuỗi rỗng]";
                                            }}
                                        }} catch (eName) {{
                                            charName = "[Lỗi đọc tên: " + eName.message + "]";
                                        }}
                                    }}
                                }} catch(eMap) {{
                                    charName = "[Lỗi check map: " + eMap.message + "]";
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
                // Bỏ qua vùng cấm
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
        print("[!] Không tìm thấy ứng dụng.")
        sys.exit()

    print(f"[*] Đang attach vào: {front_app.identifier} (PID: {front_app.pid})")
    session = device.attach(front_app.pid)

    script = session.create_script(js_code)
    script.load()
    script.exports_sync.scanrange()

    print("[*] Bấm Ctrl+C để thoát...")
    sys.stdin.read()
except Exception as e:
    print(f"[!] Lỗi: {e}")