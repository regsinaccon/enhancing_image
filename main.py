from PIL import Image
import numpy 
import matplotlib


def float_to_interger(x:float):
    if(x - int(x) >= 0.5):
        return int(x+1)
    else:
        return int(x)


def rgb_to_gray(red:int,green:int,blue:int):
    sum=red*0.3+green*0.587+blue*0.114
    return float_to_interger(sum)




image=Image.open('385541219_2236522123212993_3007922485834449612_n.jpg')
numbers_of_pixels=0
pixels_sum_value=0    
width,height=image.size
origin_values = numpy.array(image)
gray_values=numpy.zeros((height,width),dtype=int)
percentage_of_each=numpy.zeros((256,))

image_values=numpy.zeros((height,width))
for rows in range(height) :
    for coloums in range(width) :
            red = origin_values[rows,coloums][0]
            green = origin_values[rows,coloums][1]
            blue = origin_values[rows,coloums][2]
            temp=rgb_to_gray(red,green,blue)
            gray_values[rows,coloums] = temp
            percentage_of_each[temp] +=1 

gray_image=Image.fromarray(gray_values.astype('uint8'))
gray_image.save('newimage11_0.jpg')

len_of_arr=height*width

percentage_of_each[0]=percentage_of_each[0]/len_of_arr
for i in range (1,256):
    percentage_of_each[i] =percentage_of_each[i]/len_of_arr +percentage_of_each[i-1]

for row in range(height):
    for column in range(width):
        gray_values[row,column]=float_to_interger(percentage_of_each[gray_values[row,column]]*255)
        # print(int(gray_values[row,column]))
        
gray_image=Image.fromarray(gray_values.astype('uint8'))
gray_image.save('newimage11_1.jpg')



