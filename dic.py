import csv, sys, math, random
from Tkinter import *
from pygame import mixer
from PIL import ImageTk, Image


path='/home/arina/kanji/'
filename = path + str(sys.argv[1])
icon = path + 'icons/play_sound3.gif'

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
	  self.ON[kan] = line[5].decode("u8")
	  self.KUN[kan] = line[6].decode("u8")
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
 
	self.myDic = myDic
	self.num = num
        self.parent = parent        
        self.parent.title("Playkanji_tab")        
	self.pack(fill="both", expand=True)
        self.canvas = Canvas(self, background='white')
	self.frame = Frame(self.canvas, bg='white') 
        yscrollbar = Scrollbar(self, command=self.canvas.yview)
        self.canvas.config(yscrollcommand=yscrollbar.set)
	yscrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
	self.canvas.create_window((0,0), window=self.frame, anchor="nw")

	self.frame.bind("<Configure>", self.onFrameConfigure)

	## Play button image
	img = Image.open(icon)
	resized = img.resize((30, 30),Image.ANTIALIAS)
	self.imageS = ImageTk.PhotoImage(resized)

	self.Transl = {}
	b = {}
	l = {}

	for i in range(self.num):
	  kan = self.myDic.kan[i]
	  b[i] = Button(self.frame, image=self.imageS, command=lambda k=kan: play(self.myDic.Sound[k]), relief=RAISED, bg='white', activebackground='white',bd=0)
	  b[i].grid(row=i, column=0, sticky=NSEW)
	  k = Label(self.frame, text=self.myDic.Kanji[kan], font=('Purisa', 14, 'bold'), relief=RAISED, bg='white', padx=20, anchor='center')
	  k.grid(row=i, column=1, sticky=NSEW)

	  self.Transl[kan] = StringVar(self)
	  self.Transl[kan].set(self.myDic.Transl[kan].split("; ")[0])
	  l[i] = apply(OptionMenu, (self.frame, self.Transl[kan]) + tuple(self.myDic.Transl[kan].split("; ")))
	  l[i].config(font=('Purisa',14),bg='white',activebackground='white',width=40)
	  l[i]['menu'].config(font=('Purisa',14),bg='white',activebackground='white')
          l[i].grid(row=i, column=2, sticky=NSEW)

	saveBut = Button(self.frame, text='save table', command=self.Save_new, relief=RAISED, bg='grey', activebackground='green',bd=0)
	saveBut.grid(row=num+1, column=2)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def Save_new(self):
	global filename
	print 'File ', filename, ' was saved'
	with open(filename, 'w') as outfile:
	  for i in range(self.num):
		kan = self.myDic.kan[i]
                outfile.write(self.myDic.Kanji[kan].encode('u8')+'\t'+self.Transl[kan].get()+'\t'+self.myDic.ON_rom[kan]+'\t'+
				self.myDic.KUN_rom[kan]+'\t'+self.myDic.Sound[kan]+'\t'+self.myDic.ON[kan].encode('u8')+'\t'+
				self.myDic.KUN[kan].encode('u8')+'\t'+self.myDic.Transl[kan]+'\n')


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

