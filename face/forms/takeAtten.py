import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image,ImageStat
import os
from tkinter import filedialog as file
import hashlib
from tkinter import messagebox  




window = tk.Tk()
#window.minsize(1300, 1024)

window.minsize(600,500)

window.title("Take Attendance")


everySingleLineIn_hash_list1 = []
everySingleLineIn_hash_list2 = []
var = StringVar()

deathwing=Image.open('icon/D.png')
image2=deathwing.resize((250,250),Image.ANTIALIAS)
Deathwing2=ImageTk.PhotoImage(image2)
panel = ttk.Label(window, image=Deathwing2)

panel.grid(column = 3, row = 5,padx=20,pady=20)
imagepath= ttk.Label(window,textvariable=var,font=("times new roman",20,"bold"))
path="a.png"
imagepath.grid(row=5,column=1,pady=10,padx=20)


def hashfile(path, blocksize = 65536):  # getting hash function 1
    afile = open(path, 'rb')
    hasher = hashlib.sha512()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


    #hasher = hashlib.md5() should be hasher = hashlib.sha512(). MD5 is ancient and error-prone.

def hash_image(image_path): # getting hash function 1
    img = Image.open(image_path).resize((8,8), Image.LANCZOS).convert(mode="L")
    mean = ImageStat.Stat(img).mean[0]
    return sum((1 if p > mean else 0) << i for i, p in enumerate(img.getdata()))



def check_duplicate(path):
    try: #if file is not available
        hash_list1 = open("/home/amir/Documents/face/doc/hashingList1.txt", "x")
    except:
        #getting values from the first hash list text file
        hash_list1 = open("/home/amir/Documents/face/doc/hashingList1.txt", "r")

        everySingleLineIn_hash_list1 = hash_list1.readlines()
        #for x in everySingleLineIn_hash_list1:
        #    print(x)


    try:
        hash_list2 = open("/home/amir/Documents/face/doc/hashingList2.txt", "x")
    except:    
        #getting values from the second hash list text file
        hash_list2 = open("/home/amir/Documents/face/doc/hashingList2.txt", "r")

        everySingleLineIn_hash_list2 = hash_list2.readlines()
        
        #for x in everySingleLineIn_hash_list2:
        #    print(x)

    hash_list1.close()
    hash_list2.close()

    firstHashGenerate = hashfile(path)
    secondHashGenerate = hash_image(path)

    to_string1 = str(firstHashGenerate)
    to_string2 = str(secondHashGenerate)

    flag1 = 0
    flag2 = 0

    for x in everySingleLineIn_hash_list1:
        if x == to_string1:
            flag1 = 1
            break

    for x in everySingleLineIn_hash_list2:
        if x == to_string2:
            flag2 = 1
            break

    if (flag1 == 0) & (flag2 == 0):

        hash_list1 = open("/home/amir/Documents/face/doc/hashingList1.txt", "a")
        hash_list2 = open("/home/amir/Documents/face/doc/hashingList2.txt", "a")
        
        if len(everySingleLineIn_hash_list1) > 0: # if the text file contains something 
            hash_list1.write("\n") # append in to the new line
            hash_list1.write(to_string1)
        else: # if the text file contains nothing
            hash_list1.write(to_string1)

        if len(everySingleLineIn_hash_list1) > 0: # if the text file contains something 
            hash_list2.write("\n") # append in to the new line
            hash_list2.write(to_string2)
        else: # if the text file contains nothing
            hash_list2.write(to_string2)   
            
    else:
        return 0 # duplicate image found


    hash_list1.close()
    hash_list2.close()

    return 1 # no duplicate image found



def imageSelect():
    errorLable.configure(text="",borderwidth=0)
    print("enter")
    global path
    path=file.askopenfilename(initialdir="/home/amir/",filetypes=[('Image File','.jpg .jpeg .png')])
    
    try:
        upload = Image.open(path)
        uploaded = upload.resize((400,400),Image.ANTIALIAS)

        uploaded1 = ImageTk.PhotoImage(uploaded)   
        panel.configure(image=uploaded1)
        panel.image = uploaded1  
    except Exception as e:
        print(e)
        pass

def imageSubmit():
    errorLable.configure(text="",borderwidth=0)
    try:
        check = check_duplicate(path) # check if this image is already used to take attendance
        print(check)
        if check==1:
            x='python3 ../demo.py '+path  
            os.system(x)
        else:
            messagebox.showinfo("ERROR!","This Image is Already Used to Take Attendance")
    except Exception as e:
        print(e)
        errorLable.configure(text="Please Select A Valid Image!", borderwidth=10, relief="solid")


#get total class
with open('/home/amir/Documents/face/doc/total class.txt','r') as f:
    f_content = f.read()

total_class = "Total Class = "+ str(f_content)

totalClass = Label(window,text = total_class,foreground="blue",background="yellow",font=('Times bold',15))
totalClass.grid(column=1,row=0)

button = ttk.Button(window, text = "add image", command = imageSelect)
button.grid(column = 2, row = 5)

button1 = ttk.Button(window, text = "Submit", command = imageSubmit)
button1.grid(column = 3, row = 10)

errorLable = Label(window,text="",foreground="red",font=('Times bold',18))
errorLable.grid(column = 3, row = 11)

window.mainloop()