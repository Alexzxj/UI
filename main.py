import base64
import json

import shutil
from tornado.web import RequestHandler, Application, StaticFileHandler
import tornado.web
from tornado.ioloop import IOLoop
import zipfile, tarfile
from tornado.httpserver import HTTPServer
import os, time
from urllib import parse


ui_path = ''
static_ui_path = ''
model_name = ''
path = './cfg.json'
# file_name_dict = {
#     0: "其它",
#     1: "平台",
#     2: "华翔_MES"
# }


class uiServer(RequestHandler):
    @staticmethod
    def _inner():
        with open(path, 'r', encoding='utf-8')as f:
            return json.loads(f.read())
    def get(self, *args, **kwargs):
        upload = True
        with open(path, 'r', encoding='utf-8')as f:
            # file_name_dict = json.loads(f.read())
            file_name_dict = json.loads(f.read())
        self.render('index.html', datas=file_name_dict, con_list=[], dirs = "")

    def post(self):
        file_name_dict = self._inner()
        st = self.request.arguments['ST_TYPE'][0].decode()
        file = self.request.files.get('file')[0]
        name = file['filename']
        dir = file_name_dict[st]
        path_file = './ui/' + dir + '/' + name.split('.zip')[0]
        path_url = './ui/' + dir + '/'
        path = './file/' + dir + '/' + name
        if os.path.exists(path):
            os.remove(path)
        if os.path.isdir(path_file):
            shutil.rmtree(path_file)
            time.sleep(1)

        if os.path.isdir('./file/' + dir):
            pass
        else:
            os.mkdir('./file/' + dir)

        # 创建文件夹
        if os.path.isdir('./ui/' + dir):
            pass
        else:
            os.mkdir('./ui/' + dir)

        with open(path, 'wb') as f:
            f.write(file['body'])

        z = zipfile.ZipFile('./file/' + dir + '/' + name, 'r')
        for temp in z.namelist():
            z.extract(temp, './ui/' + dir + '/' + name.split('.zip')[0] + '/')
        z.close()



        url = '/index/path=' + path_url
        self.redirect(url)


class listServer(RequestHandler):
    @staticmethod
    def _inner():
        with open(path, 'r', encoding='utf-8')as f:
            return json.loads(f.read())

    def get(self, dir, *args, **kwargs):
        dir_name = ''
        name = ''
        dir = dir.split("/")
        file_name_dict = self._inner()
        if dir[2] == '':
            dir_name = file_name_dict["0"]
        else:
            dir_name = dir[2]
            name = dir[3]
        upload = False
        if dir_name not in file_name_dict.values():
            con_list = []
            f_list = []
            pass
        else:

            if os.path.isdir('./file/' + dir_name):
                con_list = []
                f_list = []
                pass
            else:
                os.mkdir('./file/' + dir_name)

            # 创建文件夹
            if os.path.isdir('./ui/' + dir_name):
                pass
            else:
                os.mkdir('./ui/' + dir_name)

            con_list = os.listdir('./file/' + dir_name)
            f_list = os.listdir('./ui/' + dir_name + '/')


        zname = name+'.zip'
        if name and zname in con_list and name not in f_list:
            # m = name.split('.')
            # fname = m[0]
            # # zip压缩文件
            # if m[-1].lower() == 'zip' and fname not in f_list:
            f_list.append(name)
            z = zipfile.ZipFile('./file/'+dir_name+'/'+zname, 'r')
            for temp in z.namelist():
                z.extract(temp, './ui/'+dir_name+'/'+name+'/')
            z.close()

            # tar压缩文件
            # elif m[1].lower() == 'tar' and m[0] not in f_list:
            #     f_list.append(m[0])
            #     try:
            #         tar = tarfile.open('./file/'+rt)
            #         names = tar.getnames()
            #         for name in names:
            #             tar.extract(name, './ui/'+m[0]+'/')
            #         tar.close()
            #     except:
            #         time.sleep(5)
            #         self.redirect('/')

            # 其他格式的文件
        else:
            pass
        self.render('list.html', ip =self.request.host_name, dirs=dir_name, con_list=sorted(f_list, reverse=False), upload=upload, datas=file_name_dict)

class addProject(RequestHandler):
    @staticmethod
    def _inner():
        with open(path, 'r', encoding='utf-8')as f:
            return json.loads(f.read())

    def post(self, *args, **kwargs):
        m = json.loads(self.request.body.decode())
        if m['val']:
            file_name_dict = self._inner()
            if m['val'] in file_name_dict.values():
                rep = json.dumps({
                    "errorCode": -2,
                    "errorMsg": "项目已存在"
                }, ensure_ascii=False)
            else:
                file_name_key = int(max(file_name_dict.keys())) + 1
                # file_name_dict[str(len(file_name_dict))] = m["val"]
                file_name_dict[str(file_name_key)] = m["val"]
                with open(path, 'w', encoding='utf-8')as f:
                    f.write(json.dumps(file_name_dict, ensure_ascii=False))
                rep = json.dumps({
                    "errorCode": 0,
                    "errorMsg": "创建成功"
                }, ensure_ascii=False)
        else:
            rep = json.dumps({
                "errorCode": -1,
                "errorMsg": "参数为空"
            }, ensure_ascii=False)
        self.write(rep)

class editProject(RequestHandler):
    @staticmethod
    def _inner():
        with open(path, 'r', encoding='utf-8')as f:
            return json.loads(f.read())

    def post(self, *args, **kwargs):
        m = json.loads(self.request.body.decode())
        file_name_dict = self._inner()
        if m['val']:
            if m['key'] in file_name_dict:
                dirname = file_name_dict[m['key']]
                file_name_dict[m['key']] = m["val"]
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(file_name_dict, ensure_ascii=False))

                d_list = m["val"].split("/")
                dir_path = './ui/' + dirname
                file_path = './file/' + dirname
                dst_dir_path = './ui/' + m["val"]
                file_dir_path = './file/' + m["val"]
                # 检查是否有此文件，有则修改
                try:
                    if os.path.isdir(dir_path):
                        os.rename(dir_path, dst_dir_path)
                        time.sleep(1)
                    if os.path.isdir(file_path):
                        os.rename(file_path, file_dir_path)
                        time.sleep(1)

                except:
                    req = {
                        "errorCode": -2,
                        "errorMsg": "删除失败！！"
                    }
                rep = {
                    "errorCode": 0,
                    "errorMsg": "修改成功"
                }
            else:
                rep = {
                    "errorCode": -1,
                    "errorMsg": "项目不存在"
                }
        else:
            rep = {
                "errorCode": -2,
                "errorMsg": "参数不存在"
            }

        self.write(json.dumps(rep, ensure_ascii=False))

class delProject(RequestHandler):
    @staticmethod
    def _inner():
        with open(path, 'r', encoding='utf-8')as f:
            return json.loads(f.read())

    def post(self, *args, **kwargs):
        m = json.loads(self.request.body.decode())
        file_name_dict = self._inner()
        if m['val'] and m['val'] in file_name_dict:
            val = file_name_dict[m["val"]]
            del file_name_dict[m["val"]]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(file_name_dict, ensure_ascii=False))

            dir_path = './ui/' + val
            zFile = './file/' + val
            down_project_path = './ui/download/project/' + val+".zip"
            down_history_path = './ui/download/history/' + val
            # 检查是否有此文件，有则删除
            try:
                if os.path.isdir(dir_path):
                    shutil.rmtree(dir_path)
                    time.sleep(1)
                if os.path.isdir(zFile):
                    shutil.rmtree(zFile)
                    time.sleep(1)
                if os.path.isfile(down_project_path):
                    os.remove(down_project_path)
                if os.path.isdir(down_history_path):
                    shutil.rmtree(down_history_path)
                    time.sleep(1)
            except:
                req = {
                    "errorCode": -2,
                    "errorMsg": "删除失败！！"
                }
            else:
                req = {
                    "errorCode": 0,
                    "errorMsg": "删除成功！！"
                }
        else:
            req = {
                "errorCode": -1,
                "errorMsg": "参数为空！！！"
            }
        self.write(json.dumps(req, ensure_ascii=False))

class listUIFile(RequestHandler):
    @staticmethod
    def _inner():
        with open(path, 'r', encoding='utf-8')as f:
            return json.loads(f.read())

    def get(self, dir, *args, **kwargs):
        dir_name = ''
        name = ''
        dir = dir.split("/")
        file_name_dict = self._inner()
        if dir[2] == '':
            dir_name = file_name_dict["0"]
        else:
            dir_name = dir[2]
            name = dir[3]

        if dir_name not in file_name_dict.values():
            con_list =[]
            f_list =[]
            pass
        else:
            if os.path.isdir('./file/' + dir_name):
                pass
            else:
                os.mkdir('./file/' + dir_name)

            # 创建文件夹
            if os.path.isdir('./ui/' + dir_name):
                pass
            else:
                os.mkdir('./ui/' + dir_name)

            con_list = os.listdir('./file/' + dir_name)
            f_list = os.listdir('./ui/' + dir_name + '/')


        #zname = name + '.zip'
        # if name and zname in con_list and name not in f_list:
        #     # m = name.split('.')
        #     # fname = m[0]
        #     # # zip压缩文件
        #     # if m[-1].lower() == 'zip' and fname not in f_list:
        #     f_list.append(name)
        #     z = zipfile.ZipFile('./file/' + dir_name + '/' + zname, 'r')
        #     for temp in z.namelist():
        #         z.extract(temp, './ui/' + dir_name + '/' + name + '/')
        #     z.close()
        #
        #     # 其他格式的文件
        # else:
        #     pass
        self.render('index.html', ip=self.request.host_name, dirs=dir_name,
                    con_list=sorted(f_list, reverse=False), datas=file_name_dict)

    def post(self):
        file_name_dict = self._inner()
        st = self.request.arguments['ST_TYPE'][0].decode()
        file = self.request.files.get('file')[0]
        name = file['filename']
        dir = file_name_dict[st]
        path_file = './ui/' + dir + '/' + name.split('.zip')[0]
        path_url = './ui/' + dir + '/'
        path = './file/' + dir + '/' +  name
        if os.path.exists(path):
            os.remove(path)
        if os.path.isdir(path_file):
            shutil.rmtree(path_file)
            time.sleep(1)

        if os.path.isdir('./file/' + dir):
            pass
        else:
            os.mkdir('./file/' + dir)

        # 创建文件夹
        if os.path.isdir('./ui/' + dir):
            pass
        else:
            os.mkdir('./ui/' + dir)

        with open(path, 'wb') as f:
            f.write(file['body'])
        z = zipfile.ZipFile('./file/' + dir + '/' + name, 'r')
        for temp in z.namelist():
            z.extract(temp, './ui/' + dir + '/' + name.split('.zip')[0] + '/')
        z.close()

        url = '/index/path=' + path_url
        self.redirect(url)

class delListInfo(RequestHandler):
    def post(self, *args, **kwargs):
        m = json.loads(self.request.body.decode())
        if m["val"]:
            d_list = m["val"].split("/")
            dir = d_list[0]
            file = d_list[1]
            dir_path = './ui/' + dir + '/' + file
            # zFile = './file/' + file + '.zip'
            # 检查是否有此文件，有则删除
            try:
                if os.path.isdir(dir_path):
                    shutil.rmtree(dir_path)
                    time.sleep(1)
                # if os.path.isfile(zFile):
                #     os.remove(zFile)
            except:
                req = {
                    "errorCode": -2,
                    "errorMsg": "删除失败！！"
                }
            else:
                req = {
                    "errorCode": 0,
                    "errorMsg": "删除成功！！"
                }
        else:
            req = {
                "errorCode": -1,
                "errorMsg": "参数为空！！！"
            }
        self.write(json.dumps(req, ensure_ascii=False))


class downloadAllFile(RequestHandler):
    def post(self, *args, **kwargs):
        m = json.loads(self.request.body.decode())
        if m["val"]:
            dir = m["val"]
            dir_path = './ui/' + dir

            try:
                get_files_path = dir_path  # 需要压缩的文件夹
                set_files_path = './ui/download/project/' + dir + '.zip'  # 存放的压缩文件地址(注意:不能与上述压缩文件夹一样)
                if os.path.isfile(set_files_path):
                    os.remove(set_files_path)
                compress(get_files_path, set_files_path)
            except:
                req = {
                    "errorCode": -2,
                    "errorMsg": "操作失败！！"
                }
            else:
                req = {
                    "errorCode": 0,
                    "errorMsg": "操作成功",
                    "request":{
                        "ip":self.request.host_name,
                        "url": '/download/project/' + dir + '.zip'
                    }
                }
        else:
            req = {
                "errorCode": -1,
                "errorMsg": "参数为空！！！"
            }
        self.write(json.dumps(req, ensure_ascii=False))

def compress(get_files_path, set_files_path):
    #压缩文件夹
    f = zipfile.ZipFile(set_files_path , 'w', zipfile.ZIP_DEFLATED )
    for dirpath, dirnames, filenames in os.walk( get_files_path ):
        fpath = dirpath.replace(get_files_path,'') #注意2
        fpath = fpath and fpath + os.sep or ''     #注意2
        for filename in filenames:
            f.write(os.path.join(dirpath,filename), fpath+filename)
    f.close()


class historyServer(RequestHandler):
    @staticmethod
    def _inner():
        with open(path, 'r', encoding='utf-8')as f:
            return json.loads(f.read())

    def get(self, dir, *args, **kwargs):
        dir = dir.split("/")
        file_name_dict = self._inner()
        if dir[2] == '':
            dir_name = file_name_dict["0"]
        else:
            dir_name = dir[2]
            name = dir[3]
        upload = False
        # 创建文件夹
        if os.path.isdir('./file/'+dir_name):
            pass
        else:
            os.mkdir('./file/'+dir_name)

        con_list = os.listdir('./file/'+dir_name+ '/')

        self.render('history.html', ip =self.request.host_name, dirs=dir_name, con_list=sorted(con_list, reverse=False), upload=upload, datas=file_name_dict)

class downloadZip(RequestHandler):
    #下载历史文件.zip
    def post(self, *args, **kwargs):
        m = json.loads(self.request.body.decode())
        if m["val"]:
            dir = m["val"]
            dir_path = './file/' + dir

            try:
                path = dir.split("/")[0]
                if os.path.isdir('./ui/download/history/'+path):
                    pass
                else:
                    os.mkdir('./ui/download/history/'+path)

                get_files_path = dir_path  # 需要压缩的文件夹
                set_files_path = './ui/download/history/' + dir  # 存放的压缩文件地址(注意:不能与上述压缩文件夹一样)
                if os.path.isfile(set_files_path):
                    os.remove(set_files_path)
                compress(get_files_path, set_files_path)
            except:
                req = {
                    "errorCode": -2,
                    "errorMsg": "操作失败！！"
                }
            else:
                req = {
                    "errorCode": 0,
                    "errorMsg": "操作成功",
                    "request":{
                        "ip":self.request.host_name,
                        "url": '/download/history/' + dir
                    }
                }
        else:
            req = {
                "errorCode": -1,
                "errorMsg": "参数为空！！！"
            }
        self.write(json.dumps(req, ensure_ascii=False))

class delZip(RequestHandler):
    def post(self, *args, **kwargs):
        m = json.loads(self.request.body.decode())
        if m["val"]:
            d_list = m["val"].split("/")
            dir = d_list[0]
            file = d_list[1]
            zFile = './file/'  + dir + '/'+ file
            # 检查是否有此文件，有则删除
            try:
                if os.path.isfile(zFile):
                    os.remove(zFile)
            except:
                req = {
                    "errorCode": -2,
                    "errorMsg": "删除失败！！"
                }
            else:
                req = {
                    "errorCode": 0,
                    "errorMsg": "删除成功！！"
                }
        else:
            req = {
                "errorCode": -1,
                "errorMsg": "参数为空！！！"
            }
        self.write(json.dumps(req, ensure_ascii=False))

settings = {
    'template_path': 'template',
    'static_path': 'static'
}



app = Application(
    [(r'/', uiServer),
     (r'/add', addProject),
     (r'/edit', editProject),
     (r'/delProject', delProject),
     (r'/index/(?P<dir>.*)', listUIFile),
     (r'/del', delListInfo),
     (r'/downloadAllFile', downloadAllFile),
     (r'/list', listServer),
     (r'/list/(?P<dir>.*)', listServer),
     (r'/history', historyServer),
     (r'/history/(?P<dir>.*)', historyServer),
     (r'/downloadZip', downloadZip),
     (r'/delZip', delZip)
     ], **settings)


if __name__ == '__main__':
    http = HTTPServer(app)
    http.listen(5555)
    IOLoop.current().start()

