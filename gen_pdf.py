from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait

img_dir = 'out/'
PAGES = 320
width = 1441
height = 2026

c = canvas.Canvas("result.pdf", pagesize=portrait((width, height)))

for i in range(1, PAGES + 1):
    img = f'{img_dir}{i}.png'
    c.drawImage(img, 0, 0, width, height)
    c.showPage()

    # Progress Bar
    print('\r{:5d} / {}'.format(i, PAGES), end='')

c.save()