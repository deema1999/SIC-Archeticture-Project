'''
SIC Architecture (Pass1).

Authors:
    Deema Hafez <161064@ppu.edu.ps>
    Dumooa Asafrah <161025@ppu.edu.ps>

File description:
    This file contains the logic to procces pass 1 in SIC architecture code with letrals.

'''
from tkinter import *
from tkinter import filedialog
import traceback
import tkinter.messagebox
import os
root = Tk()

#identify some global variables
symbol_table = {}
ProgrameLen = 0
optabel = {
        "ADD":"18",
        "AND":"40",
        "COMP":"28",
        "DIV":"24",
        "J":"3C",
        "JEQ":"30",
        "JGT":"34",
        "JLT":"38",
        "JSUB":"48",
        "LDA":"00",
        "LDCH":"50",
        "LDL":"08",
        "LDX":"04",
        "MUL":"20",
        "OR":"44",
        "RD":"D8",
        "RSUB":"4C",
        "STA":"0C",
        "STCH":"54",
        "STL":"14",
        "STSW":"E8",
        "STX":"10",
        "SUB":"1C",
        "TD":"E0",
        "TIX":"2C",
        "WD":"DC"
    }


#show error function is used to show an error message when handle an exception
def show_error(message):

    label = Label(root, text=message)
    label.pack()
    root.geometry("500x100+300+300")
    root.title("Problem")
    root.mainloop()

#Pass1 function is used to excute pass1
def Pass1():

    f1 = f.readline()
    LOCCTR = f1[17:35]
    programName = f1[0:7]
    interfile.write(hex(int(LOCCTR,16))[2:])
    interfile.write("     "+f1)
    startAddress = LOCCTR
    contents=f.readlines()
    litrals=[]
    global ProgrameLen

    try:
    #read code lines
        for line in contents:

        
            opcode = line[9:15].strip()
            operand = line[17:35].strip()
            symbol = line[0:8].strip()
            if opcode != "END":
                #check the comment line
                if line[0] != ".":

                    try:
                        if symbol != "" and symbol not in symbol_table.keys():
                            symtabel.write(symbol+"       "+hex(int(LOCCTR,16))[2:]+"\n")
                            symbol_table.update({symbol:hex(int(LOCCTR,16))[2:]})
                    except:
                        show_error("There is a problem : symbol already exist\n duplicate labels are not allowed")

                    #check the literals and store them in litrals list
                    if  '=C' in operand:
                            litrals.append(operand)

                    elif '=X' in operand:
                        if(len(operand)-4) %2 == 0:
                            litrals.append(operand)
                        else:
                            show_error("There is a problem : operand X in litral has unsuitable number of Bytes ")

                    #check the LTORG and store the literals list on symbol table
                    if opcode == "LTORG":
                        interfile.write("         "+line)
                        for i in litrals :
                            if '=X' in i:
                                symtabel.write(i+"     "+LOCCTR[2:]+"\n")
                                symbol_table.update({i:LOCCTR[2:]})
                                LOCCTR = hex(int(LOCCTR,16)+(len(i)-4)//2)

                            elif '=C' in i:
                                symtabel.write(i+"     "+LOCCTR[2:]+"\n")
                                symbol_table.update({i:LOCCTR[2:]})
                                LOCCTR = hex(int(LOCCTR,16)+(len(i)-4))

                            litrals=[]
                    
                    #writte code lines in intermmediate file
                    else:
                        forbiden = ['#', '@']
                        directives = ['RESB', 'RESW', 'BYTE', 'WORD','LTORG', 'BASE','START','END']
                        optab = ["ADD","AND","AND","COMP","DIV","J","JEQ","JGT","JLT","JSUB","LDA","LDCH"
                        ,"LDL","LDX","MUL","OR","RD","RSUB","STA","STCH",'STL',"STSW","STX","SUB","TD","TIX","WD"]
                        invalid_Min = directives + optab

                        if len(line) >= 17 and line[17] in forbiden:
                            show_error("There is a problem : Ther is an inappropriate operand , please check them\n Hint : may be you are trying to write an operend with '#' or '@' at the begining")
                
                        elif opcode not in invalid_Min:
                            show_error("There is a problem : Ther is an invalid mnemonic , please check the mnemonic table")
                            
                        else:
                            interfile.write(hex(int(LOCCTR,16))[2:]+"     "+line)

                    #increment the location counter according the opcode
                    if opcode in optabel.keys() or opcode == "WORD":
                        LOCCTR = hex(int(LOCCTR,16)+(3))

                    elif opcode == "RESW":
                        LOCCTR = hex(int(LOCCTR,16)+int(operand,10)*3)

                    elif opcode == "RESB":
                        LOCCTR = hex(int(LOCCTR,16)+(int(operand,10)))

                    elif opcode == "BYTE":
                        if line[17] == 'X':
                            if(len(operand)-3) %2 == 0:
                                LOCCTR = hex(int(LOCCTR,16)+(len(operand)-3)//2)
                            else:
                                show_error("There is a problem : operand X has unsuitable number of Bytes")
                        elif line[17] == 'C':
                            LOCCTR = hex(int(LOCCTR,16)+(len(operand)-3))    
            else:
                interfile.write("         "+line)
          
    except:
        show_error("There is a problem occurs when reading your source file")

    #after code lines finished check if there are litrals didn't store
    #to append them at end of programme & push them on symboletable
    else:
        try:
            if len(litrals) != 0:
                try:
                    for i in litrals:

                        if '=X' in i:
                            symtabel.write(i+"     "+LOCCTR[2:]+"\n")
                            symbol_table.update({i:LOCCTR[2:]})
                            LOCCTR = hex(int(LOCCTR,16)+(len(i)-4)//2)

                        elif '=C' in i:
                            symtabel.write(i+"     "+LOCCTR[2:]+"\n")
                            symbol_table.update({i:LOCCTR[2:]})
                            LOCCTR = hex(int(LOCCTR,16)+(len(i)-4))

                        litrals=[]
                except:
                    show_error("There is a problem : symbol already exists\n duplicate labels are not allowed")
        except:
            show_error("There is a problem occurs when trying to proccess letrals")

        #write program name amd program length to thier files
        else:
            ProgrameLen = int(LOCCTR,16) - int(startAddress,16)
            programname.write( "\n"+"The program name is : " +programName+"\n")
            programlength.write( "\n"+"The Program Length: " +hex(ProgrameLen)+"\n")

#Pass2 function is used to excute pass2
def Pass2():

    listt = ['START','RESW','RESB','END','LTORG']
    interfile.seek(0)
    lines = interfile.readlines()
    array = []
    codes = []
    global start
    
    for line in lines:

        locc = line[0:4].strip()
        symb = line[9:17].strip()
        op = line[18:24].strip()
        opr = line[25:43].strip()

        if op not in listt:

            if op == "WORD":
                m = hex(int(opr,10))[2:]
                if len(m)<6:
                    x = range(6-len(m))
                    for j in x:
                        m = "0" + m
                    opr = m

            elif op == "RSUB":
                opr = "4C0000"

            elif op == "BYTE":
                if 'X' in opr:
                    opr = opr[2:len(opr)-1]
                elif 'C' in opr:
                    r = ""
                    for i in opr[2:len(opr)-1].strip():
                        r = r + str(hex(ord(i))[2:])
                        opr =  r

            elif op in optabel.keys():

                if opr[len(opr)-1].strip() == 'X':

                    y = opr[0:len(opr)-2].strip()
                    s = symbol_table.get(y)
                    binary = bin(int(s,16)) 
                    binary = binary.replace(binary[0],"1",1)
                    binary = binary.replace("b","00",1)
                    b = int(binary,2)
                    h = hex(b)[2:]
                    opr = optabel.get(op) + str(h)

                else:
                    opr = optabel.get(op) + str(symbol_table.get(opr))

            listfile.write(line.rstrip() + "                        " + opr+ "\n")
            
        else:
            if op == "START":
                start = opr
                objfile.write("H^"+symb+"^00"+opr+"^00"+str(hex(ProgrameLen)[2:])+"\n")
            listfile.write(line.rstrip()+"\n")
            opr = ''
            
        codes.append(opr) 
        array.append(locc)
  
    arr = []
    i = 0 
    count_word = 0
    text = "\nT"
    while i<len(codes):
       
        if count_word < 10 and codes[i] !='':
            count_word = count_word + 1
            text = text+"^"+codes[i]
            i = i + 1 
            
        else:
            cnt = 0
            if codes[i] == '' and i<len(array)-1:
                array[i] = array[i+1] 

            non = {"T","^"}
            if text[len(text)-1] not in non:
                
                for m in range(len(text)):
                    if m >= 9 and text[m] != "^":
                        cnt = cnt + 1
                y = hex(cnt//2)       
                length = str(y[2:])
                if len(length) == 1:
                    length = "0" + length
                objfile.write(text[:10] + length+"^" + text[10:])
                 
            text = "\nT^00" +array[i] + "^" + codes[i]

            if count_word == 10:
                count_word = 1
            else:
                count_word = 0
            
            i = i + 1
        
    objfile.write("\n\nE^00"+start)
 

try:
    #open the source code file
    f = open( "Source Code.asm" , "r" )
    #creat intermmdiate file and symbole table file to writte on them
    interfile = open("Intermediate File.mdt","w+")
    symtabel = open("Symbol Tabel.txt","w+")
    programname = open("Program Name.txt","w")
    programlength = open("Program Length.txt","w")
    listfile = open("Listing File.txt","w")
    objfile = open("Object File.txt","w+")
   

except:
    show_error("There is a problem with your files , Pleask check them\n Hint : may be you are trying to write in unwritable one")

else:
    Pass1()
    Pass2()
    f.close()
    interfile.close()
    symtabel.close()
    programlength.close()
    programname.close()
    listfile.close()
    objfile.close()


    ################################## GUI ####################################

    #showcontent function is used to show content of selected files
    def showcontent(event):
        x = lbox.curselection()[0]
        file = lbox.get(x)
        with open(file) as file:
            file = file.read()
        text.delete('1.0', tkinter.END)
        text.insert(tkinter.END, file)

    flist = os.listdir()
    root['bg'] = 'black'
    root.title("Choose file")
    lbox = tkinter.Listbox(root)
    lbox.pack()

    for item in flist:
        lbox.insert(tkinter.END, item)

    text = tkinter.Text(root, bg='light blue')
    text.pack()

    lbox.bind("<<ListboxSelect>>", showcontent)
    root.mainloop()


