class ImageMetadata:
    picture_type: str = 'JPEG'
    is_exif: bool = True
    file_name: str
    exifread_tags: dict
    brightness: float
    thumbnail_dimensions: list
    image_dimensions: list
    jpeg_mode: int
    luminance_matrix_thumbnail: list
    chrominance_matrix_thumbnail: list
    luminance_matrix_image: list
    chrominance_matrix_image: list

