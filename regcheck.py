from collections import defaultdict
import volatility.utils as utils
import volatility.cache as cache
import volatility.plugins.common as common
import volatility.utils as utils
import volatility.win32.tasks as tasks
import volatility.plugins.taskmods as taskmods
import volatility.plugins.registry.registryapi as registryapi
import volatility.win32 as win32
import volatility.conf as conf
import cPickle as pickle
import markup
import os


class regcheck(common.AbstractWindowsCommand):

# This plugis collects all loaded DLLs and store them as a dict-datatype 
# on disk. This is a subsystem for the DLL_diff function.

    def __init__(self,config, *args, **kwargs):
        common.AbstractWindowsCommand.__init__(self, config, *args, **kwargs)
     
    def calculate(self):
        
        regapi = registryapi.RegistryApi(self._config)    
        addr_space = utils.load_as(self._config)
        
        tasks = win32.tasks.pslist(addr_space)
        
        registerKeys = open('/Users/Lunde/volatility_plugins/registerRunKeys.txt').read().splitlines()
        for locations in registerKeys:
            base =locations.split('\\')[0]
            search_location = locations.split('\\',2)[2]
            if base == 'HKLM':
                hive = 'software' 
            if base == 'HKCU':
                hive = 'NTUSER.DAT'
            
            #regapi.set_current(hive_name= "software", user = "administrator")
            regapi.set_current(hive_name= hive)
            key_ = search_location
        
            for value, data in regapi.reg_yield_values(hive_name = str(hive), key = str(key_)):
                yield value, data, locations
                
                                
    def render_text(self, outfd, data):
        
        registryDict = defaultdict(list)
    

        outfd.write("\n")
        outfd.write("------- register check --------\n")
        for value, data, locations in data:
            if type(data) != int and type(data) != list:
                data = data.encode('utf8')
       
            registryList = []
            registryList.append(str(value))
            registryList.append(str(data))
            registryDict[str(locations)].append(registryList)
        
        #Storing the extracted data
        
        locationString = str(conf.ConfObject.opts["location"]).rsplit('/',1)[1] + "_RegKeyList"
        outfd.write("Storing RunKeyList as \"" + locationString + "\"\n")  
        with open(locationString + '.p', 'wb') as fp:
            pickle.dump(registryDict, fp)
            
            