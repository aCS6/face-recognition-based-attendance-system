from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  
import mysql.connector as mysql
from tkinter import filedialog as fd
import shutil, os
from pathlib import Path
from PIL import Image, ImageTk
import face_recognition


# intializing the window
window = tk.Tk()
window.title("Student Management System")

# configuring size of the window 
window.geometry('770x380')
window.resizable(False,False)

def disallowDuplicate(recognizingImagePath,notCheck):  # check if the uploaded photo matched with some Existed already
    # notCheck parameter is used to 
    # delete that filepath from " files " list while change / update image
    # in inseriting this parameter would recieve empty string which is ""
    # this function calling from choosefile function

    if len(recognizingImagePath)!=0:

            #get the directories
        path = '/home/amir/Documents/face/img/known' # using pwd command in linux

        files = []  # CONTAINS FILE NAME WITH DIRECTORY
        # r=root, d = directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.jpg' in file:
                    files.append(os.path.join(r, file))
                elif '.jpeg' in file:
                    files.append(os.path.join(r, file))
                elif '.png' in file:
                    files.append(os.path.join(r, file))


        if len(notCheck)!=0:
            try:
                files.remove(notCheck)
            except:
                pass

        known_face_encodings = []
        
        for file in files:
            try:
                pictures = face_recognition.load_image_file(file)
                faceEncoding = face_recognition.face_encodings(pictures)[0]
                known_face_encodings.append(faceEncoding)

            except:
                pass

        test_image = face_recognition.load_image_file(recognizingImagePath)
        test_face_encoding = face_recognition.face_encodings(test_image)[0]

        for f in known_face_encodings:
            results = face_recognition.compare_faces([f],test_face_encoding,tolerance=0.50)

            if results[0] == True:
                print("Known Face Found")
                return 1
            else:
                print("No Fatch Matched")
                return 0
    
    else:
        return -1




def findFaces(imagepath):

    try:

        image = face_recognition.load_image_file(imagepath)
        face_locations = face_recognition.face_locations(image)

        p = len(face_locations) 
        
        # p = 0 means no face in the image [ not allowed for uplaoding in the database ]
        # p = 1 means single face in the image [ allowed ]
        # p > 1 more than one face , many faces [ not allowed ]

        if p == 0:
            return 0
        elif p == 1:
            return 1
        else:
            return 2
    
    except:
        return -1

def choosefile():
    global filename
    filename =  fd.askopenfilename(initialdir="/home/amir/",filetypes=[('Image File','.jpg .jpeg .png')])

    if len(filename)!=0:
        try:
            firstOpenTheImage = Image.open(filename)
            resizeThefirstOpenTheImage = firstOpenTheImage.resize((200,200),Image.ANTIALIAS) ## The (200, 200) is (height, width)
            finallyLoadTheResizedImage = ImageTk.PhotoImage(resizeThefirstOpenTheImage)
            
            imageLabel = tk.Label(TAB1, image=finallyLoadTheResizedImage, borderwidth=10, relief="solid")
            imageLabel.image = finallyLoadTheResizedImage 
            imageLabel.place(x=450, y=30)

            check = findFaces(filename) # check the image is valid or not

            if check == -1:
                pass
            elif check == 0:
                errorLable.config(text="(X) Not A Human Face ")
                messagebox.showinfo("Face Error", "Image must contains human face.")
                filename = ""

            elif check == 1: # image contains the single face
                
                check2 = disallowDuplicate(filename,"") # check Is there any duplicacy

                if check2 == 0:
                    errorLable.config(text="")
                elif check2 == 1:
                    print("This")
                    errorLable.config(text="(X) This Person is Already a Student")
                    filename == ""

            else:
                errorLable.config(text="(X) Single Face Required ")
                messagebox.showinfo("Face Error", "Image must not have more than one face")
                filename = ""
        except:
            pass


def clearInTab1():
    global filename
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')
    entry4.delete(0, 'end')
    errorLable.config(text="")
    filename = ""

    imageLabelHide = Label(TAB1,width=200,height=200)
    imageLabelHide.place(x=450, y=30)

def insertData():
    stdid = str(entry1.get())
    stdname = entry2.get()
    stdphone = entry3.get()
    stdemail = entry4.get()
    global filename

    if (stdid=="") or (stdname=="") or (stdphone=="") or (stdemail==""): 
        messagebox.showinfo("Insert Error !", "All Fields Required.")

    elif len(filename)==0:
        messagebox.showinfo("Insert Error !", "Please select an image")
    else:
        try:
            # print(filename) # This the file path
            
            realpathWithRealName = filename
            realpath = os.path.dirname(realpathWithRealName)

            # os.path.splittext() this function takes "Any Path with filename"
            # and return two variables
            # 1. Just File Name without extension
            # 2. just File Extension

            filename, file_extension = os.path.splitext(filename)  
            
            # print(filename)
            # print(file_extension) 
            
            #setting new filename [ path + filename + extension ]
            rename = realpath+"/"+str(entry1.get())+file_extension  
            
            #print(rename)
    
            os.rename(realpathWithRealName,rename)

            ### Just Get the filename with Extension from the filepath
            stdphoto = os.path.basename(rename)
            #print(stdphoto)



            try:
                ### insert into database now ###
                con = mysql.connect(host="localhost",user="root",password="pass",database="student")
                cursor = con.cursor()
                cursor.execute("insert into std values('"+ str(stdid) +"','"+ stdname +"','"+ stdphone +"','"+ stdemail +"','"+ stdphoto +"')")
                cursor.execute("commit")
                messagebox.showinfo("Success", "New Student Inserted")
                
                fetch_data()
                clearInTab1()                
                con.close()

                ### copy the image to the destination ###
                shutil.copy(rename,'/home/amir/Documents/face/img/known')
            except shutil.SameFileError:
                messagebox.showinfo("ERROR !", "Already This ID has been taken.")
                pass
            else:
                pass

        except Exception as e:
            #print(e)
            messagebox.showinfo("ERROR !", "Please select valid Image")


def fetch_data():
    con = mysql.connect(host="localhost",user="root",password="pass",database="student")
    cur = con.cursor()
    cur.execute("select * from std ORDER BY id")
    rows=cur.fetchall()

    strs = "Total => ( " + str( len(rows) ) + " )"
    totalstd.config(text=strs)
    if len(rows) !=0:
        Student_table.delete(*Student_table.get_children())
        for row in rows:
            Student_table.insert('',END,values=row)
        con.commit()
    con.close()

def get():

    global nameLabel
    global idLabel
    global contactLabel
    global emailLabel
    global entrys1
    global entrys2
    global entrys3
    global imgpath
    global updateButton
    global deleteButton
    global labimg
    global updateImageBtn

    if searchEntry.get() == "":
        messagebox.showinfo("ERROR !", "Please Enter 'ID' to Search.")
    
    else:
        con = mysql.connect(host="localhost",user="root",password="pass",database="student")
        cur = con.cursor()
        cur.execute("select * from std where id='"+ searchEntry.get() + "'")
        rows=cur.fetchall() 

        if len(rows)==0:
                messagebox.showinfo("Miss Match", "No Records Found.")
        else:
            for row in rows:
                    ### Basic Data Section ###
                
                show = "ID : " + str(row[0]) 
                idVariable.set(show)


                idLabel = ttk.Label(TAB3,font=('Times bold',20), textvariable=idVariable)
                idLabel.place(x=300+100,y=50)


                nameLabel = ttk.Label(TAB3,text="Name",font=('arial bold',12))
                nameLabel.place(x=300+100,y=90)

                entrys1 = Entry(TAB3)
                entrys1.place(x=380+100,y=90)
                entrys1.insert(0,row[1])


                contactLabel = ttk.Label(TAB3,text="Contact",font=('arial bold',12))
                contactLabel.place(x=300+100,y=120)

                entrys2 = Entry(TAB3)
                entrys2.place(x=380+100,y=120)
                entrys2.insert(0,row[2])


                emailLabel = ttk.Label(TAB3,text="Email",font=('arial bold',12))
                emailLabel.place(x=300+100,y=150)

                entrys3 = Entry(TAB3)
                entrys3.place(x=380+100,y=150)
                entrys3.insert(0,row[3])
               
                updateButton = Button(TAB3,text="Update",background="blue",foreground="white",command=data_update,cursor="hand1")
                updateButton.place(x=300+100,y=200)


                deleteButton = Button(TAB3,text="Delete",background="red",foreground="white",command=deleteStudent,cursor="hand1")
                deleteButton.place(x=475+100,y=200)


                ### Show Image Section ###
                
                imgpath = '/home/amir/Documents/face/img/known/' + row[4]

                try:
                    firstOpenTheImage = Image.open(imgpath)
                    resizeThefirstOpenTheImage = firstOpenTheImage.resize((200,200),Image.ANTIALIAS) ## The (200, 200) is (height, width)
                    finallyLoadTheResizedImage = ImageTk.PhotoImage(resizeThefirstOpenTheImage)
                    
                    labimg = tk.Label(TAB3, image=finallyLoadTheResizedImage)
                    labimg.image = finallyLoadTheResizedImage 
                    labimg.place(x=60, y=60)
                
                except:
                    pass

                updateImageBtn = Button(TAB3,text="Change Image",background="green",foreground="white",command=change_photo,cursor="plus")
                updateImageBtn.place(x=90,y=280)            


            con.close()


def data_update():
    update_id = searchEntry.get()
    update_name = entrys1.get()
    update_contact = entrys2.get()
    update_email = entrys3.get()

    if update_id =="" or update_name == "" or update_contact == "" or update_email == "":
        messagebox.showinfo("ERROR !!!","All Fields are required")
    else:
        con = mysql.connect(host="localhost",user="root",password="pass",database="student")
        cursor = con.cursor()
        cursor.execute(" update std set name = '"+ update_name + "' , phone = '"+ update_contact + "' , email = '" + update_email + "' where id ='"+ update_id +"' ")
        cursor.execute("commit")
        messagebox.showinfo("Success", "Data Updated Successfully.")

        fetch_data()  ## just recall and refresh data from database
        get()  ## just recall and refresh data from database

def change_photo():
    global filename
    update_id = searchEntry.get()
    filename =  fd.askopenfilename(initialdir="/home/amir/",filetypes=[('Image File','.jpg .jpeg .png')])
    
    if len(filename)!=0:
        check = findFaces(filename) # check the image is valid or not

        if check == -1:
            pass
        elif check == 0:
            messagebox.showinfo("Face Error", "Image must contains human face.")
            filename = ""

        elif check == 1:
            pass

        else:
            messagebox.showinfo("Face Error", "Image must not have more than one face")
            filename = ""

    if len(filename)==0:
        pass # do nothing
    
    else:
        try:
            print(filename)
            os.remove(imgpath) # remove the Previous image of the student from the folder
            # imgpath variable comes from the get() function

        except:
            pass
        
        ## Showing the selected image ##
        try:
            firstOpenTheImage = Image.open(filename)
            resizeThefirstOpenTheImage = firstOpenTheImage.resize((200,200),Image.ANTIALIAS) ## The (200, 200) is (height, width)
            finallyLoadTheResizedImage = ImageTk.PhotoImage(resizeThefirstOpenTheImage)
            
            labimg = tk.Label(TAB3, image=finallyLoadTheResizedImage)
            labimg.image = finallyLoadTheResizedImage 
            labimg.place(x=60, y=60)
     
            ## To understand these bunch of coding goto insertdata() function ##
            # And the [ else ] part explains all
                
            realpathWithRealName = filename
            realpath = os.path.dirname(realpathWithRealName)

            filename, file_extension = os.path.splitext(filename)  

            rename = realpath+"/"+str(update_id)+file_extension  

            os.rename(realpathWithRealName,rename)

            stdphoto = os.path.basename(rename)
            
            ### Update the database ###

            con = mysql.connect(host="localhost",user="root",password="pass",database="student")
            cursor = con.cursor()
            cursor.execute(" update std set photo = '"+ stdphoto +"' where id ='"+ update_id +"' ")
            cursor.execute("commit")
            messagebox.showinfo("Success", "Image has been changed")


            ### copy the image to the destination ###
            shutil.copy(rename,'/home/amir/Documents/face/img/known')

            filename = ""
            fetch_data()  ## just recall and refresh data from database
            get()  ## just recall and refresh data from database

        except:
            pass
            
def deleteStudent():
    update_id = searchEntry.get()
    update_name = entrys1.get()
    update_contact = entrys2.get()
    update_email = entrys3.get()

    if update_id =="" :
        messagebox.showinfo("ERROR !!!","All Fields are required")
    else:
        con = mysql.connect(host="localhost",user="root",password="pass",database="student")
        cursor = con.cursor()
        cursor.execute(" delete from std where id ='"+ update_id +"' ")
        cursor.execute("commit")
        messagebox.showinfo("Success", "Data Deleted Successfully.")
        
        try:
            os.remove(imgpath) # delete the image from the folder
        except:
            pass
        
        #attach a frame to hide the components in TAB3 
        myframe = Frame(TAB3,height=330,width=770)
        myframe.place(x=0,y=50)

        searchEntry.delete(0, 'end')

        fetch_data()



#Create Tab Control
TAB_CONTROL = ttk.Notebook(window)

#Tab1
TAB1 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB1, text='Add Student')

#Tab2
TAB2 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB2, text='All Student')

#Tab3
TAB3 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB3, text='Profile card')

TAB_CONTROL.pack(expand=1, fill="both")


#Tab1 Elements

ids = ttk.Label(TAB1,text="Enter ID ",font=('bold',10))
ids.place(x=30,y=30)

name = ttk.Label(TAB1,text="Enter Name",font=('bold',10))
name.place(x=30,y=60)

phone = ttk.Label(TAB1,text="Enter Phone",font=('bold',10))
phone.place(x=30,y=90)

email = ttk.Label(TAB1,text="Enter Email",font=('bold',10))
email.place(x=30,y=120)

photo = ttk.Label(TAB1,text="Insert Photo",font=('bold',10))
photo.place(x=30,y=170)

errorLable = Label(TAB1,text="",foreground="red",font=('Times bold',12))
errorLable.place(x=455,y=255)


entry1 = Entry(TAB1)
entry1.place(x=120,y=30)

entry2 = Entry(TAB1)
entry2.place(x=120,y=60)

entry3 = Entry(TAB1)
entry3.place(x=120,y=90)

entry4 = Entry(TAB1)
entry4.place(x=120,y=120)

buttonAddImage = Button(TAB1,text="Browse",bd='5',command=choosefile,cursor="plus")
buttonAddImage.place(x=120,y=160)

clearButton = Button(TAB1,text=" Clear ",command=clearInTab1,borderwidth="2",relief="solid",foreground="red",cursor="hand1")
clearButton.place(x=30,y=220)

insertButton = Button(TAB1,text="Add Student",command=insertData,background="red",foreground="white",cursor="hand1")
insertButton.place(x=180,y=220)


#TAB2 Elements


tab2Heading = ttk.Label(TAB2,text="All Students Records",font=('Arial bold',20),background="black",foreground="white")
tab2Heading.place(x=250,y=5)

totalstd = ttk.Label(TAB2,text="",font=('Arial bold',12),foreground="red")
totalstd.place(x=1,y=1)

#### This is the table for showing Records #####

Table_Frame = Frame(TAB2,bd=4,relief=RIDGE,bg="blue")
Table_Frame.place(x=10,y=50,width=750,height=300)

scroll_x = Scrollbar(Table_Frame,orient=HORIZONTAL)
scroll_y = Scrollbar(Table_Frame,orient=VERTICAL)
Student_table = ttk.Treeview(Table_Frame,columns=("roll","name","contact","email","image"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=Student_table.xview)
scroll_y.config(command=Student_table.yview)

Student_table.heading("roll",text="Roll")
Student_table.heading("name",text="Name")
Student_table.heading("email",text="Email")
Student_table.heading("contact",text="Contact")
Student_table.heading("image",text="Image")

Student_table['show'] = 'headings'

Student_table.column("roll",width=50)
Student_table.column("name",width=200)
Student_table.column("contact",width=170)
Student_table.column("email",width=200)
Student_table.column("image",width=80)

Student_table.pack(fill=BOTH,expand=1)

fetch_data()  # executing sql query to retrieve data

#Tab3 Elements


label1Tab3 = ttk.Label(TAB3,text="Enter ID to get ",font=('helvetica bold',12))
label1Tab3.place(x=2,y=8)

searchEntry = Entry(TAB3)
searchEntry.place(x=140,y=8,height=30)

buttonSeach = Button(TAB3,text="  Get  ",bd='1', font = ('calibri', 10, 'bold', 'underline'), 
                foreground = 'red',command=get, cursor="hand2")
buttonSeach.place(x=320,y=8)

idVariable = tk.StringVar()




#Calling Main()
window.mainloop()