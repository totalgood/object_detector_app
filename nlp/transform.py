from PIL import Image

def normalize_x_and_y(image,xmin,xmax,ymin,ymax):
	""" 
	Takes in an image which will be provided and then computes the normalized bouding box information.
	Args:
	xmin - this is the left most point of the bounding box
	xmax - this is the right most point of the bounding box
	ymin - this is the lowest point of the bounding box
	ymax - this is the highest point of the bouding box
	From image, try to get image width and height such that we can scale it appropriately

		(xmin,ymax).    (xmax,ymax)
		---------------
		|			  |
		|			  |
		|			  |
		|			  |		
		|			  |
		________________
		(xmin,ymin)		(xmax,ymin)



	The output will be the following 6 parameters
	x - the left most point and is scaled between -1 and 1. to scale, can do (xmin-image_width/2)/(image_width/2)
	y - the bottom most point and is scaled between -1 and 1. to scale, can do (ymin-image_height/2)/(image_height/2)
	width - this is defined as xmax-xmin. to scale, compute (xmax-xmin)/(image_width/2)
	height - this is defined as ymax-ymin. to scale, compute (ymax-ymin)/(image_height/2)
	z - set to 0
	depth - set to 0

		(x,y+height).   (x+width, y+height)
		---------------
		|			  |
		|			  |
		|			  |
		|			  |		
		|			  |
		________________
		(x,y)			(x+width,y)

	these test cases are for a 100*100 image but generic code is built to run any height and width
	>>> normalize_x_and_y(image,100,100,50,50)
	1.0 0.0 0.0 0.0 0.0 0.0
	>>> normalize_x_and_y(image,10,90,10,90)
	-0.8 -0.8 1.6 1.6 0.0 0.0
	>>> normalize_x_and_y(image,90,10,10,90)
	xmin is greater than xmax
	>>> normalize_x_and_y(image,110,190,10,40)
	xmin is greater than image width
	>>> normalize_x_and_y(image,-10,10,10,90)
	xmin < 0
	>>> normalize_x_and_y(image,10,90,90,10)
	ymin is greater than ymax
	>>> normalize_x_and_y(image,101,150,50,100)
	xmin is greater than image width
	>>> normalize_x_and_y(image,10,90,10,190)
	ymax is greater than image height
	>>> normalize_x_and_y(iamge,0,200,100,100)
	xmax is greater than image width
	>>> normalize_x_and_y(image,0,100,-10,100)
	ymin < 0
	>>> normalize_x_and_y(image,50,50,50,50)
	0.0 0.0 0.0 0.0 0.0 0.0
	>>> normalize_x_and_y(image,50,100,50,100)
	0.0 0.0 1.0 1.0 0.0 0.0
	>>> normalize_x_and_y(image,0,100,0,100)
	-1.0 -1.0 2.0 2.0 0.0 0.0
	
	"""

	#TODO: Check if I really need this next line or not
	im = Image.open(image)
	im_width, im_height = im.size
	if (xmin > xmax):
		print ("xmin is greater than xmax")
		return ("error")

	if (ymin>ymax):
		print("ymin is greater than ymax")
		return ("error")

	if (xmin > im_width):
		print("xmin is greater than image width")
		return ("error")

	if (xmax > im_width):
		print("xmax is greater than image width")
		return ("error")

	if (ymin > im_height):
		print ("ymin is greater than image height")
		return ("error")
	if (ymax > im_height):
		print ("ymax is greater than image height")
		return ("error")

	if (xmin < 0):
		print ("xmin < 0")
		return ("error")

	if (ymin < 0):
		print ("ymin < 0")
		return ("error")
	
	x = (xmin-(im_width/2))/(im_width/2)
	y = (ymin-(im_height/2))/(im_height/2)
	width = ((xmax-xmin)/(im_width/2))
	height = ((ymax-ymin))/(im_height/2)
	z = 0.0
	depth = 0.0
	return(x,y,width,height,z,depth)

def position(a):
	""" 
	this function takes in the image as its argument.
	the function then calls the normalizing function to get the values of x,y, width and height from
	normalize function. 
	Once the values of x,y,width and height are received, the function returns what it believes to be the
	position of the object.
	The position of the object has been defined in the follwing manner:
		if the x position is less than half of the image widht, it is in the left side but to check if it is 
		centered or not, I check the value of x+width of box. If the value of x+width is greater than 0 and the
		value of x is less than 0, i say that the object is centered. In the case that x < 0 and x+width < 0, 
		I say the object is to the left. In any case, since the width cannot be negative, if x >= 0, I say that it
		is to the right as the position. 

	Also have accounted for error messages. 
	
	>>> a = (normalize_x_and_y("/Users/ashwin/Documents/Coding/vish.jpg",0,60,0,100))
	>>> position(a)
	center
	>>> a = (normalize_x_and_y("/Users/ashwin/Documents/Coding/vish.jpg",0,10,0,100))
	left
	>>> a = (normalize_x_and_y("/Users/ashwin/Documents/Coding/vish.jpg",50,60,0,100))
	right
	>>> a = (normalize_x_and_y("/Users/ashwin/Documents/Coding/vish.jpg",40,60,0,100))
	center
	>>> a = (normalize_x_and_y("/Users/ashwin/Documents/Coding/vish.jpg",110,60,0,100))
	xmin is greater than xmax
	see above error message

	"""

	if (a != "error"):
		#print("test passed")
		x,y,width,height,z,depth = a
		position = ""
		if (x <= (0)):
			if (x+width <= 0):
				position = "left"
			else:
				position = "center"
		if (x >= (0)):
			position = "right"
	
		print (position)
	else:
		print("see above error message")

a = (normalize_x_and_y("/Users/ashwin/Documents/Coding/vish.jpg",110,60,0,100))
position = position(a)