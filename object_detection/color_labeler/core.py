"""
Assigns a human understandable label to a color value


"""
from collections import OrderedDict
import pandas as pd
import numpy as np
import cv2


def estimate_color(img, box=None):
    """

    Args:
        img: source RGB image
        box: bounding box (ymin, xmin, ymax, xmax)

    Examples:
        >>> from skimage.data import coffee
        >>> img = coffee()
        >>> result = estimate_color(img)
        >>> result.get('black', None) is not None
        True
        >>> result.get('white', None) is not None
        True

        # Colors are within sensible range
        >>> 0 <= result['black'] <= 0.4
        True
        >>> 0.1 <= result['white'] <= 0.3
        True
        >>> 0 <= result['blue'] <= 0.1
        True
        >>> 0.4 <= result['red'] <= 1
        True

        # Order of output is enforced
        >>> abs(result['black'] - result[0]) < 0.0001
        True
        >>> abs(result['white'] - result[1]) < 0.0001
        True
        >>> abs(result['purple'] - result[-2] < 0.0001)
        True
        >>> abs(result['pink'] - result[-1] < 0.0001)
        True

    Returns:
        Dictionary of color-frequency pairs.

    """

    # Get center of image (via bounding box)
    cropped_img = _get_bbox_center_img(img, box)

    # Convert to Hue, Saturation, Value color space
    hsv_img = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2HSV)

    # Flatten pixels in image
    flat_img = hsv_img.reshape((hsv_img.shape[0] * hsv_img.shape[1], 3))

    # Calculate indexed histograms of the Value dimension
    n_bins_val = 32
    bw_bin_thresh = 5

    bins_val = np.linspace(0, 255, n_bins_val, endpoint=True, dtype='uint8')
    hist_val_idx = np.digitize(flat_img[:, 2], bins_val)
    # hist_val, _ = np.histogram(hist_val_idx)

    is_black_pxl = hist_val_idx <= bw_bin_thresh
    is_white_pxl = hist_val_idx >= (n_bins_val - bw_bin_thresh)

    black_idx = hist_val_idx[is_black_pxl]
    white_idx = hist_val_idx[is_white_pxl]

    n_black = len(black_idx)
    n_white = len(white_idx)

    # Calculate histogram of Hue dimension
    color_flat_img = flat_img[~np.logical_or(is_black_pxl, is_white_pxl), :]  # exclude black or white pixels

    # Mathematical approach doesn't provide human understandable color ranges. Going to hardcode...
    # color_centers = np.arange(0, 360, 30)  # produces 12 color centers
    # color_ranges = (color_centers - 15) % 360  # maps to 360 deg bin ranges
    # bins_hue = color_ranges // 2  # ranges need to fit in uint8 space [0, 179]

    # [red, orange, yellow, green, cyan, blue, purple, pink]
    bins_hue = [-8, 7, 22, 37, 82, 97, 127, 142, 171]
    hist_hue, _ = np.histogram(color_flat_img[:, 0], bins=bins_hue)

    total = n_black + n_white + sum(hist_hue)

    od = OrderedDict()
    od['black'] = n_black / total
    od['white'] = n_white / total
    od['red'] = hist_hue[0] / total
    od['orange'] = hist_hue[1] / total
    od['yellow'] = hist_hue[2] / total
    od['green'] = hist_hue[3] / total
    od['cyan'] = hist_hue[4] / total
    od['blue'] = hist_hue[5] / total
    od['purple'] = hist_hue[6] / total
    od['pink'] = hist_hue[7]
    output = pd.Series(od)

    return output





def _get_bbox_center_img(img, box=None):
    """

    Args:
        img:
        box:
    Examples:
        >>> from skimage.data import coffee
        >>> img = coffee()
        >>> cropped = _get_bbox_center_img(img)

    Returns:
        A cropped image around the center about half the original size

    """
    # get space measures
    if not box:
        ymin, xmin, ymax, xmax = (0, 0, img.shape[0], img.shape[1])
    else:
        ymin, xmin, ymax, xmax = box

        if sum(box) <= 4:
            ymin = int(ymin * img.shape[0])
            ymax = int(ymax * img.shape[0])
            xmin = int(xmin * img.shape[1])
            xmax = int(xmax * img.shape[1])

    wd = xmax - xmin
    ht = ymax - ymin

    # Get center area of the object inside the bounding box
    ystart = ymin + (ht // 4)
    yend = ymax - (ht // 4)
    xstart = xmin + (wd // 4)
    xend = xmax - (wd // 4)

    obj_center = img[ystart:yend, xstart:xend, :]

    return obj_center






