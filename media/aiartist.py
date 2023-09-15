from cgi import test
import random
import cv2
import os
import numpy as np
from colorthief import ColorThief
import math
import sys

#AI Artist Source Code


#gets the height of the image in the img_path
def get_height(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    dimensions = img.shape
    return img.shape[0]

#gets the width of the image in the img_path
def get_width(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    dimensions = img.shape
    return img.shape[1]

#gets the color of a pixel given its coordinates and the img
def getColor(img, coordinates):
    x = coordinates[1]-1
    y = coordinates[0]-1
    b,g,r = (img[x,y])
    
    return b,g,r

#generates random coordinates given an x-bound and y-bound
def generateRandomCoords(xmax,ymax):
    randX = random.randint(0,xmax)
    randY = random.randint(0,ymax)
    return(randX,randY)

#draws a circle on the image at the given coordinates with given radius, color, and thickness
def drawCircle(img,coordinates,r,color,thickness):
    final = cv2.circle(img, coordinates, r , color, thickness)
    return final

#returns a white canvas
def canvas(height,width):
    blank_image = np.zeros((height,width,3),np.uint8)
    blank_image[np.all(blank_image == (0, 0, 0), axis=-1)] = (255,255,255)
    return blank_image

'''
def drawRandomTriangle(img, test_image,width,height):
    coords1 = generateRandomCoords(width,height)
    coords2 = generateRandomCoords(width,height)
    coords3 = generateRandomCoords(width,height)
    centroid = ((coords1[0]+coords2[0]+coords3[0])//3, (coords1[1]+coords2[1]+coords3[1])//3)
    test_color = getColor(test_image,centroid)
    test_color = (int(test_color[0]), int(test_color[1]), int(test_color[2]))
    points = np.array([coords1,coords2,coords3])
    cv2.line(img, coords1, coords2, test_color, 3)
    cv2.line(img, coords2, coords3, test_color, 3)
    cv2.line(img, coords1, coords3, test_color, 3)
    cv2.fillPoly(img,pts=[points],color=test_color)
    return img
'''
#Draws a random circle, given the test case, the image and the dimensions and scaling factor
def drawRandomCircle(img,test_image,width,height,scale):
    max_length = max(width,height)/2
    min_length = min(width,height)/2
    lower_bound = min_length
    upper_bound = max_length
    lower_bound = round(scale*lower_bound)
    upper_bound = round(scale*upper_bound)
    radius = random.randint(lower_bound,upper_bound)
    coords = generateRandomCoords(width,height)
    color = getColor(test_image,coords)
    color = (int(color[0]), int(color[1]), int(color[2])) 
    thickness = -1
    circle = drawCircle(img,coords,radius,color,thickness)
    return circle

#Generates images based on test case and given canvas with its dimensions, rigor, file name, scaling factor and file extension
def generate_images(canvas,test_img,width,height,rigor,name,scale,file_extension):
    for i in range(rigor):
        img = canvas.copy()
        new_img = drawRandomCircle(img,test_img,width,height,scale)
        #new_img = drawRandomTriangle(img,test_img,width,height)
        similarity = compare_images(canvas,new_img)
        while(similarity == 1):
            #new_img = drawRandomTriangle(img,test_img,width,height)
            new_img = drawRandomCircle(img,test_img,width,height)
        filename = name + str(i) + file_extension
        cv2.imwrite(filename,new_img)

#Returns the Euclidean Distance (how dissimilar) between the test case and image
def compare_images(test_img, img):
    gray_test = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    test_hist = cv2.calcHist([gray_test],[0],None,[256],[0,256])

    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_hist = cv2.calcHist([gray_img],[0],None,[256],[0,256])

    dist1=0

    i = 0
    while(i < len(test_hist) and i < len(img_hist)):
        dist1 += (test_hist[i]-img_hist[i])**2
        i+=1
    return float(dist1**(1/2))

#compares a set of test cases given rigor and returning the list of euclidean distances
def compare_multiple(test_img,rigor,name,file_extension):
    sim_list = []
    for i in range(rigor):
        filename = name + str(i) + file_extension
        img = cv2.imread(filename,cv2.IMREAD_COLOR)
        similarity = (compare_images(test_img,img))
        sim_list.append(similarity)
    return sim_list

#generates a scale for the size of circle given the similarity and file's natural simfactor
def generate_scale(similarity,simfactor):
        return simfactor*math.sqrt(similarity)

#gets the mininum index in a list        
def get_index_min(list):
    min_index = 0
    length = len(list)
    for i in range(1,length):
        if(list[i]<list[min_index]):
            min_index = i
    print(list[min_index])
    return min_index

#gets an image given the name, extension, and index
def get_image_from_index(index,name,file_extension):
    return  name+ str(index) + file_extension

#deletes all temporary files generated
def clear_temp_files(filename,file_extension,num):
    for i in range(num):
        try:
            os.remove(filename+str(i)+file_extension)
        except:
            pass

def main(file):
    test_path = file
    split_tup=os.path.splitext(test_path)
    filename = split_tup[0]
    file_extension = split_tup[1]
    test_img = cv2.imread(test_path, cv2.IMREAD_COLOR)
    height = get_height(test_path)
    width = get_width(test_path)
    
    board = canvas(height,width)
    cv2.imwrite(filename+"final"+file_extension,board)

    sim_factor = 0.00025
    scale = 2.0
    trials = 2000
    rigor = 50
    initial_sim = 0
    final_sim = compare_images(test_img,board)

    generate_images(board,test_img,width,height,rigor,filename,scale,file_extension)
    sim_list = compare_multiple(test_img,rigor,filename,file_extension)
    min_index = get_index_min(sim_list)
    final_sim = sim_list[min_index]
    if(final_sim < initial_sim):
        min_path = get_image_from_index(min_index,filename,file_extension)
        min_img = cv2.imread(min_path,cv2.IMREAD_COLOR)
        cv2.imwrite(filename+"final"+file_extension,min_img)
    
    for i in range(trials):
            scale = generate_scale(final_sim,sim_factor)
            new_board = cv2.imread(filename+"final"+file_extension,cv2.IMREAD_COLOR)
            generate_images(new_board,test_img,width,height,rigor,filename,scale,file_extension)
            sim_list = compare_multiple(test_img,rigor,filename,file_extension)
            min_index = get_index_min(sim_list)
            initial_sim = final_sim
            final_sim = sim_list[min_index]
            if(final_sim < initial_sim):
                min_path = get_image_from_index(min_index,filename,file_extension)
                min_img = cv2.imread(min_path,cv2.IMREAD_COLOR)
                cv2.imwrite(filename+"final"+file_extension,min_img) 

    clear_temp_files(filename,file_extension,rigor)

filename = sys.argv[1]    
main(filename)
