#######################imports:################################
import webbrowser
#######################variables:##############################
MEM = 4096*['0000000000000000']
tmp=[]
label_list=[]
label_lines=[]
value_lines=[]
IO_instruct=['INP','OUT','SKI','SKO','ION','IOF']
IO_instruct_HEX=[0xf800,0xf400,0xf200,0xf100,0xf080,0xf040]
IO_instruct_lines=[]
ALU_instruct=['AND','ADD','LDA','STA','BUN','BSA','ISZ']
ALU_instruct_bin_0=['0000','0001','0010','0011','0100','0101','0110']
ALU_instruct_bin_1=['1000','1001','1010','1011','1100','1101','1110']
ALU_instruct_lines=[]
Register_instruct=['CLA','CLE','CMA','CME','CIR','CIL','INC','SPA','SNA','SZA','SZE','HLT']
Register_instruct_HEX=[0x7800,0x7400,0x7200,0x7100,0x7080,0x7040,0x7020,0x7010,0x7008,0x7004,0x7002,0x7001]
Register_instruct_lines=[]
###################function definitions:#######################
def convert_to_Nbits(string,n):
    string=list(string)
    while(len(string)<n):
        string.insert(0,'0')
    string=str(''.join(string))
    return string  
###############
def detect_labels(line):
    for i in range(1,len(line)-1):
        if(', ' in line[i]):
            label_list.insert(i-1,line[i][0:line[i].index(',')])
            label_lines.insert(i-1,i)
###############
def get_org_end(line_O,line_E):
    if ('END' not in line_E):
        print('ERROR! Define END at last line \n press Enter to Edit...')
        raw_input()
        webbrowser.open("input.txt")
        exit()
    a=0
    if ('ORG' in line_O) :
        for i in range(-2,-len(line_O),-1):
            if (line_O[i]==' '):
                break
            tmp.insert(a,line_O[i])
            a=a-1
        return int(''.join(tmp))
    else:
        print('ERROR! Define ORG at first line \n press Enter to Edit...')
        raw_input()
        webbrowser.open("input.txt")
        exit()
###############
def detect_Register_instruct(line,ORG):
    for i in range(1,len(line)-1):
        if(i in label_lines):
            if((line[i][line[i].index(' ')+1:line[i].index(' ')+4]) in Register_instruct):
                Register_instruct_lines.insert(i-1,i)
                a=bin(Register_instruct_HEX[Register_instruct.index((line[i][line[i].index(' ')+1:line[i].index(' ')+4]))])[2:]
                a=convert_to_Nbits(a,16)
                MEM[i-1+ORG]=a
                
        else:
            if((line[i][0:3]) in Register_instruct):
                a=bin(Register_instruct_HEX[Register_instruct.index((line[i][0:3]))])[2:]
                Register_instruct_lines.insert(i-1,i)
                a=convert_to_Nbits(a,16)
                MEM[i-1+ORG]=a
###############
def detect_IO_instruct(line,ORG):
    for i in range(1,len(line)-1):
        if(i in label_lines):
            if((line[i][line[i].index(' ')+1:line[i].index(' ')+4]) in IO_instruct):
                IO_instruct_lines.insert(i-1,i)
                a=bin(IO_instruct_HEX[IO_instruct.index((line[i][line[i].index(' ')+1:line[i].index(' ')+4]))])[2:]
                a=convert_to_Nbits(a,16)
                MEM[i-1+ORG]=a 
        else:
            if((line[i][0:3]) in IO_instruct):
                a=bin(IO_instruct_HEX[IO_instruct.index((line[i][0:3]))])[2:]
                IO_instruct_lines.insert(i-1,i)
                a=convert_to_Nbits(a,16)
                MEM[i-1+ORG]=a
###############
def detect_ALU_instruct(line,ORG):
    for i in range(1,len(line)-1):
        if(i in label_lines):
            if((line[i][line[i].index(' ')+1:line[i].index(' ')+4]) in ALU_instruct):
                ALU_instruct_lines.insert(i-1,i)
                if(line[i][-2]=='I'):
                    tmp=''
                    for j in range(9,12):
                        if(line[i][j]==' '):
                            break
                        tmp=tmp+line[i][j]
                    a=str(bin((label_lines[label_list.index(tmp)])+ORG-1)[2:])
                    a=convert_to_Nbits(a,12)
                    a=ALU_instruct_bin_1[ALU_instruct.index((line[i][line[i].index(' ')+1:line[i].index(' ')+4]))]+a
                    MEM[i-1+ORG]=a
                else:
                    tmp=''
                    for j in range(9,12):
                        if(line[i][j]=='\n'):
                            break
                        tmp=tmp+line[i][j]
                    a=str(bin((label_lines[label_list.index(tmp)])+ORG-1)[2:])
                    a=convert_to_Nbits(a,12)
                    a=ALU_instruct_bin_0[ALU_instruct.index((line[i][line[i].index(' ')+1:line[i].index(' ')+4]))]+a
                    MEM[i-1+ORG]=a
        else:
            if ((line[i][0:3]) in ALU_instruct):
                ALU_instruct_lines.insert(i-1,i)
                if(line[i][-2]=='I'):
                    tmp=''
                    for j in range(4,7):
                        if(line[i][j]==' '):
                            break
                        tmp=tmp+line[i][j]
                    a=str(bin((label_lines[label_list.index(tmp)])+ORG-1)[2:])
                    a=convert_to_Nbits(a,12)
                    a=ALU_instruct_bin_1[ALU_instruct.index((line[i][0:3]))]+a
                    MEM[i-1+ORG]=a
                else:
                    tmp=''
                    for j in range(4,7):
                        if(line[i][j]=='\n'):
                            break
                        tmp=tmp+line[i][j]
                    a=str(bin((label_lines[label_list.index(tmp)])+ORG-1)[2:])
                    a=convert_to_Nbits(a,12)
                    a=ALU_instruct_bin_0[ALU_instruct.index((line[i][0:3]))]+a
                    MEM[i-1+ORG]=a        
###############
def detect_values(line):
    for i in range(1,len(line)-1):
        if(i in Register_instruct_lines):
            continue
        if(i in IO_instruct_lines):
            continue
        if(i in ALU_instruct_lines):
            continue
        else:
            value_lines.insert(i-1,i)
###############
def two_complement(string):
    string=list(string)
    for i in range(len(string)):
        if(string[i]=='0'):
            string[i]='1'
        else:
            string[i]='0'
    string=str(''.join(string))
    return bin(int(string,2)+1)[2:]
###############
def assign_values(line,ORG):
    for i in range(len(value_lines)):
        tmp=''
        if('DEC' in line[value_lines[i]]):
            for j in range(-2,-len(line[value_lines[i]]),-1):
                if(line[value_lines[i]][j]==' '):
                    break
                tmp=tmp+line[value_lines[i]][j]
            tmp=list(tmp)
            tmp.reverse()
            tmp=int(str(''.join(tmp)))
            if(tmp<0):
                tmp=abs(tmp)
                tmp=bin(tmp)[2:]
                tmp=two_complement(tmp)
                tmp=convert_to_Nbits(tmp,16)
            else:
                tmp=bin(tmp)[2:]
                tmp=convert_to_Nbits(tmp,16)
            MEM[value_lines[i]-1+ORG]=tmp
        if('HEX' in line[value_lines[i]]):
            for j in range(-2,-len(line[value_lines[i]]),-1):
                if(line[value_lines[i]][j]==' '):
                    break
                tmp=tmp+line[value_lines[i]][j]
            tmp=list(tmp)
            tmp.reverse()
            tmp=(str(''.join(tmp)))
            tmp=tmp.lower()
            tmp=int(tmp,16)
            tmp=bin(tmp)[2:]
            tmp=convert_to_Nbits(tmp,16)
            MEM[value_lines[i]-1+ORG]=tmp
        if('BIN' in line[value_lines[i]]):
            for j in range(-2,-len(line[value_lines[i]]),-1):
                if(line[value_lines[i]][j]==' '):
                    break
                tmp=tmp+line[value_lines[i]][j]
            tmp=list(tmp)
            tmp.reverse()
            tmp=tmp=(str(''.join(tmp)))
            tmp=convert_to_Nbits(tmp,16)
            MEM[value_lines[i]-1+ORG]=tmp               
##########################Main:##############################
input_file=open("input.asm","r")
line=input_file.readlines()
input_file.close()
ORG = get_org_end(line[0],line[-1])
detect_labels(line)
detect_Register_instruct(line,ORG)
detect_IO_instruct(line,ORG)
detect_ALU_instruct(line,ORG)
detect_values(line)
assign_values(line,ORG)
output_file=open("output.bin","w")
output_file.write('ALIREZA AZADI        91126025\n')
for i in range(4096):
    output_file.write((str(hex(i))) + "              " +str(MEM[i])+'\n')
output_file.close()

