import customtkinter as ctk
from tkinter import ttk

class UniversalTable(ctk.CTkFrame):
    def __init__(self, master, data_list=None, empty_message="No data available", **kwargs):
        super().__init__(master, **kwargs)
        
        self.data_list = data_list or []
        self.empty_message = empty_message

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True)

        self.table = ttk.Treeview(self.table_frame, show="headings")
        self.table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=scrollbar.set)

        self.display_data(self.data_list)

    def display_data(self, data_list):
        self.table.delete(*self.table.get_children())
        self.table["columns"] = []

        if data_list:
            headers = list(data_list[0].keys())
            self.table["columns"] = headers

            for header in headers:
                self.table.heading(header, text=header)
                self.table.column(header, minwidth=100, width=150, stretch=True)
            
            for item in data_list:
                values = [item[key] for key in headers]
                self.table.insert("", "end", values=values)
        else:
            self.table["columns"] = ("Message",)
            self.table.heading("Message", text="")
            self.table.column("Message", minwidth=200, anchor="center")
            self.table.insert("", "end", values=(self.empty_message,))
