#!/usr/bin/env python2
import re
import os
import sys
#"""/tmp/SDASE/SDASE_ROOT_BASE/SDASE_CRT/SDABS_CNT/SDAX_CAA/business/subscriberDataAccess/src/"""


path_to_test = sys.argv[1:]


def percentage(part, whole):
    perc=str(100 * float(part)/float(whole)).split(".",1)
    return int(perc[0])

def f(line):
    if re.search('^\s*$',line): 
        isExecutableCodeLine = False
    elif re.search('^\s*[/]{2}',line):
        isExecutableCodeLine = False
    elif re.search('\s*[{}]\s*',line):
        isExecutableCodeLine = False
    elif re.search('\s*[\/\*]\s*',line):
        isExecutableCodeLine = False
    elif re.search('\sunion\s.*',line):
        isExecutableCodeLine = False
    elif re.search('\selse\s.*',line):
        isExecutableCodeLine = False
    elif re.search('\scase\s.*',line):
        isExecutableCodeLine = False
    else:
        isExecutableCodeLine = True
    return isExecutableCodeLine



def f_find_lines_covered(className ):
    set_of_covered_lines=[]   
    file_to_read = open('/tmp/SDASE/SDASE_ROOT_BASE/SDASE_CRT/SDABS_CNT/SDAX_CAA/business/coverage.info').readlines()
    for num, line in enumerate(file_to_read,1):
        if re.search(".*"+path_to_test+className+'.*',line):
            for next_line in range(num,len(file_to_read),1):
                if re.search('^DA:[1-9]*,[1-9].*',file_to_read[next_line]):
                    mo = re.search("(?<=:)[^}]*(?=,)",file_to_read[next_line])
                    if mo:
                        set_of_covered_lines.append(mo.group())
                if re.search('.*end_of_record.*',file_to_read[next_line]):
                    break
    return set_of_covered_lines



def f_get_new_code_coverage(class_name):
    print path_to_test,class_name
    new_lines_covered = []
    set_of_impacted_lines=[] 
    set_of_covered_lines=[]
    file = open ("impacted_classes/"+class_name).readlines()
    for num, line in enumerate(file,1):        
        if re.search('.*>INS.*',line):
            startRange = num
            for next_line in range(startRange,len(file),1):
                if f(file[next_line]):
                    set_of_impacted_lines.append(str(next_line+1))    
#                    print next_line+1,"INS",file[next_line]
                if re.search('.*<INS.*',file[next_line]):
                    break
        if re.search('.*>MOD.*',line):
            startRange = num
            for next_line in range(startRange,len(file),1):                
                if f(file[next_line]):
                    set_of_impacted_lines.append(str(next_line+1))    
#                    print next_line+1,"MOD",file[next_line]
                if re.search('.*<MOD.*',file[next_line]):
                    break
    set_of_covered_lines =     f_find_lines_covered(class_name)                                            
    for bx in set_of_covered_lines:
        if bx in set_of_impacted_lines:
            new_lines_covered.append(bx)
    print "New Lines ",len(set_of_impacted_lines)
    print "New Lines Covered",len(new_lines_covered)
    if len(set_of_impacted_lines) > 0:
        print "New Code Coverage Percentage:",percentage(len(new_lines_covered), len(set_of_impacted_lines))
    print " "
    return (len(set_of_impacted_lines),len(new_lines_covered))

def f_get_total_code_coverage():
    buff_total_new_lines = 0;
    buff_total_new_lines_covered = 0;
    total_new_lines = 0;
    total_new_lines_covered = 0;
    for file_name in os.listdir(path_to_test):
        if os.path.isfile(path_to_test+file_name) and file_name.endswith("cpp"): #headers
            file = open (path_to_test+file_name).readlines()
    for num, line in enumerate(file,1):        
        if re.search('.*>INS.*',line):
            buff_total_new_lines,buff_total_new_lines_covered = f_get_new_code_coverage(file_name)
            total_new_lines = total_new_lines + buff_total_new_lines
            total_new_lines_covered = total_new_lines_covered + buff_total_new_lines_covered 
            break                             
        if re.search('.*>MOD.*',line):
            buff_total_new_lines,buff_total_new_lines_covered = f_get_new_code_coverage(file_name)
            total_new_lines = total_new_lines + buff_total_new_lines
            total_new_lines_covered = total_new_lines_covered + buff_total_new_lines_covered 
            break
      


####################################################################################################################
    total_new_lines,total_new_lines_covered = f_get_total_code_coverage()
    print "++++++Total Statistics++++++"
    print "Total New Lines ",total_new_lines
    print "Total New Lines Covered",total_new_lines_covered
    if total_new_lines > 0:
        print "Total New Code Coverage Percentage:",percentage(total_new_lines_covered,total_new_lines)
    print " "
    return (total_new_lines,total_new_lines_covered) 

print "Wywolany skrypt:", sys.argv[1:]
print "Liczba argumentow:", len(sys.argv)
print "Przekazane argumenty:", str(sys.argv)

for i in range(0, len(sys.argv)):
    print "targument", i, ":", sys.argv[i]                                                         