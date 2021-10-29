import io
import os
import numpy as np
import metadatos_matriz
import metadatos_info
from tkinter import Tk, Frame, Button, Label, Text, INSERT, PhotoImage, messagebox, Entry, NSEW, END, GROOVE, ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

path = None

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
        #self.image.destroy()
        # path = None
        path = askopenfilename()
        if '.JPG' not in path and '.jpg' not in path:
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
        #load_image.thumbnail((225, 225), Image.ANTIALIAS)
        load_image = ImageTk.PhotoImage(load_image)
        self.image = Label(frame, image=load_image)
        self.image.image = load_image
        self.image.place(x=1, y=1)


    def obtenerMetadatos(self):
        if self.path is None:
            messagebox.showerror(title='Error', message='Primero selecciona una imagen')
            return

        #Variables que indican el inicio de diferentes metadatos
        SOI = 0
        exif_header = 6
        tiff_header = 12
        num_campos_ad = 21
        inicio_campos = 23

        #Se obtienen los datos de la imagen en decimal y hexadecimal.
        self.image = Image.open(self.path)
        datos, hex_datos = abrir_imagen_bin(self.path)

        # Orden: Big Endian o Little Endian
        orden = endian(datos, tiff_header)

        res = ''
        text = Text()

        # Revisar si el archivo es JPEG o no (JPEG == ffd8)
        if hex_datos[SOI][0] != 'f' or hex_datos[SOI][1] != 'f' or hex_datos[SOI + 1][0] != 'd' or hex_datos[SOI + 1][
            1] != '8':
            messagebox.showerror(title='Error', message='No es un archivo JPEG')

            # text.insert(INSERT, res)
            # text.place(x=10, y=250, height=220, width=580)
            # text['state'] = 'disabled'

            return
        elif not check_exif(datos[exif_header: tiff_header]):
            messagebox.showerror(title='Error', message='El archivo no es archivo EXIF')
            text.destroy()

            # text.insert(INSERT, res)
            # text.place(x=10, y=250, height=220, width=580)
            # text['state'] = 'disabled'

            return

        # Si el archivo es JPEG/EXIF

        # Obtener First 0th-IFD
        f_ifd_offset = num_campos_ad
        exif_offset, gps_offset, ifd, metadatos = metadatos_info.first_ifd_process(datos, f_ifd_offset, tiff_header, orden)
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

        for key, value in metadatos['Oth IFD Metadatos'].items():
            listbox.insert('', 'end', values=(key, value))
        # listbox.pack()
        # frame.pack()
        # for key, value in metadatos['Oth IFD Metadatos'].items():
        #    cols = []
        #    tabla = Entry(text, relief=GROOVE, width=50)
        #    tabla.grid(row=cont, column=0, sticky=NSEW)
        #    tabla.insert(END, key)
        #    cols.append(tabla)
        #    tabla = Entry(text, relief=GROOVE, width=50)
        #    tabla.grid(row=cont, column=1, sticky=NSEW)
        #    tabla.insert(END, value)
        #    cols.append(tabla)
        #    rows.append(cols)
        #    cont += 1
        # res += ifd
        # Obtencion de metadatos EXIF
        exif, brillo, metadatos_exif = metadatos_info.exif_ifd_process(datos, exif_offset, tiff_header, orden)
        res += exif
        res += brillo
        metadatos['EXIF IFD Metadatos'] = metadatos_exif
        for key, value in metadatos['EXIF IFD Metadatos'].items():
            listbox.insert('', 'end', values=(key, value))

        if gps_offset > 0:
            gps, gps_dict = metadatos_info.gps_process(datos, gps_offset, tiff_header, orden)
            res += gps
        else:
            gps_dict = {}
            gps_dict['--------------GPS IFD----------------'] = ''
            gps_dict['Datos de GPS no disponibles'] = ''
            res += '--------------GPS IFD----------------\n'
            res += 'Datos de GPS no disponible\n'

        metadatos['GPS IFD'] = gps_dict
        for key, value in metadatos['GPS IFD'].items():
            listbox.insert('', 'end', values=(key, value))
        res += '-------------Matriz de Cuantificacion------------\n'
        metadatos['-------------Matriz de Cuantificacion------------'] = ''
        matrices, matriz_dict = metadatos_matriz.matriz_cuant(datos)
        res += matrices
        metadatos['Matriz de Cuantificacion'] = matriz_dict

        for key, value in metadatos['Matriz de Cuantificacion'].items():
            listbox.insert('', 'end', values=(key, value))

        # text.insert(INSERT, res)
        # text.place(x=10, y=250, height=220, width=580)
        text['state'] = 'disabled'




'''
class ExcepcionTexto(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def interfaz():
    global img
    global pagina_principal
    pagina_principal = Tk()
    pagina_principal.geometry('600x500')
    pagina_principal.resizable(height=0, width=0)
    pagina_principal.title('Metadatos')
    icon = PhotoImage(file='./13879395_1760023490945364_2764101805014374945_n.png')
    pagina_principal.iconphoto(False, icon)
    #titulo = Label(pagina_principal, text = 'Programa para conseguir metadatos de una imagen')
    #titulo.config(font=('Arial', 18))
    #titulo.pack()
    load_image = Image.open('./13879395_1760023490945364_2764101805014374945_n.png')
    load_image.thumbnail((225, 225), Image.ANTIALIAS)
    load_image = ImageTk.PhotoImage(load_image)
    img = Label(image = load_image)
    boton_subir_imagen = Button(text='Selecciona un archivo', command=lambda: [subir_imagen()])
    boton_subir_imagen.place(x=400, y=75)
    boton_metadatos = Button(text='  Obtener metadatos  ', command=obtener_metadatos)
    boton_metadatos.place(x=400, y=150)
    pagina_principal.mainloop()


def subir_imagen():
    global path
    global img
    img.destroy()
    #path = None
    path = askopenfilename()
    if '.JPG' not in path and '.jpg' not in path:
        messagebox.showerror(title='Error', message='No es un archivo jpg')
        path = None
        return
    load_image = Image.open(path)
    forma = np.array(load_image)
    load_image.thumbnail((225, 225), Image.ANTIALIAS)
    load_image = ImageTk.PhotoImage(load_image)
    img = Label(image=load_image)
    img.image = load_image
    img.place(x=40, y=20)

def obtener_metadatos():
    global pagina_principal
    if path is None:
        messagebox.showerror(title='Error', message='Primero selecciona una imagen')
        return
    SOI = 0
    exif_header = 6
    tiff_header = 12
    num_campos_ad = 21
    inicio_campos = 23

    img = Image.open(path)
    datos, hex_datos = abrir_imagen_bin(path)

    # Orden: Big Endian o Little Endian
    orden = endian(datos, tiff_header)

    res = ''
    text = Text()

    # Revisar si el archivo es JPEG o no
    if hex_datos[SOI][0] != 'f' or hex_datos[SOI][1] != 'f' or hex_datos[SOI + 1][0] != 'd' or hex_datos[SOI + 1][
        1] != '8':
        messagebox.showerror(title='Error', message='No es un archivo JPEG')
        
        #text.insert(INSERT, res)
        #text.place(x=10, y=250, height=220, width=580)
        #text['state'] = 'disabled'
        

        return
    elif not check_exif(datos[exif_header: tiff_header]):
        messagebox.showerror(title='Error', message='El archivo no es archivo EXIF')
        text.destroy()
        
        #text.insert(INSERT, res)
        #text.place(x=10, y=250, height=220, width=580)
        #text['state'] = 'disabled'
        
        return

        # Si el archivo es JPEG/EXIF

        # Obtener First 0th-IFD
    f_ifd_offset = num_campos_ad
    exif_offset, gps_offset, ifd, metadatos = metadatos_info.first_ifd_process(datos, f_ifd_offset, tiff_header, orden)
    cont = 0
    rows = []
    frame = Frame( width=500, height=500)
    frame.place(x=20, y=230)
    cols = ('Datos', 'Valor')
    listbox = ttk.Treeview(frame, columns=cols, show='headings')
    for col in cols:
        listbox.heading(col, text=col)
        listbox.column(col, width=280)
    listbox.grid(row=1, column=0, columnspan=2)


    for key, value in metadatos['Oth IFD Metadatos'].items():
        listbox.insert('', 'end', values=(key, value))
    #listbox.pack()
    #frame.pack()
    #for key, value in metadatos['Oth IFD Metadatos'].items():
    #    cols = []
    #    tabla = Entry(text, relief=GROOVE, width=50)
    #    tabla.grid(row=cont, column=0, sticky=NSEW)
    #    tabla.insert(END, key)
    #    cols.append(tabla)
    #    tabla = Entry(text, relief=GROOVE, width=50)
    #    tabla.grid(row=cont, column=1, sticky=NSEW)
    #    tabla.insert(END, value)
    #    cols.append(tabla)
    #    rows.append(cols)
    #    cont += 1
    #res += ifd
    # Obtencion de metadatos EXIF
    exif, brillo = metadatos_info.exif_ifd_process(datos, exif_offset, tiff_header, orden)
    res += exif
    res += brillo

    if gps_offset > 0:
        gps = metadatos_info.gps_process(datos, gps_offset, tiff_header, orden)
        res += gps
    else:
        res += '--------------GPS IFD----------------\n'
        res += 'Datos de GPS no disponible\n'

    res += '-------------Matriz de Cuantificacion------------\n'
    matrices = metadatos_matriz.matriz_cuant(datos)
    res += matrices
    #text.insert(INSERT, res)
    #text.place(x=10, y=250, height=220, width=580)
    text['state'] ='disabled'
'''

def main(path):
    #interfaz()
    # Direcciones fijas de metadatos
    SOI = 0
    exif_header = 6
    tiff_header = 12
    num_campos_ad = 21
    inicio_campos = 23

    img = Image.open(path)
    datos, hex_datos = abrir_imagen_bin(path)

    #Orden: Big Endian o Little Endian
    orden = endian(datos, tiff_header)

    # Revisar si el archivo es JPEG o no
    if hex_datos[SOI][0] != 'f' or hex_datos[SOI][1] != 'f' or hex_datos[SOI + 1][0] != 'd' or hex_datos[SOI + 1][
        1] != '8':
        print('Error: no es un archivo JPEG')
        return
    elif not check_exif(datos[exif_header: tiff_header]):
        print('Error: El archivo no es archivo EXIF')
        return

    # Si el archivo es JPEG/EXIF

    # Obtener First 0th-IFD
    f_ifd_offset = num_campos_ad
    exif_offset, gps_offset, dict, aux = metadatos_info.first_ifd_process(datos, f_ifd_offset, tiff_header, orden)
    print(dict)

    #Obtencion de metadatos EXIF
    exif, aux, aux1 = metadatos_info.exif_ifd_process(datos, exif_offset, tiff_header, orden)
    print(exif)

    if gps_offset > 0:
        gps, aux = metadatos_info.gps_process(datos, gps_offset, tiff_header, orden)
        print(gps)
    else:
        print('--------------GPS IFD----------------')
        print('Datos de GPS no disponible')

    print('-------------Matriz de Cuantificacion------------')
    matriz, aux = metadatos_matriz.matriz_cuant(datos)

    print(matriz)



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


def extraer_metadatos(path):
    pass

def check_exif(datos):
    tipo = ''
    for i in datos:
        tipo += chr(i)
    if 'Exif' in tipo:
        return True
    else:
        return False

if __name__ == '__main__':
    '''
    tel = []
    for i in os.listdir(dir):
        tel.append(os.path.join(dir, i))
    images = []
    for i in tel:
        for j in os.listdir(i):
            images.append(os.path.join(i, j))
    for i in images:
        print(i)
        main(i)
    '''
    app = ForenseFotografia()
    app.geometry('680x500')
    app.resizable(width=False, height=False)
    app.mainloop()








