import tkinter as tk
from tkinter import ttk

import ALPtest
import os
import threading

class Testwindow(tk.Tk):
    def __init__(self, windowName):
        super().__init__()
        self.title(windowName)
        self.geometry("600x400")
        self.label = tk.Label(self, text="Hello, world!")
        
        self.tools() # 组件
        self.layOut()
        
    def run(self):
        self.mainloop()
        
    def clickRun(self, type):
        if type == "click":
            text = self.entry.get()
            if not text:
                if hasattr(self, "errwindow") and self.errwindow.winfo_exists():
                    self.errwindow.destroy()
                    return
                self.errwindow = tk.Toplevel(self)
                self.errwindow.title("Error")
                self.errwindow.geometry("200x100")
                self.errlabel = tk.Label(self.errwindow, text="Please input something!")
                self.errlabel.pack()
                return
        elif type == "New":
            print("New")
            pass
            return
        
        self.label.config(text="Hello, ALP! {text}".format(text=text))
        self.entry.delete(0, tk.END)
    
    def tools(self):
        self.entry = tk.Entry(self, width=20)
        self.entry.bind("<Return>", lambda x: self.clickRun("click"))
        
        self.text_box = tk.Text(self, width=40, height=10)
        self.text_box.grid(row=3, column=0, pady=10)
        
        # 菜单
        self.menu = tk.Menu(self)
        
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="New", command=lambda: self.clickRun("New"))
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        # 将 File 添加到菜单
        self.menu.add_cascade(label="File", menu=file_menu)
        
        edit_menu = tk.Menu(self.menu, tearoff=0)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        
        self.config(menu=self.menu)

        button = tk.Button(self, text="click", command=lambda :self.clickRun("click"))
        # button.pack(pady=10)
        button.grid(row=2, column=0, pady=10)
    
    def layOut(self):
        self.label.grid(row=0, column=0, pady=10)
        self.entry.grid(row=1, column=0, pady=10)


class ALPwindow(tk.Tk):
    window = tk.Tk()
    
    def __init__(self, windowName):
        self.window.title(windowName)
        self.window.geometry("600x400")
        
    def addButtons(self, id, buttonName: str):
        button = tk.Button(self.window, text=buttonName, command=lambda :self.clickRun(buttonName))
        button.pack(padx=10, pady=10)
    
    def dropMenu(self, options: list):
        '''
        下拉菜单
        '''
        self.COMbox = ttk.Combobox(self.window, values=options)
        self.COMbox.current(0) # 默认
        self.COMbox.pack(pady=20)
        
        COMbtn = tk.Button(self.window, text="打开串口", command=lambda: self.clickRun(self.COMbox.get()))
        COMbtn.pack(pady=10)
        
    def run(self):
        self.window.mainloop()
        
    def clickRun(self, type: str):
        if type == "click":
            print("click")
            return
        elif type == "New":
            print("New")
            return
        elif type == "Save":
            print("Save")
            # 使用线程避免阻塞
            thread = threading.Thread(target=ALPtest.serialSave)
            thread.daemon = True
            thread.start()
            return
        elif type == "Exit":
            # 退出
            print(f"已保存数据至 {os.getcwd()}") # 当前工作路径
            self.window.destroy()
            exit(0)
            return
        #  提取出COM后面的数字
        if "COM" in type:
            ALPtest.serialPortOpen(type, 115200)
            print(f"打开串口{type},波特率为115200")
            return



class DropdownCombobox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Combobox 下拉选项卡")
        self.geometry("300x200")
        
        # 定义多个选项
        options = ["选项A", "选项B", "选项C", "选项D", "选项E"]
        
        # 创建 Combobox
        self.combobox =ttk.Combobox(self, values=options)
        self.combobox.current(0)  # 设置默认选项
        self.combobox.pack(pady=20)
        
        # 按钮用于打印选中的选项
        btn = tk.Button(self, text="打印选择", command=self.print_option)
        btn.pack(pady=10)
        
    def print_option(self):
        print("当前选择：", self.combobox.get())
        

if __name__ == "__main__":
    # win = Testwindow("test")
    # win.run()
    win = ALPwindow("ALP")
    win.run()
    
    # app = DropdownCombobox()
    # app.mainloop()