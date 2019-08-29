from fetching_data.fetching_data import Fetch
from utils.utils import Utils
import json
if __name__ == '__main__':
    UTILS_OBJ = Utils()
    CONFIG = UTILS_OBJ.get_config_file('config.ini')
    OWNER = CONFIG.get('Repository', 'owner')
    REPOSITORY_NAME = CONFIG.get('Repository', 'repository_name')
    FETCH_OBJ=Fetch()
    feature_data = FETCH_OBJ.fetching_data({})
    
    # SEARCH_KEYWORD = CONFIG.get('Search','search_keyword')
    # data_frame = FETCH_OBJ.multiple_repository_to_dataframe(SEARCH_KEYWORD)
    # FETCH_OBJ.dataframe_to_csv(data_frame)
