import tkinter as tk

class ALPwindow(tk.Tk):
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
    
if __name__ == "__main__":
    win = ALPwindow("test")
    win.run()