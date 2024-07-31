import tkinter as tk
from tkinter import messagebox
import random


# Leer los verbos desde un archivo
def leer_verbos(archivo):
    verbos = []
    with open(archivo, 'r') as file:
        for linea in file:
            partes = linea.strip().split(',')
            verbos.append({
                'infinitivo': partes[0],
                'pasado': partes[1],
                'participio': partes[2],
                'tipo': partes[3],
                'espanol': partes[4]
            })
    return verbos


class VerbosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Práctica de Verbos en Inglés")
        self.root.state('zoomed')  # Ocupa el 100% de la pantalla
        self.verbos = leer_verbos('verbos.txt')
        self.verbo_actual_reg = {}
        self.verbo_actual_irreg = {}
        self.intentos_reg = 0
        self.intentos_irreg = 0

        self.setup_ui()
        self.siguiente_verbo_reg()
        self.siguiente_verbo_irreg()

    def setup_ui(self):
        self.root.configure(bg='#2E3B4E')  # Fondo gris oscuro

        # Configurar la cuadrícula principal
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Contenedor principal para centrar el contenido verticalmente
        main_frame = tk.Frame(self.root, bg='#2E3B4E')
        main_frame.grid(row=0, column=0, columnspan=2, pady=50, padx=20, sticky='nsew')

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Columna izquierda (Verbos Regulares)
        frame_regulares = tk.Frame(main_frame, bg='#2E3B4E')
        frame_regulares.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        frame_regulares.columnconfigure(0, weight=1)
        frame_regulares.columnconfigure(1, weight=1)

        self.label_verbo_reg = tk.Label(frame_regulares, text="Verbo en Español:", bg='#2E3B4E', fg='white',
                                        font=('Arial', 14))
        self.label_verbo_reg.grid(row=0, column=0, pady=10, sticky='w')
        self.verbo_espanol_reg = tk.Label(frame_regulares, text="", bg='#2E3B4E', fg='#F4D03F',
                                          font=('Arial', 16, 'bold'))
        self.verbo_espanol_reg.grid(row=0, column=1, pady=10, sticky='w')

        self.label_infinitivo_reg = tk.Label(frame_regulares, text="Infinitivo:", bg='#2E3B4E', fg='white',
                                             font=('Arial', 14))
        self.label_infinitivo_reg.grid(row=1, column=0, pady=10, sticky='w')
        self.entry_infinitivo_reg = tk.Entry(frame_regulares, font=('Arial', 14), relief='flat', borderwidth=2,
                                             highlightthickness=1, highlightcolor='#1ABC9C')
        self.entry_infinitivo_reg.grid(row=1, column=1, pady=10, padx=10, sticky='ew')

        self.label_pasado_reg = tk.Label(frame_regulares, text="Pasado:", bg='#2E3B4E', fg='white', font=('Arial', 14))
        self.label_pasado_reg.grid(row=2, column=0, pady=10, sticky='w')
        self.entry_pasado_reg = tk.Entry(frame_regulares, font=('Arial', 14), relief='flat', borderwidth=2,
                                         highlightthickness=1, highlightcolor='#1ABC9C')
        self.entry_pasado_reg.grid(row=2, column=1, pady=10, padx=10, sticky='ew')

        self.label_participio_reg = tk.Label(frame_regulares, text="Pasado Participio:", bg='#2E3B4E', fg='white',
                                             font=('Arial', 14))
        self.label_participio_reg.grid(row=3, column=0, pady=10, sticky='w')
        self.entry_participio_reg = tk.Entry(frame_regulares, font=('Arial', 14), relief='flat', borderwidth=2,
                                             highlightthickness=1, highlightcolor='#1ABC9C')
        self.entry_participio_reg.grid(row=3, column=1, pady=10, padx=10, sticky='ew')

        self.button_validar_reg = tk.Button(frame_regulares, text="Validar", command=self.validar_verbo_reg,
                                            bg='#1ABC9C', fg='white', font=('Arial', 14))
        self.button_validar_reg.grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')

        self.label_tipo_reg = tk.Label(frame_regulares, text="", bg='#2E3B4E', fg='white', font=('Arial', 14))
        self.label_tipo_reg.grid(row=5, column=0, columnspan=2, pady=10, sticky='ew')

        self.resultado_reg = tk.Label(frame_regulares, text="", bg='#2E3B4E', fg='white', font=('Arial', 14, 'bold'))
        self.resultado_reg.grid(row=6, column=0, columnspan=2, pady=10, sticky='ew')

        self.entry_infinitivo_reg.bind("<Return>", self.focus_pasado_reg)
        self.entry_pasado_reg.bind("<Return>", self.focus_participio_reg)
        self.entry_participio_reg.bind("<Return>", self.validar_con_enter_reg)

        self.entry_infinitivo_reg.bind("<Down>", self.focus_pasado_reg)
        self.entry_pasado_reg.bind("<Down>", self.focus_participio_reg)
        self.entry_participio_reg.bind("<Down>", self.validar_con_enter_reg)

        self.entry_participio_reg.bind("<Up>", self.focus_pasado_reg)
        self.entry_pasado_reg.bind("<Up>", self.focus_infinitivo_reg)
        self.entry_infinitivo_reg.bind("<Up>", self.focus_participio_reg)

        # Columna derecha (Verbos Irregulares)
        frame_irregulares = tk.Frame(main_frame, bg='#2E3B4E')
        frame_irregulares.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

        frame_irregulares.columnconfigure(0, weight=1)
        frame_irregulares.columnconfigure(1, weight=1)

        self.label_verbo_irreg = tk.Label(frame_irregulares, text="Verbo en Español:", bg='#2E3B4E', fg='white',
                                          font=('Arial', 14))
        self.label_verbo_irreg.grid(row=0, column=0, pady=10, sticky='w')
        self.verbo_espanol_irreg = tk.Label(frame_irregulares, text="", bg='#2E3B4E', fg='#F4D03F',
                                            font=('Arial', 16, 'bold'))
        self.verbo_espanol_irreg.grid(row=0, column=1, pady=10, sticky='w')

        self.label_infinitivo_irreg = tk.Label(frame_irregulares, text="Infinitivo:", bg='#2E3B4E', fg='white',
                                               font=('Arial', 14))
        self.label_infinitivo_irreg.grid(row=1, column=0, pady=10, sticky='w')
        self.entry_infinitivo_irreg = tk.Entry(frame_irregulares, font=('Arial', 14), relief='flat', borderwidth=2,
                                               highlightthickness=1, highlightcolor='#1ABC9C')
        self.entry_infinitivo_irreg.grid(row=1, column=1, pady=10, padx=10, sticky='ew')

        self.label_pasado_irreg = tk.Label(frame_irregulares, text="Pasado:", bg='#2E3B4E', fg='white',
                                           font=('Arial', 14))
        self.label_pasado_irreg.grid(row=2, column=0, pady=10, sticky='w')
        self.entry_pasado_irreg = tk.Entry(frame_irregulares, font=('Arial', 14), relief='flat', borderwidth=2,
                                           highlightthickness=1, highlightcolor='#1ABC9C')
        self.entry_pasado_irreg.grid(row=2, column=1, pady=10, padx=10, sticky='ew')

        self.label_participio_irreg = tk.Label(frame_irregulares, text="Pasado Participio:", bg='#2E3B4E', fg='white',
                                               font=('Arial', 14))
        self.label_participio_irreg.grid(row=3, column=0, pady=10, sticky='w')
        self.entry_participio_irreg = tk.Entry(frame_irregulares, font=('Arial', 14), relief='flat', borderwidth=2,
                                               highlightthickness=1, highlightcolor='#1ABC9C')
        self.entry_participio_irreg.grid(row=3, column=1, pady=10, padx=10, sticky='ew')

        self.button_validar_irreg = tk.Button(frame_irregulares, text="Validar", command=self.validar_verbo_irreg,
                                              bg='#1ABC9C', fg='white', font=('Arial', 14))
        self.button_validar_irreg.grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')

        self.label_tipo_irreg = tk.Label(frame_irregulares, text="", bg='#2E3B4E', fg='white', font=('Arial', 14))
        self.label_tipo_irreg.grid(row=5, column=0, columnspan=2, pady=10, sticky='ew')

        self.resultado_irreg = tk.Label(frame_irregulares, text="", bg='#2E3B4E', fg='white',
                                        font=('Arial', 14, 'bold'))
        self.resultado_irreg.grid(row=6, column=0, columnspan=2, pady=10, sticky='ew')

        self.entry_infinitivo_irreg.bind("<Return>", self.focus_pasado_irreg)
        self.entry_pasado_irreg.bind("<Return>", self.focus_participio_irreg)
        self.entry_participio_irreg.bind("<Return>", self.validar_con_enter_irreg)

        self.entry_infinitivo_irreg.bind("<Down>", self.focus_pasado_irreg)
        self.entry_pasado_irreg.bind("<Down>", self.focus_participio_irreg)
        self.entry_participio_irreg.bind("<Down>", self.validar_con_enter_irreg)

        self.entry_participio_irreg.bind("<Up>", self.focus_pasado_irreg)
        self.entry_pasado_irreg.bind("<Up>", self.focus_infinitivo_irreg)
        self.entry_infinitivo_irreg.bind("<Up>", self.focus_participio_irreg)

    def focus_infinitivo_reg(self, event):
        self.entry_infinitivo_reg.focus()

    def focus_pasado_reg(self, event):
        self.entry_pasado_reg.focus()

    def focus_participio_reg(self, event):
        self.entry_participio_reg.focus()

    def validar_con_enter_reg(self, event):
        self.validar_verbo_reg()

    def focus_infinitivo_irreg(self, event):
        self.entry_infinitivo_irreg.focus()

    def focus_pasado_irreg(self, event):
        self.entry_pasado_irreg.focus()

    def focus_participio_irreg(self, event):
        self.entry_participio_irreg.focus()

    def validar_con_enter_irreg(self, event):
        self.validar_verbo_irreg()

    def siguiente_verbo_reg(self):
        self.verbo_actual_reg = random.choice([verbo for verbo in self.verbos if verbo['tipo'] == 'R'])
        self.entry_infinitivo_reg.delete(0, tk.END)
        self.entry_pasado_reg.delete(0, tk.END)
        self.entry_participio_reg.delete(0, tk.END)
        self.verbo_espanol_reg.config(text=self.verbo_actual_reg['espanol'])
        self.label_tipo_reg.config(text="Tipo de verbo: Regular")
        self.resultado_reg.config(text="")
        self.intentos_reg = 0

    def siguiente_verbo_irreg(self):
        self.verbo_actual_irreg = random.choice([verbo for verbo in self.verbos if verbo['tipo'] == 'I'])
        self.entry_infinitivo_irreg.delete(0, tk.END)
        self.entry_pasado_irreg.delete(0, tk.END)
        self.entry_participio_irreg.delete(0, tk.END)
        self.verbo_espanol_irreg.config(text=self.verbo_actual_irreg['espanol'])
        self.label_tipo_irreg.config(text="Tipo de verbo: Irregular")
        self.resultado_irreg.config(text="")
        self.intentos_irreg = 0

#fn.fthbj
    def validar_verbo_reg(self):
        infinitivo = self.entry_infinitivo_reg.get().strip().lower()
        pasado = self.entry_pasado_reg.get().strip().lower()
        participio = self.entry_participio_reg.get().strip().lower()

        if (infinitivo == self.verbo_actual_reg['infinitivo'] and
                pasado == self.verbo_actual_reg['pasado'] and
                participio == self.verbo_actual_reg['participio']):
            self.resultado_reg.config(text="¡Respuesta correcta!", fg='#1ABC9C')
            self.siguiente_verbo_reg()
        else:
            self.intentos_reg += 1
            self.resultado_reg.config(
                text=f"Respuesta incorrecta. Intento {self.intentos_reg}. Traducciones: {self.verbo_actual_reg['infinitivo']} - {self.verbo_actual_reg['pasado']} - {self.verbo_actual_reg['participio']}",
                fg='#E74C3C')

    def validar_verbo_irreg(self):
        infinitivo = self.entry_infinitivo_irreg.get().strip().lower()
        pasado = self.entry_pasado_irreg.get().strip().lower()
        participio = self.entry_participio_irreg.get().strip().lower()

        if (infinitivo == self.verbo_actual_irreg['infinitivo'] and
                pasado == self.verbo_actual_irreg['pasado'] and
                participio == self.verbo_actual_irreg['participio']):
            self.resultado_irreg.config(text="¡Respuesta correcta!", fg='#1ABC9C')
            self.siguiente_verbo_irreg()
        else:
            self.intentos_irreg += 1
            self.resultado_irreg.config(
                text=f"Respuesta incorrecta. Intento {self.intentos_irreg}. Traducciones: {self.verbo_actual_irreg['infinitivo']} - {self.verbo_actual_irreg['pasado']} - {self.verbo_actual_irreg['participio']}",
                fg='#E74C3C')

hola = "hola"
if __name__ == "__main__":
    root = tk.Tk()
    app = VerbosApp(root)
    root.mainloop()
