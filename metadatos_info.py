import numpy as np
import math

#Aqui se encuentran las diferentes funciones que obtienen informacion sobre la imagen

def get_ascii(val, c):
    res = ''
    for i in range(c):
        if val[i] in range(31):
            res += ''
        else:
            res += chr(val[i])
    return res

def get_byte_number(tipo, cont):
    if tipo == 1:
        num_bytes = cont
    elif tipo == 2:
        num_bytes = cont
    elif tipo == 3:
        num_bytes = cont * 2
    elif tipo == 4:
        num_bytes = cont * 4
    elif tipo == 5:
        num_bytes = cont * 2 * 4
    elif tipo == 7:
        num_bytes = cont * 1
    elif tipo == 9:
        num_bytes = cont * 4
    elif tipo == 10:
        num_bytes = cont * 2 * 4
    else:
        num_bytes = 0

    return num_bytes

def get_final_value(datos, tipo, cont, orden):
    if tipo == 1:
        res = datos
    elif tipo == 2:
        res = get_ascii(datos, len(datos))
    elif tipo == 3:
        res = []
        for i in range(cont):
            if orden == 1:
                res.append(datos[(2*i)+1] * 16**2 + datos[2*i])
            else:
                res.append(datos[2*i] * 16**2 + datos[(2*i)+1])
    elif tipo == 4:
        res = []
        for i in range(cont):
            if orden == 1:
                res.append(datos[3] * 16**6 + datos[2] * 16**4 + datos[1] * 16**2 + datos[0])
            else:
                res.append(datos[0] * 16**6 + datos[1] * 16**4 + datos[2] * 16**2 + datos[3])
    elif tipo == 5:
        res = []
        for i in range(cont):
            st = (((i+1)-1) * 8)
            if orden == 1:
                numera = datos[(st + 4)-1] * 16**6 + datos[(st + 3)-1] * 16**4 + datos[(st+2)-1] * 16**2 + \
                         datos[(st + 1)-1]
            else:
                numera = datos[(st + 1)-1] * 16**6 + datos[(st + 2)-1] * 16**4 + datos[(st + 3)-1] * 16**2 + \
                         datos[(st + 4)-1]

            if orden == 1:
                denom = datos[(st + 8)-1] * 16**6 + datos[(st + 7)-1] * 16**4 + datos[(st + 6)-1] * 16**2 + \
                        datos[(st + 5)-1]
            else:
                denom = datos[(st + 5)-1] * 16**6 + datos[(st + 6)-1] * 16**4 + datos[(st + 7)-1] * 16**2 + \
                        datos[(st + 8)-1]
            res.append(numera/denom)
    elif tipo == 7:
        res = []
        if cont == 8:
            if orden == 1:
                res.append(datos[2-1] * 16**2 + datos[1-1])
                res.append(datos[4-1] * 16**2 + datos[3-1])
                res.append(datos[5-1])
                res.append(datos[6-1])
                res.append(datos[7-1])
                res.append(datos[8-1])
            else:
                res.append(datos[1-1] * 16**2 + datos[2-1])
                res.append(datos[3-1] * 16**2 + datos[4-1])
                res.append(datos[5-1])
                res.append(datos[6-1])
                res.append(datos[7-1])
                res.append(datos[8-1])
        else:
            res.append(get_ascii(datos, len(datos)))
    elif tipo == 10:
        res = []
        for i in range(cont):
            if orden == 1:
                numera = datos[4-1] * 16**6 + datos[3-1] * 16**4 + datos[2-1] * 16**2 + datos[1-1]
            else:
                numera = datos[1-1] * 16**6 + datos[2-1] * 16**4 + datos[3-1] * 16**2 + datos[4-1]

            if orden == 1:
                denom = datos[8-1] * 16**6 + datos[7-1] * 16**4 + datos[6-1] * 16**2 + datos[5-1]
            else:
                denom = datos[5-1] * 16**6 + datos[6-1] * 16**4 + datos[7-1] * 16**2 + datos[8-1]
            res.append(numera/denom)
    else:
        res = np.zeros(1, cont)

    return res


def segment_campo(campo, orden):
    #Little Endian
    if orden == 1:
        tag_val = campo[1] * (16**2) + campo[0]
        tipo_val = campo[3] * (16**2) + campo[2]
        count_val = campo[7] * (16**4) + campo[6] * (16**3) + campo[5] * (16**2) + campo[4]

        #Byte
        if tipo_val == 1:
            off_val = campo[8]
        #Ascii
        elif tipo_val == 2:
            if count_val <= 4:
                off_val = get_ascii(campo[8:11], len(campo[8:11]))
            else:
                off_val = campo[11] * 16**4 + campo[10] * 16**2 + campo[9] * 16**2 + campo[8]
        #No definido
        elif tipo_val == 7:
            if count_val == 4:
                off_val = get_ascii([campo[8], campo[9], campo[10], campo[11]], 4)
            else:
                off_val = campo[11] * 16**4 + campo[10] * 16**3 + campo[9] * 16**2 + campo[8]
        else:
            off_val = campo[11] * 16**4 + campo[10] * 16**3 + campo[9] * 16**2 + campo[8]
    else:
        tag_val = campo[0] * 16**2 + campo[1]
        tipo_val = campo[2] * 16**2 + campo[3]
        count_val = campo[4] * 16**4 + campo[5] * 16**3 + campo[6] * 16**2 + campo[7]

        #Byte
        if tipo_val == 1:
            off_val = campo[8]
        #Ascii
        elif tipo_val == 2:
            if count_val <= 4:
                off_val = get_ascii(campo[8:11], len(campo[8:11]))
            else:
                off_val = campo[8] * 16**4 + campo[9] * 16**3 + campo[10] * 16**2 + campo[11]
        #Short
        elif tipo_val == 3:
            if count_val < 2:
                off_val = campo[8] * 16**2 + campo[9]
            else:
                off_val = campo[8] * 16**4 + campo[9] * 16**3 + campo[10] * 16**2 + campo[11]
        #No definido
        elif tipo_val == 7:
            if count_val == 4:
                off_val = get_ascii([campo[8], campo[9], campo[10], campo[11]], 4)
            elif count_val == 1:
                off_val = campo[8]
            else:
                off_val = campo[8] * 16**4 + campo[9] * 16**3 + campo[10] * 16**2 + campo[11]
        else:
            off_val = campo[8] * 16 ** 4 + campo[9] * 16 ** 3 + campo[10] * 16 ** 2 + campo[11]

    return tag_val, tipo_val, count_val, off_val


def first_ifd_process(datos, offset, tiff_header, orden):
    image_data_name = ['Ancho de la Imagen','Alto de la Imagen', 'Bits por muestra',
                        'Compresion (1: no-comprimido, 6; JPEG Compression)', 'Pixel_Comp (2: RGB, 6: YCbCr)',
                        'Orientacion (1-8)','Sample por Pixel (3: default)','Plana Config',
                        'YCbCrSubSample [2,1]: 4:2:2, [2,2]: 4:2:0', 'YCbCrPosition (1: centered, 2: co-sited)',
                        'Resolución en X','Resolución en Y', 'Unidad de Resolución (2: inches, 3: centimetros)',
                        'StripOffsets', 'RowsperStrip','StripByteCounts','JPEGInterchangeFormat',
                        'JPEGInterchangeFLength', 'TransferFunction','WhitePoint','PrimaryChromaticities',
                        'YCbCrCoefficients','ReferenceBlackWhite','DateTime','ImageDescription','Make','Model',
                        'Software', 'Artist', 'Copyright', 'Exif_offset', 'GPS_offset']

    image_tag = [256, 257, 258, 259, 262, 274, 277, 284, 530, 531, 282, 283, 296, 273, 278, 279, 513, 514,
                  301, 318, 319, 529, 532, 306, 270, 271, 272, 305, 315, 33432, 34665, 34853]

    val_o_offset = [0,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0]
    tabla_l = len(image_tag)
    inicio_campos = offset + 2

    num1 = offset
    num2 = num1 + 1

    if orden == 1:
        num_campos = datos[num2-1] * (16**2) + datos[num1-1]
    else:
        num_campos = datos[num1-1] * (16**2) + datos[num2-1]

    # Analiza cada campo
    inicio = inicio_campos-1
    campo = []
    tag_val = np.zeros((1, num_campos), dtype='int64')
    tipo_val = np.zeros((1, num_campos), dtype='int64')
    count_val = np.zeros((1, num_campos), dtype='int64')
    off_val = np.zeros((1, num_campos), dtype='int64')

    for i in range(num_campos):
        fin = inicio+12
        campo.append(datos[inicio:fin])
        tag_val[0][i], tipo_val[0][i], count_val[0][i], off_val[0][i] = segment_campo(campo[i], orden)
        inicio = fin

    final_value = []
    final_data_name = []

    for i in range(num_campos):
        try:
            ind = image_tag.index(tag_val[0][i])
        except:
            final_value.append(None)
            final_data_name.append(None)
            continue

        flag_offset = val_o_offset[ind]

        if flag_offset == 1:
            #TIFF_HEADER + off_val(i)
            count = count_val[0, i]
            sp = tiff_header + off_val[0, i]
            count_byte = get_byte_number(tipo_val[0, i], count)
            b = datos[int(sp):int(sp+count_byte)]
            final_value.append(get_final_value(b, tipo_val[0, i], int(count), orden))
        else:
            final_value.append(off_val[0, i])

        final_data_name.append(image_data_name[ind])

    #Desplegar resultados
    for i in range(len(final_value)):

        if final_value[i] is None:
            final_value[i] = 'No especifica'

    ifd = ''

    metadatos = {}

    if orden == 1:
        ifd += 'Orden: Little Endian (Intel)\n'
        metadatos['Orden'] = 'Little Endian (Intel)'
    else:
        ifd +='Orden: Big Endian (Motorola)\n'
        metadatos['Orden'] = 'Big Endian (Motorola)'

    ifd +='----------Oth IFD Metadatos -------------\n'
    metadatos_ifd = {}
    metadatos_ifd['----------Oth IFD Metadatos -------------'] = ''
    for i in range(len(final_value)):
        if final_data_name[i] is None:
            continue
        else:
            #ifd += f'{final_data_name[i]} = {final_value[i]}\n'
            if tipo_val[0, i] == 1:
                ifd +=f'{final_data_name[i]} = {final_value[i]}\n'
                metadatos_ifd[final_data_name[i]] = final_value[i]
            elif tipo_val[0, i] == 3:
                ifd +=f'{final_data_name[i]} = {final_value[i]}\n'
                metadatos_ifd[final_data_name[i]] = final_value[i]
            elif tipo_val[0, i] == 4:
                ifd +=f'{final_data_name[i]} = {final_value[i]}\n'
                metadatos_ifd[final_data_name[i]] = final_value[i]
            elif tipo_val[0, i] == 5:
                ifd +=f'{final_data_name[i]} = {final_value[i]}\n'
                metadatos_ifd[final_data_name[i]] = final_value[i]
            else:
                ifd +=f'{final_data_name[i]} = {final_value[i]}\n'
                metadatos_ifd[final_data_name[i]] = final_value[i]

    metadatos['Oth IFD Metadatos'] = metadatos_ifd
    aux = np.ndarray.tolist(tag_val)[0]
    aux = [int(i) for i in aux]
    exif_offset = final_value[aux.index(34665)]



    try:
        gps = aux.index(34853)
        gps_offset = final_value[gps]
    except ValueError:
        gps_offset = -1

    return exif_offset, gps_offset, ifd, metadatos

def exif_ifd_process(datos, exif_offset, tiff_header, orden):
    exif_data_name = ['Versión de Exif','Versión de Flashpix','Espacio de color',
    'Tiempo de apertura(Exposure Time)','F Number','Clase de programa usada por la cámara para definir exposición',
    'Sensibilidad espectral de cada canal','Velocidad de ISO ',
    'OECF (Opto-Electric Conversion Function)','Shutter Speed(APEX)','Apertura(APEX)','Valor de Brightness (APEX)',
    'Bias de exposición (APEX)','Máxima Apertura (APEX) ','Distancia entre cámara y objeto (metros)',
    'Metering Mode','Tipo de fuente de luz','Estado de flash','Longitud Focal','Localización y área de objeto',
    'Energía de flash (Beam Candle Power Second)','Respuesta de frecuencia especial',
    'Número de pixeles en ancho de imagen por la unidad de resolución focal ',
    'Número de pixeles en alto de imagen por la unidad de resolución focal','Unidad para medir Resolución focal',
    'Localización de objeto principal','Índice de exposición seleccionada por la cámara','Tipo de sensor de la cámara',
    'Fuente de imagen','Tipo de escena','Geometrica de Color Filter Array (CFA)',
    'Uso de proceso especial sobre la imagen','Modo de exposición','Balance de blancos','Tasa de zoom digital',
    'Valor equivalente de focal length para cámara de 35mm film', 'Tipo de escena que tomó',
    'Ajuste de ganancia de imagen','Ajuste de contraste','Ajuste de saturación','Procesamiento de “Sharpness”',
    'Condición especial de una cámara particular','Distancia a objeto','Identificador de imagen']

    exif_tag = [36864,40960,40961,33434,33437,34850,34852,34855,34856,37377,37378,37379,37380,37381,37382,37383,37384,
                37385,37386,37396,41483,41484,41486,41487,41488,41492,41493,41495,41728,41729,41730,41985,41986,41987,
                41988,41989,41990,41991,41992,41993,41994,41995,41996,42016]

    exif_offset_1 = [0,0,0,1,1,0,1,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,1]

    exif_table = len(exif_tag)

    pos_campos_exif = exif_offset + tiff_header
    in_campos_exif = exif_offset + tiff_header + 2

    #Obtener el numero de campos EXIF

    num1 = pos_campos_exif
    num2 = num1 + 1

    if orden == 1:
        num_campos_exif = datos[num2] * 16**2 + datos[num1]
    else:
        num_campos_exif = datos[num1] * 16**2 + datos[num2]

    #Analizar cada campo
    ini_exif = int(in_campos_exif)
    campo_exif = []
    tag_val_exif = np.zeros((1, num_campos_exif), dtype='int64')
    tipo_val_exif = np.zeros((1, num_campos_exif), dtype='int64')
    count_val_exif = np.zeros((1, num_campos_exif), dtype='int64')
    off_val_exif = []

    for i in range(num_campos_exif):
        fin_exif = ini_exif + 12
        campo_exif.append(datos[ini_exif: fin_exif])
        tag_val_exif[0][i], tipo_val_exif[0][i], count_val_exif[0][i], offset_var = \
            segment_campo(campo_exif[i], orden)
        off_val_exif.append(offset_var)
        ini_exif = fin_exif

    final_value_exif = []
    final_name_exif = []

    for i in range(num_campos_exif):
        try:
            ind = exif_tag.index(tag_val_exif[0][i])
        except ValueError:
            final_name_exif.append(None)
            final_value_exif.append(None)
            continue

        flag_offset = exif_offset_1[ind]

        if flag_offset == 1:
            count = count_val_exif[0][i]
            sp = tiff_header + off_val_exif[i]
            count_byte = get_byte_number(tipo_val_exif[0][i], count)
            b = datos[int(sp) : int(sp + count_byte)]
            final_value_exif.append(get_final_value(b, tipo_val_exif[0][i], count, orden))
        else:
            final_value_exif.append(off_val_exif[i])

        final_name_exif.append(exif_data_name[ind])

    for i in range(num_campos_exif):
        if final_value_exif[i] is None:
            final_value_exif[i] = 'No especifica'
    '''
    print(type(final_value_exif))
    for i in range(num_campos_exif):
        if type(final_value_exif[i]) == type([]):
            final_value_exif[i] = final_value_exif[i][0]
    '''

    metadatos_exif = {}

    exif = ''
    exif += '------------EXIF IFD Metadatos ----------------\n'
    metadatos_exif['------------EXIF IFD Metadatos ----------------'] = ''

    for i in range(num_campos_exif):
        if final_name_exif[i] is None:
            continue
        else:
            if tipo_val_exif[0, i] == 1:
                exif += f'{final_name_exif[i]} = {final_value_exif[i]}\n'
                metadatos_exif[final_name_exif[i]] = final_value_exif[i]
            elif tipo_val_exif[0, i] == 3:
                exif += f'{final_name_exif[i]} = {final_value_exif[i]}\n'
                metadatos_exif[final_name_exif[i]] = final_value_exif[i]
            elif tipo_val_exif[0, i] == 4:
                exif += f'{final_name_exif[i]} = {final_value_exif[i]}\n'
                metadatos_exif[final_name_exif[i]] = final_value_exif[i]
            elif tipo_val_exif[0, i] == 5:
                exif += f'{final_name_exif[i]} = {final_value_exif[i]}\n'
                metadatos_exif[final_name_exif[i]] = final_value_exif[i]
            elif tipo_val_exif[0, i] == 10:
                exif += f'{final_name_exif[i]} = {final_value_exif[i]}\n'
                metadatos_exif[final_name_exif[i]] = final_value_exif[i]
            else:
                exif += f'{final_name_exif[i]} = {final_value_exif[i]}\n'
                metadatos_exif[final_name_exif[i]] = final_value_exif[i]

    #Calculo de brillo

    aux = np.ndarray.tolist(tag_val_exif)
    brillo = ''
    if not exif_tag[9] in aux[0] and not exif_tag[3] in aux[0]:
        brillo += 'No es posible calcular el brillo\n'
        metadatos_exif['Brillo'] = 'No es posible calcular el brillo'
    elif not exif_tag[7] in aux[0] or not exif_tag[4] in aux[0]:
        brillo += 'No es posible calcular el brillo\n'
        metadatos_exif['Brillo'] = 'No es posible calcular el brillo'
    else:
        if not exif_tag[7] in aux[0]:
            t = final_value_exif[aux[0].index(exif_tag[9])]
        else:
            t = final_value_exif[aux[0].index(exif_tag[3])]
        s = final_value_exif[aux[0].index(exif_tag[7])]
        n = final_value_exif[aux[0].index(exif_tag[4])]
        bamb = n[0] ** 2 / (t[0] * s)
        bv = 3.32 * math.log(bamb, 10) + 1.66
        brillo += 'Brillo (APEX) = {:.4f}\n'.format(bv)
        metadatos_exif['Brillo (APEX)'] = '{:.4f}'.format(bv)

    return exif, brillo, metadatos_exif

    '''
    try:
        brillo = ''
        brillo = aux[0].index(exif_tag[9])
    except ValueError:
        try:
            brillo = aux[0].index(exif_tag[3])
        except ValueError:
            print('No es posible calcular el brillo')

    try:
        brillo = ''
        brillo = aux[0].index(exif_tag[7])
        brillo = aux[0].index(exif_tag[4])
    except ValueError:
        print('No se puede calcular el brillo')

    try:
        t = final_value_exif[aux[0].index(exif_tag[9])]
    except ValueError:
        t = final_value_exif[aux[0].index(exif_tag[3])]
    '''



    # ¿Distancia?

def gps_process(datos, gps_offset, tiff_header, orden):
    gps_data_name = ['GPS tag version', 'North or South Latitude', 'Latitude', 'East or West Longitude', 'Longitude',
                     'Altitude reference', 'Altitude', 'GPS time', 'GPS Satellites used for measurement',
                     'GPS receiver status', 'GPS measurement mode', 'Measurement precision', 'Speed unit',
                     'Speed of GPS receiver', 'Reference for direction of movement', 'Direction of movement',
                     'Reference for direction of image', 'Direction of image', 'Geodetic survey data used',
                     'Reference for latitute of destination', 'latitude of destination',
                     'Reference for longitude of destination', 'longitude of destination',
                     'Reference for bearing of destination', 'Bearing of destination',
                     'Reference for distance to destination', 'Distance to destination',
                     'Name of GPS processing method', 'Name of GPS area', 'GPS date', 'GPS differential correction']

    gps_tag = [i for i in range(31)]
    offset_flag = [0,0,1,0,1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,1,1,1,0]

    pos_campos_gps = gps_offset + tiff_header
    in_campos_gps = pos_campos_gps + 2

    #Obtener el numero de campos de GPS IFD
    num1 = pos_campos_gps
    num2 = num1 + 1

    if orden == 1:
        num_campos_gps = datos[num2] * 16**2 + datos[num1]
    else:
        num_campos_gps = datos[num1] * 16**2 + datos[num2]

    # Se analiza cada campo
    ini_gps = in_campos_gps
    campo_gps = []
    tag_val_gps = np.zeros((1, num_campos_gps), dtype='int64')
    tipo_val_gps = np.zeros((1, num_campos_gps), dtype='int64')
    count_val_gps = np.zeros((1, num_campos_gps), dtype='int64')
    off_val_gps = []

    for i in range(num_campos_gps):
        #cada campo tiene 12 bytes
        fin_gps = ini_gps + 12
        campo_gps.append(datos[int(ini_gps) : int(fin_gps)])
        tag_val_gps[0, i], tipo_val_gps[0, i], count_val_gps[0, i], offset_var = segment_campo(campo_gps[i], orden)
        off_val_gps.append(offset_var)
        ini_gps = fin_gps

    #Depende del valor de tag, se realiza una operacion
    final_value_gps = []
    final_name_gps = []
    for i in range(num_campos_gps):
        try:
            ind = gps_tag.index(tag_val_gps[0, i])
        except ValueError:
            final_name_gps.append(None)
            final_value_gps.append(None)
            continue

        flag_offset = offset_flag[ind]

        if flag_offset == 1:
            count = count_val_gps[0, i]
            #Contabiliza desde el tiff_header + 1
            sp = tiff_header + off_val_gps[i]
            #Cuantos se leeran
            count_byte = get_byte_number(tipo_val_gps[0, i], count)
            b = datos[sp:sp+count_byte]
            final_value_gps.append(get_final_value(b, tipo_val_gps[0, i], count, orden))
        else:
            final_value_gps.append(off_val_gps[i])

        final_name_gps.append(gps_data_name[ind])

    for i in range(num_campos_gps):
        if final_value_gps[i] is None:
            final_value_gps[i] = 'No especifica'

    gps = ''

    gps += '---------------GPS IFD Metadatos-----------------\n'
    gps_dict = {}
    gps_dict['---------------GPS IFD Metadatos-----------------'] = ''

    for i in range(num_campos_gps):
        if final_name_gps[i] is None:
            continue
        else:
            if tipo_val_gps[0, i] == 1:
                gps += f'{final_name_gps[i]} = {final_value_gps[i]}\n'
                gps_dict[final_name_gps[i]] = final_value_gps[i]
            elif tipo_val_gps[0, i] == 2:
                gps += f'{final_name_gps[i]} = {final_value_gps[i]}\n'
                gps_dict[final_name_gps[i]] = final_value_gps[i]
            elif tipo_val_gps[0, i] == 3:
                gps += f'{final_name_gps[i]} = {final_value_gps[i]}\n'
                gps_dict[final_name_gps[i]] = final_value_gps[i]
            elif tipo_val_gps[0, i] == 4:
                gps += f'{final_name_gps[i]} = {final_value_gps[i]}\n'
                gps_dict[final_name_gps[i]] = final_value_gps[i]
            elif tipo_val_gps[0, i] == 5:
                gps += f'{final_name_gps[i]} = {final_value_gps[i]}\n'
                gps_dict[final_name_gps[i]] = final_value_gps[i]
            elif tipo_val_gps[0, i] == 10:
                gps += f'{final_name_gps[i]} = {final_value_gps[i]}\n'
                gps_dict[final_name_gps[i]] = final_value_gps[i]
            else:
                gps += f'{final_name_gps[i]} = {final_value_gps[i]}\n'
                gps_dict[final_name_gps[i]] = final_value_gps[i]

    return gps, gps_dict