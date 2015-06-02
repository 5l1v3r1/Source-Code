import volatility.utils as utils
import volatility.cache as cache
from collections import defaultdict
import volatility.plugins.common as common
import volatility.utils as utils
import volatility.win32.tasks as tasks
import volatility.plugins.taskmods as taskmods
import volatility.plugins.registry.registryapi as registryapi
import volatility.plugins.malware.svcscan as svcscan
import os
import markup
import volatility.win32 as win32
import volatility.conf as conf
import cPickle as pickle


class servicecheck(common.AbstractWindowsCommand):

# This class collect all services, running, stopped and newly installed services


    def __init__(self,config, *args, **kwargs):
        common.AbstractWindowsCommand.__init__(self, config, *args, **kwargs)
    
    @staticmethod
    #The staticmethod is based on the original source

    def get_service_info(regapi):
        ccs = regapi.reg_get_currentcontrolset()
        key_name = "{0}\\services".format(ccs)
        info = {}
        for subkey in regapi.reg_get_all_subkeys(hive_name = "system", key = key_name):

            path_value = ""
            dll_value = ""

            image_path = regapi.reg_get_value(hive_name = "system", key = "", value = "ImagePath", given_root = subkey)
            if image_path:
                path_value = utils.remove_unprintable(image_path)

            for rootkey in regapi.reg_get_all_subkeys(hive_name = "system", key = "", given_root = subkey):
                if rootkey.Name == "Parameters":
                    service_dll = regapi.reg_get_value(hive_name = "system", key = "", value = "ServiceDll", given_root = rootkey)
                    if service_dll != None:
                        dll_value = utils.remove_unprintable(service_dll)
                    break

            info[utils.remove_unprintable(str(subkey.Name))] = (dll_value, path_value)

        return info
     
     
    def calculate(self):
          
        addr_space = utils.load_as(self._config)
        tasks = win32.tasks.pslist(addr_space)
        scanner = svcscan.SvcScan(self._config)
        
        for service in scanner.calculate():
            yield service

              
    def render_text(self, outfd, data):
        
        serviceDict = defaultdict(list)
        
        #this is for the ServiceDLL data
        regapi = registryapi.RegistryApi(self._config)
        info = self.get_service_info(regapi)
        
        outfd.write("\n")
        outfd.write("------- service check -------- \n\n")
        numberOfServices = 0
        
        for rec in data:
            
            serviceInfo = []
            
            vals = info.get("{0}".format(rec.ServiceName.dereference()), None)

            serviceDict[str(rec.ServiceName.dereference())].append(str(rec.DisplayName.dereference()))
            serviceDict[str(rec.ServiceName.dereference())].append(str(rec.Type))
            serviceDict[str(rec.ServiceName.dereference())].append(str(rec.State))
            
            if vals:
                    serviceDict[str(rec.ServiceName.dereference())].append(str(vals[0]))
            else:
                    serviceDict[str(rec.ServiceName.dereference())].append("")

            numberOfServices += 1
        outfd.write("# of services: " + str(numberOfServices) +"\n\n" )
        
        locationString = str(conf.ConfObject.opts["location"]).rsplit('/',1)[1] + "_ServiceList"
        outfd.write("Storing ServiceList as \"" + locationString + "\"\n")  
        
        with open(locationString + '.p', 'wb') as fp:
            pickle.dump(serviceDict, fp)


            