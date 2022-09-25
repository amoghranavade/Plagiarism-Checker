from tkinter import *

import tkinter
from turtle import back
from PIL import ImageTk, Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter.filedialog as fd

from tkinter.filedialog import askopenfile
import tkinter.filedialog as fd
win = Tk()
win.iconbitmap("./app/applogo.ico")

global student_files 
student_files = []

def check_plagiarism():
    global s_vectors
    print(student_files)
    student_notes =[open(File).read() for File in  student_files]
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
    vectors = vectorize(student_notes)
    s_vectors = list(zip(student_files, vectors))
    plagiarism_results = set()
    for student_a, text_vector_a in s_vectors:
        new_vectors =s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b , text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1],int(sim_score * 100))
            plagiarism_results.add(score)
    return plagiarism_results

def answers() :
    global button,label1, start_label, buttonUpload, back_button
    button.destroy()
    label1.destroy()
    buttonUpload.destroy()
    
    lb = Label(win, text='The result for the given input files are given below',font=('Poppins 17 bold'))
    lb.place(x=170,y=65)
    labels=[] 
    output = ""
    for data in check_plagiarism():
        print(data)
        output += "The percentage of similarity between " + str(data[0].split(".")[0]) + " and " + str(data[1].split(".")[0]) + " is " + str(data[2]) + "%\n"
    label = Label(win, text=output, font=('Poppins 16 bold'), bg='black', fg='white', padx=10, pady=10)
    label.place(x=120, y=120)

def upload_files():
    files = fd.askopenfilenames(parent=win, title='Choose a file',multiple=True)
    my_str = tkinter.StringVar()
    l2 = tkinter.Label(win,textvariable=my_str,fg='red' )
    my_str.set("")
    file_name = ""
    for file in files:
        if(file):
            file_name = file_name + file + "\n"
        student_files.append(file.split("/")[-1])
    my_str.set(file_name)
    print(file_name)
    print(student_files)

    l2.place(x=320,y=500)
        
win.title('Plagiarism Checker App')
win.configure(bg='#F2F3F7')
win.geometry("900x600")
win.resizable(False, False)
image = Image.open("./app/displayImage.jpg")
resize_image = image.resize((500, 300))
img = ImageTk.PhotoImage(resize_image)
label1 = Label(image=img)
label1.image = img
label1.place(x = 220, y=80)
Label(win, text="Plagarism Checker", font=('Poppins 18 bold')).place(x=350,y=10)
button = Button(win,border="0", command=answers)
img = PhotoImage(file="./app/submit.png")
img2 = PhotoImage(file="./app/upload.png")
button.config(image=img)
button.place(x = 480, y = 400)
global buttonUpload
buttonUpload = Button(win, border="0", text="Choose Files",command=upload_files)
buttonUpload.config(image=img2)
buttonUpload.place(x = 320, y = 400)

win.mainloop()