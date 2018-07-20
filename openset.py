import csv, sys, math
from Tkinter import *
from PIL import ImageTk, Image


path='/home/arina/kanji/'
icon='/home/arina/kanji/icons/icon_5_small.png'

class Myframe(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title("Playkanji")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self, background='white')

        self.img = Image.open(icon)
        resized = self.img.resize((60, 80),Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(resized)

        myfile= path + 'kanji_1001_read.tab'
        button = Button(self.canvas, compound=TOP, image=self.icon, text = "Junior", command = lambda k=myfile: self.openset(k) )
        button.pack(side = LEFT)
        self.canvas.pack(fill=BOTH, expand=1)


    def openset(self, myfile):
        print 'you are going to open kanji set ==> ', myfile
        self.parent.destroy()


def main():

    root = Tk()
    ex = Myframe(root)
    root.geometry("600x400+300+300")
    root.mainloop()

if __name__ == '__main__':
    main()



