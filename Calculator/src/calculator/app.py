import tkinter as tk
from tkinter import ttk, messagebox
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rechner Pro")
        # Fenstergröße für gute Lesbarkeit
        self.root.geometry("360x520") 
        self.root.resizable(False, False)

        # ===================================================================
        # Status-Variablen
        # ===================================================================
        self.current_input = "" 
        self.stored_value = None
        self.pending_operation = None
        
        # result_var: Die große Hauptzahl unten
        self.result_var = tk.StringVar(value="0")   
        # history_var: Die kleine Anzeige oben drüber (zeigt z.B. "5 ^" an)
        self.history_var = tk.StringVar(value="")  

        self.setup_styles()
        self.create_display()
        self.create_buttons()

    def setup_styles(self):
        """Definiert das visuelle Design (Blau/Orange/Grau)."""
        style = ttk.Style()
        style.theme_use('clam')

        # Farbpalette
        self.bg_color = "#2c3e50"       # Dunkelblau (Hintergrund)
        self.display_bg = "#ecf0f1"     # Hellgrau (Display)
        self.display_text = "#2c3e50"   # Dunkelblau (Schrift Display)
        btn_num_bg = "#34495e"          # Anthrazit (Zahlen)
        btn_op_bg = "#e67e22"           # Orange (Operatoren)
        btn_func_bg = "#95a5a6"         # Mittelgrau (C, √)
        text_white = "#ffffff"

        self.root.configure(bg=self.bg_color)

        # Button Styles
        style.configure("TButton", font=('Helvetica', 14, 'bold'), borderwidth=0, focuscolor='none')
        style.configure("Num.TButton", background=btn_num_bg, foreground=text_white)
        style.configure("Op.TButton", background=btn_op_bg, foreground=text_white)
        style.configure("Func.TButton", background=btn_func_bg, foreground=text_white)
        
        # Hover-Effekte
        style.map("Num.TButton", background=[('active', "#46627f")])
        style.map("Op.TButton", background=[('active', "#d35400")])
        style.map("Func.TButton", background=[('active', "#bdc3c7")])

    def create_display(self):
        """Erstellt das zweizeilige Display ohne den 'bad screen distance' Fehler."""
        # Container für das Display (sieht aus wie ein Eingabefeld)
        display_container = tk.Frame(self.root, bg=self.display_bg, bd=5, relief="flat")
        display_container.pack(fill='x', pady=(20, 15), padx=15)

        # Zeile 1: Kleine History-Anzeige
        history_label = tk.Label(display_container, 
                                 textvariable=self.history_var, 
                                 anchor='e', 
                                 bg=self.display_bg, 
                                 fg="#7f8c8d", 
                                 font=('Helvetica', 12),
                                 padx=10,
                                 pady=5) 
        history_label.pack(fill='x')

        # Zeile 2: Große Hauptanzeige
        main_display = tk.Label(display_container, 
                                textvariable=self.result_var, 
                                anchor='e', 
                                bg=self.display_bg, 
                                fg=self.display_text, 
                                font=('Helvetica', 32, 'bold'), 
                                padx=10, 
                                pady=10) 
        main_display.pack(fill='x')

    def create_buttons(self):
        """Erstellt das Button-Raster."""
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill='both', expand=True, padx=10, pady=10)

        for i in range(5): button_frame.rowconfigure(i, weight=1)
        for i in range(4): button_frame.columnconfigure(i, weight=1)

        buttons = [
            ['C', self.clear_all, "Func.TButton"], ['√', self.calc_sqrt, "Func.TButton"], ['xʸ', lambda: self.set_operation('pow'), "Op.TButton"], ['÷', lambda: self.set_operation('/'), "Op.TButton"],
            ['7', lambda: self.add_digit('7'), "Num.TButton"], ['8', lambda: self.add_digit('8'), "Num.TButton"], ['9', lambda: self.add_digit('9'), "Num.TButton"], ['×', lambda: self.set_operation('*'), "Op.TButton"],
            ['4', lambda: self.add_digit('4'), "Num.TButton"], ['5', lambda: self.add_digit('5'), "Num.TButton"], ['6', lambda: self.add_digit('6'), "Num.TButton"], ['-', lambda: self.set_operation('-'), "Op.TButton"],
            ['1', lambda: self.add_digit('1'), "Num.TButton"], ['2', lambda: self.add_digit('2'), "Num.TButton"], ['3', lambda: self.add_digit('3'), "Num.TButton"], ['+', lambda: self.set_operation('+'), "Op.TButton"],
            ['π', self.add_pi, "Num.TButton"], ['0', lambda: self.add_digit('0'), "Num.TButton"], ['.', self.add_decimal, "Num.TButton"], ['=', self.calculate_result, "Op.TButton"],
        ]

        row, col = 0, 0
        for text, command, style_name in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, style=style_name)
            btn.grid(row=row, column=col, sticky='nsew', padx=3, pady=3, ipady=8)
            col += 1
            if col > 3: col = 0; row += 1

    # --- Logik Funktionen ---

    def update_display(self):
        val = self.current_input if self.current_input else "0"
        try:
            if "." not in val and len(val) > 3:
                # Tausender-Trennzeichen für bessere Lesbarkeit
                formatted = "{:,}".format(int(val)).replace(",", " ")
                self.result_var.set(formatted)
            else:
                self.result_var.set(val[:15]) 
        except:
            self.result_var.set(val)

    def add_digit(self, digit):
        if len(self.current_input) < 15:
            if self.current_input == "0" and digit != ".":
                self.current_input = digit
            else:
                self.current_input += digit
            self.update_display()

    def set_operation(self, op):
        if self.current_input:
            self.stored_value = float(self.current_input)
            symbols = {'pow': '^', '*': '×', '/': '÷', '+': '+', '-': '-'}
            self.history_var.set(f"{self.result_var.get()} {symbols.get(op, op)}")
            self.pending_operation = op
            self.current_input = ""

    def calculate_result(self):
        if self.stored_value is None or not self.current_input: return
        try:
            second_val = float(self.current_input)
            history_text = self.history_var.get()
            
            if self.pending_operation == 'pow': res = math.pow(self.stored_value, second_val)
            elif self.pending_operation == '+': res = self.stored_value + second_val
            elif self.pending_operation == '-': res = self.stored_value - second_val
            elif self.pending_operation == '*': res = self.stored_value * second_val
            elif self.pending_operation == '/': res = self.stored_value / second_val

            self.history_var.set(f"{history_text} {self.current_input} =")
            
            res = round(res, 8)
            self.current_input = str(int(res) if res.is_integer() else res)
            self.update_display()
            self.stored_value = None
            self.pending_operation = None
            self.current_input = "" 
        except ZeroDivisionError: self.show_error("Division durch 0")
        except: self.show_error("Fehler")

    def calc_sqrt(self):
        try:
            val = float(self.current_input) if self.current_input else float(self.result_var.get().replace(" ", ""))
            self.history_var.set(f"√({val}) =")
            res = math.sqrt(val)
            self.current_input = str(int(res) if res.is_integer() else round(res, 8))
            self.update_display()
            self.current_input = ""
        except: self.show_error("Ungültig")

    def add_pi(self):
        self.current_input = str(round(math.pi, 8))
        self.update_display()

    def add_decimal(self):
        if "." not in self.current_input:
            self.current_input += "." if self.current_input else "0."
            self.update_display()

    def clear_all(self):
        self.current_input = ""
        self.stored_value = None
        self.pending_operation = None
        self.history_var.set("")
        self.result_var.set("0")

    def show_error(self, msg):
        self.result_var.set("Error")
        self.history_var.set(msg)
        self.current_input = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
