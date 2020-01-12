import tkinter as tk
from tkinter import ttk
import glob
import os
import json

class SettingInfo:
    def __init__(self, settings):
        self.title = settings["Application"]["title"]
        self.version = settings["Application"]["version"]
        self.width = settings["Application"]["width"]
        self.height = settings["Application"]["height"]
        self.archive_directory = settings["Application"]["ArchiveDirectory"]

class ApplicationInfo:
    def __init__(self, settings):
        self.archive_directory = settings["Application"]["ArchiveDirectory"]
        self.manga_titles = tuple(self.get_manga_titles(self.archive_directory))
        self.manga_title = ""
        self.manga_numbers = ""
        self.manga_number = ""
    
    def get_manga_titles(self, archive_directory):
        return [os.path.basename(m) for m in glob.glob(os.path.join(archive_directory, "*"))]
    
    def set_manga_numbers(self, archive_directory, manga_title):
        return tuple([os.path.basename(m) for m in glob.glob(os.path.join(archive_directory, manga_title + os.sep + "*"))])


class ImageViewer():
    def __init__(self, root=None):
        # 設定読み込み
        with open("settings.json", mode="r", encoding="utf-8") as f:
            self.settings = json.load(f)
        
        self.setting_info = SettingInfo(self.settings)
        self.application_info = ApplicationInfo(self.settings)
        self.init(root)
    
    def init(self, root=None):
        ### window
        ### name : window_main
        root.title(self.setting_info.title + " " + self.setting_info.version)
        root.geometry(self.setting_info.width + "x" + self.setting_info.height)

        ### Frame
        ### name : Frame_Explorer
        Frame_Explorer = ttk.Labelframe(root, text="漫画を選択する",
                                        borderwidth=7, relief="ridge")
        Frame_Explorer.grid(column=0, row=0)
        ### widget
        label_manga = ttk.Label(Frame_Explorer, text="manga", padding=5)
        label_manga.grid(column=0, row=0)

        self.value_manga_title = tk.StringVar()
        combobox_mangatitle = ttk.Combobox(Frame_Explorer, textvariable=self.value_manga_title, width=20)
        combobox_mangatitle.bind("<<ComboboxSelected>>", self.select_combobox_manga_title)
        combobox_mangatitle["values"] = self.application_info.manga_titles
        combobox_mangatitle.grid(column=1, row=0)

        label_number = ttk.Label(Frame_Explorer, text="話数", padding=5)
        label_number.grid(column=0, row=1)

        self.value_manga_number = tk.StringVar()
        self.combobox_manganumber = ttk.Combobox(Frame_Explorer, textvariable=self.value_manga_number, width=20)
        # combobox_manganumber.bind("<<ComboboxSelected>>", self.select_combobox_manga_title)
        # combobox_manganumber["values"] = self.application_info.manga_numbers
        self.combobox_manganumber.grid(column=1, row=1)


        # Frame_commonSetting
        Frame_commonSetting = ttk.Labelframe(root, text="共通設定")
        Frame_commonSetting.grid(column=0, row=1)

        # wigdet
        
        label1 = ttk.Label(Frame_commonSetting, text="label1")
        label1.grid(column=0, row=0)


    
    def create_pane(self):
        self.pw_main = tk.PanedWindow(self, orient="horizontal", bg="blue")
        self.pw_main.pack(expand=True, fill=tk.BOTH, side="left")

        self.pw_left = tk.PanedWindow(self.pw_main, bg="cyan", orient='vertical')
        self.pw_main.add(self.pw_left)
        self.pw_right = tk.PanedWindow(self.pw_main, bg="yellow", orient='vertical')
        self.pw_main.add(self.pw_right)

    def create_widgets(self):
        self.hi_there = tk.Button(self, text="Hello World\n(click me)",
                                  command=self.say_hi, bg="yellow")
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def popup_error(self, title, message):
        tk.messagebox.showerror(title, message)

    ###
    ### application event method
    ###
    def say_hi(self):
        print("hi there, everyone!")
    
    def select_combobox_manga_title(self, event):
        self.application_info.manga_title = self.value_manga_title.get()
        self.application_info.set_manga_numbers(self.application_info.archive_directory, self.application_info.manga_title)
        self.combobox_manganumber["values"] = self.application_info.manga_numbers
        print(self.application_info.manga_title)




if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()


# Todo
"""
漫画選択後に話数フォルダをcomboboxに表示する
"""