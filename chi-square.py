import sys
import cv2
import numpy as np
from math import pow

class LSB:
    def __init__(self):
        self.R0 = 0.5000804  # the probaility of LSB of red is 0
        self.R1 = 0.4999196  # the probaility of LSB of red is 1
        self.G0 = 0.5069362  # the probaility of LSB of green is 0
        self.G1 = 0.4930638  # the probaility of LSB of green is 1
        self.B0 = 0.50182161  # the probaility of LSB of blue is 0
        self.B1 = 0.49817839  # the probaility of LSB of blue is 1
        
        self.R00 = 0.24893262 # the probaility of LSB of red is 00
        self.R01 = 0.24999414 # the probaility of LSB of red is 01
        self.R10 = 0.25114779 # the probaility of LSB of red is 10
        self.R11 = 0.24992546 # the probaility of LSB of red is 11
        self.G00 = 0.26106413 # the probaility of LSB of green is 00
        self.G01 = 0.24789388 # the probaility of LSB of green is 01
        self.G10 = 0.24587207 # the probaility of LSB of green is 10
        self.G11 = 0.24516992 # the probaility of LSB of green is 11
        self.B00 = 0.2536543 # the probaility of LSB of blue is 00
        self.B01 = 0.2490752 # the probaility of LSB of blue is 01
        self.B10 = 0.24816732 # the probaility of LSB of blue is 10
        self.B11 = 0.24910319 # the probaility of LSB of blue is 11
        
        self.Red = []
        self.Green = []
        self.Blue = []
        self.All = []
        
    def create(self, num):
        if(num == 1):       # for one bit
            self.Red = [self.R0, self.R1]
            self.Green = [self.G0, self.G1]
            self.Blue = [self.B0, self.B1]
        elif(num == 2):
            self.Red = [self.R00, self.R01, self.R10, self.R11]
            self.Green = [self.G00, self.G01, self.G10, self.G11]
            self.Blue = [self.B00, self.B01, self.B10, self.B11]
            
        self.All = [(self.Red[i] + self.Green[i] + self.Blue[i]) / 3 for i in range(int(pow(2, num)))]

def Redplane(Object, num):
    if(Object > 3.84 and num == 1):
        print("There is something hidding in the last one bit of red plane")
    elif(Object > 7.81 and num == 2):
        print("There is something hidding in the last two bits of red plane")
    else:
        print("Red plane is fine")
        
def Greenplane(Object, num):
    if(Object > 3.84 and num == 1):
        print("There is something hidding in the last one bit of green plane")
    elif(Object > 7.81 and num == 2):
        print("There is something hidding in the last two bits of green plane")
    else:
        print("Green plane is fine")

def Blueplane(Object, num):
    if(Object > 3.84 and num == 1):
        print("There is something hidding in the last one bit of blue plane")
    elif(Object > 7.81 and num == 2):
        print("There is something hidding in the last two bits of blue plane")
    else:
        print("Blue plane is fine")
        
        
def Plane(Object, num):
    if(Object > 3.84 and num == 1):
        print("There is something hidding in the last one bit of this picture")
    elif(Object > 7.81 and num == 2):
        print("There is something hidding in the last two bits of this picture")
    else:
        print("This picture is fine")
    
if __name__ == "__main__":    
    try:
        img = cv2.imread("") # input shoto name 
    except Exception as f:
        print(f)
        sys.exit()
    
    try:
        num = int() # input number of least bit
    except Exception as f:
        print(f)
        sys.exit()
    else:
        if(num < 1 or num > 2):
            print("The number of bits must bigger than 0 and smaller than 4.")
            sys.exit()
    
    Red = np.array([0 for i in range(int(pow(2, num)))])       # initialize
    Green = np.array([0 for i in range(int(pow(2, num)))])
    Blue = np.array([0 for i in range(int(pow(2, num)))])
    
    B, G, R = cv2.split(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            Red[ R[i][j] % int(pow(2, num)) ] += 1       # counting for red channel
            Green[ G[i][j] % int(pow(2, num)) ] += 1     # counting for green channel
            Blue[ B[i][j] % int(pow(2, num)) ] += 1      # counting for blue channel
    
    All = np.array([(Red[i] + Green[i] + Blue[i]) / 3 for i in range(int(pow(2, num)))]) # counting for all chhanel
    
    Red = Red / (img.shape[0] * img.shape[1])        # get ratio for all classes
    Green = Green / (img.shape[0] * img.shape[1])
    Blue = Blue / (img.shape[0] * img.shape[1])
    All = All / (img.shape[0] * img.shape[1])
    
    ObjectRed = 0
    ObjectGreen = 0
    ObjectBlue = 0
    ObjectAll = 0
    
    standard = LSB()
    standard.create(num)    # select how many bits
    
    for i in range(int(pow(2, num))):    # calculate chi-square value
        ObjectRed += pow( (Red[i] - standard.Red[i]), 2 ) / standard.Red[i]
        ObjectGreen += pow( (Green[i] - standard.Green[i]), 2 ) / standard.Green[i]
        ObjectBlue += pow( (Blue[i] - standard.Blue[i]), 2 ) / standard.Blue[i]
        ObjectAll += pow( (All[i] - standard.All[i]), 2 ) / standard.All[i]
        
    Redplane(ObjectRed, num)
    Greenplane(ObjectGreen, num)
    Blueplane(ObjectBlue, num)
    Plane(ObjectAll, num)