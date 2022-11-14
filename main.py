from asyncio.windows_events import NULL

from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import frm.FrmAdmin as frmAdmin
import sys
from threading import Thread
from tkinter import messagebox
import threading
from time import sleep
import multiprocessing
import ctypes
import inspect
import frm.FrmImgWidget as imgWidget
import frm.FrmSobreDialog as sobreDialog
import frm.FrmGeraRelatorio as relatorioDialog
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

def existWindow():
   if 'window' in globals():
      return True

def existVideoWidget():
   if 'video_widget' in globals():
      return True
   
   return False

def threaded_update():  
   global runThread
   global window
   global root
   global video_widget
   global _start_time
   global dt
   global faceStatus
   global labelDescrip
   global relatorio_window
      
   while runThread :
      sleep(0.1)

      if( not runThread ):
         return

      if( "relatorio_window" in globals() ):
         relatorio_window.myLoop()

      if( existWindow() ):
         window.myLoop()
      
      if( "video_widget" in globals() and video_widget ):
         video_widget.myLoop()
         now = time.time()
         dt = now - _start_time
         _start_time = now

         if 'window' in globals() and hasattr(window, "close_window") and window.close_window:
            window.close_window = False   
            window.destroy()
            video_widget.setRole( imgWidget.VideoRole.RECOGNIZE_PERSON )
            video_widget.getImageSets()
            
         fileName = ""
         
         if existWindow() and video_widget.role == imgWidget.VideoRole.TAKE_PHOTO_WIDGET:
            videoFrame = cv2.cvtColor(video_widget.getVideoFrame(), cv2.COLOR_BGR2GRAY) 
            face_cascade = cv2.CascadeClassifier('./db/haarcascade_frontalface_alt2.xml')
            faces = face_cascade.detectMultiScale(videoFrame, 1.1, 4)

            if( len(faces) == 1 ):                     
               if window.updateFoto:
                  for (x, y, w, h) in faces:
                     offset = 50
                     # cv2.rectangle(video_widget.getVideoFrame(), (x-offset, y-offset), (x+w+offset, y+h+offset), 
                     #                (0, 0, 255), 2)
                        
                     faces = video_widget.getVideoFrame()[y:y + h +offset, x:x + w]
                     fileName = "./tmpFoto.png"
                     cv2.imwrite(fileName, faces)
                     print( "Take Foto" )
                  
                  window.updateFoto = False
                  window.showTmpImage = True

               video_widget.faceStatus = imgWidget.FaceStatus.TIRE_FOTO

            elif( len(faces) > 1 ): 
               video_widget.faceStatus = imgWidget.FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO  
               if window.updateFoto:
                  messagebox.showerror('Erro ao tirar foto', f'Erro: Mais de uma pessoa detecta.')    
                  window.updateFoto = False

            elif( len(faces) <= 0 ):
               video_widget.faceStatus = imgWidget.FaceStatus.PROCURANDO
               if window.updateFoto:
                  messagebox.showerror('Erro ao tirar foto', f'Erro: Nenhuma pessoa detecta.')   
                  window.updateFoto = False   
            
         faceStatus = video_widget.getFaceRegisterStatus()

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
            
   print( "End thread ")
   raise SystemExit
   raise Exception('Close')
   
def openThread():
   global thread_

   thread_ = ThreadWithExc(target=threaded_update)
   thread_.start()  

def openSobre():
   global sobre_dialog
   sobre_dialog = sobreDialog.FrmSobre( root )
   sobre_dialog.grab_set()
   
def openAdmin():   
   global runThread
   global window
   global thread_
   global video_widget

   video_widget.setRole( imgWidget.VideoRole.TAKE_PHOTO_WIDGET )

   window = frmAdmin.FrmAdmin( root )
   window.grab_set() 

def closeWindow():
   global runThread
   global root
   global video_widget
   runThread = False
   video_widget.setPause(True)
   video_widget.destroy
   del video_widget
   root.destroy()

def openRelatorio():
   global relatorio_window

   relatorio_window = relatorioDialog.FrmRelatorio( root )
   relatorio_window.grab_set()

if __name__ == "__main__":
   root = Tk()
   root.title("Presença de alunos")
   root.config( bg="white" )
   root.geometry( '1024x862' )
   root.attributes('-fullscreen', True)

   frame = Frame( root, width=800, height=600 )
   video_widget = imgWidget.VideoWidget( frame, imgWidget.VideoRole.RECOGNIZE_PERSON )

   runThread = True

   _start_time = time.time()

   openThread()   

   menubar = Menu(root)
   filemenu = Menu(menubar, tearoff=0)
   filemenu.add_command(label="Gerenciar", command=openAdmin)
   filemenu.add_command(label="Gerar Relatório", command=openRelatorio)
   filemenu.add_separator()
   filemenu.add_command(label="Sair", command=root.quit)
   menubar.add_cascade(label="Opções", menu=filemenu)

   helpmenu = Menu(menubar, tearoff=0)
   helpmenu.add_command(label="Sobre...", command=openSobre)
   menubar.add_cascade(label="Ajuda", menu=helpmenu)

   root.config(menu=menubar)

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
