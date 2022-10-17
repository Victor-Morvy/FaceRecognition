import cv2
import face_recognition as fr
from tkinter import *
from PIL import ImageTk, Image

def donothing():
   x = 0

root = Tk()
root.title("Presença de alunos")
root.config( bg="white" )
root.geometry( '1024x862' )

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


frame = Frame(root, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

statusText = StringVar()

labelDescrip = Label( frame, text=statusText )
statusText.set("Test")
labelDescrip.pack()

image = Image.open("victor1.jpg")
image.height
image.width
image = image.resize((600, 450))
img = ImageTk.PhotoImage(image)
# img.zoom(0.5)

label = Label(frame, image = img)
label.pack()



root.mainloop()


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