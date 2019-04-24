import skimage.data
img = skimage.data.chelsea()
img = skimage.color.rgb2gray(img)

# Preparing Filters
l1_filter = numpy.zeros((2,3,3))
