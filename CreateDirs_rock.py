import os
import re

from bs4 import BeautifulSoup
from collections import defaultdict

"""
@author: lzw
@date: 2021-10-19
This Spider Program is adapted to NIMRF database website, so there are many module fit the website
therefore they maybe are not fit in other website. 
"""

header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
}

# start page have <div> with id=tree, class=ztree, get all <li>
def loadStartPage():
    return open("document2.html", encoding="utf-8").read()

def getDirTree(html, layers={}, key="class", pattern=r">(\S*\(\d+\))<", index=0):
    id = index
    sub = []
    if(index >= len(layers[key])):
        return None
    soup = BeautifulSoup(html, "lxml")
    # ith node
    tree = soup.find_all("li", {"class": layers[key][index]})
    layer = [re.search(string=str(t), pattern=pattern).group(1) for t in tree]
    for t in tree:
        node = getDirTree(str(t), layers=layers, index=id+1)
        sub+=node
    if sub is not []:
        layer.append(sub)
    return layer

# layer sequence to generate structure
def createDirPath(tree):
    for i in range(len(tree[0])):
        for k in range(len(tree[1][i])):
            tree[1][i][k] = tree[0][i]+'/'+tree[1][i][k]
            if not os.path.exists(tree[1][i][k]):
                pass
                #os.mkdir(tree[1][i][k])
    if type(tree[1][1][0]) == type([]):
        tree[1] = createDirPath(tree[1])
    else:
        tree[1] = once(tree[1])
    return tree


def once(tree):
    t = []
    for i in range(3):
        t.extend(tree[i])
    t = [t]
    t.append(tree[3])
    for i in range(len(t[0])):
        for k in range(len(t[1][i])):
            t[1][i][k] = t[0][i] + '/' + t[1][i][k]
            if not os.path.exists(t[1][i][k]):
                pass
                #os.mkdir(t[1][i][k])
    return t


# generate layer sequence
def dill_tree(tree):
    t = []
    a = []
    res = []
    for i in tree:
        if type(i) is not type([]):
            t.append(i)
        elif len(i) > 0:
            tree_s = i
            d = dill_tree(tree_s)
            if d != []:
                a.extend(d)
            if len(t) > 0:
                res.append(t)
            t = []
    if len(t) > 0:
        res.append(t)
    if len(a) > 0:
        res.append(a)
    return res

def get_leaf_dict():
    html_str = loadStartPage()
    tree = getDirTree(html_str, layers={"class": ["level0", "level1", "level2", "level3", "level4"]})
    tree = dill_tree(tree)
    #print(tree[1][1])
    tree = createDirPath(tree)
    res = {}
    for t in tree[1][1][1][::]:
        for e in t:
            res[e.split("/")[-1]] = "".join(e[0:len(e)-len(e.split("/")[-1])])
    return res

if __name__ == "__main__":
    res = get_leaf_dict()
    print(res)