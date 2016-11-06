import sys
import numpy
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import morphology, label

def boxes(orig):
    img = ImageOps.grayscale(orig)
    im = numpy.array(img)

    # Inner morphological gradient.
    im = morphology.grey_dilation(im, (3, 3)) - im

    # Binarize.
    mean, std = im.mean(), im.std()
    t = mean + std
    im[im < t] = 0
    im[im >= t] = 1

    # Connected components.
    lbl, numcc = label(im)
    # Size threshold.
    min_size = 200 # pixels
    box = []
    for i in range(1, numcc + 1):
        py, px = numpy.nonzero(lbl == i)
        if len(py) < min_size:
            im[lbl == i] = 0
            continue

        xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
        # Four corners and centroid.
        box.append([
            [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)],
            (numpy.mean(px), numpy.mean(py))])

    return im.astype(numpy.uint8) * 255, box

def detect(image_file):

    image_type = image_file.split('.')[1]

    orig = Image.open(image_file)
    im, box = boxes(orig)

    # Draw perfect rectangles and the component centroid.
    img = Image.fromarray(im)
    visual = img.convert('RGB')
    draw = ImageDraw.Draw(visual)
    for b, centroid in box:
        draw.line(b + [b[0]], fill='green')
        cx, cy = centroid
        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill='red')
    visual.save(image_file.replace('.%s'%(image_type), '_squares.png'))

detect(sys.argv[1])