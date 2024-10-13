import tkinter as tk
from tkinter import filedialog, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Logica import Logica
from AnalizadorLexico import AnalizadorLexico

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador")

        # Área de texto principal (editable inicialmente)
        self.text_area = tk.Text(self.root, wrap='none', height=10, width=50)
        self.text_area.pack(pady=10)

        # Barra de desplazamiento para el TextArea
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.text_area.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scroll_y.set)

        self.scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.text_area.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.config(xscrollcommand=self.scroll_x.set)

        # Botones en la parte superior
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        archivo_menu = tk.Menu(self.menu_bar, tearoff=0)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Guardar como", command=self.guardar_como)
        self.menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
         
        self.menu_bar.add_command(label="Ejecutar", command=self.ejecutar_logica)
        # Instancia de la clase lógica
        self.logica = Logica()
        self.analizador_lexico = AnalizadorLexico()
        # Área de texto para la consola (inicialmente oculta)
        self.consola = None
        # Frame para el diagrama de Venn
        self.frame_venn = tk.Frame(self.root)
        self.frame_venn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas_venn = None  # Placeholder para el canvas del diagrama de Venn

    def abrir_archivo(self):
        archivo_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CA Files", "*.ca")])
        if archivo_path:
            with open(archivo_path, 'r') as archivo:
                contenido = archivo.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, contenido)

    def guardar_archivo(self):
        archivo_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if archivo_path:
            with open(archivo_path, 'w') as archivo:
                archivo.write(self.text_area.get(1.0, tk.END))

    def guardar_como(self):
        archivo_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if archivo_path:
            with open(archivo_path, 'w') as archivo:
                archivo.write(self.text_area.get(1.0, tk.END))

    def ejecutar_logica(self):
        # Hacer el TextArea inmutable
        self.text_area.config(state=tk.DISABLED)

        # Expandir la ventana si la consola no está creada
        if not self.consola:
            self.expandir_ventana()

        # Obtener el contenido del TextArea
        codigo = str(self.text_area.get(1.0, tk.END))
        print(codigo)
        # Pasar el código a la clase Logica para analizarlo
        resultado = self.analizador_lexico.analizar_lexico(codigo)
        
        # Imprimir resultado para depuración
        print("Resultado:", resultado)

        # Mostrar el resultado en la consola
        self.consola.config(state=tk.NORMAL)  # Permitir escribir en la consola
        self.consola.delete(1.0, tk.END)
        for diccionario in resultado:
            cadena = str(diccionario) + '\n'
            self.consola.insert(tk.END, cadena)
        self.consola.config(state=tk.DISABLED)  # Hacer la consola inmutable


    def expandir_ventana(self):
        # Crear el área de texto para la consola y expandir la ventana
        self.consola = tk.Text(self.root, height=10, width=50)
        self.consola.pack(pady=10)
        #self.consola.config(state=tk.DISABLED)  # Inicialmente inmutable

        # Ajustar el tamaño de la ventana para que se vea la consola
        self.root.geometry("600x500")

    def mostrar_diagrama_venn(self, figura):
        if self.canvas_venn:
            self.canvas_venn.get_tk_widget().destroy()  # Eliminar el canvas anterior si existe

        # Crear un nuevo canvas para el diagrama de Venn
        self.canvas_venn = FigureCanvasTkAgg(figura, master=self.frame_venn)
        self.canvas_venn.draw()
        self.canvas_venn.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Inicializar la ventana principal
root = tk.Tk()
app = InterfazGrafica(root)
root.geometry("600x400")  # Tamaño inicial de la ventana
root.mainloop()
