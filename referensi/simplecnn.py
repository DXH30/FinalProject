import skimage.data
img = skimage.data.chelsea()
img = skimage.color.rgb2gray(img)

# Preparing Filters
l1_filter = numpy.zeros((2,3,3))
l1_filter[0, :, :] = numpy.array([[[-1, 0, 1],[-1, 0, 1],[-1, 0, 1]]])
l1_filter[1, :, :] = numpy.array([[[1, 1, 1],[0, 0, 0], [-1, -1, -1]]])

l1_feature_map = conv(img, l1_filter)

def conv(img, conv_filter):
    if len(img.shape) > 2 or len(conv_filter.shape) > 3:
        if img.shape[-1] != conv_filter.shape[-1]:
            print("Error: Number of channels in both image and filter must match.")
            sys.exit()
    if conv_filter.shape[1] != conv_filter.shape[2]:
        print('Error: Filter must be a square matrix. I. e. number of rows and columns must match.')
        sys.exit()
    if conv_filter.shape[1]%2 == 0:
        print('Error: Filter must have an odd size. I.e. number of rows and cols are odd')
        sys.exit()

    feature_maps = numpy.zeros((img.shape[0]-conv_filter.shape[1]+,
        img.shape[1]-conv_filter.shape[1]+1,
        conv_filter.shape[0]))

    for filter_num in range conv_filter.shape[0]):
        print("Filter ", filter_num + 1)
        curr_filter = conv_filter[filter_num, :]

        if len(curr_filter.shape) > 2:
            conv_map = conv_(img[:,:,0], curr_filter[:,:,0])
            for ch_num in range(1, curr, filter.shape[-1]):
                conv_map = conv_map + conv_(img[:, :, 0], curr_filter[:, :, ch_num])
        else:
            conv_map = conv_(img, curr_filter)
        feature_maps[:, :, filter_num] = conv_map
    return feature_maps
