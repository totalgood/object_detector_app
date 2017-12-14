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
        self.lab = np.zeros((len(self.colors), 1, 3), dtype='uint8')
        self.colorNames = []

        for i, (name, rgb) in enumerate(self.colors.items()):
            self.lab[i] = rgb
            self.colorNames.append(name)

        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)
        self.labtree = KDTree(self.lab)

    def _create_mask(self, img):
        contour = None

        # construct mask for the contour
        mask = np.zeros(img.shape[:2], dtype='uint8')
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)

        return mask

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

    def label(self, img):

        mask = self._create_mask(img)

        model = self._build_custer_model(img, mask)


        _, idxs = self.labtree.query(mean, k=1)

        return self.colorNames[idxs[0]]


