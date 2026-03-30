import numpy as np
import simpleaudio as sa
import sys
import pandas as pd
import re
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)
np.set_printoptions(threshold=sys.maxsize)
class Piano():
    def __init__(self, filename):
        self.filename=filename
        self.sheet=0
        self.audioO=0
        self.sample_rate=44100
        self.notes={
            "R": [0,0],
            "AF":(lambda x:440*2**((x*4/7)/12))( np.arange(-22,63,21)),
            "AN":(lambda x:440*2**((x*4/7)/12))( np.arange(-21,64,21)),
            "AS":(lambda x:440*2**((x*4/7)/12))( np.arange(-20,44,21)),
            "BF":(lambda x:440*2**((x*4/7)/12))( np.arange(-19,45,21)),
            "BN":(lambda x:440*2**((x*4/7)/12))( np.arange(-18,46,21)),
            "BS":(lambda x:440*2**((x*4/7)/12))( np.arange(-17,47,21)),
            "CF":(lambda x:440*2**((x*4/7)/12))( np.arange(-16,48,21)),
            "CN":(lambda x:440*2**((x*4/7)/12))( np.arange(-15,49,21)),
            "CS":(lambda x:440*2**((x*4/7)/12))( np.arange(-14,50,21)),
            "DF":(lambda x:440*2**((x*4/7)/12))( np.arange(-13,51,21)),
            "DN":(lambda x:440*2**((x*4/7)/12))( np.arange(-12,52,21)),
            "DS":(lambda x:440*2**((x*4/7)/12))( np.arange(-11,53,21)),
            "EF":(lambda x:440*2**((x*4/7)/12))( np.arange(-10,54,21)),
            "EN":(lambda x:440*2**((x*4/7)/12))( np.arange(-9,55,21)),
            "ES":(lambda x:440*2**((x*4/7)/12))( np.arange(-8,56,21)),
            "FF":(lambda x:440*2**((x*4/7)/12))( np.arange(-7,57,21)),
            "FN":(lambda x:440*2**((x*4/7)/12))( np.arange(-6,58,21)),
            "FS":(lambda x:440*2**((x*4/7)/12))( np.arange(-5,59,21)),
            "GF":(lambda x:440*2**((x*4/7)/12))( np.arange(-4,60,21)),
            "GN":(lambda x:440*2**((x*4/7)/12))( np.arange(-3,61,21)),
            "GS":(lambda x:440*2**((x*4/7)/12))( np.arange(-2,62,21))

        }

        self.ntime={
            "Q":4,
            "H":2,
            "W":1,
            "E":8,
            "T":32,
            "S":16,
            "Q-":4/1.5,
            "H-":2/1.5,
            "W-":1/1.5,
            "E-":8/1.5,
            "T-":32/1.5,
            "S-":16/1.5,
            #pause before a new note
           # "P":8
        }

    def sheetgen(self):
        #replace with file name
        self.sheet=pd.read_excel(self.filename)


     
        

  
        #add length and start of beat to table
        ltime=list(map((lambda x: self.sheet.at[x,"Lower"]/self.ntime[self.sheet.at[x,"Time"]]),self.sheet.index))
        beatstart=list(map((lambda a:lambda v:a(a,v))(lambda s,x:0 if x==0 else ltime[x-1]+s(s,x-1)),self.sheet.index))
        self.sheet.insert(len(self.sheet.columns),"ltime",ltime) 
        self.sheet.insert(len(self.sheet.columns),"beatstart",beatstart)

        #add end of beat to table
        beatend=list(map((lambda x: beatstart[x]+ltime[x] if x==self.sheet.index.max() else beatstart[x+1] if self.sheet.at[x+1,"V"]<=0 else beatstart[x+1] - ( (self.sheet.at[x,"Lower"]/self.ntime[self.sheet.at[x,"Time"]])*0.1    )   ),self.sheet.index))
        self.sheet.insert(len(self.sheet.columns),"beatend",beatend)

        tcounter=list(map((lambda x: beatstart[x]/(self.sheet.at[x,"Bpm"]/60) ),self.sheet.index))
        self.sheet.insert(len(self.sheet.columns),"tcounter",tcounter)

        #converts beats into seconds
        #newt=list(map((lambda x: np.linspace(beatstart[x]/(self.sheet.at[x,"Bpm"]/60) ,beatend[x]/(self.sheet.at[x,"Bpm"]/60) ,int(self.sample_rate*(  (beatend[x]-beatstart[x])/(self.sheet.at[x,"Bpm"]/60) ) )) ) ,self.sheet.index))
        
        print(self.sheet)
        #return sheet


    def audgen(self):
        # convert self.sheet[self.self.notes]=xy into note[x][y] format
        newt=list(map((lambda x: np.linspace(self.sheet.at[x,"beatstart"]/(self.sheet.at[x,"Bpm"]/60),self.sheet.at[x,"beatend"]/(self.sheet.at[x,"Bpm"]/60) ,int(self.sample_rate*(  (self.sheet.at[x,"beatend"]-self.sheet.at[x,"beatstart"])/(self.sheet.at[x,"Bpm"]/60) ) )) ) ,self.sheet.index))

        noteconv=  list(map((lambda x: re.split(r'(\d)',self.sheet.at[x,"Note"])),self.sheet.index))
        Aud= list(map((lambda x: self.notes[noteconv[x][0]][int(noteconv[x][1])] ),self.sheet.index))

        #generate sine wave self.self.notes
        A2=list(map((lambda x: np.sin(Aud[x]*newt[x]*2*np.pi) ),self.sheet.index))

        # normalize to 16-bit range
        a22=np.hstack(A2)
        a22 *= 32767 / np.max(np.abs(a22))

        # convert to 16-bit data
        a22 = a22.astype(np.int16)
        self.audioO=a22

    def play(self):
        
       play_obj = sa.play_buffer(self.audioO, 1, 2, self.sample_rate)

       play_obj.wait_done()
       
       

#P=Piano("UTS.xlsx")
#P.sheetgen()
#P.audgen()
#P.play()
