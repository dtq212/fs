import tkinter as tk
from tkinter import ttk
import threading
import time


class GiaoDienHienThi:
    def __init__(self, root, shared_data, command_dict):
        self.root = root
        self.shared_data = shared_data
        self.command_dict = command_dict

        self.root.title("Phong Thần")
        self.root.geometry("450x900")
        self.root.resizable(False, True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight = 25, font = ("Arial", 9))
        style.configure("TLabelFrame", font = ("Arial", 10, "bold"))
        style.configure("TCheckbutton", font = ("Arial", 10))
        style.configure("Compact.TButton", padding = (4, 0))

        self.paned = ttk.PanedWindow(self.root, orient = tk.VERTICAL)
        self.paned.pack(fill = tk.BOTH, expand = True, padx = 2, pady = 2)

        self.frame_top = ttk.Frame(self.paned, height = 200)
        self.paned.add(self.frame_top, weight = 1)

        cols = ("tennhanvat", "phantramsinhluc", "phantramnoiluc", "tenbando")
        self.tree = ttk.Treeview(self.frame_top, columns = cols, show = "headings")

        self.tree.heading("tennhanvat", text = "Tên nhân vật")
        self.tree.heading("phantramsinhluc", text = "%SL")
        self.tree.heading("phantramnoiluc", text = "%NL")
        self.tree.heading("tenbando", text = "Tên bản đồ")

        self.tree.column("tennhanvat", width = 140, anchor = "w")
        self.tree.column("phantramsinhluc", width = 50, anchor = "center")
        self.tree.column("phantramnoiluc", width = 50, anchor = "center")
        self.tree.column("tenbando", width = 130, anchor = "w")

        vsb = ttk.Scrollbar(self.frame_top, orient = "vertical", command = self.tree.yview)
        self.tree.configure(yscroll = vsb.set)

        self.tree.pack(side = "left", fill = tk.BOTH, expand = True)
        vsb.pack(side = "right", fill = "y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select_char)

        self.custom_order = []
        self.drag_data = {"item": None}

        self.tree.bind("<ButtonPress-1>", self.on_drag_start)
        self.tree.bind("<B1-Motion>", self.on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_drag_release)

        self.frame_bot = ttk.Frame(self.paned)
        self.paned.add(self.frame_bot, weight = 3)

        self.grp_config = ttk.LabelFrame(self.frame_bot, text = " Trạng Thái & Phím Tắt ")
        self.grp_config.pack(fill = tk.BOTH, expand = True, padx = 5, pady = 2)

        self.vars_config = {}

        r = 0

        self.add_check(self.grp_config, "Tự động Farm & Bán rác", "_is_tudongfarm", r, "Ctrl+Alt+Shift+H", "battat_tudongfarm")
        r += 1
        self.add_check(self.grp_config, "Tự động vứt rác", "_is_tudongvutvatpham", r, "Ctrl+Alt+Shift+D", "battat_is_tudongvutvatpham")
        r += 1
        self.add_check(self.grp_config, "Tự động mua vật phẩm", "_is_tudongmuavatphamkytrancac", r, "Ctrl+Alt+Shift+M", "battat_is_tudongmuavatphamkytrancac")
        r += 1
        self.add_check(self.grp_config, "Đánh theo sau trưởng nhóm", "_is_tudongdanhtheosautruongnhom", r, "Ctrl+Alt+Shift+T", "battat_tudongdanhtheosautruongnhom")
        r += 1
        self.add_check(self.grp_config, "Tự bật / tắt lắc", "_is_tudongbattathieuungbotro", r, "Ctrl+Alt+Shift+J", "battat_is_tudongbattathieuungbotro")
        r += 1
        self.add_check(self.grp_config, "Phục sinh nhanh", "_is_phucsinhnhanh", r, "Ctrl+Alt+Shift+N", "battat_phucsinhnhanh")
        r += 1
        self.add_check(self.grp_config, "Tự động đổi sét đồ (Sét 1: Đánh, Sét 2: Chạy)", "_is_tudongdoisetdo", r, "Ctrl+Alt+Shift+W", "battat_is_tudongdoisetdo")
        r += 1
        lbl_guide_set = ttk.Label(self.grp_config, text = "[Ctrl+Alt+1/2] Lưu Sét Đồ 1/2", font = ("Arial", 9, "bold"))
        lbl_guide_set.grid(row = r, column = 0, sticky = "w", padx = 25, pady = (2, 2))
        r += 1

        self.lbl_set_1 = ttk.Label(self.grp_config, text = "→ Sét 1 (Đánh): Chưa lưu", foreground = "blue", wraplength = 380)
        self.lbl_set_1.grid(row = r, column = 0, sticky = "w", padx = 25, pady = (0, 2))
        r += 1

        self.lbl_set_2 = ttk.Label(self.grp_config, text = "→ Sét 2 (Chạy): Chưa lưu", foreground = "blue", wraplength = 380)
        self.lbl_set_2.grid(row = r, column = 0, sticky = "w", padx = 25, pady = (0, 5))
        r += 1

        ttk.Separator(self.grp_config, orient = "horizontal").grid(row = r, column = 0, sticky = "ew", pady = 2)
        r += 1
        self.add_check(self.grp_config, "Tự tìm mục tiêu", "_is_tudongtimkiemmuctieu", r, "Ctrl+Alt+Shift+F", "battat_tudongtimkiemmuctieu")
        r += 1
        self.add_check(self.grp_config, "Tự động đuổi mục tiêu", "_is_duoitheo", r, "Ctrl+Alt+Shift+P", "battat_is_duoitheo")
        r += 1
        self.add_check(self.grp_config, "Chỉ dùng 1 kỹ năng (Đạo sĩ)", "_is_khongsudungnhieukynang", r, "Ctrl+Alt+Shift+O", "battat_is_khongsudungnhieukynang")
        r += 1
        self.add_check(self.grp_config, "Không đánh cùng Bang", "_is_khongdanhcungbang", r, "Ctrl+Alt+Shift+B", "battat_is_khongdanhcungbang")
        r += 1
        ttk.Separator(self.grp_config, orient = "horizontal").grid(row = r, column = 0, sticky = "ew", pady = 2)
        r += 1
        self.add_check(self.grp_config, "Chỉ đánh Người / Phong quyển", "_is_chidanhnguoichoivatrieuhoithu", r, "Ctrl+D / Ctrl+A", "battat_is_chidanhnguoichoivatrieuhoithu")
        r += 1
        self.add_check(self.grp_config, "Ưu tiên đánh Phong quyển", "_is_uutientrieuhoithu", r, "Ctrl + S", "battat_is_uutientrieuhoithu")
        r += 1
        self.add_check(self.grp_config, "Giữ khoảng cách (Đạo sĩ)", "_is_giukhoangcach", r, "Ctrl+Alt+Shift+K", "battat_is_giukhoangcach")
        r += 1
        self.add_check(self.grp_config, "Đánh phủ đầu (Đạo sĩ / Vũ sĩ)", "_is_danhphudau", r, "", "battat_is_danhphudau")
        r += 1
        ttk.Separator(self.grp_config, orient = "horizontal").grid(row = r, column = 0, sticky = "ew", pady = 4)
        r += 1

        self.lbl_info_2 = ttk.Label(self.grp_config, text = "Tọa độ: (0, 0)")
        self.lbl_info_2.grid(row = r, column = 0, sticky = "w", padx = 10)
        r += 1

        self.lbl_info_farm = ttk.Label(self.grp_config, text = "Điểm Farm: ---")
        self.lbl_info_farm.grid(row = r, column = 0, sticky = "w", padx = 10)
        r += 1

        ttk.Separator(self.grp_config, orient = "horizontal").grid(row = r, column = 0, sticky = "ew", pady = 2)
        r += 1
        ttk.Separator(self.grp_config, orient = "horizontal").grid(row = r, column = 0, sticky = "ew", pady = 2)
        r += 1

        lbl_guide_tc = ttk.Label(self.grp_config, text = "[Ctrl+C] Thêm  |  [Ctrl+Alt+C] Xóa danh sách Tấn công", font = ("Arial", 9, "bold"))
        lbl_guide_tc.grid(row = r, column = 0, sticky = "w", padx = 10)
        r += 1

        self.add_check(self.grp_config, "Chỉ đánh theo tên trong danh sách", "_is_danhtheotennhanvat", r, "Ctrl+Alt+Shift+C", "battat_is_danhtheotennhanvat")
        r += 1

        frame_chon_nhanh = ttk.Frame(self.grp_config)
        frame_chon_nhanh.grid(row = r, column = 0, sticky = "w", padx = 10, pady = 2)
        r += 1

        self.cbo_nguoichoi = ttk.Combobox(frame_chon_nhanh, width = 22)
        self.cbo_nguoichoi.pack(side = "left", padx = (0, 5), fill = "y")
        btn_them_ui = ttk.Button(frame_chon_nhanh, text = "Thêm nhanh", command = self.on_them_tu_ui, style = "Compact.TButton")
        btn_them_ui.pack(side = "left", fill = "y")

        self.lbl_tennhanvattancongs = ttk.Label(self.grp_config, text = "→ Trống", foreground = "red", wraplength = 380)
        self.lbl_tennhanvattancongs.grid(row = r, column = 0, sticky = "w", padx = 10, pady = (0, 5))
        r += 1

        lbl_guide_ktc = ttk.Label(self.grp_config, text = "[Ctrl+X] Thêm  |  [Ctrl+Alt+X] Xóa danh sách Bỏ qua", font = ("Arial", 9, "bold"))
        lbl_guide_ktc.grid(row = r, column = 0, sticky = "w", padx = 10)
        r += 1

        self.lbl_tennhanvatkhongtancongs = ttk.Label(self.grp_config, text = "→ Trống", foreground = "green", wraplength = 380)
        self.lbl_tennhanvatkhongtancongs.grid(row = r, column = 0, sticky = "w", padx = 10, pady = (0, 5))
        r += 1

        self.current_hwnd = None
        self.is_running = True
        self.thread = threading.Thread(target = self.loop_update_ui, daemon = True)
        self.thread.start()

    def on_drag_start(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.drag_data["item"] = item

    def on_drag_motion(self, event):
        if not self.drag_data["item"]:
            return
        target_item = self.tree.identify_row(event.y)
        if target_item and target_item != self.drag_data["item"]:
            target_index = self.tree.index(target_item)
            self.tree.move(self.drag_data["item"], "", target_index)

    def on_drag_release(self, event):
        if self.drag_data["item"]:
            self.drag_data["item"] = None
            self.custom_order = [int(iid) for iid in self.tree.get_children()]

    def on_them_tu_ui(self):
        tennhanvatduocchon = self.cbo_nguoichoi.get().strip()
        if tennhanvatduocchon and self.current_hwnd:
            self.command_dict[self.current_hwnd] = f"them_tennhanvattancong_theotennhanvat:{tennhanvatduocchon}"
            self.cbo_nguoichoi.set("")

    def add_check(self, parent, text, key, r, shortcut, cmd_string):
        var = tk.BooleanVar()
        display_text = text
        if shortcut:
            display_text = f"{text}   [{shortcut}]"

        def on_toggle():
            if self.current_hwnd:
                self.command_dict[self.current_hwnd] = cmd_string

        chk = ttk.Checkbutton(parent, text = display_text, variable = var, command = on_toggle)
        chk.grid(row = r, column = 0, sticky = "w", padx = 10, pady = 0)
        self.vars_config[key] = var

    def on_select_char(self, event):
        sel = self.tree.selection()
        if sel:
            try:
                self.current_hwnd = int(sel[0])
                self.refresh_detail()
            except:
                pass

    def refresh_detail(self):
        if not self.current_hwnd or self.current_hwnd not in self.shared_data:
            self.lbl_tennhanvattancongs.config(text = "→ Trống")
            self.lbl_tennhanvatkhongtancongs.config(text = "→ Trống")
            return

        data = self.shared_data[self.current_hwnd]

        for key, var in self.vars_config.items():
            var.set(data.get(key, False))

        self.lbl_info_2.config(text = f"Tọa độ: {data.get('x', 0)}, {data.get('y', 0)} | Map: {data.get('tenbando', '-')}")

        farm_map = data.get("idbandotudongfarm", 0)
        farm_x = data.get("toadoxtudongfarm", 0)
        farm_y = data.get("toadoytudongfarm", 0)
        self.lbl_info_farm.config(text = f"Điểm Farm: ({farm_x}, {farm_y}) | ID Map: {farm_map}")

        str_tancong = data.get("_tennhanvattancongs", "")
        str_khongtancong = data.get("_tennhanvatkhongtancongs", "")

        if not str_tancong: str_tancong = "Trống"
        if not str_khongtancong: str_khongtancong = "Trống"

        self.lbl_tennhanvattancongs.config(text = f"→ {str_tancong}")
        self.lbl_tennhanvatkhongtancongs.config(text = f"→ {str_khongtancong}")

        str_tancong = data.get("_tennhanvattancongs", "")
        str_khongtancong = data.get("_tennhanvatkhongtancongs", "")

        if not str_tancong: str_tancong = "Trống"
        if not str_khongtancong: str_khongtancong = "Trống"

        self.lbl_tennhanvattancongs.config(text = f"→ {str_tancong}")
        self.lbl_tennhanvatkhongtancongs.config(text = f"→ {str_khongtancong}")

        set_1 = data.get("_setdo1_map", {})
        set_2 = data.get("_setdo2_map", {})

        str_set_1 = f"Cần đổi {len(set_1)} món ({', '.join(set_1.values())})" if set_1 else "Chưa lưu / Không có khác biệt"
        str_set_2 = f"Cần đổi {len(set_2)} món ({', '.join(set_2.values())})" if set_2 else "Chưa lưu / Không có khác biệt"

        self.lbl_set_1.config(text = f"→ Sét 1 (Đánh): {str_set_1}")
        self.lbl_set_2.config(text = f"→ Sét 2 (Chạy): {str_set_2}")

        tennguoichoixungquanhs = data.get("tennguoichoixungquanhs", [])
        current_values = self.cbo_nguoichoi["values"]

        if tuple(tennguoichoixungquanhs) != current_values:
            self.cbo_nguoichoi["values"] = tennguoichoixungquanhs
            if tennguoichoixungquanhs and not self.cbo_nguoichoi.get():
                self.cbo_nguoichoi.set(tennguoichoixungquanhs[0])
            elif not tennguoichoixungquanhs:
                self.cbo_nguoichoi.set("")

    def loop_update_ui(self):
        while self.is_running:
            try:
                raw_list = []
                for hwnd, data in self.shared_data.items():
                    raw_list.append((hwnd, data))

                def sort_key(item):
                    hwnd = item[0]
                    try:
                        return self.custom_order.index(hwnd)
                    except ValueError:
                        return 1_000_000

                sorted_list = sorted(raw_list, key = lambda x: (sort_key(x), x[1].get("tennhanvat", "").lower()))

                active_hwnds = [item[0] for item in sorted_list]
                active_focus_hwnd = None

                self.root.title(f"Phong Thần - {len(active_hwnds)} tài khoản đang online")

                items = self.tree.get_children()
                existing = {int(i): i for i in items}

                for index, (hwnd, data) in enumerate(sorted_list):
                    ten = data.get("tennhanvat", "Đang tải...")
                    hp = f"{data.get('phantramsinhluc', 0)}%"
                    mp = f"{data.get('phantramnoiluc', 0)}%"
                    bando = data.get("tenbando", "-")
                    is_active = data.get("is_window_active", False)

                    if is_active:
                        active_focus_hwnd = hwnd

                    values = (ten, hp, mp, bando)

                    if hwnd in existing:
                        self.tree.item(str(hwnd), values = values)
                        self.tree.move(str(hwnd), "", index)
                    else:
                        self.tree.insert("", index, iid = str(hwnd), values = values)

                for iid in items:
                    if int(iid) not in active_hwnds:
                        self.tree.delete(iid)

                if active_focus_hwnd:
                    if self.current_hwnd != active_focus_hwnd:
                        self.current_hwnd = active_focus_hwnd
                        try:
                            self.tree.selection_set(str(active_focus_hwnd))
                            self.tree.see(str(active_focus_hwnd))
                        except:
                            pass

                self.refresh_detail()

            except Exception:
                pass
            time.sleep(1.)
