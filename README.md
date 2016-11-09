# Detect Squares

Makes use of the brilliant scikit-image library to detect the centers of basic square-like shapes in imagery and output these as points in a shapefile.

An application is shown below using a Landsat-8 panchromatic band as a test image. Although the resolution of the imagery does limit detection accuracy, a good number of squares were detected correctly providing a basic human population map. Landsat-8 imagery is freely available from [USGS Earthexplorer](https://aws.amazon.com/public-data-sets/landsat/).

Test image:
![alt text](https://github.com/BarnabyGordon/detect-squares/blob/master/figures/image_overview.jpeg)

Test image + detected squares (green points):
![alt text](https://github.com/BarnabyGordon/detect-squares/blob/master/figures/image%2Bpoints.jpeg)

Test image + heatmap of detected squares:
![alt text](https://github.com/BarnabyGordon/detect-squares/blob/master/figures/image%2Bheatmap.jpeg)


## Dependencies

- GDAL
- Numpy
- Scipy 
- Shapely
- Fiona
- Skimage