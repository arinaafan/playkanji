import csv, sys, math, random, time, datetime
from Tkinter import *
from pygame import mixer
from PIL import ImageTk, Image
from dic import Dic, openSet, Set, play
from play2 import end_game

icon='/home/arina/tmp/play_sound3.gif'
path='/home/arina/kanji/'
scorefile = path + 'play3.topscore'
scorelines = csv.reader(open(scorefile, 'r'), delimiter='\t')

ii=0
sec=0
Score=0
hearts=0
playoption=''
timer_init=0
playlist={}
date_=datetime.date.today()
myDic = {}
keys = []


class Myframe(Frame):
  
    def __init__(self, parent, myDic, keys):
        Frame.__init__(self, parent)   
        
        self.parent = parent        
	self.kan0 = keys[0]
        self.parent.title("Playkanji")        
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, background='white')
        self.canvas.pack(fill=BOTH, expand=1)

        self.BGimg = Image.open(path + 'icons/back4.jpg')
        self.BGimg = self.BGimg.resize((420, 500),Image.ANTIALIAS)
        self.BGimg = ImageTk.PhotoImage(self.BGimg)

	self.chooseOpt()

    def chooseOpt(self):
        MODES = [
          ("Translation", "tr"),
          ("ON-reading", "on"),
          ("KUN-reading", "kun"),
        ]

        self.opt = StringVar()
	self.current_mode = 0
        self.opt.set("tr") # initialize

        height=60
	self.b = {}
        for text, mode in MODES:
          height+=30
          self.b[mode] = Radiobutton(self.canvas, text=text, font=("Arial", 16), variable=self.opt, value=mode, bg="white", activebackground="white", bd=0, highlightthickness=0)
          self.b[mode].place(relx=0.3, y=height, anchor="w")

	self.parent.bind('<Return>', self.start_game)
        self.button = Button(self.canvas, text="Start Game", font=("Arial", 16), fg='white', command=lambda k='<Return>': self.start_game(k), bg="grey", activebackground="green")
        self.button.place(relx=0.5, y=height+70, anchor="c")

    def start_game(self, event):
        global timer_init, playoption, playlist, mylist
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
	canBg = self.canvas.create_image(0, 0, image=self.BGimg, anchor='nw')

        self.img = Image.open(path + 'icons/back.jpeg')
        self.img = self.img.resize((420, 500),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)

        canBg = self.canvas.create_image(0, 0, image=self.img, anchor='nw')

	self.text1 = self.canvas.create_text(210, 75, font=("Purisa", 27, 'bold'), text=playlist[self.kan0])
	self.buttons = {}
	self.textL = {}
	for opt in range(5):
	  height=185+47*opt
	  self.buttons[opt] = Button(self.canvas, text = mylist[opt], font=("Purisa", 20), command = lambda k=opt: self.check(k), width=14, bg="white", activebackground="#DFECF2")
	  self.buttons[opt].place(x=210, y=height, anchor='c')
	  self.textL[opt] = self.canvas.create_text(80, height, text=str(opt+1), font=("Purisa", 15), anchor='c')
	# autoplay image
	self.img = Image.open(icon)
	resized = self.img.resize((40, 40),Image.ANTIALIAS)
	self.im = ImageTk.PhotoImage(resized)
	# autoplay button
	self.buttonS = Button(self.canvas, image=self.im, command=lambda k=ii: play(myDic.Sound[keys[k]]), relief=FLAT, bg='white', activebackground='white',highlightthickness=0,bd=0)
	self.buttonS.place(x=210, y=115,anchor='c')
	
	# Hearts
	self.heartL = {}
	for it in range(3):
	  self.heartL[it] = self.canvas.create_text(20+it*17,480, text=u"\u2665", font=('Purisa',16),fill='#DFECF2')

	# Print score
	self.printScore = self.canvas.create_text(70,480, text='Score: '+str(Score), font=('Purisa',14),fill='#778899',anchor=W)

	# Autoplay checkbox
        self.auto = IntVar()
        self.auto.set(1)
	self.ch = Checkbutton(self.canvas, text="Autoplay", font=('Arial',13), variable=self.auto, bg='white', highlightthickness=0, bd=0, activebackground='white')
	self.ch.place(x=310,y=472)

	# Timer
	self.canvas.create_oval(10,10,50,50,fill='#DFECF2',outline='white')
	self.timer_=self.canvas.create_arc(10,10,50,50,fill='#708090',start=0,extent=10,outline='#708090')
	self.timertext=self.canvas.create_text(30,30, text=u'\u6642', font=('Purisa',14,'bold'),fill='#DFECF2')
	self.run_timer()

    def check(self, num):
	global hearts, Score, ii
	if myDic.Kanji[keys[ii]] == mylist[num]:
	  hearts+=1
	  if hearts < 5: Score+=1
	  elif 5 <= hearts < 10: 
		Score+=3
		self.canvas.itemconfig(self.heartL[0], fill='#708090')
          elif 10 <= hearts < 15:
                Score+=3
                self.canvas.itemconfig(self.heartL[1], fill='#708090')
	  else: 
		Score+=6
		self.canvas.itemconfig(self.heartL[2], fill='#708090')
          self.buttons[num].configure(bg="green", activebackground="green")
	  if self.auto.get():
                try: play(myDic.Sound[keys[ii]])
                except: print('No sound file...')

	  self.after(1000, self.next_)
	  self.canvas.itemconfig(self.printScore, text='Score: '+str(Score))
	else:
	  hearts=0
	  for i in range(3):
		self.canvas.itemconfig(self.heartL[i], fill='#DFECF2')
	  self.buttons[num].configure(bg="red", activebackground="red")
	  jj=mylist.index(myDic.Kanji[keys[ii]])
	  self.buttons[jj].configure(bg="green", activebackground="green")
	  self.after(1000, self.next_)

    def next_(self):
	global ii, mylist, keys
        print ii, playlist[keys[ii]], mylist
	if ii == len(keys)-1: 
		ii=0
		keys = myDic.shuffled()
	else:
		ii+=1
        self.canvas.itemconfig(self.text1, text=playlist[keys[ii]])
	mylist=newlist(ii)
	for opt in range(5):
	  self.buttons[opt].configure(text=mylist[opt], bg='white', activebackground="#DFECF2")
	self.buttonS.configure(command=lambda k=ii: play(myDic.Sound[keys[k]]))

    def run_timer(self):
	global sec
	if timer_init: sec+=0.1
	self.canvas.itemconfig(self.timer_, extent=-sec*4)
	if sec > 90: end_game(self)
	self.after(100, self.run_timer)


def main():
    global root, myDic, keys
    root = Tk()
    chooseSet = openSet(root, Set)
    root.geometry("600x700+300+300")
    root.mainloop()
    myfile = chooseSet.myfile.get()
    print myfile
    infile = open(myfile, 'r')
    tsvfile = csv.reader(infile, delimiter='\t')
    myDic = Dic(tsvfile)
    keys = myDic.shuffled()
    root = Tk()
    frame = Myframe(root, myDic, keys)
    root.geometry("420x500+300+300")
    def defkey(event):
       if event.keysym in ['1','2','3','4','5']:
         jj=int(event.keysym)-1
         frame.check(jj)
       if event.keysym in ['KP_1','KP_2','KP_3','KP_4','KP_5']:
         jj=int(event.keysym[3])-1
         frame.check(jj)
       if event.keysym=='Up':
         frame.current_mode=(frame.current_mode-1)%3
         frame.opt.set(['tr','on','kun'][frame.current_mode])
       if event.keysym=='Down':
         frame.current_mode=(frame.current_mode+1)%3
         frame.opt.set(['tr','on','kun'][frame.current_mode])

    root.bind("<Key>", defkey)
    root.mainloop()

def newlist(ii):
    mylist = []
    mylist.append(myDic.Kanji[keys[ii]])
    shuffled=myDic.Kanji.values()[:]
    random.shuffle(shuffled)
    shuffled.remove(myDic.Kanji[keys[ii]])
    for i in range(0,4):
	mylist.append(shuffled[i])
    random.shuffle(mylist)
    return mylist

def end_game(fr):
    global root, playoption, Date, TopScore, Mode, date_
    fr.destroy()
    new_canvas = Canvas(root, background='white')
    new_canvas.create_text(210,125,font=("Purisa", 16, 'bold'), text='Score: '+str(Score) )
    buttonMore = Button(new_canvas, text = 'Play again!',
                                font=("Purisa", 16,'bold'),
                                command = start_over, width=10,
                                fg='white', bg='#41a6db', relief=GROOVE)
    buttonMore.place(x=210, y=400, anchor="c")

    TopScore.append(Score)
    TopScore.sort(reverse=True)
    Date[Score] = date_.strftime("%d/%m/%y")
    Mode[Score] = playoption

    for i in range(5):
	try:
	  score_ent = new_canvas.create_text(100,170+14*(i+1),font=("Purisa",12,'bold'),fill='dark blue', text=Date[TopScore[i]]+'\t'+str(TopScore[i])+'\t'+Mode[TopScore[i]], anchor=W )
	  if TopScore[i] == Score: new_canvas.itemconfig(score_ent, fill='black')
	except IndexError: pass
    new_canvas.pack(fill=BOTH, expand=1)
    mainloop()

    with open(scorefile, 'w') as outfile:
 	for i in range(len(TopScore)):
          outfile.write(Date[TopScore[i]]+'\t'+str(TopScore[i])+'\t'+Mode[TopScore[i]]+'\n')

def start_over():
   global root, ii, sec, Score, hearts, timer_init, date_
   root.destroy()
   ii=0
   sec=0
   Score=0
   hearts=0
   timer_init=1
   date_=datetime.date.today()
   main()

# Read top scores:
Date = {}
TopScore = []
Mode = {}
for lines in scorelines:
   score = int(lines[1])
   TopScore.append(score)
   Date[score] = lines[0]
   Mode[score] = lines[2]

if __name__ == '__main__':
    main() 

