def normalize_x_and_y(image,xmin,xmax, ymin,ymax):
	""" 
	Takes in an image which will be provided and then computes the normalized bouding box information.
	Args:
	xmin - this is the left most point of the bounding box
	xmax - this is the right most point of the bounding box
	ymin - this is the lowest point of the bounding box
	ymax - this is the highest point of the bouding box
	From image, try to get image width and height such that we can scale it appropriately

		(xmin,ymax)
		---------------(xmax,ymax)
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

		(x,y+height)
		---------------(x+width, y+height)
		|			  |
		|			  |
		|			  |
		|			  |		
		|			  |
		________________
		(x,y)			(x+width,y)



	"""

