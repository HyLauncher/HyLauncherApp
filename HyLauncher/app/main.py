
from msilib.schema import Error
import sys
import logging
import subprocess
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from functools import partial
import threading
import getpass
import utilities as ut
import get_deps as gd


USER = getpass.getuser()

CURRENT_PATH = os.getcwd()

def c_typ():
    import ctypes
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HyLauncher")
        c_typ()
        self.setWindowIcon(QtGui.QIcon(r'{}\app\src\icon.png'.format(CURRENT_PATH)))
        self.setWindowFlags(QtCore.Qt.Window)
        width = 1000
        height = 500

          
        # setting  the fixed width of window
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.MC_path = r'C:\Users\{}\AppData\Roaming\.minecraft'.format(USER)

        self.good_version = '1.18.2-40.1.0'
  
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets(self):
        self.widgets = {}
        self.widgets['user_lbl'] = QtWidgets.QLabel("Username") 
        self.widgets['username'] = QtWidgets.QLineEdit("Haarrii") 
        self.widgets['server_lbl'] = QtWidgets.QLabel("Server") 
        self.widgets['server'] = QtWidgets.QLineEdit("Lagunaak.aternos.me") 
        self.widgets['launch_btn'] = QtWidgets.QPushButton("Jugar!")  

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout()
        user_lyt = QtWidgets.QHBoxLayout()
        server_lyt = QtWidgets.QHBoxLayout()
        
        user_lyt.addWidget(self.widgets.get('user_lbl'))
        user_lyt.addWidget(self.widgets.get('username'))

        server_lyt.addWidget(self.widgets.get('server_lbl'))
        server_lyt.addWidget(self.widgets.get('server'))

        # for w  in self.widgets:
        #     main_layout.addWidget(self.widgets.get(w))
        main_layout.addLayout(user_lyt)
        main_layout.addLayout(server_lyt)

        main_layout.addWidget(self.widgets.get('launch_btn'))

        self.setLayout(main_layout)

        
    def create_connections(self):
        self.widgets.get('launch_btn').clicked.connect(self.launch)

    def launch(self):
        logger.info('Check Minecraft folders...')
        version_checked = ut.check_version(self.MC_path, self.good_version)
        if version_checked:
            logger.info('Checked!')
        else:
            logger.info('Minecraft default version not installed, installing...')
            ut.download_deault_version(self.MC_path, CURRENT_PATH)
            logger.info('Installed!')

        logger.info('Checking and downloading new mods...')
        gd.get_deps()
        logger.info('All syncronized!')

        logger.info('Applying resource pack in option file')
        ap_u = ut.apply_resources(self.MC_path)
        if ap_u:
            logger.info('Applyed correctly!')
        else:
            logger.warning('Not minecraft installed yet')

        set_username = self.widgets.get('username').text()
        set_server = self.widgets.get('server').text()
        version = ut.get_version(self.good_version)


        self.command = partial(ut.get_command, self.good_version, set_username, set_server)()
        
        logger.info(f'Executing Minecraft Version {version} with Username {set_username}')
        logger.info(f'Command: {self.command}')
        t=threading.Thread(target=self.launch_thread)

        logger.info('Closing Launcher')
        self.close()
        t.start()
        


    def launch_thread(self, *args):
        subprocess.call(self.command)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()






