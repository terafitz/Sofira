from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import expense as exp
import financedata as fd
import filehandle as fh
import tkinter as tk
import os


class Window(tk.Tk):
    def __init__(self, title, theme, version):

        # Main
        super().__init__()
        self.title(title)
        self.geometry("800x600")
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", theme)
        self.settings = fh.readFile('settings.txt')
        self.menu = Menu(self, version)
        # change the settings file into JSON or similar, so you can name the configuration entries
        # instead of "settings[9]" settings.filename or similar offers a better developer experience
        if self.settings[9][:-1] == '':
            self.menu.create_file(filename="standard")
        self.finance = fd.FinanceData(self.settings[9][:-1])

        # Widgets
        self.main = Main(self)
        self.bottom = Bottom(self)
        self.listbutton = ListButton(self)

        # run
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent, version):
        super().__init__(parent)
        self.parent = parent
        self.leftframe = ttk.Frame(self)
        self.rightframe = ttk.Frame(self)
        # maybe consolidate all these lines into one object!
        ttk.Button(self.leftframe, text="Quit", command=parent.quit).pack(side="left", padx=5)
        ttk.Button(self.leftframe, text="Open...", command=self.open).pack(side="left")
        ttk.Button(self.leftframe, text="About...", command=self.showAbout).pack(side="left", padx=5)
        ttk.Button(self.leftframe, text="reload Data", command=self.reload).pack(side='left')
        self.abWin1 = None
        self.abWin2 = None
        self.abWin3 = None
        self.abWin4 = None
        self.version = version

        self.settingsIcon = ImageTk.PhotoImage(Image.open("icons/setting.png").resize((30, 30), Image.Resampling.LANCZOS))
        ttk.Button(self.rightframe, image=self.settingsIcon,
                   command=self.settingsWindow).pack(padx=40, pady=5, side='right')
        self.leftframe.pack(side='left', anchor='nw', fill='x', expand=True)
        self.rightframe.pack(side='right', anchor='ne', fill='x', expand=True)
        self.pack(anchor="n", fill='x', expand=True)

    def showAbout(self):
        if self.abWin1 is not None and self.abWin1.winfo_exists():
            return
        self.abWin1 = tk.Toplevel()
        self.abWin1.title("about")
        self.abWin1.resizable(False, False)
        frame = ttk.Frame(self.abWin1)
        frame.pack(padx=10, pady=10)
        entry = f"""per-SO-nal FI-nance t-RA-cker version: {self.version}
                    created by YuKiNe
                    \n Theme: Azure by rdbende
                     https://github.com/rdbende/Azure-ttk-theme/blob/main/LICENSE
                    \n icons from Flaticon: 
                    https://www.flaticon.com/
                    plus-icon courtesy of Freepik
                    list-icon courtesy of Kirill Kazachek
                    settings-icon courtesy of Phoenix Group
                    """

        ttk.Label(frame, text=entry).pack()

    def open(self):
        
        self.filename = filedialog.askopenfilename(initialdir="", title="Select file",
                                                   filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if self.filename:
            self.parent.settings[9] = str(self.filename) + "\n"
            self.parent.main.refresh(file=self.filename)
            fh.writeFile(self.parent.settings, "settings.txt")

    def settingsWindow(self):
        # initializing
        if self.abWin2 is not None and self.abWin2.winfo_exists():
            return
        self.abWin2 = tk.Toplevel()
        self.abWin2.title("settings")
        self.abWin2.resizable(False, False)

        self.settingsFrame = ttk.Frame(self.abWin2, padding=40)

        #settings var
        size = 14
        self.settheme = tk.BooleanVar()
        self.setIncome = tk.StringVar()
        self.setCategory = tk.StringVar()

        if self.parent.settings[7] == "dark\n":
            self.settheme.set(True)

        # Settings Widgets
        self.themeFrame = ttk.Frame(self.settingsFrame, style="Card.TFrame", padding=5)

        ttk.Checkbutton(self.themeFrame, text="dark theme", variable=self.settheme).pack()

        self.themeFrame.pack(side="top", pady=(0, 20), fill='x')

        ttk.Label(self.settingsFrame, text="set monthly income:",
                  font=("Centaur", size)).pack(side="top")

        self.incomeEntry = ttk.Entry(self.settingsFrame, textvariable=self.setIncome,
                  font=("Centaur", size), justify=tk.CENTER)
        self.incomeEntry.pack(pady=(0, 20), side='top')

        ttk.Label(self.settingsFrame, text="set expense category:",
                  font=("Centaur", size)).pack(side="top")

        self.catext = tk.Text(self.settingsFrame, height=4, width=20)
        self.catext.pack(side='top', fill='x', pady=(0, 20))

        ttk.Button(self.settingsFrame, text="set monthly expenses",
                   command=self.monthlyWindow).pack(side='top', fill='x')

        ttk.Button(self.settingsFrame, text="create new File",
                   command=self.create_file_window).pack(side="top", fill='x', pady=(20, 0))

        self.settingsFrame.pack()

        ttk.Label(self.abWin2, text="for settings to take effect, restart"
                  , font=("Centaur", 10)).pack(padx=10, pady=(0, 5))
        ttk.Button(self.abWin2, text="save", command=self.save,
                   style='Accent.TButton').pack(padx=10, pady=(0, 10), fill='x')

        # Setting inserts
        self.incomeEntry.insert(0, self.parent.settings[3][:-1])
        self.catext.insert(tk.END, self.parent.settings[11][:-1].replace(", ", "\n"))

    def create_file_window(self):
        if self.abWin4 is not None and self.abWin4.winfo_exists():
            return

        # Another Windowwww yay
        self.abWin4 = tk.Toplevel()
        self.abWin4.title("new file")
        self.abWin4.resizable(False, False)
        self.entry_Var = tk.StringVar()
        ttk.Label(self.abWin4, text="name: ", font=("Centaur", 14)).pack(padx=20, pady=(20, 10))
        ttk.Entry(self.abWin4, textvariable=self.entry_Var, font=("Centaur", 14)).pack(padx=20, pady=10)
        ttk.Button(self.abWin4, text="accept name",
                   command=self.create_file
                   ).pack(padx=20, pady=(10, 20))

    def create_file(self, filename=None):
        """ohne .txt"""
        if filename == None:
            filename = self.entry_Var.get()
        with open(f"finance data/{filename}.txt", "w") as file:
            file.write("""date:
2024-09-26-3
total:
0.0
weekly:
0.0
daily:
0.0
""")
        self.parent.settings[9] = f"finance data/{filename}.txt\n"
        fh.writeFile(self.parent.settings, "settings.txt")
        if self.abWin4 is not None and self.abWin4.winfo_exists():
            self.abWin4.destroy()

    def monthlyWindow(self):
        # initializing
        if self.abWin3 is not None and self.abWin3.winfo_exists():
            return
        self.abWin3 = tk.Toplevel()
        # set all texts into an external file for internationalization
        self.abWin3.title("monthly expenses")
        self.abWin3.resizable(False, False)

        # getting Data
        self.monthlyData = dict()

        for element in self.parent.settings[5].split(", "):
            element = element.replace("\n", "")
            temp = element.split(": ")
            self.monthlyData[temp[0]] = temp[1]

        # Treeeeeviieeewwww :D
        style1 = ttk.Style(self.abWin3)
        style1.configure("Treeview", font=("Centaur", 13))
        self.dataView = ttk.Treeview(self.abWin3, columns=('expenses', 'amount'), show='headings', style="Treeview")
        self.dataView.heading('expenses', text='expenses')
        self.dataView.heading('amount', text='amount')
        self.dataView.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # inserting into treeview
        for element in self.monthlyData.keys():
            self.dataView.insert(parent='', index=tk.END, values=(element, self.monthlyData[element]))

        # event
        self.dataView.bind('<Delete>', self.delete_items)
        # add row
        self.monthlyName = tk.StringVar()
        self.monthlyAmount = tk.DoubleVar()

        ttk.Entry(self.abWin3, textvariable=self.monthlyName,
                  font=("Centaur", 14)).grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=10, sticky="ew")
        ttk.Entry(self.abWin3, textvariable=self.monthlyAmount,
                  font=("Centaur", 14)).grid(row=2, column=2, columnspan=2, padx=(10, 5), pady=10, sticky="ew")

        ttk.Button(self.abWin3, text='add', style="Accent.TButton",
                   command=self.add_Monthly).grid(row=3, column=1, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

        ttk.Label(self.abWin3, text="to delete, select item and press 'del'",
                  font=("Centaur", 12)).grid(row=4, column=1, columnspan=2, padx=10, pady=(5, 10), sticky="ew")

    def add_Monthly(self):
        name = self.monthlyName.get()
        amount = self.monthlyAmount.get()
        if len(self.dataView.get_children()) == 0:
            self.parent.settings[5] = name + ': ' + str(amount) + '\n'
            print('it should work')
        else:
            self.parent.settings[5] = self.parent.settings[5][:-1]+', '+name+': '+str(amount)+'\n'
        self.dataView.insert(parent='', index=tk.END, values=(name, amount))

    def delete_items(self, _):
        for i in self.dataView.selection():
            self.monthlyData.pop(self.dataView.item(i)['values'][0])
            self.dataString = str(self.monthlyData).replace("{", '')
            self.dataString = self.dataString.replace("}", "\n")
            self.parent.settings[5] = self.dataString.replace("'", '')
            self.dataView.delete(i)

    def save(self):
        newTheme = self.settheme.get()
        newIncome = self.setIncome.get()
        categories = self.catext.get(1.0, tk.END)
        try:
            newIncome = float(newIncome)
        except:
            print("User error: New Income must be number.")

        if categories == '' or float(newIncome) < 0:
            print("User error: wrong input.")
        else:

            if newTheme:
                self.parent.settings[7] = 'dark' + '\n'
            else:
                self.parent.settings[7] = 'light' + '\n'

            self.parent.settings[3] = str(newIncome) + '\n'
            self.parent.settings[11] = categories.replace("\n", ", ")

        fh.writeFile(self.parent.settings, 'settings.txt')
        self.abWin2.destroy()

    def reload(self):
        self.parent.finance.load()
        with open(f"{self.parent.settings[9][:-1]}.txt", "w") as file:
            file.write(f"""date:
2024-09-26-3
total:
{self.parent.finance.total}
weekly:
{self.parent.finance.weekly}
daily:
{self.parent.finance.daily}
""")
        self.parent.main.refresh(file=self.parent.settings[9][:-1])

class Main(ttk.Frame):
    def __init__(self, parent, file=None):
        super().__init__(parent)
        self.file = file
        self.parent = parent
        fileName = self.parent.settings[9][:-1]

        if file is None:
            if os.path.isfile(fileName) is False or fileName == '\n':
                self.parent.menu.create_file("standard")
                self.file = "finance data/standard.txt"
                self.parent.finance = fd.FinanceData(self.file)
                self.parent.settings[9] = self.file + '\n'
                fh.writeFile(self.parent.settings, "settings.txt")
                self.parent.finance.load()
            else:
                self.file = fileName
                self.parent.settings[9] = self.file + '\n'
                fh.writeFile(self.parent.settings, "settings.txt")

        self.updateMain()
        self.stats()
        self.pack(anchor="center", expand=True, fill='y')

    def stats(self):
        #self.statsFrame = ttk.Frame(self, )
        pass

    def updateMain(self):

        # Alte Widgets entfernen
        for widget in self.winfo_children():
            widget.destroy()

        self.parent.finance._fileName = self.file

        # label frames
        self.allFrames = ttk.Frame(self)
        self.frame_total = ttk.Frame(self.allFrames, style='Card.TFrame')
        self.frame_total.pack(side='top', pady=20)

        self.frame_weekly = ttk.Frame(self.allFrames, style='Card.TFrame')
        self.frame_weekly.pack(side='right', padx=20)

        self.frame_daily = ttk.Frame(self.allFrames, style='Card.TFrame')
        self.frame_daily.pack(side='left', padx=20)


        # finance labels
        ttk.Label(self.frame_total, text=f"Total: \n{self.parent.finance.total:.2f}€",
                  font=("Centaur", 22)).pack(pady=20, padx=20)
        ttk.Label(self.frame_daily, text=f"Daily: \n{self.parent.finance.daily:.2f}€",
                  font=("Centaur", 22)).pack(pady=20, padx=20)
        ttk.Label(self.frame_weekly, text=f"Weekly: \n{self.parent.finance.weekly:.2f}€",
                  font=("Centaur", 22)).pack(pady=20, padx=20)


        self.allFrames.pack(anchor="center")

    def refresh(self, file=None):
        if file:
            self.file = file
        self.parent.finance._fileName = file
        self.updateMain()


class Bottom(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.plusIcon = ImageTk.PhotoImage(Image.open("icons/add.png").resize((80, 80), Image.Resampling.LANCZOS))

        ttk.Button(self, image=self.plusIcon,
                   command=self.expenseWindow).pack(pady=(20, 0))
        self.pack(anchor='s')
        self.abWin = None

    def expenseWindow(self):
        if self.abWin is not None and self.abWin.winfo_exists():
            return
        self.abWin = tk.Toplevel()
        self.abWin.resizable(False, False)
        self.abWin.title("add expense")
        expframe = ttk.Frame(self.abWin)
        expframe.grid(padx=20, pady=20)

        # Menu Style
        optionStyle = ttk.Style()
        optionStyle.configure('cat.TMenubutton', font=('Centaur', 14))

        # Variables
        self.chosenName = tk.StringVar(self)
        self.chosenAmount = tk.DoubleVar(self)
        self.chosenCategory = tk.StringVar(self)
        self.chosenDate = tk.StringVar(self)

        # labels
        txt = ["Name", "Amount", "Type", "Date (leave for now)"]
        for title, col in zip(txt, range(4)):
            ttk.Label(expframe, text=title, font=("Centaur", 14)).grid(row=0, column=col)

        # entries
        nameEntry = ttk.Entry(expframe, font=("Centaur", 14), textvariable=self.chosenName)
        amountSpinbox = ttk.Spinbox(expframe, font=("Centaur", 14), from_=0.0, to=200.0, wrap=True,
                                    format="%.2f", increment=0.1, textvariable=self.chosenAmount)
        typeOption = ttk.OptionMenu(expframe, self.chosenCategory, *self.parent.settings[11][:-1].split(", "),
                                    style='cat.TMenubutton')
        typeOption.configure()
        dateEntry = ttk.Entry(expframe, font=("Centaur", 14), textvariable=self.chosenDate)

        nameEntry.insert(0, "type anything")
        dateEntry.insert(0, "yyyy/mm/dd/hh/mm")

        nameEntry.grid(row=1, column=0, padx=10)
        dateEntry.grid(row=1, column=3, padx=10)
        amountSpinbox.grid(row=1, column=1, padx=10)
        typeOption.grid(row=1, column=2, padx=10)

        # calculation Buttons
        ttk.Button(expframe, text="Subtract", style='Accent.TButton',
                   command=self.subtraction).grid(row=0, column=4, padx=10)
        ttk.Button(expframe, text="Add", command=self.addition).grid(row=1, column=4, padx=10)

    def subtraction(self, amount=None):
        name = self.chosenName.get()
        if self.chosenAmount.get() == str or self.chosenAmount.get() < 0:
            print("User Error: Amount must be >0 and a number.")
        else:
            if not amount:
                amount = self.chosenAmount.get()
        category = self.chosenCategory.get()
        date = self.chosenDate.get()

        self.sub_obj = exp.Expense(name, amount, category, date)
        fh.savexp(self.sub_obj)

        self.parent.finance = self.parent.finance - self.sub_obj

        fh.writeFile(self.parent.finance._file, self.parent.finance._fileName)

        self.parent.main.refresh(file=self.parent.finance._fileName)
        self.abWin.destroy()
        self.expenseWindow()

    def addition(self):
        amount = self.chosenAmount.get()
        amount *= -1
        self.subtraction(amount)


class ListButton(ttk.Frame):
    def __init__(self, parent):
        super(ListButton, self).__init__(parent)
        self.listIcon = ImageTk.PhotoImage(Image.open("icons/list.png"). resize((30, 30), Image.Resampling.LANCZOS))
        ttk.Button(self, image=self.listIcon,
                   command=self.listWindow).pack(pady=40, padx=40, side='left')
        self.pack(anchor='sw')
        self.data = fh.readFile("database.txt")
        self.abWin = None

    def listWindow(self):
        if self.abWin is not None and self.abWin.winfo_exists():
            return
        self.abWin = tk.Toplevel()
        self.abWin.title("expense list")
        self.abWin.resizable(False, False)

        # Frame
        self.tableFrame = ttk.Frame(self.abWin)
        self.tableFrame.pack(padx=10, pady=10)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tableFrame)
        self.scrollbar.pack(side="right", fill="y")

        # Table
        columns = ('name', 'amount', 'category', 'date')
        self.table = ttk.Treeview(
            self.tableFrame,
            selectmode='browse',
            yscrollcommand=self.scrollbar.set,
            columns=columns,
            show='headings',
            padding=10
        )
        for title in columns:
            self.table.heading(title, text=title, command =lambda: \
                    self.tablesort(self.table, title, False))
        self.table.pack(fill='both', expand=True)
        self.scrollbar.config(command=self.table.yview)

        # inserting to table
        self.dataArray = [self.data[x].split(", ") for x in range(len(self.data))]

        for entry in self.dataArray:
            entry[1] = float(entry[1]) * (-1)

        for i in range(len(self.data)):
            self.table.insert(parent='', index=0, values=self.dataArray[i])

    def tablesort(self, table, col, desc):
        # Prüfen, ob die Spalte 'amount' sortiert wird
        if col == 'amount':
            l = [(float(table.set(k, col)), k) for k in table.get_children('')]
        else:
            l = [(table.set(k, col), k) for k in table.get_children('')]
        l.sort(reverse=desc)

        # Elemente nach der neuen Reihenfolge verschieben
        for index, (val, k) in enumerate(l):
            table.move(k, '', index)

        # Spaltenüberschrift aktualisieren, um bei erneutem Klick die Sortierreihenfolge umzukehren
        table.heading(col, command=lambda: self.tablesort(table, col, not desc))


settings = fh.readFile('settings.txt')

root = Window("Sofira", settings[7][:-1], settings[1][:-1])
