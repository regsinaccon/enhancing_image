from PIL import Image
import numpy 
import matplotlib.pyplot as plt
import numba
import time
import os
import time

@numba.jit(nopython=True)
def float_to_interger(x:float):
    if(x - int(x) >= 0.5):
        return int(x+1)
    else:
        return int(x)

@numba.jit(nopython=True)
def extract_to_gray(array,emptyarray,PRarray,height,width):

    for rows in range(height) :
        for coloums in range(width) :
                red = array[rows,coloums][0]
                green = array[rows,coloums][1]
                blue = array[rows,coloums][2]
                temp= float_to_interger(red*0.299+blue*0.114+green*0.587)
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

def set_figure(array,save_to,title_name,Bins=256,color='gray'):
    plt.title(title_name)
    plt.xlabel('Gray scale value')
    plt.ylabel('number of pixels')
    plt.hist(array.ravel(),bins=Bins,color=color,range=(0,255))
    plt.savefig(save_to)

@numba.jit(nopython=True)
def median_filter(input_array):
    m, n = input_array.shape
    output_array = numpy.zeros((m,n),dtype=numpy.int32)
    for i in range(m):
        for j in range(n):
            neighbors = numpy.zeros((9,),dtype=numpy.int32)
            sequence = 0
            for k in range(max(0, i-2), min(i+3, m)):
                for l in range(max(0, j-2), min(j+3, n)):
                    neighbors[sequence] = input_array[k][l]
                    sequence += 1
#mask size:2
            output_array[i][j] = numpy.sort(neighbors)[4]
# sorted function invalid in jit
    return output_array
 


@numba.jit(nopython=True)
def sharp_image(input_array,Excute_type):
    m, n = input_array.shape
    output_array = numpy.zeros((m,n),dtype=numpy.int32)
    if Excute_type == 0:
        for row in range(1,m-1):
            for column in range(1,n-1):
                    output_array[row][column] += input_array[row][column-1] -input_array[row][column+1]
    elif Excute_type == 1:
        for row in range(1,m-1):
            for column in range(1,n-1):
                    output_array[row][column] += input_array[row-1][column] -input_array[row][column+1]
#mask size:1
    return output_array
@numba.jit(nopython=True)
def Combine(array):

    Excute_type = 0
    first_array = sharp_image(array,Excute_type=Excute_type)

    Excute_type+=1
    second_array = sharp_image(array,Excute_type=Excute_type)
    rows,columns = array.shape
    output_array = numpy.zeros((rows,columns),dtype=numpy.int32)
    for row in range(rows):
        for column in range(columns):
            output_array[row][column] = (first_array[row][column]+second_array[row][column])/2

    return output_array
if __name__=="__main__":
    open_image = input("Select the input image file path:")
    while os.path.exists(open_image)!=True:
        open_image=input("File path error ,please try again:")
    save_to = input("Select the file path that the image be saved:")
    
    to_sharp = input("Do you want to show edges(yes/no):")
        
    start = time.time()
    image=Image.open(open_image) 
#___________________________________________________________________________#       
    origin_values = numpy.array(image)
    width,height=image.size
    len_of_arr=height*width
    gray_values=numpy.zeros((height,width),dtype=int)
    PRarray=numpy.zeros((256,))
    image_values=numpy.zeros((height,width))
#___________________________________________________________________________#

    gray_values = extract_to_gray(origin_values,gray_values,PRarray,height,width)
    gray_image = Image.fromarray(gray_values.astype('uint8'))
    gray_image.save(save_to)
    set_figure(gray_values,'figure2','Histogram of the image(unprocessed)',color='red')
        
    PRarray = rating_values(len_of_arr,gray_values,PRarray)
    gray_values = process_image(gray_values,PRarray,height,width)

    # gray_values = median_filter(gray_values)

    if to_sharp=='yes':
        gray_values = Combine(gray_values)


    gray_image = Image.fromarray(gray_values.astype('uint8'))
    gray_image.save(save_to)
    set_figure(gray_values,'figure1','Histogram of the image (unprocessed and after processed)',color='green')
    print(f"process done after {time.time()-start} second")    
