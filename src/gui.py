from tkinter import *
from src.chatbot import Chatbot


class gui:

    def __init__(self, database_name, nrows):
        self.bot = Chatbot(database_name = database_name, nrows=nrows)

        self.fenetre = Tk()
        self.canvas = Canvas(self.fenetre, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(self.fenetre, orient="vertical", command=self.canvas.yview)

        botrun = self.bot.run(information = ' ')
        self.question = StringVar(self.fenetre)
        self.question.set(botrun[0])
        self.reponse = StringVar(self.fenetre)
        self.reponse.set(botrun[1])

        self.entree = Entry(self.fenetre, textvariable=' ', width=30)
        self.LabelResultat = Label(self.fenetre, textvariable = self.reponse, width=30, wraplength=250)
        self.label = Label(self.fenetre, textvariable=self.question)

        self.liste_offres = [StringVar(self.fenetre) for i in range(10)]
        for row in range(10):
            Label(self.frame, text="%s" % (row + 1), width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            Label(self.frame, textvariable=self.liste_offres[row]).grid(row=row, column=1)

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.run()

    def populate(self, liste_offres):
        for row in range(10):
            self.liste_offres[row].set(liste_offres[row])

    def send_info(self, event):
        entree = self.entree.get()

        print("bot step ", self.bot.step)

        if self.bot.step < 5 :
            botrun = self.bot.run(entree)
            self.question.set(botrun[0])
            self.reponse.set(botrun[1])
            self.LabelResultat.configure(textvariable = self.reponse)
            self.entree.delete(0, 'end')
        else :
            self.bot.step += 1

        print("bot step ", self.bot.step)

        if self.bot.step == 5 :
            self.populate(self.bot.liste_offres)
        print("bot step ", self.bot.step)

        if self.bot.step == 6:
            if entree in ["Oui", "oui", "1"]:
                self.reset(event=event)
            else :
                self.fenetre.destroy()

    def reset(self, event):
        self.bot.reset()
        botrun = self.bot.run(information = ' ')
        self.question.set(botrun[0])
        self.reponse.set(botrun[1])
        self.entree.delete(0, 'end')
        for row in range(10):
            self.liste_offres[row].set(" ")
        self.LabelResultat.configure(textvariable = "")

    def onFrameConfigure(self):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run(self):
        # Buttons declaration
        ok_button = Button(self.fenetre, text ='OK')
        ok_button.bind("<Button-1>", self.send_info)
        ok_button.grid(row=2,column=0)

        reset_button = Button(self.fenetre, text ='Reset')
        reset_button.bind("<Button-1>", self.reset)
        reset_button.grid(row=2,column=1)

        quit_button = Button(self.fenetre, text ='Quitter', command=self.fenetre.destroy)
        quit_button.grid(row=2,column=2)

        self.fenetre.wm_title("Chatbot")
        self.fenetre.resizable(width=True, height=True)
        self.fenetre.bind('<Return>', self.send_info)

        self.label.grid(row=0, column=0)
        self.entree.grid(row=1, column=0)
        self.LabelResultat.grid(row=3,column=0)

        self.vsb.grid(row=0, column=4)
        self.canvas.grid(row=0, column=3)
        # self.canvas.pack( side="left", fill="both", expand=True)
        self.canvas.create_window((10,10), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure())

        self.fenetre.mainloop()
