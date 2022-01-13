import tkinter
import time
import requests
import cv2
import numpy as np
import imutils
import os
from tkinter import ttk
from tkinter import messagebox
import read_plate

path_in = 'C:\\Users\\Dai Duong\\Desktop\\btl_tgmt\\xe_in'
path_out = 'C:\\Users\\Dai Duong\\Desktop\\btl_tgmt\\xe_out'


win = tkinter.Tk()
win.title("Kiểm tra xe ra vào")
win.geometry("1280x200+320+0")

data = tkinter.Tk()
data.geometry("1280x720+320+200")

cTableContainer = tkinter.Canvas(data)
fTable = tkinter.Frame(cTableContainer)
fTable.config(bg='#DDDDDD')
sbVerticalScrollBar = tkinter.Scrollbar(data)

url = "http://192.168.1.160:8080/shot.jpg"

i=0

lmain = tkinter.Label(win)

def get_frame():
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=1000, height=1800)
    return img

def show_frame():
    global i
    cv2.imshow("Android_cam", get_frame())
    lmain.after(10, show_frame)
    
def get_plate_in():
    global i
    i=i+1
    cv2.imwrite(os.path.join(path_in , 'plate'+str(i)+'.jpg'), get_frame())
    plate_file = path_in+"\\plate"+str(i)+".jpg"

    return plate_file

def get_plate_out():
    global i
    cv2.imwrite(os.path.join(path_out , 'plate'+str(i)+'.jpg'), get_frame())
    plate_file = path_out+"\\plate"+str(i)+".jpg"
    return plate_file


def updateScrollRegion():
    cTableContainer.update_idletasks()
    cTableContainer.config(scrollregion=fTable.bbox())

def createScrollableContainer():
    cTableContainer.config(yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
    sbVerticalScrollBar.config(orient=tkinter.VERTICAL, command=cTableContainer.yview)

    sbVerticalScrollBar.pack(fill=tkinter.Y, side=tkinter.RIGHT, expand=tkinter.FALSE)
    cTableContainer.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=tkinter.TRUE)
    cTableContainer.create_window(0, 0, window=fTable, anchor=tkinter.NW)

name = tkinter.Label(win, text="Kiểm tra xe ra vào", font=("Times New Roman",48), bg="cyan")
name.place(x=5,y=5,width=945,height=100)

def function_clock():
    string = time.strftime('%H:%M:%S %p')
    lbl_clock.config(text = string)
    lbl_clock.after(1000, function_clock)
    
temp_number=[]
temp_index=[]
global index
index=0
def function_in(number):
    global index
    data,licPlate = read_plate.main(number)
    if data not in temp_number:
        time_in = str(time.strftime('%H-%M-%S %p'))
        print("time in: " + time_in)
        cv2.imwrite(os.path.join(path_in,'plate'+data+'-'+time_in+'.jpg'), licPlate) #ghi ảnh
        temp_number.append(data)
        temp_index.append(index)
        cars = tkinter.Label(win,text = "Số lượng xe " +str(len(temp_number)), font=('Times New Roman', 24))
        cars.place(x=540,y=125,width=200,height=55)
        tkinter.Label(fTable, text=index+1, font=('Times New Roman', 24)).grid(row=index+1,column=0,pady=5)
        tkinter.Label(fTable, text=data, font=('Times New Roman', 24)).grid(row=index+1,column=1,pady=5)
        tkinter.Label(fTable, text=time.strftime('%H:%M:%S %p'), font=('Times New Roman', 24)).grid(row=index+1,column=2,pady=5)
        index+=1
        updateScrollRegion()
    else:
        messagebox.showinfo("Có lỗi!","Xe mang biển số "+data+" đang đỗ trong bãi!")
    

def function_out(number):
    data,licPlate = read_plate.main(number)
    if data in temp_number:
        time_out = str(time.strftime('%H-%M-%S %p'))
        print("time in: " + time_out)
        cv2.imwrite(os.path.join(path_out,'plate'+data+'-'+time_out+'.jpg'), licPlate) #ghi ảnh
        index = temp_number.index(data)
        tkinter.Label(fTable, text=time.strftime('%H:%M:%S %p'), font=('Times New Roman', 24)).grid(row=temp_index[index]+1,column=3)
        temp_number.pop(index)
        temp_index.pop(index)
        cars = tkinter.Label(win,text = "Số lượng xe " +str(len(temp_number)), font=('Times New Roman', 24))
        cars.place(x=540,y=125,width=200,height=55)
        updateScrollRegion()
    else:
        messagebox.showinfo("Có lỗi!","Trong bãi không có xe mang biển số "+data+"!")
        
check_in = tkinter.Button(win, text="In", font=('Times New Roman', 24), command=lambda: function_in(get_plate_in()))
check_in.place(x=400,y=125,width=100,height=55)

check_out = tkinter.Button(win, text="Out", font=('Times New Roman', 24), command=lambda: function_out(get_plate_out())) 
check_out.place(x=780,y=125,width=100,height=55)

cars = tkinter.Label(win,text = "Số lượng xe " +str(len(temp_number)), font=('Times New Roman', 24))
cars.place(x=540,y=125,width=200,height=55)

lbl_clock = tkinter.Label(win, font=('Times New Roman', 36, 'bold'), background = 'magenta', foreground = 'white')
lbl_clock.place(x=960,y=5,width=315,height=100)

createScrollableContainer()

tkinter.Label(fTable, text="Số thứ tự".center(15, " "), font=('Times New Roman', 24), bg='red').grid(row=0,column=0,padx=5,pady=5)
tkinter.Label(fTable, text="Biển số xe".center(20, " "), font=('Times New Roman', 24), bg='green').grid(row=0,column=1,padx=5,pady=5)
tkinter.Label(fTable, text="Thời gian vào".center(40, " "), font=('Times New Roman', 24), bg='blue').grid(row=0,column=2,padx=5,pady=5)
tkinter.Label(fTable, text="Thời gian ra".center(40, " "), font=('Times New Roman', 24), bg='yellow').grid(row=0,column=3,padx=5,pady=5)

function_clock()
show_frame()


win.resizable(False, False) 
win.mainloop()



