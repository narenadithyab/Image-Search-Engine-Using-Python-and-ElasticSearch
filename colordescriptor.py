
import numpy as np
import cv2

class ColorDescriptor:
	def __init__(self, bins):
		self.bins = bins

	def describe(self, image):
		 
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),(0, cX, cY, h)]
                

		(axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
 		

		for (startX, endX, startY, endY) in segments:
			

			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)
			hist = cv2.calcHist([image], [0, 1, 2], cornerMask, self.bins,[0,180,0,256,0,256])
			hist = cv2.normalize(hist).flatten()
			#print(hist)
			#hist = self.histogram(image, cornerMask)
			features.extend(hist)
 
		#hist = self.histogram(image, ellipMask)
		hist = cv2.calcHist([image], [0, 1, 2], ellipMask, self.bins,[0,180,0,256,0,256])
		hist = cv2.normalize(hist).flatten()
		features.extend(hist)
		#print (len(features))
		return features
	
#def histogram(self, image, mask):
		#print("2")
		#hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,[0, 180, 0, 256, 0, 256])
		#print("3")
		#hist = cv2.normalize(hist).flatten()
		#return hist
