import requests

params = {

}
data = {
    "pageNo": 2,
    "pageSize": 20,
    "zym": None,
    "office.id": None,
    "cd": None,
    "zyglbm.id": None,
    "zydlId": None
}
header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50'
}

resp = requests.post("http://www.nimrf.net.cn/ept/treeList", data=data,headers=header,
                     verify=False, timeout=10)
print(resp.text)
