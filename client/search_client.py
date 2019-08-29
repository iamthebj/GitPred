'''Entry point for Search class'''
from search.search import Search
from utils.utils import Utils

if __name__ == '__main__':
    UTILS = Utils()
    CONFIG = UTILS.get_config_file('config.ini')
    SEARCH_KEYWORD = CONFIG.get('Search', 'search_keyword')
    UTILS.user_path()
    SEARCH = Search()
    SEARCH.search(search_keyword=SEARCH_KEYWORD)
    