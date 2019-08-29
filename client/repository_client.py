'''Entry point for Repository'''
from utils.utils import Utils
from repository.repository import Repository
if __name__ == '__main__':
    CONFIG = Utils().get_config_file('config.ini')
    REPOSITORY_URL = CONFIG.get('repository_client_parameters', 'repo_url')
    PUSHED_AT = CONFIG.get('repository_client_parameters', 'pushed_at')
    LAST_PAGE = CONFIG.get('repository_client_parameters', 'last_page')
    WATCHERS_COUNT = CONFIG.get('repository_client_parameters', 'watchers_count')
    FORKS_COUNT = CONFIG.get('repository_client_parameters', 'forks_count')
    OPEN_ISSUE = CONFIG.get('repository_client_parameters', 'open_issue_count')
    CONTRIBUTOR_URL = CONFIG.get('repository_client_parameters', 'contributor_url')
    Utils().user_path()
    REPOSITORY = Repository()
    LAST_PAGE = Utils().pagination('sjain3097', 'new')
    PUSHED_TIME = REPOSITORY.pushed_time(PUSHED_AT)
    OPEN_PR_COUNT = REPOSITORY.open_pr_count(REPOSITORY_URL, LAST_PAGE)
    WATCHERS_COUNT = REPOSITORY.watchers_count(WATCHERS_COUNT)
    FORKS_COUNT = REPOSITORY.get_forks_count(FORKS_COUNT)
    ISSUE_COUNT = REPOSITORY.get_open_issue_count(OPEN_ISSUE)
    TOTAL_CONTRIBUTOR_URL = REPOSITORY.total_contribution(LAST_PAGE, CONTRIBUTOR_URL)
    ACCEPTANCE_RATE = REPOSITORY.get_repo_probability(LAST_PAGE, REPOSITORY_URL)
