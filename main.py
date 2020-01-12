import tkinter as tk
import application as app

def main():
    """main"""
    try:
        root = tk.Tk()
        application = app.ImageViewer(root)
        root.mainloop()
    except Exception as e:
        application.popup_error("予期しないError", e)
    finally:
        # 初期化などの実装が必要？
        pass        

if __name__ == "__main__":
    main()
