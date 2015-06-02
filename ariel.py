import volatility.utils as utils
import volatility.cache as cache
from collections import defaultdict
import volatility.plugins.common as common
import volatility.utils as utils
import volatility.win32.tasks as tasks
import volatility.plugins.taskmods as taskmods
import volatility.debug as debug
import os
import markup
import volatility.win32 as win32
import volatility.conf as conf
import cPickle as pickle



class ariel(common.AbstractWindowsCommand):

# This plugis collects all loaded DLLs and store them as a dict-datatype 
# on disk. This is a subsystem for the DLLCOMPARE function.
#
#
    """ news """ 
    def __init__(self,config, *args, **kwargs):
        common.AbstractWindowsCommand.__init__(self, config, *args, **kwargs)
     
    def calculate(self):
            
        addr_space = utils.load_as(self._config)
        tasks = win32.tasks.pslist(addr_space)
        
        return tasks
        
    def filter_tasks(self, tasks):
        return tasks
    
    def generator(self, data):
        for task in data:
            pid = task.UniqueProcessId
            
            for m in task.get_load_modules():
                yield (0, [str(m.FullDllName)])

    def render_text(self, outfd, data):
        #print self._remove_unprintable(fileinfo.get_name())
        
        
        outfd.write("\n")
        outfd.write("------- DLL check --------\n\n")
        dllData = defaultdict(list)
        
        for task in data:
            dllList = []
            pid = task.UniqueProcessId
            #outfd.write("Collecting DLLs for PID: " + str(pid) + "\n")
            if task.Peb:
                for m in task.get_load_modules():
                    dllList.append(str(m.FullDllName or ''))
            
            #possible to use just task.ImageFileName    
            j = (str(task.Peb.ProcessParameters.CommandLine or ''))
            #print j
            dllData[j].append(dllList)
            
                
        
        
        #names the file by getting the path
        locationString = str(conf.ConfObject.opts["location"]).rsplit('/',1)[1] + "_DLL_List"
        #print locationString
        
        outfd.write("Storing DllList as \"" + locationString + "\"\n")  
        with open(locationString + '.p', 'wb') as fp:
            pickle.dump(dllData, fp)
            
 