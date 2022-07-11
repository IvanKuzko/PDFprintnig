import fitz
import io
from PIL import Image


zoom = 10  # zoom for pixmap, for increasing picture quality
mat = fitz.Matrix(zoom, zoom)  # fitz.Matrix will add .get_pixmap
A4_size = [3508, 2480]
blank_size = [int(value/4) for value in A4_size]

pdf_path = "/Users/ivankuzko/Documents/Python_staff/PDFprintnig/documents/bbb.pdf"


A4_in_PIL = Image.new('RGB',
              A4_size,  # A4 at 300dpi
              (255, 255, 255))#(2478, 3504))

new_doc = fitz.open()


def a4_new():
    global A4_in_PIL
    global coords
    A4_in_PIL = Image.new('RGB',
                          A4_size,  # A4 at 300dpi
                          (255, 255, 255))  # (2478, 3504))
    coords = [0, 0]

path = "/Users/ivankuzko/Downloads/Prezentace z Endokrinologie a metabolizmu-20220711/Stitna zlaza - kazuistika - Limanova.pdf"
doc = fitz.open(path)
coords = [0, 0]

list_of_A4 = []

for page in doc:

    pixmap = page.get_pixmap(colorspace=fitz.csRGB, matrix=mat)
    bytes = pixmap.tobytes(output="png")
    io_ = io.BytesIO(bytes)
    slide = Image.open(io_)
    slide.thumbnail(blank_size)
    print(coords)
    try:
        if coords == [2631, 1860]:
            A4_in_PIL.paste(slide, box=tuple(coords))
            list_of_A4.append(A4_in_PIL)

            a4_new()
            #print(coordinates)


        if coords[0] != 3508:
            A4_in_PIL.paste(slide, box=tuple(coords))
            coords[0] = coords[0] + 877

        if coords[0] == 3508:
            A4_in_PIL.paste(slide, box=tuple(coords))
            coords[1] += 620
            coords[0] = 0
    except IndexError:
        pass

list_of_A4[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=list_of_A4)



