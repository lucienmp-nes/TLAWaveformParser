#!/usr/bin/env python

import sys
import re
import csv
from pprint import pprint
import string

# Expected format from TLA for SPI memory interface
# [Vectors]
# CS#[],SI/IO0[],SO/IO1[],WP#/IO2[],HOLD#/IO3[]
# 0  ,0     ,0     ,0      ,1
# ...
#

#filepath = 'Linsting1.txt'
#filepath = 'Listing3.txt'
print(sys.argv[1])
filepath = sys.argv[1]

value=0
with open(filepath) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    bits=0
    byte=""
    line=0

    valuecount=0
    ContRead=0

    # For mid-run reads, we should already be in ContRead mode for E7h command
    ContRead=1

    addr=""
    mode=""
    databyte=""
    for row in spamreader:
        # ROW[0]=CS#, ROW[1]=SI/IO0, ROW[2]=SO/IO1, ROW[3]=WP#/IO2, ROW[4]=HOLD#/IO3
        
        # Skip first 3 entreis
        line=line+1
        if line < 3 :
            continue

        # Ignore lines that do not confirm to having 5 fields
        if len(row)<5 :
            continue

        # CS# is disabled, so just keep reading
        if string.strip(row[0])=="1" and value==0:
            if ContRead==1:
                print "EXITED READ MODE.........."
                break
            
        # ignore CS#=1
        if string.strip(row[0])=="1":
            ContRead=0
            if value==0xe7:
                print "CS#=1, ignoring ----------------------"
                ContRead=1
            continue
        
        #print "XXXXXXXXXXXX"
        #print ', '.join(row)
        #print (row[1])
        
        # SPI Commnd E7h with "Continuous Read Mode"; CS# drops and block will now be read back to back in 14 cycle chunks
        #  A23-18 / A15-08 / A07-00 / M7-0 / Dummy / Byte 1 / Byte 2
        if ContRead==1:
            nibble=string.strip(row[4])+string.strip(row[3])+string.strip(row[2])+string.strip(row[1])
            nibbleval=int(nibble,2)
            valuecount=valuecount+1
            #if valuecount==1:
            #    print "________________________"
            #print " Nibble#"+str(valuecount)+": "+nibble+" hex:"+hex(nibbleval)
            
            if valuecount<=6:
                addr=addr+nibble
            if valuecount==7 or valuecount==8:
                mode=mode+nibble
            if valuecount==9 or valuecount==10:
                mode=mode # ignore; this is dummy two cyucles
            if valuecount==11 or valuecount==12:
                databyte=databyte+nibble
            if valuecount==13 or valuecount==14:
                databyte=databyte+nibble
                
            if valuecount==14:
                print  " line# " + str(line) +" READ:* "+hex(int(addr,2))+"(mode="+hex(int(mode,2))+"): "+hex(int(databyte,2))

            # End of Quad I/O Word Fast Read
            if valuecount==14:
                addr=""
                mode=""
                databyte=""
                
                valuecount=0
                #value=0
            value=0
            continue

        # Quad I/O Word Fast Read with "Continuous Read Mode"
        #  A23-18 / A15-08 / A07-00 / M7-0 / Dummy / Byte 1 / Byte 2        
        if value==0xe7:
            nibble=string.strip(row[4])+string.strip(row[3])+string.strip(row[2])+string.strip(row[1])
            nibbleval=int(nibble,2)
            valuecount=valuecount+1
            #if valuecount==1:
            #    print "________________________"
            #print " Nibble#"+str(valuecount)+": "+nibble+" hex:"+hex(nibbleval)
            
            if valuecount<=6:
                addr=addr+nibble
            if valuecount==7 or valuecount==8:
                mode=mode+nibble
            if valuecount==9 or valuecount==10:
                mode=mode # ignore; this is dummy two cyucles
            if valuecount==11 or valuecount==12:
                databyte=databyte+nibble
            if valuecount==13 or valuecount==14:
                databyte=databyte+nibble

            # M[5:4]=10 is continuous mode, else E7h needs to be issued on next read
            if valuecount==14:
                print " line# " + str(line) + " READ:  "+hex(int(addr,2))+"(mode="+hex(int(mode,2))+"): "+hex(int(databyte,2))
                
            if valuecount==14:
                addr=""
                mode=""
                databyte=""
                
                valuecount=0
#                value=0
            continue
            
#            nibble=string.strip(row[4])+string.strip(row[3])+string.strip(row[2])+string.strip(row[1])
#            nibbleval=int(nibble,2)
#            valuecount=valuecount+1
#            print " Nibble#"+str(valuecount)+": "+nibble+" hex:"+hex(nibbleval)            
#            if valuecount==14:
#                valuecount=0
#                #value=0
#            continue
        
        bits=bits+1
        byte=byte+string.strip(row[1])
        if bits == 8 :
            value=int(byte,2)
            print( "Serial CMD:"+byte+" - "+hex(value) )
            bits=0
            byte=""
            valuecount=0

            
        #print 'XX'+row
 
#with open(filepath) as fp:
#   line = fp.readline()
#   cnt = 1
#   while line:
#       print("Line {}: {}".format(cnt, line.strip()))
#       line = fp.readline()
#       cnt += 1
       
       
