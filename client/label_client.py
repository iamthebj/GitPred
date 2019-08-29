'''Entry point for label class'''
from labels.label import Label
from utils.utils import Utils
if __name__ == '__main__':
    UTILS_OBJ = Utils()
    CONFIG = UTILS_OBJ.get_config_file('config.ini')
    PULLS_CLIENT_URL = CONFIG.get('client_url', 'pulls_client_url')
    UTILS_OBJ.user_path()
    Label().get_label(PULLS_CLIENT_URL)
