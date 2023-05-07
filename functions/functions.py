import cv2
import os
import numpy as np

vector = []
P = []
T = []
weights = np.array([])
bias = np.array([])
image = ''
text = "Type is : ???"

def start():
    
    #vector = get_feature(cv2.imread(image,cv2.IMREAD_GRAYSCALE))
    #print(vector)
    global weights, T, P
    for i in range(2):
        P.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Adenovirus/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
        T.append([1, 1, -1])
        P.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Astrovirus/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
        T.append([1, -1, 1])
        P.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Ebola/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
        T.append([1, 1, 1])
        P.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Influenza/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
        T.append([-1, -1, -1])
        P.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Machupo/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
        T.append([-1, 1, -1])       
    
    P = np.array(P)
    print(P)
    T = np.array(T) 
    #T = np.transpose(T)
    weights = np.dot(T, np.dot(np.linalg.inv(np.dot(P, P.T)), P))
    print(weights) 
###################################################  

def get_feature(image):
    new = conv_relu(image)
    new = pooling(new)
    new = conv_relu(new)
    new = pooling(new)
    new = conv_relu(new)
    new = pooling(new)
    new = conv_relu(new)
    new = pooling(new)
    new = conv_relu(new)
    new = pooling(new)
    new = conv_relu(new)
    new = pooling(new)
    new = flatten(new)

    return new

###################################################

def conv_relu(image):
    mask = [[-1,-1,1],[0,1,-1],[0,1,1]]
    size1 = len(image) - 2
    size2 = len(image[0]) - 2
    new_image = [[0 for _ in range(size2)]for _ in range(size1)]
    for i in range(size1):
        for j in range(size2):
            x = 0
            for k in range(3):
                x += (image[i+k][j+0]*mask[k][0] + image[i+k][j+1]*mask[k][1] + image[i+k][j+2]*mask[k][2])
            new_image[i][j] = x if x > 0 else 0
    return new_image

###################################################

def pooling(image): 
    size1 = int(len(image)/2)
    size2 = int(len(image[0])/2)
    new_image = [[0 for _ in range(size2)]for _ in range(size1)]
    for i in range(0,size1):
        for j in range(0,size2):
            x = 0
            for k in range(2):
                x += (image[(i*2)+k][(j*2)+0] + image[(i*2)+k][(j*2)+1])/4
            new_image[i][j] = int(x)
    return new_image
    
###################################################

def flatten(image):
    new_image = []
    for row in image:
        for el in row:
            new_image.append(el)
    return new_image

###################################################

def details(image):
    
    path = os.path.dirname(image)
    folder_name = os.path.basename(path)
    print(folder_name)

    if (folder_name == 'Adenovirus'):
        return """A members of the family Adenoviridae, are medium-sized (90:100 nm), nonenveloped (without an outer lipid bilayer) viruses with an icosahedral nucleocapsid containing a double-stranded DNA genome.
        """
    if (folder_name == 'Astrovirus'):
        return """A type of virus that was first discovered in 1975 using electron microscopes following an outbreak of diarrhea in humans. In addition to humans, astroviruses have now been isolated from numerous mammalian animal species.
        """
    if (folder_name == 'Ebola'):
        return """Known as Ebola virus disease (EVD) and Ebola hemorrhagic fever (EHF), is a viral hemorrhagic fever in humans and other primates,caused by ebolaviruses.
        """
    if (folder_name == 'Influenza'):
        return """Commonly known as "the flu", is an infectious disease caused by influenza viruses. Symptoms range from mild to severe and often include fever, runny nose, sore throat, muscle pain, headache, coughing, and fatigue.
        """
    if (folder_name == 'Machupo'):
        return """Also known as black typhus or Ordog Fever, is a hemorrhagic fever and zoonotic infectious disease originating in Bolivia after infection by Machupo mammarenavirus.
        """        
    else:
        return None
###################################################

def neural():
    start()
    global image, weights, text
    p = np.array(get_feature(cv2.imread('F:/virus_classification_materials/project/media/virues images/Adenovirus/p.2.jpg',cv2.IMREAD_GRAYSCALE)))
    p = p.T
    print(p)
    print(weights)
    n = np.dot(weights, p)
    print(n)
    # text = 

neural()    
