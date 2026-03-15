import frida
import sys

js_code = """
rpc.exports = {
    findmodulebase: function() {
        var moduleName = "libcocos2dcpp.so";
        var baseAddress = null;

        try {
            var file = new File("/proc/self/maps", "r");
            var line;
            while ((line = file.readLine()) !== null) {
                if (line.indexOf(moduleName) !== -1) {
                    var addressRange = line.split(" ")[0];
                    var baseStr = addressRange.split("-")[0];
                    baseAddress = "0x" + baseStr;
                    break; 
                }
            }
            file.close();
        } catch (e) {
            return { "status": "error", "message": "Không thể đọc file maps: " + e.message };
        }

        if (baseAddress) {
            return { "status": "success", "base": baseAddress };
        } else {
            return { "status": "error", "message": "Thực sự không thấy bóng dáng libcocos2dcpp.so trong maps!" };
        }
    }
};
"""

try:
    device = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
    front_app = device.get_frontmost_application()

    if not front_app:
        print("[!] Lỗi: Game chưa mở hoặc chưa hiện trên màn hình.")
        sys.exit()

    print(f"[*] Đang thọc vào PID: {front_app.pid}")
    session = device.attach(front_app.pid)
    script = session.create_script(js_code)
    script.load()

    result = script.exports_sync.findmodulebase()

    if result['status'] == 'success':
        print("\n" + "=" * 50)
        print(f"[+] TÌM THẤY RỒI!")
        print(f"    Module: libcocos2dcpp.so")
        print(f"    Base Address: {result['base']}")
        print("=" * 50)
        print(f"[*] Giờ ông lấy {result['base']} cộng với offset tĩnh là ra lúa nhé.")
    else:
        print(f"\n[!] Thất bại: {result['message']}")

    session.detach()
except Exception as e:
    print(f"[!] Lỗi: {e}")