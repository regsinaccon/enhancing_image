from PIL import Image
import numpy 
import time



def float_to_interger(x:float):
    if(x - int(x) >= 0.5):
        return int(x+1)
    else:
        return int(x)


def rgb_to_gray(red:int,green:int,blue:int):
    sum=red*0.3+green*0.587+blue*0.114
    return float_to_interger(sum)


image=Image.open('input_image_path')
numbers_of_pixels=0
pixels_sum_value=0    
width,height=image.size
origin_values = numpy.array(image)
gray_values=numpy.zeros((height,width))

image_values=numpy.zeros((height,width))
for rows in range(height) :
    for coloums in range(width) :
            red = origin_values[rows,coloums][0]
            green = origin_values[rows,coloums][1]
            blue = origin_values[rows,coloums][2]
            gray_values[rows,coloums]=rgb_to_gray(red,green,blue)
            #print(gray_values[rows][coloums])
gray_image=Image.fromarray(gray_values.astype('uint8'))
gray_image.save('out_put_image_path')




