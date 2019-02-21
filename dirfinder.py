import requests, os, argparse, re
from bs4 import BeautifulSoup
def regex(content):
    pattern = "(\"|')(\/[\w\d?\/&=#.!:_-]{1,})(\"|')"
    matches = re.findall(pattern, content)
    response = ""
    i = 0
    for match in matches:
        i += 1
        if i == len(matches):
            response += match[1]
        else:
            response += match[1] + "\n"
    return(response)
print("     _ _                              _____      \n  __| (_)_ __ ___  ___ _ __ __ _ _ __|___ / _ __ \n / _` | | '__/ __|/ __| '__/ _` | '_ \ |_ \| '__|\n| (_| | | |  \__ \ (__| | | (_| | |_) |__) | |   \n \__,_|_|_|  |___/\___|_|  \__,_| .__/____/|_|   \n                                |_|\n\n                        ~Cillian Collins\nOutput:")

parser = argparse.ArgumentParser(description='Extract GET parameters from javascript files.')
parser.add_argument('-u', help='URL of the website to scan.')
parser.add_argument('-o', help='Output file (for results).', nargs="?")
args = parser.parse_args()

linkArr = [args.u]
dirArr = []
url = args.u + "/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html5lib')
scripts = soup.find_all('script')
for script in scripts:
    try:
        if script['src'][0] == "/" and script['src'][1] != "/":
            script = url.split("/")[0:2] + script['src']
            linkArr.append(script)
        else:
            pass
    except:
        pass
for link in linkArr:
    res = requests.get(link)
    out = regex(res.text).split("\n")
    for line in out:
        pathArr = line.strip().split("/")
        if line[0] == "/" and line[1] == "/":
            pass
        else:
            path = ""
            for i in range(len(pathArr)):
                if i == len(pathArr) - 1:
                    if "." in pathArr[i]:
                        pass
                    else:
                         path += pathArr[i] + "/"
                else:
                    path += pathArr[i] + "/"
            if path != "/" and path != "//":
                dirArr.append(path.replace("//", "/").split("#")[0])
            else:
                pass

for directory in list(set(dirArr)):
    print(directory)
