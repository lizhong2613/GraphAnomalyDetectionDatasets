import json
import os.path
import sys
import urllib
import urllib2

import requests
from joblib import Parallel, delayed

from utils import read_file, append_list_to_csv


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


getter = requests.Session()


# keepalive_handler = HTTPHandler()
# opener = urllib2.build_opener(keepalive_handler)
# urllib2.install_opener(opener)


def list_to_string(str_list, delimiter=","):
    return delimiter.join(map(str, str_list))


def two_dimensional_list_to_string(my_list):
    str_list = []
    if isinstance(my_list[0], list):
        for row in my_list:
            str_list.append(list_to_string(row))
        my_list = str_list
    return list_to_string(my_list, "\n")


def get_webpage_source(url):
    page = urllib2.urlopen(url)
    return page.read()


def get_webpage_final_url(url):
    # start = time.clock()
    failed = 0
    while failed < 4:
        try:
            page = getter.head(url, allow_redirects='true')
            # print time.clock() - start
            return page.url, page.status_code
        except requests.ConnectionError as e:
            print(e.message)
            print("Error, Try:" + str(failed) + " ,URL: " + url)
    return None, None


def yql_url_builder(search_url):
    base_url = "http://query.yahooapis.com/v1/public/yql?q="
    url_prefix = "&format=json&diagnostics=true"
    query = urllib.quote("select href from html where url=" + "'" + search_url + "'")
    return base_url + query + url_prefix
    # http://query.yahooapis.com/v1/public/yql?q=select%20href%20from%20html%20where%20url=%27http%3A//goo.gl/Q5EgIz%27&format=json&diagnostics=true


def get_webpage_final_url_yql(url):
    query_result = get_webpage_source(yql_url_builder(url))
    response = json.loads(query_result)
    if "redirect" not in response["query"]["diagnostics"]:
        return ""
    redirect_route = response["query"]["diagnostics"]["redirect"]
    if "content" not in redirect_route:
        return redirect_route[len(redirect_route) - 1]["content"]
    else:
        return redirect_route["content"]


def append_to_file(data, path):
    f = open(path, 'a')
    f.write(data)
    f.close()


def write_to_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def append_url_record(response, result):
    if 'data' in response:
        response = (response['data'])[0]
    if len(result) == 0:
        result.append(response.keys())
    result.append(response.values())


def read_csv(file_path):
    return [line.strip().split(",") for line in read_file(file_path)]


def slice_csv(file_path):
    f = open(file_path, "rb")
    return set([line.strip().split(",")[0] for line in f])


def get_twitter_account_state(user_id):
    url = twitter_user_name_to_url(user_id)
    full_url = get_webpage_final_url(url[1])
    if full_url[1] == 200:
        # print(url)
        if "suspended" in full_url[0]:
            print(url[0], "Fake")
            return url[0], "Fake"
    elif full_url[1] == 404:
        print(full_url, "Not Found")
        return url[0], "Not Found"
    else:
        print(url)
        # time.sleep(sleep_time + random.randint(0, 10))


def batch_url_extractor(input_path, output_path):
    last_id = False
    if os.path.isfile(output_path):
        last_id = get_last_written_id(output_path)
    f = read_file(input_path)
    for line_count, link in enumerate(f):
        user_id = link[0].strip()
        if last_id == user_id:
            last_id = False
            break
    if last_id is False:
        processes = Parallel(n_jobs=4)(
            delayed(get_twitter_account_state)(user_id) for user_id in f)
        processes = [x for x in processes if x is not None]
        # if line_count % 10000 == 0:
        append_list_to_csv(output_path, processes)
        # write_to_file(output_path, two_dimensional_list_to_string(result))


def twitter_user_name_to_url(username):
    return username, "https://twitter.com/" + username


def get_last_written_id(file_path):
    for line in read_file(file_path):
        pass
    return line


if __name__ == '__main__':
    print("start")
    batch_url_extractor("twitter_nodes.csv", "fake_users.txt")
    # if len(sys.argv) == 3:
    # batch_url_extractor(sys.argv[2], sys.argv[3], 0)
    # else:
    #     print "Error: Please enter 2 parameters"
    """
    if len(sys.argv) == 4:
        if sys.argv[1] == "facebook":
            batch_share_extractor(get_url_share_count, sys.argv[2], sys.argv[3], 3)
        elif sys.argv[1] == "twitter":
            batch_share_extractor(get_url_twitt_count, sys.argv[2], sys.argv[3], 3)
    else:
        print "Error: Please enter 3 parameters"
    """
    print("finished")
    sys.exit(1)
