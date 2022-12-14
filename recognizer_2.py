from vosk import Model, KaldiRecognizer
import sys
import json
import os
import time
import wave
from tkinter import *


root = Tk() # Создание окна
root.title("Recognizer") # Название окна


file = Entry(root) #сам аудио файл
file.grid(row = 0, column = 0) 


LoadModel = Entry(root)  # Загрузка самой модели языка
LoadModel.grid(row = 0, column = 1)

result = ''
last_n = False

def RecognizeAudio(event): # Преобразование аудиофайла в текст

    model = Model(LoadModel.get())

    wf = wave.open(file.get(), "rb")
    rec = KaldiRecognizer(model, 90000)

    while True:
        data = wf.readframes(90000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            global result
            
            if res['text'] != '':
                result += f" {res['text']}"
                last_n = False
            elif not last_n:
                result += '\n'
                last_n = True

    res = json.loads(rec.FinalResult())
    result += f" {res['text']}"
    
    global Text
    
    Text = Text(width=40, height=20) # Создание поля для текста
    Text.insert(INSERT, result)
    Text.configure(state='disabled')
    Text.grid()
    
    scroll = Scrollbar(command=Text.yview) # Создание scrollbar
    scroll.grid()
    

button = Button(root, text = "Вывести текст") # Вывод полученных данных
button.grid(row = 0, column = 2)
button.bind("<Button-1>", RecognizeAudio)

   

root.mainloop()