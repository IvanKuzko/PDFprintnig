import os
import fitz
import io
from PIL import Image
import PIL.ImageOps
import dominant_color

zoom = 10  # zoom for pixmap, for increasing picture quality
mat = fitz.Matrix(zoom, zoom)  # fitz.Matrix will add .get_pixmap
A4_size = [3508, 2480]
blank_size = [int(value/4) for value in A4_size]
A4_in_PIL = Image.new('RGB',A4_size,(255, 255, 255))
coords = [0, 0]
list_of_A4 = []


def a4_new():
    global A4_in_PIL
    global coords
    A4_in_PIL = Image.new('RGB',
                          A4_size,  # A4 at 300dpi
                          (255, 255, 255))  # (2478, 3504))
    coords = [0, 0]


def invert(pil):
    inverted_image = PIL.ImageOps.invert(pil)
    return inverted_image


def make_pil(page,inversion):
    pixmap = page.get_pixmap(colorspace=fitz.csRGB, matrix=mat)
    bytes = pixmap.tobytes(output="png")
    io_ = io.BytesIO(bytes)
    slide = Image.open(io_)
    color = dominant_color.get_dominant(slide)
    if inversion == False and color < (250, 250, 250):
        slide = invert(slide)
    slide.thumbnail(blank_size)
    return slide


def extend_with_blanks(list_of_PILs:list):
    number_of_blank = 16 - len(list_of_PILs) % 16

    blank_slide = Image.new("RGB", blank_size, (255, 255, 255))
    list_of_blanks = number_of_blank * [blank_slide]
    list_of_PILs.extend(list_of_blanks)
    return list_of_PILs


def add_to_a4(defenetive_list_of_pils):
    for slide in defenetive_list_of_pils:
        try:
            if coords == [2631, 1860]:
                A4_in_PIL.paste(slide, box=tuple(coords))
                list_of_A4.append(A4_in_PIL)
                a4_new()
            if coords[0] != 3508:
                A4_in_PIL.paste(slide, box=tuple(coords))
                coords[0] = coords[0] + 877

            if coords[0] == 3508:
                A4_in_PIL.paste(slide, box=tuple(coords))
                coords[1] += 620
                coords[0] = 0
        except IndexError:
            pass

def save_pdf(path, inversion):
    doc = fitz.open(path)
    list_of_PILs = [make_pil(page, inversion) for page in doc]
    defenetive_list_of_PILs = extend_with_blanks(list_of_PILs)
    add_to_a4(defenetive_list_of_PILs)
    pdf_path = "/Users/ivankuzko/Desktop/Prezentace/" + os.path.basename(path)
    list_of_A4[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=list_of_A4)



