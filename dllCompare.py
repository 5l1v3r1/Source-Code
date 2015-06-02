import os
from collections import defaultdict
import cPickle as pickle
import sys
from optparse import OptionParser
import itertools


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    
    The MIT License (MIT)

    Copyright (c) 2013, Hugh Brown.
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

parser = OptionParser()
parser.add_option("-w", "--whitelist",
                  action="store_true", dest="whitelist",
                  help="this flag invokes whitelist")
parser.add_option("-d", "--details",
                  action="store_true", dest="details",
                  help="this flag invokes whitelist")

(options, args) = parser.parse_args()

print ("\n------- DLL compare module --------\n")
if options.whitelist:
    print "Whitelist filtereing is ON \n"


def WhiteListFilter(rawList):
    """
    Filter out the baseline processes DLLs
    """
    #open and loads the whitelist
    whitelist = open('whitelist.txt').read().splitlines() 
    
    #print "Whitelist:"        
    #print whitelist        
    
    for key in rawList.keys():
        for white in whitelist:
            #print white
            if key == white:
                del rawList[key]
    return rawList

    #returns the list without the Whitelist entries. 

if len(sys.argv) == 2:
    print 'need two files to compare'
    sys.exit(-1)

filename1 = sys.argv[1]
filename2 = sys.argv[2]



with open(filename1, 'rb') as fp:
    dllData1 = pickle.load(fp)
    
with open(filename2, 'rb') as fp:
    dllData2 = pickle.load(fp)

#if options.whitelist:
    #dllData1 = WhiteListFilter(dllData1)
    #dllData2 = WhiteListFilter(dllData2)
    
result = DictDiffer(dllData1,dllData2)
resultPrintAdded = result.added()
resultPrintChanged = result.changed()

print "--- Processes not seen in baseline:"
newProcesses = []
for key in dllData2:
    print key
    if key not in dllData1:
        newProcesses.append(key)
        
for key in newProcesses:
    print key
print "\n"

print "--- Processes with changed dll modules:"

for key in resultPrintChanged:
    print key
print "\n"

print "--- Processes with added dll modules:"
for key in resultPrintAdded:
    print key


#Listing out the changed DLL MODULES
if options.details:
    print "\n\n--- Outputting the changed dll modules "
    for processes in resultPrintChanged:
        dllData1_temp = list(dllData1.get(processes))
        dllData2_temp = list(dllData2.get(processes))
    
        #merging the data 
        mergeddllData1 = list(itertools.chain.from_iterable(dllData1_temp))
        mergeddllData2 = list(itertools.chain.from_iterable(dllData2_temp))

        setDllData1 = set(mergeddllData1)
        setDllData2 = set(mergeddllData2)
        print "--Process name: " + str(processes) + ":"
        print "- Removed: " + str(setDllData1 - setDllData2) 
        print "+ Added: " + str(setDllData2 - setDllData1)
        
        print "\n"