import csv, sys, math, random
from Tkinter import *
from pygame import mixer
from PIL import ImageTk, Image


path='/home/arina/kanji/'
icon = path + 'icons/play_sound3.gif'

Kanji_set = [
        'kanji_1001_read.tab', 
        'kanji_1002_1_read.tab',
        'kanji_1002_2_read.tab',
        'kanji_1003_1_read.tab',
        'kanji_1003_2_read.tab',
        'kanji_1004_1_read.tab',
        'kanji_1004_2_read.tab',
        'kanji_1005_1_read.tab',
        'kanji_1005_2_read.tab',
        'kanji_1006_1_read.tab',
        'kanji_1006_2_read.tab',
	'verbs_JLPT5.tab',
	'new_List.tab'
]

Set = {
	'kanji_1001_read.tab': 'images00.jpeg',
	'kanji_1002_1_read.tab': 'images0.jpeg',
	'kanji_1002_2_read.tab': 'index1.jpeg',
	'kanji_1003_1_read.tab': 'images4.jpeg',
	'kanji_1003_2_read.tab': 'images6.jpeg',
        'kanji_1004_1_read.tab': 'imagestw3_1.jpeg',
        'kanji_1004_2_read.tab': 'imagestw3_2.jpeg',
        'kanji_1005_1_read.tab': 'imagestw1_2.jpeg',
        'kanji_1005_2_read.tab': 'imagestw1_1.jpeg',
        'kanji_1006_1_read.tab': 'imagestw2_1.jpeg',
        'kanji_1006_2_read.tab': 'imagestw2_2.jpeg',
	'verbs_JLPT5.tab': 'verbs1.png',
	'new_List.tab': 'vintage-hand-new-words.png'
}

Set_name = {
	'kanji_1001_read.tab': 'Baby level',
        'kanji_1002_1_read.tab': 'Elementary 1',
        'kanji_1002_2_read.tab': 'Elementary 2',
        'kanji_1003_1_read.tab': 'Primary 1', 
        'kanji_1003_2_read.tab': 'Primary 2',
        'kanji_1004_1_read.tab': 'Intermediate 1',
        'kanji_1004_2_read.tab': 'Intermediate 2',
        'kanji_1005_1_read.tab': 'Junior 1',
        'kanji_1005_2_read.tab': 'Junior 2',
        'kanji_1006_1_read.tab': 'Senior 1',
        'kanji_1006_2_read.tab': 'Senior 2',
	'verbs_JLPT5.tab': 'Verbs JLPT5',
	'new_List.tab': 'New words'
}

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

class openSet(Frame):

    def __init__(self, parent, Set):
        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title("Playkanji_tab")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self, background='white')
        self.canvas.pack(fill=BOTH, expand=1)

	self.text = self.canvas.create_text(300, 50, font=("Purisa", 20, 'bold'), text="Please choose set for training", )

	i=1; j=1; ii=0
	self.button = {}
	self.icon = {}
	file_ = {}
	self.myfile = StringVar()
	self.myfile.set("")
	for myset in Kanji_set:
	  ii=ii+1
	  j=j%4+1
	  i=ii/4+1
	  self.img = Image.open('icons/' + Set[myset])
          resized = self.img.resize((60, 80),Image.ANTIALIAS)
          self.icon[ii] = ImageTk.PhotoImage(resized)
          file_[ii]= path + 'tabs/' + myset
          self.button[ii] = Button(self.canvas, compound=TOP, image=self.icon[ii], bg="white", text=Set_name[myset], command=lambda k=file_[ii]: self.openset(k))
	  self.button[ii].configure(width=70)
	  self.button[ii].place(x=50+j*100, y=50+i*120, anchor="c")
	  print i,j,Set_name[myset], Set[myset], file_[ii]

    def openset(self, file_):
	self.myfile.set(file_)
        print 'you are going to open kanji set ==> ', file_
        self.parent.destroy()
	

class Table(Frame):

    def __init__(self, parent, myDic, num, myfile):
        Frame.__init__(self, parent)   
 
	self.myDic = myDic
	self.num = num
	self.myfile = myfile
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
	print 'File ', self.myfile, ' was saved'
	with open(self.myfile, 'w') as outfile:
	  for i in range(self.num):
		kan = self.myDic.kan[i]
                outfile.write(self.myDic.Kanji[kan].encode('u8')+'\t'+self.Transl[kan].get()+'\t'+self.myDic.ON_rom[kan]+'\t'+
				self.myDic.KUN_rom[kan]+'\t'+self.myDic.Sound[kan]+'\t'+self.myDic.ON[kan].encode('u8')+'\t'+
				self.myDic.KUN[kan].encode('u8')+'\t'+self.myDic.Transl[kan]+'\n')

def play(sound):
    mixer.init()
    mixer.music.load(path + sound)
    mixer.music.play()
    print sound


def main():
  
    root = Tk()
    chooseSet = openSet(root, Set)
    root.geometry("600x700+300+300")
    root.mainloop()
    myfile = chooseSet.myfile.get()
    print myfile
    infile = open(myfile, 'r')
    tsvfile = csv.reader(infile, delimiter='\t')
    myDic = Dic(tsvfile)
    num = len(myDic.kan)
    root = Tk()
    mytab = Table(root, myDic, num, myfile)
    root.geometry("600x500+300+300")
    root.mainloop()


if __name__ == '__main__':
    main() 

