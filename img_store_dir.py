from pathlib import Path
from tqdm import tqdm, trange

from NIMRF.src_id_search import search, get_cache
from monopt.find import find

root = Path('E:/数据/博物馆/博物馆标本照片')
new_root = Path('E:/数据/博物馆/岩石101403')


def redir(root: Path):
    count = 0
    # pbar = tqdm(root.glob("*"))
    # pbar: list[Path]
    for file in root.glob("*"):
        src_id = file.name.split('.')[0].split('-')[0]
        # 数据库搜索
        # res = find({'src_id': src_id})
        # 在线搜索
        res = search(src_id)
        if res:
            res = Path(res)
            # test_dir = Path(search(src_id))
            # test_dir = new_root / res['Class']['Class_of_3'] / res['Class']['Class_of_m'] / res['Class']['Class_of_n']
            if not res.exists():
                res.mkdir(parents=True, exist_ok=True)
            file.replace(res / file.name)


if __name__ == '__main__':
    #redir(root)
    #res = get_cache()
    #print(res)
    m = {'氧化物': 75, '硫酸盐': 21, '硅酸盐': 128, '氟化物': 8, '单质': 12, '碳酸盐': 34, '硫化物': 60, '磷酸盐': 8, '钨酸盐': 1, '氧化物和氢氧化物': 1, '铬酸盐': 1, '氢氧化物': 0, '硼酸盐': 11, '钼酸盐': 0, '碲化物': 0}
    for k,v in m.items():
        m[k] += 1
    print(m)
