import frida
import sys

js_code = """
// Khai báo biến toàn cục để lưu trữ trạng thái, không bị mất context
var targetAddr = null;
var useSkillCall = null;
var fakeThis = null;
var pendingCast = false;
var skillID = 0;
var targetX = 0;
var targetY = 0;

rpc.exports = {
    setup: function(baseAddress) {
        try {
            var libBase = ptr(baseAddress);
            // Tọa độ hàm UseSkill (04732240 - 04000000 = 0x732240)
            targetAddr = libBase.add(0x732240);

            // Ép kiểu hàm
            useSkillCall = new NativeFunction(targetAddr, 'int', ['pointer', 'int', 'int', 'int', 'int']);
            fakeThis = Memory.alloc(0x100); // Tạo vùng nhớ giả cho con trỏ 'this'

            console.log("[*] Đã gài bom NativeFunction tại: " + targetAddr);

            // TÌM HÀM ĐỂ KÝ SINH (Trực tiếp chỉ định libc.so để chống lỗi JS)
            var hookTarget = Module.findExportByName("libc.so", "gettimeofday");

            if (!hookTarget) {
                return "[-] Toang, không tìm thấy hàm gettimeofday của libc.so!";
            }

            // Đặt trạm thu phí vào hàm hệ thống
            Interceptor.attach(hookTarget, {
                onEnter: function(args) {
                    // Nếu Python có lệnh nạp đạn -> BÓP CÒ BẰNG CHÍNH LUỒNG CỦA GAME!
                    if (pendingCast) {
                        pendingCast = false; // Tắt cờ ngay lập tức để không xả liên thanh
                        try {
                            // Tham số 4 là -1 để khóa mục tiêu tự động/AOE
                            useSkillCall(fakeThis, targetX, targetY, skillID, -1);
                            console.log("[+] BÙM! Đã mượn luồng thành công, BYPASS khoảng cách 500!");
                        } catch (e) {
                            console.log("[-] Lỗi khi gọi hàm bên trong luồng: " + e.message);
                        }
                    }
                }
            });

            return "[+] Setup hệ thống Ký sinh luồng thành công!";
        } catch(e) {
            return "[-] Lỗi sập lúc Setup: " + e.message;
        }
    },

    // Hàm trigger giống hệt cách ông dùng write_int trên PC
    triggercast: function(id, x, y) {
        skillID = id;
        targetX = x;
        targetY = y;
        pendingCast = true; 
        return "Đã nạp đạn vào luồng, chờ game múa chiêu ở cự ly 600!";
    }
};
"""

try:
    device = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
    front_app = device.get_frontmost_application()

    if not front_app:
        print("[!] Lỗi: Game chưa mở.")
        sys.exit()

    print(f"[*] Đang móc vào PID: {front_app.pid}")
    session = device.attach(front_app.pid)

    script = session.create_script(js_code)
    # Lắng nghe log console.log từ JS bắn lên
    script.on('message', lambda msg, data: print(msg['payload']) if msg['type'] == 'send' else None)
    script.load()

    # 1. SETUP KÝ SINH (Truyền đúng Base Address ông tìm được vào đây)
    BASE_ADDRESS = "0x04000000"
    print(script.exports_sync.setup(BASE_ADDRESS))

    # 2. TRIGGER ĐÁNH CHẶN TỪ XA
    skill_can_danh = 9
    toa_do_X = 55361
    toa_do_Y = 108834
    print(f"\n[*] Ra lệnh ép Cast Skill {skill_can_danh} vào X:{toa_do_X}, Y:{toa_do_Y} ...")
    print(script.exports_sync.triggercast(skill_can_danh, toa_do_X, toa_do_Y))

    sys.stdin.read()
except Exception as e:
    print(f"[!] Lỗi: {e}")