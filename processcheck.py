import volatility.plugins.common as common
import volatility.utils as utils
import volatility.win32.tasks as tasks
import os
import markup
import cPickle as pickle
import volatility.conf as conf #to get the location

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class processcheck(common.AbstractWindowsCommand):
    """experimental plugin alpha"""

    def __init__(self,config, *args, **kwargs):
        common.AbstractWindowsCommand.__init__(self, config, *args, **kwargs)
        self._config.add_option('NAME', short_option = 'n', default = None,
                                help = 'Process name to match',
                                action = 'store', type = 'str')
    def calculate(self):
        kernel_space = utils.load_as(self._config)
        
        #This should be collected from online eks r0ar.net/memory/whitelist.txt
        #check for efficiency stuff - process slow atm
        whitelist = open('/Users/Lunde/Documents/mrwhite.txt').read().splitlines()
        matchlist = []

        for line in whitelist:
            for process in tasks.pslist(kernel_space):
                if(str(line) == str(process.ImageFileName)):
                    matchlist.append(line)
        
        matchlist = sorted(set(matchlist))
        for process in tasks.pslist(kernel_space):
            if(str(process.ImageFileName) not in matchlist):
                yield process
            #if (not self._config.NAME or self._config.NAME.lower() == str(process.ImageFileName).lower()):
        
        #create_html()        
            
    def render_text(self, outfd, data):
        outfd.write("\n")
        outfd.write("------- Processlist dump -------- \n\n")
        self.table_header(outfd, [("Offset", "[addrpad]"),
                                  ("Process", "20"),
                                  ("Pid", "8")])
        
        
        items = []
        offsets = []
        prosessNames = []
        
        for process in data:
            self.table_row(outfd, process.obj_offset, 
                                  process.ImageFileName, process.UniqueProcessId)
            items.append(str(process.ImageFileName))
            offsets.append(str(process.UniqueProcessId))
       
        print items 
        #storing the data
        locationString = str(conf.ConfObject.opts["location"]).rsplit('/',1)[1] + "_processlist"
        outfd.write("Storing the processlist as \"" + locationString + "\"\n")  
        with open(locationString + '.p', 'wb') as fp:
            pickle.dump(items, fp)
        
        
        
        
        
        
        
        
        
        
        
        
        