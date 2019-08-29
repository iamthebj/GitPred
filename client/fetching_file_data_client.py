'''client for fetching file extraction'''
import json
from fetching_file_data.fetching_file_data import Fetch_file
from utils.utils import Utils
from search.search import Search

if __name__ == '__main__':
    UTILS_OBJ = Utils()
    CONFIG = UTILS_OBJ.get_config_file('config.ini')
    OWNER = CONFIG.get('Repository', 'owner')
    REPOSITORY_NAME = CONFIG.get('Repository', 'repository_name')
    FETCH_OBJ = Fetch_file()
    SEARCH_KEYWORD = CONFIG.get('Search', 'search_keyword')
    owner_repositories = Search.search(SEARCH_KEYWORD)
    for i in owner_repositories:
        owner_name = i["owner_name"]
        repository_name = i["repository_name"]
        data_frame = FETCH_OBJ.json_to_csv(owner_name, repository_name)
