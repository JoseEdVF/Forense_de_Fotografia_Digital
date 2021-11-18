from json import dump

def exportar_a_txt(metadata_info_lists, path):
    with open(path, 'w+') as f:
        for metadata_info in metadata_info_lists:
            if metadata_info.is_exif and metadata_info.picture_type == 'JPEG':
                f.write(f'El archivo actual es: {metadata_info.file_name}\n')
                for key, value in metadata_info.exifread_tags.items():
                    f.write(f'{key} = {value["printable"]}\n')
                f.write(f'Brightness = {metadata_info.brightness}\n')
                f.write(f'Thumbnail Dimensions = {metadata_info.thumbnail_dimensions}\n')
                f.write(f'Image Dimensions = {metadata_info.image_dimensions}\n')
                f.write(f'JPEG Mode = {metadata_info.jpeg_mode}\n')
                f.write(f'-------------Matriz de Cuantificacion------------\n')
                f.write('Matrices de cuantificacion de Thumbnail\n')
                f.write(f'Matriz de Luminancia thumbnail (Y)\n')
                for i in metadata_info.luminance_matrix_thumbnail:
                    f.write(str(i)+'\n')
                f.write(f'Matriz de Cromas thumbnail (CbCr)\n')
                for i in metadata_info.chrominance_matrix_thumbnail:
                    f.write(str(i)+'\n')
                f.write('Matrices de Cuantificacion de la Imagen Primaria\n')
                f.write('Matriz de Luminancia (Y)\n')
                for i in metadata_info.luminance_matrix_image:
                    f.write(str(i)+'\n')
                f.write('Matriz de Cromas (CbCr)\n')
                for i in metadata_info.chrominance_matrix_image:
                    f.write(str(i)+'\n')
            else:
                if metadata_info.picture_type == 'Otro':
                    f.write(f'{metadata_info.file_name} no es JPEG\n')
                if not metadata_info.is_exif:
                    f.write(f'{metadata_info.file_name} es JFIF\n')



def exportar_a_json(metadata_info_list, path):
    meta_info = [{
        'file_name': metadata_info.file_name,
        'exifread_tags': metadata_info.exifread_tags,
        'brightness': metadata_info.brightness,
        'thumbnail_dimensions': metadata_info.thumbnail_dimensions,
        'image_dimensions': metadata_info.image_dimensions,
        'jpeg_mode': metadata_info.jpeg_mode,
        'luminance_matrix_thumbnail': metadata_info.luminance_matrix_thumbnail,
        'chrominance_matrix_thumbnail': metadata_info.chrominance_matrix_thumbnail,
        'luminance_matrix_image': metadata_info.luminance_matrix_image,
        'chrominance_matrix_image': metadata_info.chrominance_matrix_image
    } if metadata_info.is_exif and metadata_info.picture_type == 'JPEG' else {'file_name': metadata_info.file_name, 'message':'Archivo no valido'} for metadata_info in metadata_info_list]
    with open(path, 'w') as f:
        dump(meta_info, f, indent='\t')
