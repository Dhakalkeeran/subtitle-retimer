'''
usage: subtitle.py [-h] -i INPUT -o OUTPUT -s DELAY [-m INCLINED]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to the input file
  -o OUTPUT, --output OUTPUT
                        path to the output file
  -s DELAY, --delay DELAY
                        delay in seconds
  -m INCLINED, --inclined INCLINED
                        inclined delay in milliseconds, slope
'''

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required = True, help = "path to the input file")
parser.add_argument("-o", "--output", required = True, help = "path to the output file")
parser.add_argument("-s", "--delay", required = True, help = "delay in seconds")
parser.add_argument("-m", "--inclined", help = "inclined delay in milliseconds, slope")
args = vars(parser.parse_args())

filepath = args["input"]
delay_in_seconds = float(args["delay"]) #time to delay the subtitles(in seconds); fixed delay
inclined_delay = args["inclined"] #inclined time to delay the subtitles per second (generally in milliseconds) i.e. slope; variable delay
new_filepath = args["output"]

#checking if inclined_delay is provided as argument or not, if not initializing it to zero
if (inclined_delay == None):
    inclined_delay = 0
else:
    inclined_delay = float(inclined_delay)

lines_array = []
count = 0
quotient = 0
#print(type(lines_array))

with open(filepath, "r+") as sub_file: #opening the original subtitle file for reading the contents in it
    for line in sub_file:
        line = line.rstrip() #stripping the whitespace or newline at the end of the string
        lines_array.append(line) #appending the lines in an empty array

for i in range(int(len(lines_array)/4) + 1): #the subtitle file contains at least 4 lines for a single subtitle, so dividing by 4; adding 1 is for ceiling number purpose i.e. ceil()
    for j in range(len(lines_array)): #looping through the elements of the list
        if str(i) == lines_array[j]: #matching the numbers in the subtitle file to extract the next line containing time transitions of subtitle
            x = lines_array[j+1] #extracting the time transition in a variable 
            split = x.split("-->") #splitting time transitions joined by "-->" into two time points
            #print(split)
            split_copy = []
            
            for sp in split: #looping through the time points splitted from time transitions
                sp = sp.split(":") #splitting time point joined by ":" into hours, minutes and seconds
                #print(sp[1])
                sp_copy = []     
                
                for spl in sp: #looping through the time hands i.e. hours, minutes, seconds of a time point
                    spl = spl.split(",") #splitting second point joined by "," into seconds and milliseconds
                    count += 1
                    
                    if count == 3: #3rd count leads us to the seconds portion, 1st count is the hours hand and 2nd count is the minutes hand
                        #print(str(int(spl[0]) + 6))
                        float_delay = delay_in_seconds - int(delay_in_seconds) #float_delay is the fixed delay value after decimal in seconds 
                        spl[1] = str(int(spl[1]) + int(float_delay * 1000) + int(inclined_delay * (int(sp_copy[0])*3600 + int(sp_copy[1])*60 + int(spl[0])))) #inclined delay or slope
                        if int(spl[1]) >= 1000: #condition for milliseconds going above 1000; spl[1] is the milliseconds hand
                            quotient = int(int(spl[1]) / 1000) 
                            spl[1] = str(int(spl[1]) % 1000)
                            spl[0] = str(int(spl[0]) + quotient) #adding quotient into the seconds hand, spl[0] is the seconds hand
                            
                        if len(spl[1]) <= 2: #fixing the length of string for single and two digits milliseconds value
                            spl[1] = (3 - len(spl[1])) * "0" + spl[1]
                            
                        spl[0] = str(int(spl[0]) + int(delay_in_seconds)) #fixed delay in seconds before decimal
                        
                        if int(spl[0]) >= 60: #checking for seconds exceeding 60
                            #print("greater than 60")
                            quotient = int(int(spl[0]) / 60)
                            spl[0] = str(int(spl[0]) % 60)
                            #print(spl[0])
                            #print(quotient)
                        else:
                            quotient = 0
                        count = 0
                        
                        if len(spl[0]) == 1: #fixing the length of seconds value
                            spl[0] = "0" + spl[0]
                        #print(spl)
                        spl = [",".join(spl)] #joining the seconds and milliseconds values with ","
                        
                        sp_copy[1] = str(int(sp_copy[1]) + quotient) #sp_copy[1] is the minutes hand since hours and minutes values are appended in the list i.e. sp_copy
                        if len(sp_copy[1]) == 1: #fixing the length of the minutes value
                            sp_copy[1] = "0" + sp_copy[1]
                            
                        if int(sp_copy[1]) >= 60: #checking for minutes exceeding 60
                            quotient = int(int(sp_copy[1]) / 60)
                            sp_copy[1] = str(int(sp_copy[1]) % 60)
                            sp_copy[0] = str(int(sp_copy[0]) + quotient)
                            
                        if len(sp_copy[0]) == 1: #fixing the length of hours value
                            sp_copy[0] = "0" + sp_copy[0]
                            
                    sp_copy.append(spl[0]) #appending the time hands i.e. hours, minutes and seconds values into a list
                #print(sp_copy)
                sp = [":".join(sp_copy)] #joining the list containing time hands with ":"
                #print(sp)
                split_copy.append(sp[0]) #appending the time points into a list        
                
            split = "-->".join(split_copy) #joining the time points with "-->"
            #print(split)
            lines_array[j+1] = split #placing the modified time frame in place of the original time frame
            #print(lines_array[j+1])
            #print(x)            
            
#print(lines_array)
lines_array = "\n".join(lines_array) #joining the elements of the list using newline character

with open(new_filepath, "w+") as sub_file: #saving the contents of the array into a file
    sub_file.write(lines_array)
    