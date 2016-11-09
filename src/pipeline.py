import numpy as np
from skimage import exposure
from scipy.ndimage import morphology, label
from shapely.geometry import Point, mapping
from fiona import collection

def find_squares(x, y, KERNEL_SIZE, image):

    p2, p98 = np.percentile(image, (2, 98))
    im = exposure.rescale_intensity(image, in_range=(p2, p98))

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
    min_size = 60 # pixels
    box = []
    for i in range(1, numcc + 1):
        py, px = np.nonzero(lbl == i)
        if len(py) < min_size:
            continue

        xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
        # Four corners and centroid.
        box.append([
            [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)],
            (np.mean(px)+(x*KERNEL_SIZE), np.mean(py)+(y*KERNEL_SIZE))])

    return box


def squares_to_shapefile(squares, shapefile, gt):

    schema = { 'geometry': 'Point', 'properties': { 'SITEID': 'str' } }

    with collection(shapefile, 'w', 'ESRI Shapefile', schema) as output:
        for square in squares:
            for b, centroid in square:
                cx, cy = centroid
                lng, lat = _pixel2world(gt, cx, cy)
                point = Point(lng, lat)
                output.write({
                        'properties': {'SITEID': 'hello'},
                        'geometry': mapping(point)
                    })


def _pixel2world(gt, x, y):

    gsd = gt[1]
    ulX, ulY = gt[0], gt[3]

    lat, lng = (-y*gsd)+ulY, (x*gsd)+ulX

    return lng, lat


def gridspec(KERNEL_SIZE, src, gt):

    image_width = src.RasterXSize
    image_height = src.RasterYSize
    gsd = gt[1]
    grid_width = int(np.floor(image_width/KERNEL_SIZE))
    grid_height = int(np.floor(image_height/KERNEL_SIZE))

    return grid_width, grid_height




