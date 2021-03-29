from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
#from PIL import ImageTk, Image
#from gender_prediction import emotion,ageAndgender
names = set()
23

class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("700x330+300+200")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='homepagepic.png')
            
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=1, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="   Facial Recognition System       ", font=self.controller.title_font,fg="teal")
            label.grid(row=0, columnspan=2,sticky="ew")
            label2 = tk.Label(self, text="         2021 Unity University All Rights Reserved        ",font=(self.controller.title_font,12),fg="teal")
            label2.grid(row=5, columnspan=2,sticky="ew")
            button1 = tk.Button(self, text="   Add a User  ", fg="#ffffff", bg="teal",font=(self.controller.title_font,12),command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="teal",font=(self.controller.title_font,12),command=lambda: self.controller.show_frame("PageTwo"))
            button4 = tk.Button(self, text="   About Us  ", fg="#ffffff", bg="teal",font=(self.controller.title_font,12),command=lambda: self.controller.show_frame("PageFive"))
            button3 = tk.Button(self, text="Quit", fg="#ffffff", bg="red",font=(self.controller.title_font,12), command=self.on_closing)
            button1.grid(row=1, column=0, ipady=17, ipadx=78)
            button2.grid(row=2, column=0, ipady=17, ipadx=70)
            button4.grid(row=3, column=0, ipady=17, ipadx=85)
            button3.grid(row=4, column=0, ipady=17, ipadx=113)

        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Register a User", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=1, pady=6, padx=4)
        tk.Label(self, text="Enter Name", fg="#263942", font='Helvetica 12 bold').grid(row=5, column=4, pady=60, padx=40)
        self.user_name = tk.Entry(self, borderwidth=3, bg="#ffffff", font=(self.controller.title_font,12))
        self.user_name.grid(row=5, column=5, pady=20, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="red", fg="#ffffff",font=(self.controller.title_font,12), command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="teal" ,font=(self.controller.title_font,12), command=self.start_training)
        self.buttoncanc.grid(row=6, column=4, pady=1, ipadx=25, ipady=5)
        self.buttonext.grid(row=6, column=5, pady=1, ipadx=40, ipady=5)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select User to identify his face", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=1, padx=10, pady=30)
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=5, column=2, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="red", fg="#ffffff")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="teal")
        self.dropdown.grid(row=5, column=3, ipadx=28, padx=6, pady=10)
        self.buttoncanc.grid(row=6, ipadx=20, ipady=4, column=2, pady=10)
        self.buttonext.grid(row=6, ipadx=30, ipady=4, column=3, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="     Take User photo ", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=2, column=3, columnspan=2, sticky="ew", pady=10)
        self.label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=30,ipadx=30)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="teal", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="teal",command=self.trainmodel)
        self.capturebutton.grid(row=3, column=3, ipadx=5, ipady=4, padx=5, pady=20)
        self.trainbutton.grid(row=3, column=4, ipadx=5, ipady=4, padx=5, pady=20)
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="teal", fg="#ffffff").grid(row=0, column=5, padx=10, pady=10)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="This system is designed and developed by:", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=30, pady=10)
        tk.Label(self, text="Developed By", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0, padx=30, pady=10)
        tk.Label(self, text="Mitku Dubale", fg="#263942", font='Helvetica 12 bold').grid(row=2, column=0, padx=30, pady=10)
        tk.Label(self, text="Abdulmjied Kedir", fg="#263942", font='Helvetica 12 bold').grid(row=3, column=0, padx=30, pady=10)
        tk.Label(self, text="Dawit Abera", fg="#263942", font='Helvetica 12 bold').grid(row=4, column=0, padx=30, pady=10)
        tk.Label(self, text="Redwan Nuredin", fg="#263942", font='Helvetica 12 bold').grid(row=5, column=0, padx=30, pady=10)
        tk.Label(self, text="Ayalnesh Belete", fg="#263942", font='Helvetica 12 bold').grid(row=6, column=0, padx=30, pady=10)
        tk.Label(self, text="ID Number", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self, text="UU70723R", fg="#263942", font='Helvetica 12 bold').grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self, text="UU70615R", fg="#263942", font='Helvetica 12 bold').grid(row=3, column=1, padx=10, pady=10)
        tk.Label(self, text="UU71209R", fg="#263942", font='Helvetica 12 bold').grid(row=4, column=1, padx=10, pady=10)
        tk.Label(self, text="UU70801R", fg="#263942", font='Helvetica 12 bold').grid(row=5, column=1, padx=10, pady=10)
        tk.Label(self, text="UU70559R", fg="#263942", font='Helvetica 12 bold').grid(row=6, column=1, padx=10, pady=10)
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="teal", fg="#ffffff").grid(row=0, column=3, padx=10, pady=10)



class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew", ipadx=4, ipady=20)
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="teal")
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="teal", fg="#ffffff")
        button1.grid(row=3,column=2, sticky="ew", ipadx=20, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=3,column=3, sticky="ew", ipadx=20, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)
    #def gender_age_pred(self):
     #  ageAndgender()
    #def emot(self):
     #   emotion()



app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

