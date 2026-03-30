import numpy as np
import simpleaudio as sa
import sys
import pandas as pd
import re
notes={
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

ntime={
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
    "P":64
}

#replace with file name
sheet=pd.read_excel("WA.xlsx")


sample_rate = 44100
np.set_printoptions(threshold=sys.maxsize)

  
#add length and start of beat to table
ltime=list(map((lambda x: sheet.at[x,"Lower"]/ntime[sheet.at[x,"Time"]]),sheet.index))
beatstart=list(map((lambda a:lambda v:a(a,v))(lambda s,x:0 if x==0 else ltime[x-1]+s(s,x-1)),sheet.index))
sheet.insert(len(sheet.columns),"ltime",ltime) 
sheet.insert(len(sheet.columns),"beatstart",beatstart)

#add end of beat to table
beatend=list(map((lambda x: beatstart[x]+ltime[x] if x==sheet.index.max() else beatstart[x+1] if sheet.at[x+1,"V"]<=0 else beatstart[x+1] - 1/ntime["P"]),sheet.index))
sheet.insert(len(sheet.columns),"beatend",beatend)

#tcounter=list(map((lambda x: beatstart[x]/(sheet.at[x,"Bpm"]/60) ),sheet.index))
#sheet.insert(len(sheet.columns),"tcounter",tcounter)

#converts beats into seconds
newt=list(map((lambda x: np.linspace(beatstart[x]/(sheet.at[x,"Bpm"]/60) ,beatend[x]/(sheet.at[x,"Bpm"]/60) ,int(sample_rate*(     (beatend[x]-beatstart[x])/(sheet.at[x,"Bpm"]/60)            )   )) ) ,sheet.index))


print(sheet)



# convert sheet[Notes]=xy into note[x][y] format
noteconv=  list(map((lambda x: re.split(r'(\d)',sheet.at[x,"Note"])),sheet.index))
Aud= list(map((lambda x: notes[noteconv[x][0]][int(noteconv[x][1])] ),sheet.index))


#generate sine wave notes
A2=list(map((lambda x: np.sin(Aud[x]*newt[x]*2*np.pi) ),sheet.index))





# normalize to 16-bit range
a22=np.hstack(A2)
a22 *= 32767 / np.max(np.abs(a22))

# convert to 16-bit data
a22 = a22.astype(np.int16)


play_obj = sa.play_buffer(a22, 1, 2, sample_rate)

play_obj.wait_done()
