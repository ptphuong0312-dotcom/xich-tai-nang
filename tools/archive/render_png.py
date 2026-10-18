import fitz # PyMuPDF
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Render rendered_svg.html directly with PyMuPDF
doc = fitz.open(stream=open('rendered_svg.html', 'rb').read(), filetype="svg")
page = doc[0]
pix = page.get_pixmap(dpi=300)
pix.save("debug_fullview_render.png")
print("Saved debug_fullview_render.png")
