#coding: utf-8

import os
import hashlib
import sys

def md5sum(fname):
    if not os.path.isfile(fname):
        return u"错误：文件路径不存在或不是文件！"
    try:
        f = file(fname, 'rb')
    except:
        return u"错误：文件无法打开！"
    m = hashlib.md5()
    # 大文件处理
    while True:
        d = f.read(8096)
        if not d:
            break
        m.update(d)
    ret = m.hexdigest()
    f.close()
    return ret

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(u"错误：请输入文件路径！")
        sys.exit(1)
    filepath = sys.argv[1]
    print(md5sum(filepath))
