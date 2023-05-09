import functions.functions as fn
import flet as ft
import base64
import os

image_path = ""
result = "No Image Was Selected"

def main(page:ft.Page):
    
    page.title = "Virus Classification"
    page.window_width = 600
    page.window_height = 700
    page.padding = 0
    
    image_holder = ft.Image(
        width = 380,
        height = 400,
        src = os.path.abspath("media/images/loading.gif"),
        fit = ft.ImageFit.COVER,
    )
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        print(e.files)
        if e.files and len(e.files):
            with open(e.files[0].path, 'rb') as r:
                # the path of selected image
                global image_path
                image_path = str(e.files[0].path)
                image_holder.src_base64 = base64.b64encode(r.read()).decode('utf-8')           
                page.update()

    pick_file = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_file)
    
    # The process   
    def process(e: ft.TapEvent):
        print("The path is: "+image_path)
        text = fn.neural(image_path)
        print(f'here: '+text)
        show_result.content = ft.Text(
            text,
            size = 20,
            color = "white",
            weight = ft.FontWeight.W_500,
        )
        page.update()
        show_details.content = ft.Text(
            fn.details(text),
            size = 18,
            color = "white",
            weight = ft.FontWeight.W_500,
        )
        show_details.height = 400,
        page.update()

    show_result = ft.Container(
        content = ft.Text(
            result,
            size = 20,
            color = "white",
            weight = ft.FontWeight.W_500,
        ),
    )
    show_details = ft.Container(
        width = 380,
        height = 0,
        opacity = 0.8,
        bgcolor= "black",
        padding = ft.padding.all(10)
    )
    
    page.add(ft.Container(
        image_src= os.path.abspath("media/images/virus.gif"),
        image_fit = ft.ImageFit.COVER,
        alignment = ft.alignment.center,
        expand = True,
        content = ft.Column(
            [
                ft.Text(
                    'Virus Classification',
                    size = 40,
                    color = "red100",
                    weight = ft.FontWeight.BOLD,
                ),
                image_holder,
                ft.Text(
                    'The Type Of Virus Is:',
                    size = 25,
                    color = "blue100",
                    weight = ft.FontWeight.W_800,
                ),
                show_result,
                show_details,    
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
                ft.Container(
                    height = 20,
                    width = 20,
                ),
            ],
            scroll = "always",
            alignment = ft.CrossAxisAlignment.CENTER,
        )
      )
    )
    page.update()
ft.app(target=main, assets_dir="project")





