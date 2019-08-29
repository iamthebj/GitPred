import requests
from urllib import request
import lizard
from utils.utils import Utils
import os

merge_file = []
commit_file_data = []
counter = 0
changed_lines = 0
file_dict_critical = {}
file_dict1_non_critical = {}
config = Utils().get_config_file('config.ini')
user_id = config.get('GithubCredential', 'user_id', raw=True)
password = config.get('GithubCredential', 'password')
requests_commit = config.get('commit_api', 'commit_url')
requests_merged = config.get('merge_api', 'merge_url')

res_merge_files = requests.get(requests_merged, auth=(user_id, password))
temp_dir_complexity = config.get('temp_directory', 'temp_dir')


class commit:
    """
        create the dictionary
    """
    lizard_dict = {}
    lines_data = []

    def commit_files(self, file_names_commit, count, res_commit_api, filename=None):
        """
        :param file_name1:
        :param count:
        :param res_commit_api:
        :param filename:
        :return:
        """
        # print (file_name1)
        for files_info in res_commit_api['files']:
            if files_info['filename'] == file_names_commit:
                raw_url = ((files_info['raw_url']))
                response = request.urlopen(raw_url)
                data_file = (response.read())
                data_file = data_file.decode()
                commit_file_data.append(data_file)
                commit.lines_data = commit_file_data[count].rsplit('\n')

    def lizard(self, file_names_commit, res_commit_api):
        """
        :param file_name1:
        :param res_commit_api:
        :return:
        """
        print(file_names_commit)
        for file_data in res_commit_api['files']:
            if file_data['filename'] == file_names_commit:
                file_url = ((file_data['raw_url']))
                filename, file_extension = os.path.splitext(file_url)
                # print(filename +' '+ file_extension)
                response = request.urlopen(file_url)
                html = response.read()
                html = html.decode()
                full_path = temp_dir_complexity + file_extension
                with open(full_path, 'w') as file_path:
                    print(html, file=file_path)
                lizard_analyzer = lizard.analyze_file(full_path)
        try:
            commit.lizard_dict = lizard_analyzer.function_list[0].__dict__
            os.remove(full_path)
        except:
            print('Code not generic so no complexity')
            pass

    def repo_files(self, file_names_commit):
        """
        :param file_name1:
        :return:
        """
        response_file = requests.get(requests_merged + "/" + file_names_commit, auth=(user_id, password))
        for file_data in response_file:
            merge_file.append(file_data.decode())
        self.merge_file_lines = merge_file[0].rsplit('\n')

    def cmp_file(self, file):
        """
        :param file:
        :return:
        """
        complex_key = "cyclomatic_complexity"
        nonchanged_lines = 0

        for line_data in commit.lines_data:
            for merge_lines in self.merge_file_lines:
                if line_data == merge_lines:
                    if line_data == '' or merge_lines == '':
                        pass
                    else:
                        nonchanged_lines += 1
                else:
                    pass
        perc_change_files = ((len(commit.lines_data) - nonchanged_lines)/(len(self.merge_file_lines) - nonchanged_lines))
        del commit.lines_data[:]
        if perc_change_files > 25:
            ret_val = []
            ret_val.append("critical")
            ret_val.append(perc_change_files)
            if complex_key in commit.lizard_dict:
                complexity = complex_key + " : " + str(commit.lizard_dict[complex_key])
            else:
                complexity = complex_key + " : 0"
            ret_val.append(complexity)
            file_dict_critical[file] = ret_val
        """
        else:
            ret_val = []
            ret_val.append("Non-critical")
            ret_val.append(perc_change_files)
            if complex_key in commit.temp1:
                complexity = complex_key + " : " + str(commit.temp1[complex_key])
            else:
                complexity = complex_key + " : 0"
            ret_val.append(complexity)
            file_dict_critical[file] = ret_val
        """


class api_call(commit):
    """
    commit file criticality
    """
    file_names = []
    count = 0

    def postman(self,res_commit_api):
        """
        :param res_commit_api:
        :return:
        """
        for files in res_commit_api['files']:
            self.file_names.append(files['filename'])
        class_obj = commit()
        for files in self.file_names:
            class_obj.commit_files(files, self.count, res_commit_api)
            self.count += 1
            class_obj.repo_files(files)
            class_obj.lizard(files, res_commit_api)
            class_obj.cmp_file(files)

    def critical_files(self):
        """
        :return:
        """
        print(file_dict_critical)
        return (file_dict_critical)


def main(url):
    """
    :param url:
    :return:
    """
    #res_commit_api = requests.get(url,auth=(user_id, password)).json()
    res_commit_api = requests.get(url,auth=(user_id, password)).json()
    apicall_obj = api_call()
    apicall_obj.postman(res_commit_api)
    critical_dict = apicall_obj.critical_files()
    return critical_dict


if __name__ == "__main__":
    url = 'https://api.github.com/repos/rishab2611/project1/commits/rish4'
    main(url)
