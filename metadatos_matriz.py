import numpy as np

def matrices(hex_datos):
    num_mat = 0
    place = []
    for i in range(len(hex_datos)):
        if hex_datos[i] == 'ff' and hex_datos[i+1] == 'db':
            place.append(i+1)
            num_mat += 1

    matrices = []
    size_m = 0
    for i in range(len(place)):
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

    cont = 1
    mat_dict = {}
    mat_dict['Matriz'] = '-------------Matriz de Cuantificacion------------'
    for i in range(len(matrices)):
        aux = np.array(matrices[i])
        aux = aux.reshape((8,8))
        if i == 0:
            mat_dict['Thumbnail'] = 'Matrices de cuantificacion de Thumbnail'
            mat_dict['Thumbnail Y'] = 'Matriz de Luminancia thumbnail (Y)'
        elif i == 1:
            mat_dict['Thumbnail CbCr'] = 'Matriz de Cromas thumbnail (CbCr)'
        elif i == 2:
            mat_dict['Imagen Primaria'] = 'Matrices de Cuantificacion de la Imagen Primaria'
            mat_dict['Imagen Primaria Y'] = 'Matriz de Luminancia (Y)'
        elif i == 3:
            mat_dict['Imagen Primaria CbCr'] = 'Matriz de Cromas (CbCr)'
        elif i > 3:
            mat_dict['Info Extra'] = 'Matriz extra'
        for j in range(8):
            mat_dict[' ' * cont] = aux[j]
            cont += 1
    return mat_dict

def matriz_cuant(datos):
    tag_ff = []
    aux = []
    matrices = ''
    for i in range(len(datos)):
        if datos[i] == 255:
            tag_ff.append(i)
            aux.append(i+1)

    tag_db = []
    for i in range(len(aux)):
        if datos[aux[i]] == 219:
            tag_db.append(i)

    tag_mquant = []
    for i in tag_db:
        tag_mquant.append(tag_ff[i])

    matriz_dict = {}
    matriz_dict['-------------Matriz de Cuantificacion------------'] = ''
    if len(tag_db) == 1:
        vectorqy_thumb = datos[(tag_mquant[0] + 5): (tag_mquant[0] + 68) + 1]
        vectorqy_thumb = np.array(vectorqy_thumb).reshape((8, 8))
        matrices += 'Matriz de Luminancia (Y) = \n'
        matriz_dict['Matriz de Luminancia thumbnail (Y)'] = ''
        for i in range(8):
            matrices += f'{vectorqy_thumb[i]}\n'
            matriz_dict[' ' * i] = str(vectorqy_thumb[i])[1:-1]

        vectorqcr_thumb = datos[tag_mquant[0] + 70: (tag_mquant[0] + 133) + 1]
        vectorqcr_thumb = np.array(vectorqcr_thumb).reshape((8, 8))
        matrices += 'Matriz de Cromas (CbCr) = \n'
        matriz_dict['Matriz de Cromas thumbnail (CbCr)'] = ''
        for i in range(8):
            matrices += f'{vectorqcr_thumb[i]}\n'
            matriz_dict[' ' * (8 + i)] = str(vectorqcr_thumb[i])[1:-1]

        return matrices, matriz_dict

    matriz_thumb = {}
    matrices += 'Matrices de cuantificacion de Thumbnail: \n'
    matriz_dict['Matrices de cuantificacion de Thumbnail'] = ''
    vectorqy_thumb = datos[(tag_mquant[0]+5): (tag_mquant[0] + 68)+1]
    vectorqy_thumb = np.array(vectorqy_thumb).reshape((8, 8))
    matrices += 'Matriz de Luminancia (Y) = \n'
    matriz_dict['Matriz de Luminancia thumbnail (Y)'] = ''
    for i in range(8):
        matrices += f'{vectorqy_thumb[i]}\n'
        matriz_dict[' ' * i] = str(vectorqy_thumb[i])[1:-1]


    vectorqcr_thumb = datos[tag_mquant[0] + 70 : (tag_mquant[0] + 133) + 1]
    vectorqcr_thumb = np.array(vectorqcr_thumb).reshape((8, 8))
    matrices += 'Matriz de Cromas (CbCr) = \n'
    matriz_dict['Matriz de Cromas thumbnail (CbCr)'] = ''
    for i in range(8):
        matrices += f'{vectorqcr_thumb[i]}\n'
        matriz_dict[' ' * (8+i)] = str(vectorqcr_thumb[i])[1:-1]
    #matriz_dict['Matriz de Cromas thumbnail (CbCr)'] = vectorqcr_thumb

    # Matriz de Imagen
    matrices += ' Matrices de Cuantificacion de la Imagen Primaria: \n'
    matriz_dict['Matrices de Cuantificacion de la Imagen Primaria'] = ''

    vectorqy_img = datos[tag_mquant[1] + 5 : (tag_mquant[1] + 68) + 1]
    vectorqy_img = np.array(vectorqy_img).reshape((8, 8))
    matrices += 'Matriz de Luminancia (Y) = \n'
    matriz_dict['Matriz de Luminancia (Y)'] = ''
    for i in range(8):
        matrices += f'{vectorqy_img[i]}\n'
        matriz_dict[' ' * (16+i)] = str(vectorqy_img[i])[1:-1]
    #matriz_dict['Matriz de Luminancia (Y)'] = vectorqy_img

    vectorqcr_img = datos[tag_mquant[1] + 70: (tag_mquant[1] + 133) + 1]
    vectorqcr_img = np.array(vectorqcr_img).reshape((8, 8))
    matrices += 'Matriz de Cromas (CrCb) = \n'
    matriz_dict['Matriz de Cromas (CrCb))'] = ''
    for i in range(8):
        matrices += f'{vectorqcr_img[i]}\n'
        matriz_dict[' ' * (24+i)] = str(vectorqcr_img[i])[1:-1]
    #matriz_dict['Matriz de Cromas (CrCb)'] = vectorqcr_img

    return matrices, matriz_dict