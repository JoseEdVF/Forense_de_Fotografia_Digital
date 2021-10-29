import numpy as np

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