import urllib.request
import os
import zipfile

def download(data_path):
    url = "https://bai-scieval.duiopen.com/bai-scieval.zip"
    save_path = data_path + "/bai-scieval.zip"
    unzip_path = data_path
    
    if not os.path.isdir(unzip_path):
        os.mkdir(unzip_path)

    try:
        urllib.request.urlretrieve(url, save_path)
    except:
        print("download failed!")
        return False
        
    #开始解压
    #判断是否是压缩文件
    if zipfile.is_zipfile(save_path):
    #读取压缩文件
        fz = zipfile.ZipFile(save_path, 'r')
    #提取文件到解压目录
        for file in fz.namelist():
            fz.extract(file, unzip_path)
    else:
    #否则返回失败
        return False
    return True