"""
Assigns a human understandable label to a color value


"""

from scipy.spatial import distance as dist
from scipy.spatial import KDTree  # TODO(Alex) use cKDTree, need to upgrade scipy
from sklearn.cluster import KMeans
from collections import OrderedDict

import numpy as np
import cv2


def determine_color_distribution(image_np, box):
    ymin, xmin, ymax, xmax = box
    wd = xmax - xmin
    ht = ymax - ymin

    # Get center area of the object inside the bounding box
    obj_center = image_np[(ymin + ht // 2):(ymax - ht // 2), (xmin + wd // 2):(xmax - wd // 2), :]


class ColorLabeler:

    colors = OrderedDict({
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    })

    def __init__(self):
        """Init L*a*b* definitions of colors"""
        pass
        # self.lab = np.zeros((len(self.colors), 1, 3), dtype='uint8')
        # self.colorNames = []
        #
        # for i, (name, rgb) in enumerate(self.colors.items()):
        #     self.lab[i] = rgb
        #     self.colorNames.append(name)
        #
        # self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)
        # self.labtree = KDTree(self.lab)

    def _create_mask(self, img):
        pass
        # contour = None
        #
        # # construct mask for the contour
        # mask = np.zeros(img.shape[:2], dtype='uint8')
        # cv2.drawContours(mask, [contour], -1, 255, -1)
        # mask = cv2.erode(mask, None, iterations=2)
        # return mask

    def _get_bbox_center_img(self, img, box):

        # get space measures
        ymin, xmin, ymax, xmax = box
        wd = xmax - xmin
        ht = ymax - ymin

        # Get center area of the object inside the bounding box
        obj_center = img[(ymin + ht // 2):(ymax - ht // 2), (xmin + wd // 2):(xmax - wd // 2), :]

        return obj_center

    def _build_custer_model(self, img, k: int = 5, mask=None) -> KMeans:

        # reshape image to vector of pixels
        flattened_img = img.reshape((img.shape[0] * img.shape[1], 3))

        model = KMeans(n_clusters=k)
        model.fit(flattened_img)

        return model

    def _centroid_histogram(self, model):

        num_labels = np.arange(0, len(np.unique(model.labels_)) + 1)
        hist, _ = np.histogram(model.labels_, bins=num_labels)

        hist = hist.astype('float')
        hist /= hist.sum()

        return hist

    def label(self, img, box=None):

        # Get center of image (via bounding box)
        if not box:
            box = (0, img.shape[0], 0, img.shape[1])

        cropped_img = self._get_bbox_center_img(img, box)

        # Convert to Hue, Saturation, Value color space
        hsv_img = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2HSV)

        # Flatten pixels in image
        flat_img = hsv_img.reshape((hsv_img.shape[0] * hsv_img.shape[1], 3))

        # Calculate indexed histograms of the Value dimension
        n_bins_val = 32
        bw_bin_thresh = 3

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
        color_flat_img = flat_img[~np.logical_or(black_idx, white_idx), :]  # exclude black or white pixels

        # Mathematical approach doesn't provide human understandable color ranges. Going to hardcode...
        # color_centers = np.arange(0, 360, 30)  # produces 12 color centers
        # color_ranges = (color_centers - 15) % 360  # maps to 360 deg bin ranges
        # bins_hue = color_ranges // 2  # ranges need to fit in uint8 space [0, 179]

        # [red, orange, yellow, green, cyan, blue, purple, pink]
        bins_hue = [-8, 7, 22, 82, 97, 127, 142, 171]
        hist_hue, _ = np.histogram(color_flat_img[:, 0], bins=bins_hue)

        total = n_black + n_white + sum(hist_hue)

        output = {
            'black': n_black / total,
            'white': n_white / total,
            'red': hist_hue[0] / total,
            'orange': hist_hue[1] / total,
            'yellow': hist_hue[2] / total,
            'green': hist_hue[3] / total,
            'cyan': hist_hue[4] / total,
            'blue': hist_hue[5] / total,
            'purple': hist_hue[6] / total,
            'pink': hist_hue[7] / total
        }

        return output








        # vhist = cv2.calcHist([hsv_img], [2], mask, [32], [0, 256])
        # black_hist = vhist[:2]
        # white_hist = vhist[:-2]




