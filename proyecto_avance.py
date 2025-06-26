from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import json


class Pelicula:
    def __init__(self, titulo, sinopsis, generos, año, imagen=None):
        self.titulo = titulo
        self.sinopsis = sinopsis
        self.generos = generos
        self.año = año
        self.imagen = imagen
        self.relaciones = []

class GrafoPeliculas:
    def __init__(self):
        self.peliculas = []

    def agregar_pelicula(self, titulo, sinopsis, generos, año,imagen=None):
        nueva = Pelicula(titulo, sinopsis, generos, año, imagen)
        self.peliculas.append(nueva)

    def buscar_pelicula(self, titulo):
        for pelicula in self.peliculas:
            if pelicula.titulo == titulo:
                return pelicula
        return None

    def buscar_por_genero(self, genero):
        return [p for p in self.peliculas if genero in p.generos]

def cargar_peliculas_archivo(grafo, archivo='archivo_peliculas.json'):
    with open(archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
        for peli in datos:
            grafo.agregar_pelicula(peli['titulo'], peli['sinopsis'], peli['generos'], peli['año'], peli.get("imagen"))

grafo = GrafoPeliculas()
cargar_peliculas_archivo(grafo)

# interfaz tkinter 
app = Tk()
app.title("Catálogo de Películas")
app.geometry("700x450")
app.config(bg="#000000")
Icono = PhotoImage(file="icono.png")
app.iconphoto(True,Icono)

#menú
menu_bar = Menu(app)

menu_archivo = Menu(menu_bar, tearoff=0)
menu_archivo.add_command(label="Salir", command=app.quit)
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

menu_ver = Menu(menu_bar, tearoff=0)
menu_ver.add_command(label="Todas las películas", command=lambda: cargar_peliculas())
menu_bar.add_cascade(label="Ver", menu=menu_ver)

menu_ayuda = Menu(menu_bar, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "Catálogo de Películas"))
menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)

app.config(menu=menu_bar)

# filtro
filtro_frame = Frame(app)
filtro_frame.pack(pady=10)


Label(filtro_frame, text="Filtrar por género:").pack(side=LEFT)

generos_unicos = set()
for peli in grafo.peliculas:
    generos_unicos.update(peli.generos)
generos = ["Todos"] + sorted(generos_unicos)

genero_combo = Combobox(filtro_frame, values=generos, state="readonly")
genero_combo.current(0)
genero_combo.pack(side=LEFT, padx=5)

tree = Treeview(app, columns=("Título", "Género", "Año"), show='headings')
tree.heading("Título", text="Título")
tree.heading("Género", text="Género")
tree.heading("Año", text="Año")
tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

def cargar_peliculas(filtro_genero=None):
    tree.delete(*tree.get_children())
    peliculas = grafo.peliculas if filtro_genero in (None, "Todos") else grafo.buscar_por_genero(filtro_genero)
    for peli in peliculas:
        genero_mostrar = peli.generos[0] if peli.generos else "Desconocido"
        tree.insert("", END, values=(peli.titulo, genero_mostrar, peli.año))

def on_genero_change(event):
    genero = genero_combo.get()
    cargar_peliculas(filtro_genero=genero)

def ver_detalles():
    item = tree.focus()
    if not item:
        messagebox.showinfo("Info", "Selecciona una película.")
        return
    datos = tree.item(item)["values"]
    titulo = datos[0]
    peli = grafo.buscar_pelicula(titulo)
    if peli:
        generos = ", ".join(peli.generos)
        mensaje = (
            f"Título: {peli.titulo}\n"
            f"Género: {generos}\n"
            f"Año: {peli.año}\n\n"
            f"Sinopsis:\n{peli.sinopsis}"
        )
        messagebox.showinfo("Detalles", mensaje)

def mostrar_menu_contextual(event):
    if tree.identify_row(event.y):
        tree.selection_set(tree.identify_row(event.y))
        menu_contextual.tk_popup(event.x_app, event.y_app)
        
def mostrar_detalles_izq(event):
    item = tree.focus()
    if not item:
        return
    datos = tree.item(item)["values"]
    titulo = datos[0]
    peli = grafo.buscar_pelicula(titulo)
    if peli:
        mostrar_ventana_detalles(peli)

        
def mostrar_ventana_detalles(pelicula):
    
    detalles_win = Toplevel(app)
    detalles_win.title(f"Detalles de: {pelicula.titulo}")
    detalles_win.geometry("400x300")
    detalles_win.config(bg="white")


    # Usamos Label (abre ventana de cada película y se agrega una imagen por cada película)
    from tkinter import Label,PhotoImage
    
    if pelicula.imagen:
        try:
            img_tk = PhotoImage(file=pelicula.imagen)
            img_label = Label(detalles_win, image=img_tk, bg="white")
            img_label.image = img_tk  # Guardar referencia
            img_label.pack(anchor='w')
        except Exception as e:
            print(f"Error cargando imagen: {e}")


    Label(detalles_win, text="Título:", font=("Arial", 16, "bold"), bg="white").pack(anchor=W, padx=10, pady=(10,0))
    Label(detalles_win, text=pelicula.titulo, font=("Arial", 14), wraplength=380, bg="white").pack(anchor=W, padx=10)

    Label(detalles_win, text="Género:", font=("Arial", 16, "bold"), bg="white").pack(anchor=W, padx=10, pady=(10,0))
    Label(detalles_win, text=", ".join(pelicula.generos),font=("Arial", 14), bg="white").pack(anchor=W, padx=10)

    Label(detalles_win, text="Año:", font=("Arial", 16, "bold"), bg="white").pack(anchor=W, padx=10, pady=(10,0))
    Label(detalles_win, text=pelicula.año, font=("Arial", 14), bg="white").pack(anchor=W, padx=10)

    Label(detalles_win, text="Sinopsis:", font=("Arial", 16, "bold"), bg="white").pack(anchor=W, padx=10, pady=(10,0))
    Label(detalles_win, text=pelicula.sinopsis,font=("Arial", 14), wraplength=1500, justify=LEFT, bg="white").pack(anchor=W, padx=10)



menu_contextual = Menu(app, tearoff=0)
menu_contextual.add_command(label="Ver detalles", command=ver_detalles)
menu_contextual.add_command(label="Eliminar (no implementado)")
tree.bind("<Button-3>", mostrar_menu_contextual)

genero_combo.bind("<<ComboboxSelected>>", on_genero_change)

cargar_peliculas()

tree.bind("<<TreeviewSelect>>", mostrar_detalles_izq)

app.mainloop()
