from turtle import bgcolor
import cv2
import face_recognition as fr
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import frm.FrmAdmin as frm

def donothing():
   x = 0


root = Tk()
root.title("Presença de alunos")
root.config( bg="white" )
root.geometry( '1024x862' )


def openAdmin():
   window = frm.FrmAdmin( root )
   window.grab_set()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Manager Dialog", command=openAdmin)
# filemenu.add_command(label="Open", command=donothing)
# filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


frame = Frame( root, width=600, height=400 )
frame.pack()
frame.place( anchor='center', relx=0.5, rely=0.5 )


labelDescrip = Label( frame, text="Searching...", font="Arial 16", fg="Yellow" )
labelDescrip.config( bg="#cca01d" )
# labelDescrip = Label( frame, text="Success", font="Arial 16", fg="#08ee33" )
# labelDescrip.config(bg="#1f4a1b")
# labelDescrip = Label( frame, text="Error!", font="Arial 16", fg="red" )
# labelDescrip.config(bg="#8a3d3d")

labelDescrip.pack(fill=X, anchor=NW, expand=True)

image = Image.open("victor1.jpg")
newHeight = image.height
newWidth = image.width

if( image.width > 600 ):
   tmpPercent = 600 / image.width
   newWidth = 600
   newHeight = tmpPercent * newHeight

image = image.resize((newWidth, int(newHeight)))
img = ImageTk.PhotoImage(image)

label = Label(frame, image = img)
label.pack()


root.mainloop()

# /////////////////////////////////////////////////////

# fromImg = fr.load_image_file('victor2.jpg')
# fromImg = cv2.cvtColor(fromImg,cv2.COLOR_BGR2RGB)
# camImg = fr.load_image_file('victor1.jpg')
# camImg = cv2.cvtColor(camImg,cv2.COLOR_BGR2RGB)

# faceLoc = fr.face_locations(fromImg)[0]
# cv2.rectangle(fromImg,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)

# encodeElon = fr.face_encodings(fromImg)[0]
# encodeElonTest = fr.face_encodings(camImg)[0]

# comparacao = fr.compare_faces([encodeElon],encodeElonTest)
# distancia = fr.face_distance([encodeElon],encodeElonTest)

# print(comparacao,distancia)
# cv2.imshow('From Image',fromImg)
# cv2.imshow('Cam Image',camImg)
# cv2.waitKey(0)