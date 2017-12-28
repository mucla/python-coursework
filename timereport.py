#!/usr/bin/env python3
# encoding: utf-8
import sys
from datetime import timedelta

"""
Produces a report of total work time.

Example:
PROGRAMMING COURSE
   demos           3.67
   lectures        4.02
   pw              3.33
   ------------ -------
   total:         11.02
   
INTEGRATION COURSE
   ex tempores     1.58
   demos           2.00
   lectures        3.22
   ------------ -------
   yht             6.80
   
   ============ =======
   Total (all):   17.82
   
"""

OUT  = "out.txt"
div = '-'

def report(proj, times):
    """ produces a report from two lists of lines """
    parts = [] # string buffer
    sub = []
    errors = [] # a list of errors
    longest_str = get_longest_str(proj,div)
    if longest_str < 12: #needs to be at least as long as str "Total (all):"
        longest_str = 12
    form = "   {0:"+str(longest_str)+"} {1:7.2f}\n"
    line_form = "   {0:"+str(longest_str)+"} {1:7}\n"
    total_time = timedelta()
    main = get_main(proj)
    for mproj in main:
        main_time = timedelta()
        parts.append(mproj.upper() + "\n")
        sub = get_sub(proj, mproj)
        for sproj in sub:
            sub_time = get_time(times, mproj + "|" + sproj, errors)
            if sub_time > timedelta():
                parts.append(form.format(sproj, float(str(sub_time.total_seconds()/3600))))
                main_time += sub_time
        parts.append(line_form.format("-"*longest_str,"-"*7))    
        parts.append(form.format("total:", float(str((main_time.total_seconds())/3600))) + "\n")
        total_time += main_time
    parts.append(line_form.format("="*longest_str, "="*7))
    parts.append(form.format("Total (all):", float(str((total_time.total_seconds())/3600))))    
    if len(errors) > 0:
        parts.append("\nErroneous lines not calculated in the report:\n" + "".join(errors))
    report = "".join(parts)    
    return report
    
    
def read(file):
    """ reads the lines from a file into a list, excluding line breaks """
    with open(file, "r") as f:
        lines = f.readlines() #returns a list of lines, including line breaks as "\n"
        lines = [line.rstrip("\n") for line in lines] #removes line breaks
    return lines
    
    
def get_main(li):
    """ returns a list of main projects """
    main = []
    for line in li:
        if line == "" or line.startswith("#"):
            continue
        if not line.startswith(div):
            main.append(line)
    return main
    
    
def get_sub(proj, mproj):
    """ returns a list of sub projects related to the given main project"""
    sub = []
    is_proj = False
    for line in proj:
        if is_proj:
            if line == "" or line.startswith("#"):
                continue
            if line.startswith(div):
                sub.append(line[1:]) #important to not include the '-'
            else:
                break
        if line == mproj:
            is_proj = True
    return sub
    
    
def get_time(times, proj_string, errors):
    """ returns the amount of time used for given sub project """
    time = timedelta()
    for idx, line in enumerate(times):
        if line.startswith(proj_string):
            items = line.split('|')
            if len(items) < 6:
                errors.append("Line " + str(idx+1) + ": wrong amount of dividers: " + line + "\n")
                continue    
            digits = items[4].split(':')
            time_exc = "Line "+ str(idx+1) + ": duration in wrong format: " + line + "\n"
            try:
                dur = timedelta(hours=int(digits[0]),minutes=int(digits[1]),seconds=int(digits[2]))
                time += dur
            except Exception as e1:
                raise TypeError(time_exc) from e1
            except Exception as e2:    
                raise OverflowError(time_exc) from e2
    return time
    

def get_longest_str(proj,div):
    """ returns the length of the longest sub project name"""
    longest = 0
    for line in proj:
        if line.startswith(div) and len(line) > longest:
            longest = len(line)
    return longest
    
    
def main():
    """ prints a project report on screen and in file 'out.txt' """
    proj = "projects.txt"
    times = "times.txt"
    try:
        if len(sys.argv) > 1:
            proj = sys.argv[1] #list always contains one element            
        proj = read(proj)
        if len(sys.argv) > 2:
            times = sys.argv[2]
        times = read(times)
    except Exception as exc:
        raise FileNotFoundError("File not found!") from exc
    rep = report(proj,times)
    print(rep)
    with open(OUT, "w") as f:
        print(rep,file=f)

######################################

if __name__ == "__main__":
    main()