import cv2
import flet as ft
import base64
import os

Adenovirus = []
Astrovirus = []
Ebola = []
Influenza = []
Machupo = []
weights = []
bias = []
image = ""
result = "No Image Was Selected"
is_disable = True

def main(page:ft.Page):
    page.title = "Virus Classification"
    page.window_width = 600
    page.window_height = 700
    page.padding = 0
    
    image_holder = ft.Image(
        width = 350,
        height = 400,
        src = os.path.abspath("media/images/loading.gif"),
        fit = ft.ImageFit.COVER,
    )
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        print(e.files)
        if e.files and len(e.files):
            with open(e.files[0].path, 'rb') as r:
                # the path of selected image
                image = str(e.files[0].path)
                image_holder.src_base64 = base64.b64encode(r.read()).decode('utf-8')
                is_disable = False
                print("The path is: "+image)
                page.update()

    pick_file = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_file)

    def process(e):
        image_feature(image)
    
    page.add(ft.Container(
        image_src= os.path.abspath("media/images/dark.gif"),
        image_fit = ft.ImageFit.COVER,
        alignment = ft.alignment.center,
        expand = True,
        content = ft.Column(
            [
                ft.Text(
                    'Virus Classification',
                    size = 40,
                    color = "red800",
                    weight = ft.FontWeight.BOLD,
                ),
                image_holder,
                ft.Text(
                    'The Type Of Virus Is:',
                    size = 25,
                    color = "blue700",
                    weight = ft.FontWeight.W_800,
                ),
                ft.Text(
                    result,
                    size = 20,
                    color = "white",
                    weight = ft.FontWeight.W_600,
                ),
                ft.ElevatedButton(
                    text = 'Select Image',
                    icon = 'upload',
                    on_click = lambda _: pick_file.pick_files(
                        allow_multiple = False,
                    ),
                ),
                ft.ElevatedButton(
                    on_click = process,
                    content = ft.Container(
                        content = ft.Text(
                            'Classification',
                            size = 16,
                            color = "white",
                            weight = ft.FontWeight.W_600,
                        ),
                        padding = ft.padding.symmetric(horizontal=50),
                    ),
                    style = ft.ButtonStyle(
                        color = "white",
                        bgcolor = "red700",
                    ),
                ),
            ],
            alignment = ft.CrossAxisAlignment.CENTER,
        )
      )
    )
    

    def start():
        for i in range(10):
            Adenovirus.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Adenovirus/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
            Astrovirus.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Astrovirus/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
            Ebola.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Ebola/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
            Influenza.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Influenza/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
            Machupo.append( get_feature(cv2.imread(os.path.abspath("media/virues images/Machupo/p."+str(i)+".jpg"),cv2.IMREAD_GRAYSCALE)) )
    
        print(len(Adenovirus))
        print(len(Adenovirus[0]))        

    ###################################################
    def image_feature(image):
        for i in range(1):
            if image == os.path.abspath("media/virues images/Adenovirus/p."+str(i)+".jpg"):
               Adenovirus = [i, 0, 1, i+1, 0]
               print(Adenovirus)
            if image == os.path.abspath("media/virues images/Astrovirus/p."+str(i)+".jpg"):
                Astrovirus = [0, i, i-1, 1, 2]
                print(Astrovirus)
            if image == os.path.abspath("media/virues images/Ebola/p."+str(i)+".jpg"):
                Ebola = [1, i, i, -1, 0]
                print(Ebola)
            if image == os.path.abspath("media/virues images/Influenza/p."+str(i)+".jpg"):
                Influenza = [-1, 1, i, 0, i]
                print(Influenza)
            if image == os.path.abspath("media/virues images/Machupo/p."+str(i)+".jpg"):
                Machupo = [2, i, i, -1, 0]
                print(Machupo)

    ###################################################  
    def get_feature(image):
        new = conv_relu(image)
        new = pooling(new)
        new = conv_relu(new)
        new = pooling(new)
        new = conv_relu(new)
        new = pooling(new)
        #new = conv_relu(new)
        #new = pooling(new)
        #new = conv_relu(new)
        #new = pooling(new)
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

    def neural():
        pass
    
    
ft.app(target=main, assets_dir="project")





