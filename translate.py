import csv, sys, math, os
from Tkinter import *
from PIL import ImageTk, Image
from pygame import mixer
from dic import play
import subprocess

path='/home/arina/kanji/'
outFile='newlist.tab'

class Myframe(Frame):
    global word, kanji, trans, pron, hirag, sound
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent        

        self.parent.title("Playkanji_translate")        
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, bg='white')
	self.canvas.pack(fill=BOTH, expand=1)

        self.img = Image.open(path + 'icons/back7.jpg')
        self.img = self.img.resize((600, 450),Image.ANTIALIAS)
#	self.img = self.img.point(lambda p: p * 0.7)
        self.img = ImageTk.PhotoImage(self.img)

	canBg = self.canvas.create_image(0, 0, image=self.img, anchor='nw')

        MODES = [
          ("JA", "ja"),
          ("EN", "en"),
          ("RU", "ru"),
        ]

        self.opt = StringVar()
        self.current_mode = 0
        self.opt.set("ja") # initialize

        dx=150
        self.b = {}
        for text, mode in MODES:
          dx+=60
          self.b[mode] = Radiobutton(self.canvas, text=text, font=("Arial", 12, 'bold'), variable=self.opt, value=mode, \
			bg="#F4DFEB", activebackground="#F4DFEB", bd=0, highlightthickness=0)
          self.b[mode].place(x=dx, y=20, anchor="w")

	l1=self.canvas.create_text(300, 50, font=("Arial", 20, 'bold'), text='Enter the word', justify='c')
	self.entry = Entry(self.canvas, font=("Arial", 12), bg='white')
	self.entry.bind("<Return>", self.search)
	self.entry.place(relx=0.5, y=100, anchor='c')
	button1 = Button(self.canvas, text = "Add to list", font=('Aurisa',14), command = self.add2list, fg="white")
        button1.configure(activebackground = "#DFECF2", relief = FLAT)
        button1.pack(side = BOTTOM)
        self.text1 = self.canvas.create_text(300, 200, font=("Purisa", 65, 'bold'), text='')
        self.text2 = self.canvas.create_text(300, 340, font=("Purisa", 20, 'bold'), text='', width='6c', justify="c")
        self.text3 = self.canvas.create_text(300, 290, font=("Purisa", 16, 'bold'), text='', width='7c', justify="c")


    def search(self, event):
	global mode, word, kanji, trans, pron, hirag, sound
	print 'Search ', self.entry.get()
	translateIt="bash /home/arina/kanji/trans.sh " + self.entry.get() + " " + self.opt.get()
	self.entry.delete(0, END)
	kanji,pron,trans,hirag,sound = subprocess.check_output(translateIt, shell=True).split("\t")
	print kanji, pron, trans, hirag, sound
	self.canvas.itemconfig(self.text1, text=kanji)
	self.canvas.itemconfig(self.text2, text=trans)
	self.canvas.itemconfig(self.text3, text=hirag)
	play(sound)

    def add2list(self):
	global mode, word, kanji, trans, pron, hirag, sound
	print 'add2list'
        print 'File new_List.tab was saved'
        with open(path+'new_List.tab', 'a') as outfile:
                outfile.write(kanji+'\t'+trans+'\t'+pron+'\t'+pron+'\t'+sound+'\t--\t'+hirag+'\t'+trans+'\n')

def main():
    root = Tk()
    game = Myframe(root)
    root.geometry("600x450+300+300")
    def defkey(event):
       if event.keysym=='Shift_R': game.add2list()
       if event.keysym=='<Return>': search(game.entry.get())

    root.bind("<Key>", defkey)
    root.mainloop()  

if __name__ == '__main__':
    main() 

