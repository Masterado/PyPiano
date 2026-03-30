# PyPiano
Piano built using Python taking sheet music turned into Excel sheet as input.
Uses pandas to store excel sheet as data that gets transformed into an audio object using simpleaudio.
Running the application opens a window that will prompt for the filename of an .xlsx file and a play button.



Sheet Format

Columns: Note, Time, Measure, V, Bpm, Upper, Lower

Note: Note and octave. Octaves are represented by an array and the number found in the excel sheet corrsponds to the index.  Currently the range of Aflat with a frequency of 220 through A Natural with a frequency of 3520 (notes["AF"][0]) through (notes["AN"][4]). Rests are represented by R0

Time: Note type (quarter, half etc.) Supported are Quarter, Half, Eight, Sixteenth, Thirtyseconds, and the dotted variants of each represented by. Q, H, E, S, T, Q-, H-, E-, S-, T-
Measure: Measure number (not used. Solely for readability and testing purposes)
Bpm: Beats per measure (used to calculate length in seconds of beats)
Upper: Upper half of time signature (currently not used)
Lower: Lower half of time signature (used to calculate length in seconds of beats)
V: Denotes volume. Values 0 or less are silent -1 is used to denote tied notes and 0 represents rests.


Current Samples
Shave and a haircut 2 bits
Under The Sea Beginning
We Are - One Piece

