import tkinter as tk
from tkinter import ttk
import glob
import os
import json
import decimal
from PIL import Image, ImageTk

class SettingInfo:
    def __init__(self, settings):
        self.title = settings["Application"]["title"]
        self.version = settings["Application"]["version"]
        self.width = settings["Application"]["width"]
        self.height = settings["Application"]["height"]
        self.archive_directory = settings["Application"]["ArchiveDirectory"]
        self.setting_area_width = settings["Application"]["settingAreaWidth"]

class ApplicationInfo:
    def __init__(self, settings):
        self.archive_directory = settings["Application"]["ArchiveDirectory"]
        self.manga_titles = tuple(self.get_manga_titles(self.archive_directory))
        self.manga_title = ""
        self.manga_numbers = ""
        self.manga_number = ""
        self.radiobutton_LR_value = tk.StringVar()
    
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
        self.create_image_area()
    
    def init(self, root=None):
        #### window_main
        root.title(self.setting_info.title + " " + self.setting_info.version)
        root.geometry(self.setting_info.width + "x" + self.setting_info.height)

        #### PanedWindow_main
        self.PanedWindow_main = tk.PanedWindow(root)
        self.PanedWindow_main.place(relheight=1, relwidth=1)
        ### PanedWindow_settings
        self.PanedWindow_settings = tk.PanedWindow(self.PanedWindow_main, orient="vertical",
                                                   bg="black",
                                                   width=self.setting_info.setting_area_width)
        self.PanedWindow_main.add(self.PanedWindow_settings)
        ### PanedWindow_ImageArea
        self.PanedWindow_ImageArea = tk.PanedWindow(self.PanedWindow_main, bg="black")
        self.PanedWindow_main.add(self.PanedWindow_ImageArea)


        ### Frame_Left
        self.Frame_Left = ttk.Frame(self.PanedWindow_settings, borderwidth=2, relief=tk.RIDGE)
        self.Frame_Left.place(relheight=1, relwidth=1)

        ## Frame_Explorer
        self.Frame_Explorer = ttk.Labelframe(self.Frame_Left, text="漫画を選択する",
                                             borderwidth=7, relief=tk.RIDGE)
        self.Frame_Explorer.grid(sticky=tk.NS)
        # widget
        self.label_manga = ttk.Label(self.Frame_Explorer, text="title", padding=5)
        self.label_manga.grid(column=0, row=0)

        self.value_manga_title = tk.StringVar()
        self.combobox_mangatitle = ttk.Combobox(self.Frame_Explorer,
                                                textvariable=self.value_manga_title, width=20)
        self.combobox_mangatitle.bind("<<ComboboxSelected>>", self.select_combobox_manga_title)
        self.combobox_mangatitle["values"] = self.application_info.manga_titles
        self.combobox_mangatitle.grid(column=1, row=0)

        self.label_number = ttk.Label(self.Frame_Explorer, text="話数", padding=5)
        self.label_number.grid(column=0, row=1)

        self.value_manga_number = tk.StringVar()
        self.combobox_manganumber = ttk.Combobox(self.Frame_Explorer,
                                                 textvariable=self.value_manga_number, width=20)
        self.combobox_manganumber.grid(column=1, row=1)


        ## Frame_CommonSetting
        self.Frame_CommonSetting = ttk.Labelframe(self.Frame_Left, text="共通設定")
        self.Frame_CommonSetting.grid(sticky=tk.EW)

        # Frame_Label_LR
        self.Frame_Label_LR = ttk.Labelframe(self.Frame_CommonSetting, text="表示方法")
        self.Frame_Label_LR.grid(sticky=tk.EW)
        # wigdet
        self.radiobutton_L = ttk.Radiobutton(self.Frame_Label_LR, text="奇数", value="odd",
                                             variable=self.application_info.radiobutton_LR_value,
                                             command=self.click_radiobutton_LR)
        self.radiobutton_R = ttk.Radiobutton(self.Frame_Label_LR, text="偶数", value="even",
                                             variable=self.application_info.radiobutton_LR_value,
                                             command=self.click_radiobutton_LR)
        self.radiobutton_C = ttk.Radiobutton(self.Frame_Label_LR, text="一枚", value="center",
                                             variable=self.application_info.radiobutton_LR_value,
                                             command=self.click_radiobutton_LR)
        self.radiobutton_L.grid(sticky=tk.E)
        self.radiobutton_R.grid(sticky=tk.E)
        self.radiobutton_C.grid(sticky=tk.E)

        self.button_read = ttk.Button(self.Frame_Left, text="読み込み", command=self.click_button_read)
        self.button_read.grid(sticky=tk.EW)


    def create_image_area(self):
        ### PanedWindow_Image_Area_Left
        self.PanedWindow_Image_Area_Left = tk.PanedWindow(self.PanedWindow_ImageArea)
        self.PanedWindow_ImageArea.add(self.PanedWindow_Image_Area_Left)

        ### PanedWindow_Image_Area_Right
        self.PanedWindow_Image_Area_Right = tk.PanedWindow(self.PanedWindow_ImageArea)
        self.PanedWindow_ImageArea.add(self.PanedWindow_Image_Area_Right)

        ## Frame_Image_Left
        self.Frame_Image_Left = tk.Canvas(self.PanedWindow_Image_Area_Left, width=400, height=300, bg="black")
        self.Frame_Image_Left.grid(sticky=tk.W+tk.NS)
        
        # image = Image.open(r"C:\Users\swk22\OneDrive\デスクトップ\workspace\開発\Download_urasunday\archive\3インチ\第41話\001.png")
        self.image = tk.PhotoImage(file="001.png")
        print(self.image.width(),self.image.height())
        self.Frame_Image_Left.create_image(0,0, image=self.image, anchor=tk.W)
    
    def redraw_Image_Area(self):
        pass

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
    
    def click_radiobutton_LR(self):
        # 左右を入れ替える、というより再描画
        self.redraw_Image_Area()
    
    def click_button_read(self):
        print("push button")
        pass

    
    def set_application_info(self, key, value):
        self.application_info.key = value



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()


# Todo
"""
OK 漫画選択後に話数フォルダをcomboboxに表示する

OK 共通設定：ラジオボタン１、２
　⇒ 基数偶数入れ替え
　　　　：チェックボックス
　⇒ 一枚表示（デフォルトは2枚表示）

イメージ表示枠：右・左
　⇒ 表示の大きさは左右同じ
　⇒ 画像自体は真ん中寄せで作成する

ラベル：イメージ表示枠の下にススム戻るボタン
　⇒ 進める。戻れる場合のみ表示、できない場合は薄く表示され、クリックはできないようにする
"""