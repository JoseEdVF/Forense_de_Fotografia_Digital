import io
import os
import exifread
import numpy as np
import metadatos_matriz
import metadatos_info
from tkinter import Tk, Frame, Button, Label, Text, INSERT, PhotoImage, messagebox, Entry, NSEW, END, GROOVE, ttk
from tkinter.filedialog import askopenfilenames
from PIL import Image, ImageTk

#Clase que respresenta la aplicacion, hereda de Tk
class ForenseFotografia(Tk):
    def __init__(self):
        Tk.__init__(self)
        #self.title('Forense Fotografia Digital')
        #Contenedor que representa una 'pila' de frames, para poder mostrar diferentes 'ventanas'
        contenedor = Frame(self)
        contenedor.pack(side='top', fill='both', expand=True)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        #Se guardan los frames en esta variable
        self.frames = {}
        #Se crea cada una de las paginas y se guardan en la variable frames
        for f in (PaginaPrincipal, Metadatos):
            nombre = f.__name__
            frame = f(parent=contenedor, controller=self)
            self.frames[nombre] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        # Se empieza mostrando la pagina principal
        self.show_frame('PaginaPrincipal')

    # Funcion que muestra el frame que se le pase
    def show_frame(self, nombre, actual=None):
        frame = self.frames[nombre]
        frame.tkraise()

#Clase que representa la pagina principal
class PaginaPrincipal(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        #En esta sección se declaran todos los widgets que se mostrarán en el frame

        label = Label(self, text='Forense de Fotografia', font='Helvetica 20')
        label.place(x=200, y=30)

        #label2 = Label(self, text='Programacion Python', font='Helvetica 20')
        #label2.place(x=220, y=100)

        load_image = Image.open('./IPN-logo-BB9124D61B-seeklogo.com.png')
        load_image.thumbnail((100, 100), Image.ANTIALIAS)
        load_image = ImageTk.PhotoImage(load_image)
        img = Label(self, image=load_image)
        img.image = load_image
        img.place(x=40, y=15)

        load_image = Image.open('./esimetwitter_400x400.png')
        load_image.thumbnail((100, 100), Image.ANTIALIAS)
        load_image = ImageTk.PhotoImage(load_image)
        img = Label(self, image=load_image)
        img.image = load_image
        img.place(x=530, y=15)

        buton_op1 = Button(self, text='Metadatos', command=lambda: controller.show_frame('Metadatos'))

        buton_op1.place(x=310, y=350)

class Metadatos(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.image = Label()
        self.path = None
        #load_image = Image.open('./13879395_1760023490945364_2764101805014374945_n.png')
        #load_image.thumbnail((225, 225), Image.ANTIALIAS)
        #load_image = ImageTk.PhotoImage(load_image)
        #self.image = Label(image=load_image)

        # En esta sección se declaran todos los widgets que se mostrarán en el frame

        label = Label(self, text='Metadatos', font='Helvetica 20')
        label.place(x=400, y=20)

        boton_subir_imagen = Button(self, text='Selecciona un archivo', command=lambda : [self.subirImagen()])
        boton_subir_imagen.place(x=400, y=75)

        boton_metadatos = Button(self, text='  Obtener metadatos  ', command=self.obtenerMetadatos)
        boton_metadatos.place(x=400, y=150)

    def subirImagen(self):
        # path = None
        paths = askopenfilenames()
        if len(paths) > 1:
            self.path = paths
            messagebox.showinfo(title='Info', message='Seleccionaste varios archivos,\n '
                                                      'los resultados se guardaran en un .txt')
            return
        else:
            path = paths[0]
            if path == '':
                messagebox.showerror(title='Error', message='Selecciona un archivo')
                path = None
                return
            elif '.JPG' not in path and '.jpg' not in path and '.JPEG' not in path and '.jpeg' not in path:
                messagebox.showerror(title='Error', message='No es un archivo jpg')
                path = None
                return
            frame = Frame(width=300, height=200)
            frame.place(x=30, y=20)
            self.path = path
            load_image = Image.open(path)
            forma = np.array(load_image)
            if forma.shape[1] > forma.shape[0]:
                load_image = load_image.resize((300, 200), Image.ANTIALIAS)
            elif forma.shape[1] == forma.shape[0]:
                load_image = load_image.resize((300, 300), Image.ANTIALIAS)
            else:
                load_image = load_image.resize((150, 200), Image.ANTIALIAS)
            # load_image.thumbnail((225, 225), Image.ANTIALIAS)
            load_image = ImageTk.PhotoImage(load_image)
            self.image = Label(frame, image=load_image)
            self.image.image = load_image
            self.image.place(x=1, y=1)

    def obtenerMetadatos(self):
        if self.path is None:
            messagebox.showerror(title='Error', message='Primero selecciona una imagen')
            return
        if type(self.path) is tuple:
            res = ''
            for path in self.path:
                res += f'El archivo actual es = {path}\n'
                # Variables que indican el inicio de diferentes metadatos
                SOI = 0
                exif_header = 6
                tiff_header = 12
                num_campos_ad = 21
                inicio_campos = 23

                # Se obtienen los datos de la imagen en decimal y hexadecimal.
                self.image = Image.open(path)
                datos, hex_datos = abrir_imagen_bin(path)

                # Orden: Big Endian o Little Endian
                orden = endian(datos, tiff_header)

                # Revisar si el archivo es JPEG o no (JPEG == ffd8)
                if hex_datos[SOI][0] != 'f' or hex_datos[SOI][1] != 'f' or hex_datos[SOI + 1][0] != 'd' or \
                        hex_datos[SOI + 1][
                            1] != '8':
                    res += f'{path} No es un archivo JPEG\n'
                    continue

                elif not check_exif(datos[exif_header: tiff_header]):
                    res += f'{path} El archivo no es archivo EXIF\n'
                    continue

                # --------Nueva implementacion--------
                try:
                    file = open(path, 'rb')
                    metadata = exifread.process_file(file)
                    metadata.pop('JPEGThumbnail')
                except:
                    file = open(path, 'rb')
                    metadata = exifread.process_file(file)

                for key, value in metadata.items():
                    res += f'{key} = {value}\n'

                # ------Nueva implementacion--------
                mat_dict = metadatos_matriz.matrices(hex_datos)
                for key, value in mat_dict.items():
                    res += f'{value}\n'
                #Se guardan los resultados
                out = open('respuesta.txt', 'w+')
                for i in range(len(res)):
                    out.write(res[i])

            messagebox.showinfo(title='Info', message='Resultados se guardaron en \'respuesta.txt\'')
        else:
            # Variables que indican el inicio de diferentes metadatos
            SOI = 0
            exif_header = 6
            tiff_header = 12
            num_campos_ad = 21
            inicio_campos = 23

            # Se obtienen los datos de la imagen en decimal y hexadecimal.
            self.image = Image.open(self.path)
            datos, hex_datos = abrir_imagen_bin(self.path)

            # Orden: Big Endian o Little Endian
            orden = endian(datos, tiff_header)

            res = ''

            # Revisar si el archivo es JPEG o no (JPEG == ffd8)
            if hex_datos[SOI][0] != 'f' or hex_datos[SOI][1] != 'f' or hex_datos[SOI + 1][0] != 'd' or \
                    hex_datos[SOI + 1][
                        1] != '8':
                messagebox.showerror(title='Error', message='No es un archivo JPEG')
                return
            elif not check_exif(datos[exif_header: tiff_header]):
                messagebox.showerror(title='Error', message='El archivo no es archivo EXIF')
                return

            # --------Nueva implementacion--------
            try:
                file = open(self.path, 'rb')
                metadata = exifread.process_file(file)
                metadata.pop('JPEGThumbnail')
            except:
                file = open(self.path, 'rb')
                metadata = exifread.process_file(file)

            cont = 0
            rows = []
            frame = Frame(width=500, height=100)
            frame.place(x=10, y=250)
            cols = ('Datos', 'Valor')
            listbox = ttk.Treeview(frame, columns=cols, show='headings')
            for col in cols:
                listbox.heading(col, text=col)
                listbox.column(col, width=330)
            listbox.grid(row=1, column=0, columnspan=2)

            for key, value in metadata.items():
                listbox.insert('', 'end', values=(key, value))

            # ------Nueva implementacion--------
            mat_dict = metadatos_matriz.matrices(hex_datos)
            for key, value in mat_dict.items():
                listbox.insert('', 'end', values=(key, value))

def abrir_imagen_bin(path):
    datos = []
    # Leer archivo binario para obtener metadatos
    with open(path, 'rb') as f:
        for i in f:
            for j in i:
                datos.append(j)
    hex_datos = np.array(datos)
    hex_datos = [hex(i).replace('0x', '') for i in datos]

    return datos, hex_datos

def endian(datos, tiff_header):
    # Orden Big Ending o Little Ending
    if chr(datos[tiff_header]) == 'I':
        orden = 1
    else:
        orden = 0
    return orden

def check_exif(datos):
    tipo = ''
    for i in datos:
        tipo += chr(i)
    if 'Exif' in tipo:
        return True
    else:
        return False

if __name__ == '__main__':
    app = ForenseFotografia()
    app.geometry('680x500')
    app.resizable(width=False, height=False)
    app.mainloop()