import csv, sys, math, random, time
from Tkinter import *
from pygame import mixer
from PIL import ImageTk, Image
from dic import Dic


icon='/home/arina/tmp/play_sound3.gif'
path='/home/arina/kanji/'
filename = str(sys.argv[1])

## open file
infile = open(filename, 'r')

## define csv reader object, assuming delimiter is tab
tsvfile = csv.reader(infile, delimiter='\t')

ii=0
sec=0
Score=0
hearts=0
playoption=''
timer_init=0
playlist={}

class Myframe(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        
        self.parent = parent        
	self.kan0 = keys[0]
        self.parent.title("Playkanji")        
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, background='white')
        self.canvas.pack(fill=BOTH, expand=1)
	self.chooseOpt()

    def chooseOpt(self):
        MODES = [
          ("Translation", "tr"),
          ("ON-reading", "on"),
          ("KUN-reading", "kun"),
        ]

        self.opt = StringVar()
        self.opt.set("tr") # initialize

        height=60
	self.b = {}
        for text, mode in MODES:
          height+=30
          self.b[mode] = Radiobutton(self.canvas, text=text, font=("Arial", 16), variable=self.opt, value=mode,
                        bg="white", activebackground="white", bd=0,
                        highlightthickness=0)
          self.b[mode].place(relx=0.5, y=height, anchor="c")

        self.button = Button(self.canvas, text="Start Game", font=("Arial", 16), fg='white', command=self.start_game,
                        bg="grey", activebackground="green")
        self.button.place(relx=0.5, y=height+70, anchor="c")

    def start_game(self):
        global timer_init, playoption, playlist, mylist, myDic
	playoption = self.opt.get()
        if playoption == 'tr': playlist = myDic.Tr1
        if playoption == 'on': playlist = myDic.ON
        if playoption == 'kun': playlist = myDic.KUN
        mylist=newlist(ii)
	for opt in ['tr','on','kun']: self.b[opt].destroy()
	self.button.destroy()
	self.initGame()
        timer_init = 1

    def initGame(self):
	self.text1 = self.canvas.create_text(100, 120, font=("Purisa", 60, 'bold'), text=myDic.Kanji[self.kan0])
	self.buttons = {}
	self.textL = {}
	for opt in range(5):
	  height=50+30*opt
	  self.buttons[opt] = Button(self.canvas, text = mylist[opt], font=("Purisa"), command = lambda k=opt: self.check(k), width=15, bg="white", activebackground="#DFECF2")
	  self.buttons[opt].place(x=210, y=height)
	  self.textL[opt] = self.canvas.create_text(385, height+20, text=str(opt+1), font=("Purisa"))
	# autoplay image
	self.img = Image.open(icon)
	resized = self.img.resize((40, 40),Image.ANTIALIAS)
	self.im = ImageTk.PhotoImage(resized)
	# autoplay button
	self.buttonS = Button(self.canvas, image=self.im, command=lambda k=ii: play(myDic.Sound[keys[k]]), relief=FLAT, bg='white', activebackground='white',highlightthickness=0,bd=0)
	self.buttonS.place(x=80, y=165)
	
	# Hearts
	self.heartL = {}
	for it in range(3):
	  self.heartL[it] = self.canvas.create_text(90+it*19,280, text=u"\u2665", font=('Purisa',18),fill='#DFECF2')

	# Autoplay checkbox
        self.auto = IntVar()
        self.auto.set(1)
	self.ch = Checkbutton(self.canvas, text="Autoplay", variable=self.auto, bg='white', highlightthickness=0, bd=0, activebackground='white')
	self.ch.place(x=310,y=275)

	# Timer
	self.canvas.create_oval(15,265,45,295,fill='#DFECF2',outline='white')
	self.timer_=self.canvas.create_arc(15,265,45,295,fill='green',start=0,extent=10,outline='green')
	self.run_timer()

    def check(self, num):
	global hearts, Score, ii
	if playlist[keys[ii]] == mylist[num]:
	  hearts+=1
	  if hearts < 5: Score+=1
	  elif 5 <= hearts < 10: 
		Score+=3
		self.canvas.itemconfig(self.heartL[0], fill='#990000')
          elif 10 <= hearts < 15:
                Score+=3
                self.canvas.itemconfig(self.heartL[1], fill='#990000')
	  else: 
		Score+=6
		self.canvas.itemconfig(self.heartL[2], fill='#990000')
          self.buttons[num].configure(bg="green", activebackground="green")
	  if self.auto.get(): play(myDic.Sound[keys[ii]]) 
	  self.after(1000, self.next_)
	else:
	  hearts=0
	  for i in range(3):
		self.canvas.itemconfig(self.heartL[i], fill='#DFECF2')
	  self.buttons[num].configure(bg="red", activebackground="red")
	  jj=mylist.index(playlist[keys[ii]])
	  self.buttons[jj].configure(bg="green", activebackground="green")
	  self.after(1000, self.next_)

    def next_(self):
	global ii, mylist
	ii+=1
        self.canvas.itemconfig(self.text1, text=myDic.Kanji[keys[ii]])
	mylist=newlist(ii)
	for opt in range(5):
	  self.buttons[opt].configure(text=mylist[opt], bg='white', activebackground="#DFECF2")
	self.buttonS.configure(command=lambda k=ii: play(myDic.Sound[keys[k]]))
	print myDic.Kanji[keys[ii]], mylist

    def run_timer(self):
	global sec
	if timer_init: sec+=0.1
	self.canvas.itemconfig(self.timer_, extent=-sec*2)
	if sec > 180: end_game(self)
	self.after(100, self.run_timer)


def main():
    global root
    root = Tk()
    frame = Myframe(root)
    root.geometry("420x300+300+300")
    def defkey(event):
       if event.keysym in ['1','2','3','4','5']:
         jj=int(event.keysym)-1
         frame.check(jj)
       if event.keysym in ['KP_1','KP_2','KP_3','KP_4','KP_5']:
         jj=int(event.keysym[3])-1
         frame.check(jj)

    root.bind("<Key>", defkey)
    root.mainloop()

def newlist(ii):
    mylist = []
    mylist.append(playlist[keys[ii]])
    shuffled=playlist.values()[:]
    random.shuffle(shuffled)
    shuffled.remove(playlist[keys[ii]])
    for i in range(0,4):
	mylist.append(shuffled[i])
    random.shuffle(mylist)
    return mylist

def play(sound):

    mixer.init()
    mixer.music.load(path + sound)
    mixer.music.play()

def end_game(fr):
    global root
    fr.destroy()
    new_canvas = Canvas(root, background='white')
    new_canvas.create_text(210,125,font=("Purisa", 16, 'bold'), text='Score: '+str(Score) )
    new_canvas.pack(fill=BOTH, expand=1)
    mainloop()

myDic = Dic(tsvfile)
keys = myDic.shuffled()
# print kanji[ii], mylist

if __name__ == '__main__':
    main() 

