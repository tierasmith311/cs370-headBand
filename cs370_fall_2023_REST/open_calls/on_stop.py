from flask import request, g #imports the request object and g object                                  
from tools.logging import logger #we import a logger object
from neurosdk.cmn_types import * 

def handle_request():
    if g.hb == None: #in python none represents a lack of a value or object
        return ["Data Flowing"]

    g.hb.exec_command(SensorCommand.CommandStopSignal)
    return ["Data Flowing"]
#
#create a new file in the directory and call that file called on_stop()
    #we can copy that file call that file using this command