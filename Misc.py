#### ProjectTitle: TBD
#### File: Misc.py
#### Created By: Kyle Nicol on 03/21/2018

import logging
from logging.handlers import RotatingFileHandler
from logging import getLogger, basicConfig, WARNING, INFO, DEBUG, LoggerAdapter

from contextlib import contextmanager
from inspect import currentframe, getouterframes
####################################
class Message:
    def __init__(self, fmt ,args):
        self.fmt = fmt
        self.args = args

    def __str__(self):
        return self.fmt.format(*self.args)

class StyleAdapter(LoggerAdapter):
    def __init__(self, logger, opt=None):
        super(StyleAdapter, self).__init__(logger, opt or {})

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg,kwargs = self.process(msg,kwargs)
            self.logger._log(level, Message(msg,args), (), **kwargs)

def get_logger(name=None):
    return StyleAdapter(getLogger(name))

def get_key_value(dict,key):

    if key in dict.keys():
        return(dict[key])
    else:
        return(None)

class _NO_DEFAULT:
    def __repr__(self):
        return("<No Default Assignment>")

@contextmanager
def let(**bindings):
    frame = getouterframes(currentframe(), 2)[-1][0] # 2 because first frame in `contextmanager` decorator  
    locals_ = frame.f_locals
    original = {var: locals_.get(var) for var in bindings.keys()}
    locals_.update(bindings)
    yield
    locals_.update(original)
