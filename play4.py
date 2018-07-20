import csv, sys, math, random, time, datetime
from collections import namedtuple
from Tkinter import *
from pygame import mixer
from PIL import ImageTk, Image
from dic import Dic, play, openSet, Set

icon='/home/arina/tmp/play_sound3.gif'
icon1='/home/arina/kanji/icons/ninja1.png'
icon2='/home/arina/kanji/icons/ninja2.png'
icon3='/home/arina/kanji/icons/ninja3.png'
path='/home/arina/kanji/'
scorefile = path + 'play4.topscore'
scorelines = csv.reader(open(scorefile, 'r'), delimiter='\t')


ii=0
sec=0
Score=0
hearts=0
timer_init=1
playlist={}
date_=datetime.date.today()
c = {}
keys = []

class Myframe(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        
        self.parent = parent        
	self.kan0 = keys[0]
	print self.kan0
        self.parent.title("Playkanji")        
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, background='black')
        self.canvas.pack(fill=BOTH, expand=1)

	# Frame
	self.color = 'white'
	self.clockColor = RGB(20,200,5).hex_format()
	print(keys[0], playlist[keys[0]])
	self.text1 = self.canvas.create_text(210, 150, font=("Purisa", 45, 'bold'), text=keys[0], fill='white')
	self.text2 = self.canvas.create_text(210, 240, font=("Purisa", 20), text=playlist[keys[0]], width='8c', fill='white')
	play(myDic.Sound[keys[0]])	
	self.buttonTrue = Button(self.canvas, text = 'True', font=("Purisa", 16,'bold'),
				 command = lambda k=1: self.check(k), width=5, 
				 fg='white', bg='#41a6db', relief=GROOVE)
	self.buttonTrue.place(x=250, y=320, anchor="c")
	self.buttonFalse = Button(self.canvas, text='False', font=("Purisa", 16,'bold'),
				  command = lambda k=0: self.check(k), width=5, 
				  fg='white', bg='#41a6db', relief=GROOVE)
	self.buttonFalse.place(x=170, y=320, anchor="c")
	
	# Ninja
        self.im1 = Image.open(icon1)
        self.im1 = self.im1.resize((90, 70),Image.ANTIALIAS)
        self.im1 = ImageTk.PhotoImage(self.im1)
	self.ninja1 = self.canvas.create_image(140,450,image=self.im1,state=HIDDEN)
        self.im2 = Image.open(icon2)
        self.im2 = self.im2.resize((50, 70),Image.ANTIALIAS)
        self.im2 = ImageTk.PhotoImage(self.im2)
	self.ninja2= self.canvas.create_image(210,450,image=self.im2,state=HIDDEN)
        self.im3 = Image.open(icon3)
        self.im3 = self.im3.resize((85, 85),Image.ANTIALIAS)
        self.im3 = ImageTk.PhotoImage(self.im3)
	self.ninja3= self.canvas.create_image(275,450,image=self.im3,state=HIDDEN)

	# Print score
	self.printScore = self.canvas.create_text(160,390, text='Score: '+str(Score), font=('Purisa',16,'bold'),fill=self.color,anchor=W)

	# Timer
	self.canvas.create_oval(340,20,400,80,fill='#DFECF2',outline='white')
	self.timer_=self.canvas.create_arc(340,20,400,80,fill=self.clockColor,start=0,extent=10,outline=self.clockColor)
	self.timertext=self.canvas.create_text(370,50, text=u'\u6642', font=('Purisa',18,'bold'),fill='#DFECF2')
	self.run_timer()

    def check(self, num):
	global hearts, Score, ii
	if (playlist[keys[ii]] == myDic.Tr1[keys[ii]]) == num:
	  hearts+=1
	  if num == 1: self.buttonTrue["bg"] = 'green'
	  elif num == 0: self.buttonFalse["bg"] = 'green'
	  if hearts < 5: Score+=1
	  elif 5 <= hearts < 10: 
		Score+=3
		self.canvas.itemconfig(self.ninja1, state=NORMAL)
		self.color='#FFC300'
          elif 10 <= hearts < 15:
                Score+=3
		self.canvas.itemconfig(self.ninja2, state=NORMAL)
		self.color='#FF5733'
	  else: 
		Score+=6
		self.canvas.itemconfig(self.ninja3, state=NORMAL)
		self.color='#C70039'
	else:
	  hearts=0
	  if num == 1: self.buttonTrue["bg"] = 'red'
	  elif num == 0: self.buttonFalse["bg"] = 'red'
	  self.color='white'
	  self.canvas.itemconfig(self.ninja1, state=HIDDEN)
	  self.canvas.itemconfig(self.ninja2, state=HIDDEN)
	  self.canvas.itemconfig(self.ninja3, state=HIDDEN)

        self.canvas.itemconfig(self.printScore, text='Score: '+str(Score),
                               fill=self.color)
	self.after(800, self.next_)


    def next_(self):
	global ii, playlist, keys
        print ii, keys[ii], playlist[keys[ii]]
	if ii == len(keys)-1: 
		ii=0
		playlist, keys = newlist()
	else:
		ii+=1
        self.canvas.itemconfig(self.text1, text=keys[ii])
	self.canvas.itemconfig(self.text2, text=playlist[keys[ii]])	
	self.buttonTrue["background"] = '#41a6db'
	self.buttonFalse["background"] = '#41a6db'
	play(myDic.Sound[keys[ii]]) # !!!!

    def run_timer(self):
	global sec
	if timer_init: sec+=0.1
	tinge=int(sec)
	self.clockColor=RGB(20+tinge,200-tinge,5).hex_format()
	self.canvas.itemconfig(self.timer_, extent=-sec*2, fill=self.clockColor,
			       outline=self.clockColor)
	if sec > 180: end_game(self)
	self.after(100, self.run_timer)


def main():
    global root, myDic, keys, playlist
    root = Tk()
    chooseSet = openSet(root, Set)
    root.geometry("600x700+300+300")
    root.mainloop()
    myfile = chooseSet.myfile.get()
    print myfile
    infile = open(myfile, 'r')
    tsvfile = csv.reader(infile, delimiter='\t')
    myDic = Dic(tsvfile)
    playlist, keys = newlist()
    root = Tk()
    frame = Myframe(root)
    root.geometry("420x500+300+300")
    def defkey(event):
       if event.keysym=='Right': jj=1; frame.check(jj); 
       if event.keysym=='Left': jj=0; frame.check(jj); # frame.buttonFalse["background"]="blue"

    root.bind("<Key>", defkey)
    root.mainloop()

def newlist():
    keys = myDic.shuffled()
    newKeys = []
    newDic = {}
    for i in range(0,len(keys)/2):
	newKeys.append(keys[i])
	newDic[newKeys[i]] = myDic.Tr1[keys[i]]
    shuff = myDic.shuffled()
    for i in range(len(keys)/2,len(keys)):
	newKeys.append(keys[i])
        newDic[newKeys[i]] = myDic.Tr1[shuff[i]]
    random.shuffle(newKeys)
    print 'First: ', newDic[newKeys[0]], newKeys[0]
    return newDic, newKeys
	
def end_game(fr):
    global root, Date, TopScore, Mode, date_
    fr.destroy()
    new_canvas = Canvas(root, background='white')
    new_canvas.create_text(210,125,font=("Purisa", 16, 'bold'), text='Score: '+str(Score) )
    new_canvas.pack(fill=BOTH, expand=1)
    buttonMore = Button(new_canvas, text = 'Play again!',
                                font=("Purisa", 16,'bold'),
                                command = start_over, width=10,
                                fg='white', bg='#41a6db', relief=GROOVE)
    buttonMore.place(x=210, y=400, anchor="c")

    TopScore.append(Score)
    TopScore.sort(reverse=True)
    Date[Score] = date_.strftime("%d/%m/%y")

    for i in range(5):
	try:
	  score_ent = new_canvas.create_text(100,170+14*(i+1),font=("Purisa",12,'bold'),fill='dark blue', text=Date[TopScore[i]]+'\t\t'+str(TopScore[i]), anchor=W )
	  if TopScore[i] == Score: new_canvas.itemconfig(score_ent, fill='#900C3F')
	except IndexError: pass

    with open(scorefile, 'w') as outfile:
        for i in range(len(TopScore)):
          outfile.write(Date[TopScore[i]]+'\t'+str(TopScore[i])+'\n')

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

Color = namedtuple('RGB','red, green, blue')
class RGB(Color):
    def hex_format(self):
	'''Returns color in hex format'''
	return '#{:02X}{:02X}{:02X}'.format(self.red,self.green,self.blue)   

# Read top scores:
Date = {}
TopScore = []
for lines in scorelines:
   score = int(lines[1])
   TopScore.append(score)
   Date[score] = lines[0]

if __name__ == '__main__':
    main() 

