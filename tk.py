import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # 設定
        settings = {
            "title": "ImageViewer",
            "width": "1000",
            "height" : "600"
        }
        self.master.title = settings["title"]
        self.master.geometry(settings["width"] + "x" + settings["height"])
        self.pack()
        # self.create_pane()
        self.create_widgets()
    
    def create_pane(self):
        self.pw_main = tk.PanedWindow(self, orient="horizontal", bg="blue")
        self.pw_main.pack(expand=True, fill=tk.BOTH, side="left")

    def create_widgets(self):
        self.hi_there = tk.Button(self, text="Hello World\n(click me)",
                                  command=self.say_hi, bg="yellow")
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()