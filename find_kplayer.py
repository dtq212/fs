import frida
import sys

js_code = """
function hookUseItem() {
    try {
        // Dùng địa chỉ tuyệt đối y hệt cách ông làm, miễn nhiễm mọi lỗi API!
        var useItemAddr = ptr("0x04769374"); 

        Interceptor.attach(useItemAddr, {
            onEnter: function(args) {
                var p1 = args[0];
                var id = args[1];
                send({
                    type: 'result', 
                    p1: p1.toString(), 
                    id: parseInt(id.toString())
                });
            }
        });
    } catch (e) {
        send({type: 'error', msg: e.message});
    }
}

// Gọi hàm trực tiếp không cần setTimeout
hookUseItem();
"""


def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        if payload.get('type') == 'result':
            print(f"\n[!] BÙM! ĐÃ TÓM ĐƯỢC HÀM USE_ITEM!")
            print(f" -> param_1 (Con trỏ KPlayer thật): {payload['p1']}")
            print(f" -> ID Vật phẩm (Slot): {payload['id']}")
            print("====================================")
        elif payload.get('type') == 'error':
            print(f"[-] Lỗi JS: {payload['msg']}")
    else:
        print(message)


try:
    device = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
    front_app = device.get_frontmost_application()

    if not front_app:
        print("[!] Không tìm thấy ứng dụng.")
        sys.exit()

    print(f"[*] Đang attach vào: {front_app.identifier} (PID: {front_app.pid})")
    session = device.attach(front_app.pid)

    script = session.create_script(js_code)
    script.on('message', on_message)
    script.load()

    print("[*] Tool đã sẵn sàng! Vào game mở túi đồ và uống 1 bình máu đi đại hiệp.")
    sys.stdin.read()
except Exception as e:
    print(f"[!] Lỗi: {e}")