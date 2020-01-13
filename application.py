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
        self.manga_numbers = tuple([os.path.basename(m) for m in glob.glob(os.path.join(archive_directory, manga_title + os.sep + "*"))])


class ImageViewer():
    def __init__(self, root=None):
        # 設定読み込み
        with open("settings.json", mode="r", encoding="utf-8") as f:
            self.settings = json.load(f)
        
        self.setting_info = SettingInfo(self.settings)
        self.application_info = ApplicationInfo(self.settings)
        self.init(root)
    
    def init(self, root=None):
        ### window_main
        root.title(self.setting_info.title + " " + self.setting_info.version)
        root.geometry(self.setting_info.width + "x" + self.setting_info.height)

        ## Frame_Explorer
        self.Frame_Explorer = ttk.Labelframe(root, text="漫画を選択する",
                                        borderwidth=7, relief="ridge")
        self.Frame_Explorer.grid(column=0, row=0)
        # widget
        self.label_manga = ttk.Label(self.Frame_Explorer, text="title", padding=5)
        self.label_manga.grid(column=0, row=0)

        self.value_manga_title = tk.StringVar()
        self.combobox_mangatitle = ttk.Combobox(self.Frame_Explorer, textvariable=self.value_manga_title, width=20)
        self.combobox_mangatitle.bind("<<ComboboxSelected>>", self.select_combobox_manga_title)
        self.combobox_mangatitle["values"] = self.application_info.manga_titles
        self.combobox_mangatitle.grid(column=1, row=0)

        self.label_number = ttk.Label(self.Frame_Explorer, text="話数", padding=5)
        self.label_number.grid(column=0, row=1)

        self.value_manga_number = tk.StringVar()
        self.combobox_manganumber = ttk.Combobox(self.Frame_Explorer, textvariable=self.value_manga_number, width=20)
        self.combobox_manganumber.grid(column=1, row=1)


        # Frame_commonSetting
        Frame_commonSetting = ttk.Labelframe(root, text="共通設定")
        Frame_commonSetting.grid(column=0, row=1)

        # wigdet
        
        label1 = ttk.Label(Frame_commonSetting, text="label1")
        label1.grid(column=0, row=0)

    def popup_error(self, title, message):
        tk.messagebox.showerror(title, message)



    ###
    ### application event method
    ###
    def select_combobox_manga_title(self, event):
        self.application_info.manga_title = self.value_manga_title.get()
        self.application_info.set_manga_numbers(self.application_info.archive_directory, self.application_info.manga_title)
        self.combobox_manganumber["values"] = self.application_info.manga_numbers
        self.combobox_manganumber.set("")




if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()


# Todo
"""
OK 漫画選択後に話数フォルダをcomboboxに表示する

共通設定：ラジオボタン１、２
　⇒ 基数偶数入れ替え
　　　　：チェックボックス
　⇒ 一枚表示（デフォルトは2枚表示）

イメージ表示枠：右・左
　⇒ 表示の大きさは左右同じ
　⇒ 画像自体は真ん中寄せで作成する

ラベル：イメージ表示枠の下にススム戻るボタン
　⇒ 進める。戻れる場合のみ表示、できない場合は薄く表示され、クリックはできないようにする
"""