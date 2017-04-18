import csv, sys, math, random, time, datetime
from Tkinter import *
from pygame import mixer
from PIL import ImageTk, Image
from dic import Dic


icon='/home/arina/tmp/play_sound3.gif'
path='/home/arina/kanji/'
filename = str(sys.argv[1])
scorefile = str(sys.argv[2])

## open file
infile = open(filename, 'r')

## define csv reader object, assuming delimiter is tab
tsvfile = csv.reader(infile, delimiter='\t')
scorelines = csv.reader(open(scorefile, 'r'), delimiter='\t')

ii=0
sec=0
Score=0
hearts=0
timer_init=1
playlist={}
date_=datetime.date.today()

class Myframe(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        
        self.parent = parent        
	self.kan0 = keys[0]
        self.parent.title("Playkanji")        
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, background='white')
        self.canvas.pack(fill=BOTH, expand=1)
	playlist = newlist()
	print 'Check: ', playlist.keys()[0], playlist.values()[0]

	# Frame
	self.color = 'red'
	self.canvas.create_rectangle(80,130,340,350, outline="grey")
#	self.canvas.create_arc(80,70,140,190, start=90, extent=90, outline=self.color, fill=self.color)
	self.canvas.create_rectangle(80,70,340,130, outline=self.color, fill=self.color)
#	self.canvas.create_arc(280,70,340,190, start=0, extent=90, outline=self.color, fill=self.color)
	self.text1 = self.canvas.create_text(210, 200, font=("Purisa", 35, 'bold'), text=playlist.keys()[0])
	self.text2 = self.canvas.create_text(210, 250, font=("Purisa", 20), text=playlist.values()[0])
	self.buttonTrue = Button(self.canvas, text = 'True', font=("Purisa", 16,'bold'), command = lambda k=1: self.check(k), width=5, bg="green", activebackground="#DFECF2")
	self.buttonTrue.place(x=250, y=300, anchor="c")
	self.buttonFalse = Button(self.canvas, text='False', font=("Purisa", 16,'bold'), command = lambda k=0: self.check(k), width=5, bg="red", activebackground="#DFECF2")
	self.buttonFalse.place(x=170, y=300, anchor="c")
	
	# Hearts
	self.heartL = {}
	for it in range(3):
	  self.heartL[it] = self.canvas.create_text(20+it*17,400, text=u"\u2665", font=('Purisa',16),fill='#DFECF2')

	# Print score
	self.printScore = self.canvas.create_text(70,400, text='Score: '+str(Score), font=('Purisa',14),fill='#778899',anchor=W)

	# Timer
	self.canvas.create_oval(10,10,50,50,fill='#DFECF2',outline='white')
	self.timer_=self.canvas.create_arc(10,10,50,50,fill='#708090',start=0,extent=10,outline='#708090')
	self.timertext=self.canvas.create_text(30,30, text=u'\u6642', font=('Purisa',14,'bold'),fill='#DFECF2')
	self.run_timer()

    def check(self, num):
	global hearts, Score, ii
	if (playlist.values()[ii] == myDic.Tr1[playlist.keys()[ii]]) == num:
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
	  self.after(1000, self.next_)
	  self.canvas.itemconfig(self.printScore, text='Score: '+str(Score))
	else:
	  hearts=0
	  for i in range(3):
		self.canvas.itemconfig(self.heartL[i], fill='#DFECF2')
	  self.after(1000, self.next_)

    def next_(self):
	global ii, playlist, keys
        print ii, playlist.keys()[ii], playlist.values()[ii]
	if ii == len(keys)-1: 
		ii=0
		playlist = newlist()
	else:
		ii+=1
        self.canvas.itemconfig(self.text1, text=playlist.keys()[ii])
	self.canvas.itemconfig(self.text2, text=playlist.values()[ii])	
	self.buttonTrue["background"] = 'green'
	self.buttonFalse["background"] = 'red'

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
    root.geometry("420x500+300+300")
    def defkey(event):
       if event.keysym=='Right': jj=1; frame.check(jj); frame.buttonTrue["background"]="grey"
       if event.keysym=='Left': jj=0; frame.check(jj); frame.buttonFalse["background"]="grey"

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
    return newDic
	

def play(sound):
    mixer.init()
    mixer.music.load(path + sound)
    mixer.music.play()

def end_game(fr):
    global root, playoption, Date, TopScore, Mode, date_
    fr.destroy()
    new_canvas = Canvas(root, background='white')
    new_canvas.create_text(210,125,font=("Purisa", 16, 'bold'), text='Score: '+str(Score) )
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

    

myDic = Dic(tsvfile)
keys = myDic.shuffled()
playlist = newlist()
# print kanji[ii], mylist

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

