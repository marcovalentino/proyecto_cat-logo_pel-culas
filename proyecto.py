import json

class Pelicula:
    def __init__(self, titulo, sinopsis, generos, año):
        self.titulo = titulo
        self.sinopsis = sinopsis
        self.generos = generos  
        self.año = año
        self.relaciones = []  

class GrafoPeliculas:
    def __init__(self):
        self.peliculas = []  

    def agregar_pelicula(self, titulo, sinopsis, generos, año):
        nueva = Pelicula(titulo, sinopsis, generos, año)
        self.peliculas.append(nueva)

    def buscar_pelicula(self, titulo, año):
        for pelicula in self.peliculas:
            if pelicula.titulo == titulo or pelicula.año == año:
                return pelicula
        return None
        

    def relacionar_peliculas(self, titulo1, titulo2):
        p1 = self.buscar_pelicula(titulo1)
        p2 = self.buscar_pelicula(titulo2)
        if p1 and p2 and p2 not in p1.relaciones:
            p1.relaciones.append(p2)
            p2.relaciones.append(p1)

    def buscar_por_genero(self, genero):
        return [p for p in self.peliculas if genero in p.generos]

    def imprimir_grafo(self):
        for pelicula in self.peliculas:
            relacionados = [p.titulo for p in pelicula.relaciones]
            print(f"{pelicula.titulo} ({', '.join(pelicula.generos)}):")
            print(f"Sinopsis: {pelicula.sinopsis}")
            print(f'Año: {pelicula.año}\n')
    
            

def cargar_peliculas_archivo(grafo, archivo='archivo_peliculas.json'):
    with open(archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
        for peli in datos:
            grafo.agregar_pelicula(peli['titulo'], peli['sinopsis'], peli['generos'],peli['año'])


grafo = GrafoPeliculas()
cargar_peliculas_archivo(grafo)
grafo.imprimir_grafo()
