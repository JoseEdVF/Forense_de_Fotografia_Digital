import math
import numpy as np

def brightness(fnumber, etime, isospeed):
    escena = []
    try:
        fnumber = fnumber.split('/')
        if len(fnumber) == 2:
            fnumber = int(fnumber[0]) / int(fnumber[1])
        else:
            fnumber = int(str(fnumber))
        etime = str(etime).split('/')
        if len(etime) == 2:
            etime = int(etime[0]) / int(etime[1])
        else:
            etime = int(str(etime))

        isospeed = str(isospeed).split('/')
        if len(isospeed) == 2:
            isospeed = int(isospeed[0]) / int(isospeed[1])
        else:
            isospeed = int(str(isospeed))
        bamb = fnumber ** 2 / (etime * isospeed)
        bv = 3.32 * math.log(bamb, 10) + 1.66
        brightness = bv
    except:
        brightness = None

    return brightness

def start_of_frame(hex_datos, orden):
    for i in range(len(hex_datos)):
        if len(hex_datos[i]) == 1:
            hex_datos[i] = '0' + hex_datos[i]

    place = []
    for i in range(len(hex_datos)):
        if hex_datos[i] == 'ff' and hex_datos[i + 1] == 'c0':
            place.append(i + 1)
    height = []
    width = []
    for i in range(len(place)):
        if hex_datos[place[i] + 1] == '00' and hex_datos[place[i] + 2] == '11':
            inicio_height = place[i] + 4
            inicio_width = inicio_height + 2

            height.append(hex_datos[inicio_height: inicio_width])
            width.append(hex_datos[inicio_width: inicio_width + 2])
        else:
            continue
    ans = {}
    aux = ''
    image_dimensions = []
    thumbnail_dimesions = []
    if len(height) == 1:
        ans['Image Dimensions'] = f'{int(aux.join(height[0]), 16)} x {int(aux.join(width[0]), 16)}'
        image_dimensions.append(int(aux.join(height[0]), 16))
        image_dimensions.append(int(aux.join(width[0]), 16))
    elif len(height) == 2:
        ans['Thumbnail Dimensions'] = f'{int(aux.join(height[0]), 16)} x {int(aux.join(width[0]), 16)}'
        ans['Image Dimensions'] = f'{int(aux.join(height[1]), 16)} x {int(aux.join(width[1]), 16)}'
        image_dimensions.append(int(aux.join(height[0]), 16))
        image_dimensions.append(int(aux.join(width[0]), 16))
        thumbnail_dimesions.append(int(aux.join(height[0]), 16))
        thumbnail_dimesions.append(int(aux.join(width[0]), 16))

    jpeg_mode = hex_datos[inicio_width + 4]
    ans['JPEG Mode'] = jpeg_mode

    return ans, thumbnail_dimesions, image_dimensions, jpeg_mode

def matrices(hex_datos):
    ZigZag_order = [[0, 0], [0, 1], [1, 0], [2, 0], [1, 1], [0, 2], [0, 3], [1, 2], [2, 1], [3, 0], [4, 0],
                    [3, 1], [2, 2], [1, 3], [0, 4], [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0], [6, 0],
                    [5, 1], [4, 2], [3, 3], [2, 4], [1, 5], [0, 6], [0, 7], [1, 6], [2, 5], [3, 4], [4, 3],
                    [5, 2], [6, 1], [7, 0], [7, 1], [6, 2], [5, 3], [4, 4], [3, 5], [2, 6], [1, 7], [2, 7],
                    [3, 6], [4, 5], [5, 4], [6, 3], [7, 2], [7, 3], [6, 4], [5, 5], [4, 6], [3, 7], [4, 7],
                    [5, 6], [6, 5], [7, 4], [7, 5], [6, 6], [5, 7], [6, 7], [7, 6], [7, 7]]

    num_mat = 0
    place = []
    for i in range(len(hex_datos)):
        if hex_datos[i] == 'ff' and hex_datos[i+1] == 'db':
            place.append(i+1)
            num_mat += 1

    matrices = []
    size_m = 0
    for i in range(len(place)):
        if hex_datos[place[i] + 2] != '84' and hex_datos[place[i] + 2] != '43':
            continue
        else:
            try:
                size_m = int(hex_datos[place[i] + 2])
            except:
                continue
            inicio_mat = place[i] + 4
            if size_m > 67:
                espacio_mat = inicio_mat + 65
                matrices.append(hex_datos[inicio_mat: inicio_mat + 64])
                matrices.append(hex_datos[espacio_mat: espacio_mat + 64])
            else:
                matrices.append(hex_datos[inicio_mat: inicio_mat + 64])

    for i in range(len(matrices)):
        for j in range(len(matrices[i])):
            matrices[i][j] = int(matrices[i][j], 16)

    aux = np.zeros((8, 8), dtype='int32')
    for i in range(len(matrices)):
        for j in range(len(matrices[i])):
            ind = ZigZag_order[j]
            aux[ind[0], ind[1]] = matrices[i][j]
        matrices[i] = aux
        aux = np.zeros((8, 8), dtype='int32')

    cont = 1
    disp_mat_dict = {}
    disp_mat_dict['Matriz'] = '-------------Matriz de Cuantificacion------------'
    mat_dict = {}
    for i in range(len(matrices)):
        aux = np.array(matrices[i])
        aux_save = aux.reshape((8,8))
        aux_disp = aux.reshape((8,8))
        if i == 0:
            disp_mat_dict['Thumbnail'] = 'Matrices de cuantificacion de Thumbnail'
            disp_mat_dict['Thumbnail Y'] = 'Matriz de Luminancia thumbnail (Y)'
            mat_dict['luminance_matrix_thumbnail'] = aux_save.tolist()
        elif i == 1:
            disp_mat_dict['Thumbnail CbCr'] = 'Matriz de Cromas thumbnail (CbCr)'
            mat_dict['chrominance_matrix_thumbnail'] = aux_save.tolist()
        elif i == 2:
            disp_mat_dict['Imagen Primaria'] = 'Matrices de Cuantificacion de la Imagen Primaria'
            disp_mat_dict['Imagen Primaria Y'] = 'Matriz de Luminancia (Y)'
            mat_dict['luminance_matrix_image'] = aux_save.tolist()
        elif i == 3:
            disp_mat_dict['Imagen Primaria CbCr'] = 'Matriz de Cromas (CbCr)'
            mat_dict['chrominance_matrix_image'] = aux_save.tolist()
        elif i > 3:
            disp_mat_dict['Info Extra'] = 'Matriz extra'
        for j in range(8):
            disp_mat_dict[' ' * cont] = aux_disp[j]
            cont += 1
    return disp_mat_dict, mat_dict