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

    if len(tag_db) == 1:
        matrices += 'No disponible'
        return matrices

    tag_mquant = []
    for i in tag_db:
        tag_mquant.append(tag_ff[i])

    matrices += 'Matrices de cuantificacion de Thumbnail: \n'

    vectorqy_thumb = datos[(tag_mquant[0]+5): (tag_mquant[0] + 68)+1]
    vectorqy_thumb = np.array(vectorqy_thumb).reshape((8, 8))
    matrices += 'Matriz de Luminancia (Y) = \n'
    for i in range(8):
        matrices += f'{vectorqy_thumb[i]}\n'

    vectorqcr_thumb = datos[tag_mquant[0] + 70 : (tag_mquant[0] + 133) + 1]
    vectorqcr_thumb = np.array(vectorqcr_thumb).reshape((8, 8))
    matrices += 'Matriz de Cromas (CbCr) = \n'
    for i in range(8):
        matrices += f'{vectorqcr_thumb[i]}\n'

    # Matriz de Imagen
    matrices += ' Matrices de Cuantificacion de la Imagen Primaria: \n'

    vectorqy_img = datos[tag_mquant[1] + 5 : (tag_mquant[1] + 68) + 1]
    vectorqy_img = np.array(vectorqy_img).reshape((8, 8))
    matrices += 'Matriz de Luminancia (Y) = \n'
    for i in range(8):
        matrices += f'{vectorqy_img[i]}\n'

    vectorqcr_img = datos[tag_mquant[1] + 70: (tag_mquant[1] + 133) + 1]
    vectorqcr_img = np.array(vectorqcr_img).reshape((8, 8))
    matrices += 'Matriz de Cromas (CrCb) = \n'
    for i in range(8):
        matrices += f'{vectorqcr_img[i]}\n'

    return matrices