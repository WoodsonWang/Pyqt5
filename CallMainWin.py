"""
@author:Wang Xinsheng
@File:CallMainWin.py
@description:...
@time:2020-10-25 23:59
"""
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox,QMenu,QFileDialog
from PyQt5.QtGui import QCursor
from view.mainview import *
from PyQt5.QtCore import  QStringListModel,QThread,pyqtSignal ,QPoint,Qt
import sys,os
from Music.getmusic import *
def get_music_list(search_content,source_count):
    music_list = []
    result = req_get(search_content,source=source_count)
    print(result)
    load = ast.literal_eval(result)
    for item in load:
        # print(item)
        music = Music()
        music.id = item['id']
        music.artist = item['artist']
        music.source = item['source']
        music.name = item['name'] + '---' + ",".join(music.artist)
        music_list.append(music)

    return music_list


class MyMainView(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        # python2 中的写法，等同于   super().__init__(parent)
        super(MyMainView,self).__init__(parent)
        super().setupUi(self)
        # self.setupUi(self)
        # 获取当前工作路径
        self.path = os.getcwd()
        self.slm = QStringListModel()
        self.qlist = []
        self.slm.setStringList(self.qlist)
        self.musicListView.setModel(self.slm)
        self.searchBtn.setStyleSheet('''QPushButton{background:#F7667;border-radius:5px;}''')

        self.searchBtn.clicked.connect(self.search_music)

        self.musicListView.clicked.connect(self.clickItem)
        self.musicListView.setContextMenuPolicy(Qt.CustomContextMenu)
        # listview 右键点击事件
        self.musicListView.customContextMenuRequested[QPoint].connect(self.listWidgetContext)

        # 选择存储文件夹
        self.selectFolder.triggered.connect(self.selectFolderAction)

        # 选择歌曲源

        self.sourceBox.addItems(['网抑云','QQ','虾米','酷狗','百度'])


    def selectFolderAction(self):
        directory = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        self.path = directory
        # 当窗口非继承QtWidgets.QDialog时，self可替换成 None
        print(directory)


    def listWidgetContext(self):
        popMenu = QMenu(self.musicListView)
        popMenu.addAction("下载",self.downloadMusic)
        popMenu.addAction("查看",self.getInfo)
        popMenu.exec_(QCursor.pos())

    def getInfo(self):
        QMessageBox.information(self, 'ListWidgets', "你选择了{}".format(self.musicListView.currentIndex().row()))


    def clickItem(self,qModelIndex):
        QMessageBox.information(self,'ListWidgets',"你选择了{}".format(self.slm.stringList()[qModelIndex.row()]))


    def search_music(self):
        '''创建线程'''
        # strip 去除字符串的前后空格
        search_content = self.musicEdit.text().strip()
        if not search_content:
            self.showMessage("请输入搜索内容！！！")
        else:
            self.back_task = BackTaskThread(search_content,self.sourceBox.currentIndex())
            # 连接信号
            self.back_task.update_music_list.connect(self.update_music_list)
            # 开始线程
            self.back_task.start()

    def update_music_list(self,music_list):

        '''根据返回结果更新UI界面'''
        self.music_list = music_list
        self.slm.removeRows(0,self.slm.rowCount())
        for music in music_list:
            row = self.slm.rowCount()
            self.slm.insertRow(row)

            self.slm.setData(self.slm.index(row),music.name)
        #
    def downloadMusic(self):
        # 获取现在选择的列表中的第几个
        row = self.musicListView.currentIndex().row()
        print(row)
        music = self.music_list[row]
        self.download_music_task = DownloadMusicThread(self.path,music.name,music.id,music.source)
        # self.download_music_task.download_music.connect(lambda : self.showMessage("下载完成!!!"))
        self.download_music_task.download_music.connect(self.updateProgressBar)
        self.download_music_task.start()



    def showMessage(self, message):
        QMessageBox.information(self,'ListWidgets',message)


    def updateProgressBar(self,progress):
        if progress == -1:
            '''无法下载删除这个条目'''
            row = self.musicListView.currentIndex().row()
            # 删除该元素
            self.music_list.remove(self.music_list[row])
            self.slm.removeRow(row)
            button = QMessageBox.warning(self, "Warning", "恢复出厂设置将导致用户数据丢失，是否继续操作？",
                                         QMessageBox.Reset | QMessageBox.Help | QMessageBox.Cancel, QMessageBox.Reset)
        else:
            self.progressBar.setValue(progress)



class BackTaskThread(QThread):
    update_music_list = pyqtSignal(list)

    def __init__(self,content,scource_count):
        super().__init__()
        self.search_content = content
        self.source_count = scource_count
        print(content)


    def run(self) -> None:

        music_list = get_music_list(self.search_content,self.source_count)

        self.update_music_list.emit(music_list)

class DownloadMusicThread(QThread):
    download_music = pyqtSignal(int)

    def __init__(self,path,name,id,source):
        super().__init__()
        self.music_name = name + '.mp3'
        self.music_id = id
        self.music_source = source
        self.path = path
        print( self.music_source, self.music_name,self.music_id)


    def run(self) -> None:

        music_url,music_size = get_download_url(self.music_id,self.music_source)
        if music_size == 0:
            self.download_music.emit(-1)
        else:
            print(music_url)
            download_file(self.path,music_url,music_size,self.music_name,self.download_music)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainView()
    myWin.setStyleSheet("#MainWindow{background-color:#FF9933}")
    myWin.show()
    sys.exit(app.exec_())