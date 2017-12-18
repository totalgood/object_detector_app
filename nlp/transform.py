def normalize_position(image, box):
    """ Takes in an image which will be provided and then computes the normalized bouding box information.

    Args:
        image (3D np.array): (rows, columns, channels)
            rows (int): width of image
            columns (int): height of image
            channels (int): number of channels, if the image is in color
        box (tuple): (xmin, xmax, ymin, ymax)
            xmin (int): left most edge of the bounding box
            xmax (int): right most edge of the bounding box
            ymin (int): lowest edge of the bounding box
            ymax (int): highest edge of the bouding box

    From image, try to get image width and height such that we can scale it appropriately

        (xmin,ymax).    (xmax,ymax)
        ---------------
        |             |
        |             |
        |             |
        |             |     
        |             |
        ________________
        (xmin,ymin)     (xmax,ymin)


    Returns: 
        tuple: (x, y, z, widht, height, depth) 
            x (float): left most point and is scaled between -1 and 1. to scale, can do (xmin-image_width/2)/(image_width/2)
            y (float): bottom most point and is scaled between -1 and 1. to scale, can do (ymin-image_height/2)/(image_height/2)
            z (float): set to 0
            width (float):this is defined as xmax-xmin. to scale, compute (xmax-xmin)/(image_width/2)
            height (float): this is defined as ymax-ymin. to scale, compute (ymax-ymin)/(image_height/2)
            depth (float): set to 0

        (x,y+height).   (x+width, y+height)
        ---------------
        |             |
        |             |
        |             |
        |             |     
        |             |
        ________________
        (x,y)           (x+width,y)

    >>> from skimage.data import coffee
    >>> img = coffee()
    >>> normalize_position(img,(100,100,50,50))
    (-0.5, -0.8333333333333334, 0.0, 0.0, 0.0, 0.0)
    >>> normalize_position(img,(10,90,10,90))
    (-0.95, -0.9666666666666667, 0.0, 0.4, 0.26666666666666666, 0.0)
    >>> normalize_position(img,(0,400,0,600))
    (-1.0, -1.0, 0.0, 2.0, 2.0, 0.0)
    >>> normalize_position(img,(100,50,0,600))
    Traceback (most recent call last):
    ...
    AssertionError: xmin is greater than xmax
    >>> normalize_position(img,(100,600,0,600))
    Traceback (most recent call last):
    ...
    AssertionError: xmax is greater than image width
    >>> normalize_position(img,(100,400,200,100))
    Traceback (most recent call last):
    ...
    AssertionError: ymin is greater than ymax
    >>> normalize_position(img,(-100,400,100,100))
    Traceback (most recent call last):
    ...
    AssertionError: xmin < 0
    """
    xmin, xmax, ymin, ymax = box
    im_width, im_height = image.shape[:2]

    assert xmin <= xmax, 'xmin is greater than xmax'
    assert ymin <= ymax, 'ymin is greater than ymax'
    assert xmin <= im_width, 'xmin is greater than image width'
    assert xmax <= im_width, 'xmax is greater than image width'
    assert ymin <= im_height, 'ymin is greater than image height'
    assert ymax <= im_height, 'ymax is greater than image height'
    assert xmin >= 0, 'xmin < 0'
    assert ymin >= 0, 'ymin < 0'
    
    x_center = im_width / 2
    y_center = im_height / 2
    x = (xmin - (x_center)) / x_center
    y = (ymin - (y_center)) / y_center
    width = (xmax - xmin) / x_center
    height = (ymax - ymin) / y_center
    z = 0.0
    depth = 0.0
    return (x, y, z, width, height, depth)

def position(image,box):
    """ takes an image and the bounding box, returns the position of the bounding box with respect to the image
    
    Args:
        image (3D np.array): (rows, columns, channels)
            rows (int): width of image
            columns (int): height of image
            channels (int): number of channels, if the image is in color
        box (tuple): (xmin, xmax, ymin, ymax)
            xmin (int): left most edge of the bounding box
            xmax (int): right most edge of the bounding box
            ymin (int): lowest edge of the bounding box
            ymax (int): highest edge of the bouding box
    
    Returns:
        string: 'left', 'right' or 'center'

    >>> from skimage.data import coffee
    >>> img = coffee()
    >>> position(img,(0,400,0,600))
    'center'
    >>> position(img,(0,100,0,200))
    'left'
    >>> position(img,(200,400,300,400))
    'right'
    >>> position(img,(-100,200,300,400))
    Traceback (most recent call last):
    ...
    AssertionError: xmin < 0
    >>> position(img,(0,400,0,800))
    Traceback (most recent call last):
    ...
    AssertionError: ymax is greater than image height

    """
    
    x, y, z, width, height, depth = normalize_position(image,box)
    position = ""
    if (x <= 0):
        if (x+width <= 0):
            position = "left"
        else:
            position = "center"
    if (x >= 0):
        position = "right"
    
    return (position)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
