from PIL import Image
import numpy 
import matplotlib.pyplot as plt
import numba
import time


@numba.jit(nopython=True)
def float_to_interger(x:float):
    if(x - int(x) >= 0.5):
        return int(x+1)
    else:
        return int(x)

@numba.jit(nopython=True)
def rgb_to_gray(red:int,green:int,blue:int):
    sum=red*0.3+green*0.587+blue*0.114
    return float_to_interger(sum)

@numba.jit(nopython=True)
def extract_to_gray(array,emptyarray,PRarray,height,width):

    for rows in range(height) :
        for coloums in range(width) :
                red = array[rows,coloums][0]
                green = array[rows,coloums][1]
                blue = array[rows,coloums][2]
                temp= float_to_interger(red*0.2+blue*0.114+green*0.587)
                emptyarray[rows,coloums] = temp
                PRarray[temp] +=1
    return  emptyarray
    
@numba.jit(nopython=True)
def process_image(gray_values,PRarray,height,width):
    for row in range(height):
        for column in range(width):
            gray_values[row,column]=int(PRarray[gray_values[row,column]]*255)
    return gray_values
        

@numba.jit(nopython=True)
def rating_values(len_of_arr,value_array,PRarray):
    PRarray[0]=PRarray[0]/len_of_arr
    for i in range (1,256):
        PRarray[i] =PRarray[i]/len_of_arr +PRarray[i-1]
    return PRarray

def show_figure(array,save_to,title_name,Bins=256,color='gray'):
    plt.title(title_name)
    plt.hist(array.ravel(),bins=Bins,color=color)
    plt.savefig(save_to)
    plt.show()


start = time.time()

image=Image.open('file path')    
origin_values = numpy.array(image)
width,height=image.size
len_of_arr=height*width

gray_values=numpy.zeros((height,width),dtype=int)
PRarray=numpy.zeros((256,))
image_values=numpy.zeros((height,width))


gray_values = extract_to_gray(origin_values,gray_values,PRarray,height,width)
PRarray = rating_values(len_of_arr,gray_values,PRarray)
gray_values = process_image(gray_values,PRarray,height,width)



gray_image=Image.fromarray(gray_values.astype('uint8'))
gray_image.save('output image')

print(time.time()-start)

show_figure(gray_values,'save file path','figure title')
