import csv, sys, math, random
from Tkinter import *
from pygame import mixer
from PIL import ImageTk, Image


path='/home/arina/kanji/'
filename = str(sys.argv[1])
icon='play_sound3.gif'

## open file
infile = open(filename, 'r')

## define csv reader object, assuming delimiter is tab
tsvfile = csv.reader(infile, delimiter='\t')


class Dic():

    def __init__(self, inpfile):

	self.inpfile = inpfile
	self.kan = []
	self.Kanji = {}
	self.Transl = {}
	self.Tr1 = {}
	self.ON = {}
	self.KUN = {}
	self.ON_rom = {}
	self.KUN_rom = {}
	self.Sound = {}
	
	for line in self.inpfile:
	  kan = line[0].decode("u8")
	  self.kan.append(kan)
	  self.Kanji[kan] = kan
	  self.Transl[kan] = line[7]
	  self.Tr1[kan] = line[1]
	  self.ON[kan] = line[5]
	  self.KUN[kan] = line[6]
	  self.ON_rom[kan] = line[2]
	  self.KUN_rom[kan] = line[3]
 	  self.Sound[kan] = line[4]

    def shuffled(self):
	newkeys = self.Kanji.keys()[:]
	random.shuffle(newkeys)
	return newkeys


class Table(Frame):

    def __init__(self, parent, myDic, num):
        Frame.__init__(self, parent)   
 
	myDic = myDic
	self.num = num
        self.parent = parent        
        self.parent.title("Playkanji_tab")        
	self.grid()
        self.canvas = Canvas(self, background='white')

	## Play button image
	img = Image.open(icon)
	resized = img.resize((30, 30),Image.ANTIALIAS)
	self.imageS = ImageTk.PhotoImage(resized)

	self.Transl = {}
	b = {}
	l = {}

	for i in range(num):
	  kan = myDic.kan[i]
	  b[i] = Button(self.canvas, image=self.imageS, command=lambda k=kan: play(myDic.Sound[k]), relief=RAISED, bg='white', activebackground='white',bd=0)
	  b[i].grid(row=i, column=0, sticky=NSEW)
	  k = Label(self.canvas, text=myDic.Kanji[kan], font=('Purisa', 14, 'bold'), relief=RAISED, bg='white', padx=20, anchor='center')
	  k.grid(row=i, column=1, sticky=NSEW)

	  self.Transl[i] = StringVar(self)
	  self.Transl[i].set(myDic.Transl[kan].split("; ")[0])
	  l[i] = apply(OptionMenu, (self.canvas, self.Transl[i]) + tuple(myDic.Transl[kan].split("; ")))
	  l[i].config(font=('Purisa',14),bg='white',activebackground='white',width=40)
	  l[i]['menu'].config(font=('Purisa',14),bg='white',activebackground='white')
          l[i].grid(row=i, column=2, sticky=NSEW)

	saveBut = Button(self.canvas, text='save table', command=self.Save_new, relief=RAISED, bg='grey', activebackground='green',bd=0)
	saveBut.grid(row=num+1, column=2)

        yscrollbar = Scrollbar(self)
        yscrollbar.grid(row=0, column=1, sticky=NS)

	self.canvas.config(scrollregion=self.canvas.bbox(ALL), yscrollcommand=yscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=NSEW)
        yscrollbar.config(command=self.canvas.yview)

    def Save_new(self):
        print "pushed!"


def main():
  
    root = Tk()
    myDic = Dic(tsvfile)
    num = len(myDic.kan)
    ex = Table(root, myDic, num)
    root.geometry("600x500+300+300")
    root.mainloop()  

def play(sound):

    mixer.init()
    mixer.music.load(path + sound)
    mixer.music.play()


if __name__ == '__main__':
    main() 

