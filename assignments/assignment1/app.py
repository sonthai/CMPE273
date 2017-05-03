from flask import Flask
import base64
import re
import sys
import json
import urllib2

app = Flask(__name__)
git_repo = sys.argv[1]
@app.route("/v1/<filename>")
def get_content(filename):
    url = get_url(filename)
    file_content = get_file_content(url)
    return file_content

def get_file_content(url):
    response = urllib2.urlopen(url)
    if response.code == 200:
        data = json.loads(response.read())
        return base64.decodestring(data['content'])
    else:
        return "Failed to get latest commits."

def get_url(filename):
    #git_repo = app.config.get('git_repo')
    m = re.search('https://github.com/(.*)', git_repo)
    url = 'https://api.github.com/repos/' + m.group(1) + '/contents/' + filename
    return url

if __name__ == "__main__":
    #app.config['git_repo'] = sys.argv[1]
    app.run(debug=True, host='0.0.0.0')