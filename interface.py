import tkinter
import numpy as np
import cv2, PySimpleGUI as sg
from numpy.core.fromnumeric import size

def new_file() -> str:
    window["body"].update(value="")
    filename = None
    return filename


def open_file() -> str:
    try:
        filename: str = sg.popup_get_file("Open File", no_window=True)
    except:
        return
    if filename not in (None, "") and not isinstance(filename, tuple):
        with open(filename, "r") as f:
            window["body"].update(value=f.read())
    return filename


def save_file(filename: str):
    if filename not in (None, ""):
        with open(filename, "w") as f:
            f.write(values.get("body"))
    else:
        save_file_as()


def save_file_as() -> str:
    try:
        filename: str = sg.popup_get_file(
            "Save File",
            save_as=True,
            no_window=True,
            default_extension='.png',
            file_types=(("images", ".png"),),
        )
    except:
        return
    if filename not in (None, "") and not isinstance(filename, tuple):
        with open(filename, "w") as f:
            f.write(values.get("body"))
    return filename

def colorToGray(image1_matNP):
    imr = image1_matNP[:,:,0]
    img = image1_matNP[:,:,1]
    imb = image1_matNP[:,:,2]
    imm = np.round((np.array(imr,dtype=float) + np.array(img,dtype=float) + np.array(imb,dtype=float))/3.0)
    mat_zero = np.zeros((len(image1_matNP),len(image1_matNP[0]),3),dtype=np.uint8)
    imm = np.array(imm,dtype=np.uint8)
    mat_zero[:,:,0] = imm
    mat_zero[:,:,1] = imm
    mat_zero[:,:,2] = imm
    return imm
    
#def threshold(imm):
    mat=imm
    mat= np.array(mat,dtype=np.uint8)
    #mat1 = np.ones(mat.shape,dtype=np.uint8)
    mat_step = np.ones(mat.shape,dtype=np.uint8)
    steps = [(0,0,0)]
    while len(steps)>0:
        step = steps.pop(0)
        if (step[0]<mat.shape[0]) and \
            (step[1]<mat.shape[1]) and \
            (step[2]<mat.shape[2]) and \
            (step[0]>=0) and \
            (step[1]>=0):
            if mat_step[step[0],step[1]]==1 and mat[step[0],step[1]]!=0:
                steps.append((step[0]+1,step[1]-1))
                steps.append((step[0]+1,step[1]+0))
                steps.append((step[0]+1,step[1]+1))
                steps.append((step[0]+0,step[1]-1))
                steps.append((step[0]+0,step[1]+1))
                steps.append((step[0]-1,step[1]-1))
                steps.append((step[0]-1,step[1]+0))
                steps.append((step[0]-1,step[1]+1))
            mat_step[step[0],step[1]]=0
            mat[step[0],step[1]]=0
    return mat
    

    

USE_CAMERA = 0      # change to 1 for front facing camera

filename = None

file_new = "Novo        (CTRL+N)"
file_open = "Abrir      (CTRL+O)"
file_save = "Salvar      (CTRL+S)"

sg.Image()
menu_layout = (
    ["Arquivo", [file_new, file_open, file_save, "Salvar como", "---", "Sair"]],
    ["Editar", ["Gray" , "Threshold"]]
)
first_value = 0

image1_matNP=cv2.imread('testLeve.png')
image2_matNP=cv2.imread('testLeve.png')

image1_byte_format=cv2.imencode('.png', image1_matNP)[1].tobytes()
image2_byte_format=cv2.imencode('.png', image2_matNP)[1].tobytes()
sz1_image1 =(len(image1_matNP[0]),len(image1_matNP))
sz2_image1 = (len(image1_matNP[0])+30,len(image1_matNP)+30)

sz1_image2 =(len(image2_matNP[0]),len(image2_matNP))
sz2_image2 = (len(image2_matNP[0])+30,len(image2_matNP)+30)
szl5=(sz2_image2[0]+sz2_image1[0]+30,sz2_image2[1])
slider_layout = [[sg.Spin([sz for sz in range(0, 172)],
                   font=('Helvetica 15'), initial_value=first_value, change_submits=True, key='spin'),
                  [sg.Text("Threshold", size=(10, 1), font="Helvetica " + str(first_value), key='text')],
           [sg.Slider(range=(0,172), orientation='h', size=(30,20), change_submits=True, key='slider', font=('Helvetica 15'))],
           ]] 
#szl = (400,400)
image=sg.Image(data=image1_byte_format, key='image',size= sz1_image1)
image2=sg.Image(data=image2_byte_format, key='image2',size= sz1_image1)
column = [[image,image2]]
# column = [[sg.Image(key='Image')]]
layout = [  [sg.MenuBar(menu_layout)],
            [sg.Column(column, size=szl5, scrollable=True,key='body')],
            [slider_layout]
         ]
sz = first_value

window = sg.Window('Demo Application - OpenCV Integration', 
    layout=layout,
    margins=(0,0),
    resizable=True,
    return_keyboard_events=True,)
window.read(timeout=1)

window["image"].expand(expand_x=True, expand_y=True)
window["image2"].expand(expand_x=True, expand_y=True)




while window(timeout=1)[0] != sg.WIN_CLOSED:
    event, values = window.read()
    
    if event in (None, "Sair"):
        window.close()
        break
    
    if event in (file_new, "n:78"):
        filename = new_file()
    
    if event in (file_open, "o:79"):
        filename = open_file()
    
    if event in (file_save, "s:83"):
        save_file(filename)
    
    if event in ("Salvar como",):
        filename = save_file_as()
    
    if event in ("Gray"):
        gray = colorToGray(image1_matNP)
        image1_byte_format = cv2.imencode('.png', gray)[1].tobytes()        
        window['image'](data=image1_byte_format)
    
    """if event in ("Threshold"):
        gray = colorToGray(image1_matNP)
        th = threshold(gray)
        image1_byte_format = cv2.imencode('.png',gray[1].tobytes())
        window['image'](data=image1_byte_format)
    """
    if event == sg.WIN_CLOSED:
        break
    sz_spin = int(values['spin'])
    sz_slider = int(values['slider'])
    sz = sz_spin if sz_spin != first_value else sz_slider 
    
    if sz != first_value:
        first_value = sz
        slider = window['slider']
        spin = window['spin']
        slider.update(sz)
        spin.update(sz)
        print(sz_slider)
        matT = image1_matNP/sz_slider
        matT_Bytes = cv2.imencode('.png', matT)[1].tobytes()
        window['image'](data=matT_Bytes)
        