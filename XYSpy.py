import os
import re
import threading
from tkinter import messagebox

import customtkinter as ctk
import keyboard
import pyautogui
import pyperclip
import pystray
from PIL import Image

# 初始化窗口
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
import locale


def get_system_language():
    try:
        lang, _ = locale.getlocale()
        if not lang:
            lang = locale.getdefaultlocale()[0]  # 兼容旧环境
        if lang is None:
            lang = locale.getpreferredencoding(False)
        if lang and (key in lang.lower() for key in ['china', 'chinese', 'zh', 'cp936']):
            return 'zh'
        else:
            return 'en'
    except Exception as e:
        # print("语言检测失败:", type(e).__name__, e)
        return 'zh'


class MouseTrackerApp:
    def __init__(self, root):
        self.lang = get_system_language()
        self.text = LANG[self.lang]
        # 测试英文
        # self.text = LANG['en']

        self.root = root
        self.root.title(self.text['title'])
        self.root.attributes('-topmost', True)
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 设置图标路径
        icon_path = os.path.join(os.path.dirname(__file__), r"images\xy_logo_com.ico")  # 图标文件路径
        self.root.iconbitmap(icon_path)  # 设置窗口图标

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        top_frame.grid_columnconfigure(1, weight=1)

        self.help_button = ctk.CTkButton(top_frame, text="?", width=30, command=self.show_help)
        self.help_button.grid(row=0, column=0, padx=(0, 5))

        self.label = ctk.CTkLabel(top_frame, text=self.text['pos_label'], fg_color="transparent")
        self.label.grid(row=0, column=1, sticky="ew")

        self.textbox = ctk.CTkTextbox(self.root, wrap="none")
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 0))
        self.textbox.bind("<MouseWheel>", self.scroll_to_bottom)

        self.button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, pady=10)

        self.clear_button = ctk.CTkButton(self.button_frame, text=self.text['btn_clear'], command=self.clear_textbox)
        self.clear_button.grid(row=0, column=0, padx=10)

        self.move_button = ctk.CTkButton(self.button_frame, text=self.text['btn_move'], command=self.move_to_position)
        self.move_button.grid(row=0, column=1, padx=10)

        self.start_key_listener()
        threading.Thread(target=self.setup_tray_icon, daemon=True).start()
        self.root.after(80, self.update_mouse_position)

    def on_closing(self):
        self.quit_app()

    def scroll_to_bottom(self, event=None):
        self.textbox.yview_moveto(1.0)
        return "break"

    def clear_textbox(self):
        self.textbox.delete("1.0", "end")

    def move_to_position(self):
        content = self.textbox.get("1.0", "end").strip().splitlines()
        if not content:
            # 无内容
            self.textbox.insert("end", f"{self.text['tip_1']}")
            return
        last = content[-1]
        match = re.match(r"\((\d+),(\d+)\)", last)
        if not match:
            # 格式无效
            self.textbox.insert("end", f"{self.text['tip_2']}")
            return
        try:
            x, y = map(int, match.groups())
            pyautogui.moveTo(x, y)
        except Exception as e:
            # 移动失败
            self.textbox.insert("end", f"{self.text['tip_3']}: {type(e).__name__}: {e}\n")

    def record_position(self):
        x, y = pyautogui.position()
        coord = f"({x},{y})\n"
        self.textbox.insert("end", coord)
        pyperclip.copy(f"({x},{y})")
        self.scroll_to_bottom()

    def start_key_listener(self):
        def on_key_event(e):
            if e.name == 'alt' and e.event_type == keyboard.KEY_DOWN:
                self.record_position()

        keyboard.hook(on_key_event)

    def quit_app(self):
        if self.icon:
            self.icon.visible = False
            self.icon.stop()
        self.root.quit()

    def setup_tray_icon(self):
        title = f"{self.text['title']}"
        icon_path = os.path.join(os.path.dirname(__file__), r"images\xy_logo_com.ico")
        image = Image.open(icon_path)  # 打开图片文件
        menu = pystray.Menu(pystray.MenuItem(f"{self.text['tray_exit']}", self.quit_app))
        self.icon = pystray.Icon(title, image, title, menu)
        self.icon.run()

    def update_mouse_position(self):
        x, y = pyautogui.position()
        self.label.configure(text=f"{self.text['pos_label']}: ({x},{y})")
        self.root.after(100, self.update_mouse_position)

    def show_help(self):
        messagebox.showinfo(self.text['help_title'], self.text['help_text'])


LANG = {
    'zh': {
        'title': '鼠标定位器XYSpy',
        'pos_label': '鼠标当前位置',
        'btn_clear': '清空',
        'btn_move': '移动到位置',
        'help_text': '按下 Alt 键记录鼠标坐标\n坐标会自动复制到剪切板\n点击“移动到位置”会移动到最后记录的位置',
        'help_title': '使用说明',
        'tip_1': '无内容\n',
        'tip_2': '格式无效\n',
        'tip_3': '移动失败',
        'tray_exit': '退出',
        'btn_ok': '确定',
    },
    'en': {
        'title': 'Mouse Locator XYSpy',
        'pos_label': 'Mouse Position',
        'btn_clear': 'Clear',
        'btn_move': 'Move to Position',
        'help_text': 'Press Alt to record mouse position\nIt will be copied to clipboard\nClick "Move to Position" to move to the last recorded point',
        'help_title': 'Instructions',
        'tip_1': 'No content\n',
        'tip_2': 'Invalid format\n',
        'tip_3': 'Move failed',
        'tray_exit': 'Exit',
        'btn_ok': 'OK',
    }
}
# =============== 打包程序 =================
# pyinstaller --upx-dir=D:\Tool\upx-5.0.0-win64\upx.exe -w --onefile --add-data "images;images" --icon=images\xy_logo_com.ico --manifest admin.manifest --clean XYSpy.py
# rmdir /s /q build  或  Remove-Item -Recurse -Force .\build
# --upx-dir=~\upx-5.0.0-win64\upx.exe       使用 UPX 压缩 PyInstaller 打包体积, 安装 UPX：https://upx.github.io/ 【可选】
# --windowed或-w                            用于创建一个没有控制台窗口(cmd.exe)的应用程序
# --onefile或-F                             将所有文件打包成一个单独的可执行文件, 包含所有的代码、库和资源
# --add-data "源文件路径;目标路径"             打包资源文件或目录
# --icon=images\xy_logo_com.ico             图标
# --manifest admin.manifest                 显式设置 EXE 的 manifest 来请求管理员权限
# --clean                                   自动清除旧的 build/ 缓存
# XYSpy.py                                  Python脚本
# rmdir /s /q build                         cmd.exe 删除 build 文件夹
# Remove-Item -Recurse -Force .\build       PowerShell 删除 build 文件夹
if __name__ == "__main__":
    root = ctk.CTk()
    app = MouseTrackerApp(root)
    root.mainloop()
