from PIL import Image
import numpy 
import time

# 63.5039
#-2   -1   0     1      2  
#0.5  64   127.5  191.5  254.5
def float_to_interger(x:float):
    if(x - int(x) >= 0.5):
        return int(x+1)
    else:
        return int(x)


def rgb_to_gray(red:int,green:int,blue:int):
    sum=red*0.3+green*0.587+blue*0.114
    return float_to_interger(sum)



numbers_of_pixels=0
pixels_sum_value=0    

gray_list=numpy.empty((0,),dtype=numpy.int8)
with Image.open('image2.png') as img:
    img_array = numpy.array(img)

for line in img_array:
    for pix in line:
        pixel_value=rgb_to_gray(pix[0],pix[1],pix[2])
        gray_list=numpy.append(gray_list,pixel_value)
        numbers_of_pixels += 1
        pixels_sum_value +=pixel_value
prime_avg=float_to_interger(pixels_sum_value/numbers_of_pixels)
