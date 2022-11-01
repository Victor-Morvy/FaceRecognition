from asyncio.windows_events import NULL

from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
# import frm.FrmAdmin as frm
import frm.utils as utils
import frm.FrmAdmin as frmAdmin
import sys
from threading import Thread
import threading
from time import sleep
import multiprocessing
import ctypes
import inspect
import frm.FrmImgWidget as imgWidget
import time
import cv2


def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class ThreadWithExc(threading.Thread):
    '''A thread class that supports raising an exception in the thread from
       another thread.
    '''
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

    def _get_my_tid(self):
        """determines this (self's) thread id

        CAREFUL: this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.is_alive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do: self.ident

        raise AssertionError("could not determine the thread's id")

    def raiseExc(self, exctype):
        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL: this function is executed in the context of the
        caller thread, to raise an exception in the context of the
        thread represented by this instance.
        """
        _async_raise( self._get_my_tid(), exctype )

def donothing():
   x = 0

root = Tk()
root.title("Presença de alunos")
root.config( bg="white" )
root.geometry( '1024x862' )

frame = Frame( root, width=800, height=600 )
video_widget = imgWidget.VideoWidget( frame, imgWidget.VideoRole.RECOGNIZE_PERSON )

runThread = True


def existWindow():
   if 'window' in globals():
      return True

def existVideoWidget():
   if 'video_widget' in globals():
      return True
   
   return False
      
_start_time = time.time()
def threaded_update():  
   global runThread
   global window
   global root
   global video_widget
   global _start_time
   global dt
   global faceStatus
   global labelDescrip
      
   while runThread :
      sleep(0.1)
      if( existWindow() ):
         window.myLoop()
      if( video_widget ):
         video_widget.myLoop()
         now = time.time()
         dt = now - _start_time

         if video_widget:

               video_widget.myLoop()
               faceStatus = video_widget.getFaceRegisterStatus()

               # try:
               if faceStatus == imgWidget.FaceStatus.MATCH_FOTO:
                  aluno = video_widget.getAlunoFound()
                  labelDescrip.config( text="Aluno presente RA " + str(aluno.ra_aluno) + " - " + aluno.nome_aluno ,
                                          bg="#1f4a1b",
                                          fg="white") 
               elif faceStatus == imgWidget.FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO:
                  labelDescrip.config( text="Reconhecendo mais de um rosto",
                                          bg="#8a3d3d",
                                          fg="black" )
               elif faceStatus == imgWidget.FaceStatus.OFF:
                  labelDescrip.config( text="Camera desligada",
                                          bg="#8a3d3d",
                                          fg="black" )
               elif faceStatus == imgWidget.FaceStatus.TIRE_FOTO:
                  labelDescrip.config( text="Olhe diretamente para a câmera",
                                          bg="#1f4a1b",
                                          fg="white") 
               elif faceStatus == imgWidget.FaceStatus.ACHOU:
                  labelDescrip.config( text="Olhe diretamente para a câmera",
                                          bg="#1f4a1b",
                                          fg="white") 
               else:# faceStatus == imgWidget.FaceStatus.PROCURANDO:
                  labelDescrip.config( text="Procurando...",
                                          bg="#FDD017",
                                          fg="black" )
            

               if 'window' in globals() and hasattr(window, "close_window") and window.close_window:
                  window.close_window = False
                  window.destroy()
                  video_widget.setRole( imgWidget.VideoRole.RECOGNIZE_PERSON )
                  video_widget.getImageSets()
                  

               if existWindow() and window.updateFoto:
                  videoFrame = video_widget.getVideoFrame()
                  print( "Take Foto" )
                  fileName = "./tmpFoto.png"
                  cv2.imwrite(fileName, videoFrame)
                  window.showTmpImage = True
                  window.updateFoto = False
      

   print( "End thread ")
   raise SystemExit
   raise Exception('Close')
   
def openThread():
   global thread_

   thread_ = ThreadWithExc(target=threaded_update)
   thread_.start()   
   
openThread()   

def openAdmin():
   
   global runThread
   global window
   global thread_
   global video_widget

   video_widget.setRole( imgWidget.VideoRole.TAKE_PHOTO_WIDGET )

   window = frmAdmin.FrmAdmin( root )
   window.grab_set()
   

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Gerenciar", command=openAdmin)
filemenu.add_separator()
filemenu.add_command(label="Sair", command=root.quit)
menubar.add_cascade(label="Opções", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Sobre...", command=donothing)
menubar.add_cascade(label="Ajuda", menu=helpmenu)

root.config(menu=menubar)

def closeWindow():
   global runThread
   global root
   global video_widget
   runThread = False
   video_widget.setPause(True)
   video_widget.destroy
   del video_widget
   root.destroy()

root.protocol("WM_DELETE_WINDOW", closeWindow)

frame.pack()
frame.place( anchor='center', relx=0.5, rely=0.5 )

labelDescrip = Label( frame, text="Searching...", font="Arial 16", fg="Yellow" )
labelDescrip.config( bg="#cca01d" )

labelDescrip.pack(fill=X, anchor=NW, expand=True)

video_widget.pack()

root.mainloop()

print("Good bye!")
   
thread_.raiseExc(OSError)
sys.exit()
raise SystemExit
