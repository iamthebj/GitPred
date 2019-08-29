'''Getting the state for pulls (Accepted/Rejected)'''
import logging
from utils.utils import Utils
logger = Utils().user_path()
logging.basicConfig(filename=logger, level=logging.DEBUG)
class Label(object): #pylint: disable=too-few-public-methods
    '''Getting the state for pulls (Accepted/Rejected)'''
    def __init__(self):
        pass
    @classmethod
    def get_label(cls, state, merged_at):
        '''Getting the state for pulls'''
        label_dict = {}
        if (state == 'closed' and merged_at):
            label_dict['state'] = 'Accepted'
        elif (state == 'closed' and not merged_at):
            label_dict['state'] = 'Rejected'
        else:
            label_dict['state'] = 'Open'
        logging.debug("Labels :{} ".format(label_dict))
        return label_dict
