from osgeo import gdal

def open_image(fname):

	src = gdal.Open(fname)
	gt = src.GetGeoTransform()
	image = src.ReadAsArray()

	return image, src, gt