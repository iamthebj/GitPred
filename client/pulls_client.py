""" client module"""
from pulls.pulls import Pulls
from utils.utils import Utils
if __name__ == '__main__':
    UTILS_OBJ = Utils()
    CONFIG = UTILS_OBJ.get_config_file('config.ini')
    PULLS_CLIENT_URL = CONFIG.get('client_url', 'pulls_client_url')
    CREATED_AT = CONFIG.get('pulls_client_parameters', 'created_at')
    CLOSED_AT = CONFIG.get('pulls_client_parameters', 'closed_at')
    STATE = CONFIG.get('pulls_client_parameters', 'state')
    COMMIT = CONFIG.get('pulls_client_parameters', 'commit')
    CHANGED_FILE = CONFIG.get('pulls_client_parameters', 'changed_file')
    CONTRIBUTOR_URL = CONFIG.get('pulls_client_parameters', 'contributor_url')
    LAST_PAGE = CONFIG.get('pulls_client_parameters', 'last_page')
    USER = CONFIG.get('pulls_client_parameters', 'user')
    UTILS_OBJ.user_path()
    PULLS_OBJ = Pulls()
    PULLS_OBJ.get_commits(COMMIT)
    PULLS_OBJ.created_time(CREATED_AT, STATE)
    PULLS_OBJ.get_changed_files(CHANGED_FILE)
    PULLS_OBJ.closed_pull_request_time(CREATED_AT, CLOSED_AT)
    PULLS_OBJ.test_total_contribution(LAST_PAGE, CONTRIBUTOR_URL, USER)
