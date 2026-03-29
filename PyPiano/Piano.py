import numpy as np
import simpleaudio as sa
import sys
import pandas as pd
import re
notes={
    "R": [0,0],
    "AF":(lambda x:440*2**((x*4/7)/12))( np.arange(-22,42,21)),
    "AN":(lambda x:440*2**((x*4/7)/12))( np.arange(-21,43,21)),
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
    "S":16
}

# calculate note frequencies
A_freq = 440
Csh_freq = A_freq * 2 ** (4 / 12)
E_freq = A_freq * 2 ** (7 / 12)


sheet=pd.read_excel("UTS.xlsx")
#print(sheet)

# get timesteps for each sample, T is note duration in seconds
sample_rate = 44100
#bpm  
T = 0.25
t = np.linspace(0, T, int(T * sample_rate), False)
np.set_printoptions(threshold=sys.maxsize)

  
# For each row use t=np.linspace to create sample starting from beat to beat end. coverted to seconds using    beatstart,beat+beattime,(lower/time)*(bpm/60)
#For each row add beat counter. Start at 0. Set beat to ltime[-1] + beat[-1]
#insert row before every row where v>0. Note = R, Time = SH2B

#print(sheet.index)
#print(sheet.columns)
#r=sheet.at[0,"Time"]
#lambda x: sheet.at[x-1,"Lower"]/sheet.at[x-1,"Time"] (sheet.Index)
ltime=list(map((lambda x: sheet.at[x,"Lower"]/ntime[sheet.at[x,"Time"]]),sheet.index))
#print(ltime)
beatstart=list(map((lambda a:lambda v:a(a,v))(lambda s,x:0 if x==0 else ltime[x-1]+s(s,x-1)),sheet.index))

#beats=list(map((lambda a:lambda v:a(a,v))(lambda s,x:0 if x==0 else sheet.at[x-1,"Lower"]/ntime[sheet.at[x-1,"Time"]]+s(s,x-1)),sheet.index))
#print(sheet.loc[sheet["V"] > 0])
sheet.insert(len(sheet.columns),"ltime",ltime) 
sheet.insert(len(sheet.columns),"beatstart",beatstart)

beatend=list(map((lambda x: beatstart[x]+ltime[x] if x==sheet.index.max() else beatstart[x+1] if sheet.at[x+1,"V"]<=0 else beatstart[x+1] - 1/64),sheet.index))
sheet.insert(len(sheet.columns),"beatend",beatend)
tcounter=list(map((lambda x: beatstart[x]/(sheet.at[x,"Bpm"]/60) ),sheet.index))
newt=list(map((lambda x: np.linspace(beatstart[x]/(sheet.at[x,"Bpm"]/60) ,beatend[x]/(sheet.at[x,"Bpm"]/60) ,int(sample_rate*(     (beatend[x]-beatstart[x])/(sheet.at[x,"Bpm"]/60)            )   )) ) ,sheet.index))
sheet.insert(len(sheet.columns),"tcounter",tcounter)
#print(newt)

print(sheet)
# generate sine wave notes
#A_note = np.sin(A_freq * t * 2 * np.pi)
#Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
#E_note = np.sin(E_freq * t * 2 * np.pi)
A_note = np.sin(notes["AN"][2]*t*2*np.pi)
Csh_note = np.sin(notes["CS"][2]*t*2*np.pi)
E_note = np.sin(notes["EN"][2] *t*2*np.pi)
noteconv=  list(map((lambda x: re.split(r'(\d)',sheet.at[x,"Note"])),sheet.index))
a=noteconv[0][0]
b=noteconv[0][1]
#print(b)
#print(notes[a][int(b)])
Aud= list(map((lambda x: notes[noteconv[x][0]][int(noteconv[x][1])] ),sheet.index))
A2=list(map((lambda x: np.sin(Aud[x]*newt[x]*2*np.pi) ),sheet.index))
#print(A2)
#print(A_note)

# concatenate notes
audio = np.hstack((A_note, Csh_note, E_note))
a22=np.hstack(A2)
#print(audio)
# normalize to 16-bit range
audio *= 32767 / np.max(np.abs(audio))
a22 *= 32767 / np.max(np.abs(a22))
# convert to 16-bit data
audio = audio.astype(np.int16)
a22 = a22.astype(np.int16)
# start playback
#play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

# wait for playback to finish before exiting
#play_obj.wait_done()


play_obj = sa.play_buffer(a22, 1, 2, sample_rate)

# wait for playback to finish before exiting
play_obj.wait_done()