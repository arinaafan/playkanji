import csv, sys, math
from Tkinter import *
from pygame import mixer
from dic import Dic

path='/home/arina/kanji/'
filename = path + str(sys.argv[1])

## open file
infile = open(filename, 'r')

## define csv reader object, assuming delimiter is tab
tsvfile = csv.reader(infile, delimiter='\t')

i=0

class Myframe(Frame):
  
    def __init__(self, parent, mydict):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
	self.myDic = mydict
	kan = self.myDic.kan[0]
        self.parent.title("Playkanji")        
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, background='white')
	button1 = Button(self.canvas, text = ">", font=('Purisa',16), command = self.next_kanji, background="white")
        button1.configure(width = 2, activebackground = '#DFECF2', relief = FLAT)
        button1.pack(side = RIGHT)
	button2 = Button(self.canvas, text = "<", font=('Purisa',16), command = self.prev_kanji, background="white")
        button2.configure(width = 2, activebackground = "#DFECF2", relief = FLAT)
        button2.pack(side = LEFT)

        self.text1 = self.canvas.create_text(190, 80, font=("Purisa", 50, 'bold'), text=self.myDic.Kanji[kan])  
        self.text2 = self.canvas.create_text(190, 130, font=("Purisa", 16, 'bold'), anchor=N, text=str(self.myDic.Tr1[kan]), width='6c', justify="c")
	self.text3 = self.canvas.create_text(80, 210, font="Purisa", anchor=NW, text="ON: "+str(self.myDic.ON_rom[kan]), width='7c')
	self.text4 = self.canvas.create_text(80, 250, font="Purisa", anchor=NW, text="KUN: "+str(self.myDic.KUN_rom[kan]), width='7c')
        self.canvas.pack(fill=BOTH, expand=1)

    def change(self):
        global i
        ii=self.myDic.kan[i]
        self.canvas.itemconfig(self.text1, text=self.myDic.Kanji[ii] )
        self.canvas.itemconfig(self.text2, text=str(self.myDic.Tr1[ii]) )
        self.canvas.itemconfig(self.text3, text="ON: "+str(self.myDic.ON_rom[ii]) )
        self.canvas.itemconfig(self.text4, text="KUN: "+str(self.myDic.KUN_rom[ii]) )
        play(self.myDic.Sound[ii])
        print self.myDic.Kanji[ii], self.myDic.Tr1[ii]

    def next_kanji(self):
	global i
	i+=1
	try:
	  self.change()
	except IndexError:
	  i-=1 

    def prev_kanji(self):
        global i
        i-=1
	try:
          self.change()
	except IndexError:
	  ii+=1

def main():
  
    root = Tk()
    myDic = Dic(tsvfile)
    ex = Myframe(root, myDic)
    root.geometry("380x330+300+300")
    play(myDic.Sound[myDic.kan[0]])
    root.mainloop()  

def play(sound):

    mixer.init()
    mixer.music.load(path + sound)
    mixer.music.play()


if __name__ == '__main__':
    main() 

