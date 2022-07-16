from PyQt5 import QtWidgets, uic ,QtGui,QtCore
import sys
import api as f
import DES as des
import string
from flask import Flask, request,current_app
from handler import validate_encrypt_request
import netifaces
import requests


class Server_Worker(QtCore.QObject):
    res = QtCore.pyqtSignal(dict)
    app = Flask(__name__)

    def __init__(self):
        super().__init__()    
     
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    

    @app.route('/encrypt', methods=['POST'])
    def encrypt():
        requestJson = request.get_json()
        validate_encrypt_request(requestJson)
        sender = requestJson['sender']
        algorithm = requestJson['algorithm']
        message = requestJson['message']
        key = requestJson['key']
        typed = requestJson['type']
        print(requestJson)
        current_app.config['obj'].res.emit(requestJson)
        return requestJson
        
    def run(self):
            self.app.config['obj'] = self
            self.app.run(host='0.0.0.0',port=3000)
    

class Ui2(QtWidgets.QMainWindow):

    def __init__(self,data,parent):
        super(Ui2, self).__init__()
        uic.loadUi('u2.ui', self)

        self.parent = parent
        self.data = data

        print(self.data)

        self.loading_gif = QtGui.QMovie("Loading_2.gif") 
        self.spin.setMovie(self.loading_gif)       

        


        self.reff_btn.setIcon(QtGui.QIcon())
        self.reff_gif = QtGui.QMovie("spin-icon-2.gif") 
        self.reff_gif.frameChanged.connect(lambda: self.reff_btn.setIcon(QtGui.QIcon(self.reff_gif.currentPixmap())))
        self.reff_gif.start()
        self.reff_gif.stop()
        
        
        self.stackedWidget.setCurrentWidget(self.main_page) 
        self.user_list.clear()

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        
        self.user_list.clear()
        try:
            self.peer_data = []
            self.peer_data = self.request(self.data['sender'])
            print(self.peer_data)
            self.user_list.addItems(self.get_list_of_names())
        except:
            self.peer_data = []
        
               
        if len(self.peer_data) != 0:
                self.user_list.setCurrentRow(0)
                self.submit.setEnabled(True)
        else:
               self.submit.setEnabled(False)


        self.submit.clicked.connect(self.sub)
        self.cancel.clicked.connect(self.can)
        self.reff_btn.clicked.connect(self.Refresh)
        
    def get_list_of_names(self):
        list_of_users = []
        for user in self.peer_data:
                list_of_users.append(user['name'])
        
        return list_of_users
    
    def get_user_ip_by_name(self,name):
        ip = ''

        for user in self.peer_data:
                if name == user['name']:
                        ip = user['ip']
        return ip

    def sub(self):
        if self.user_list.currentRow() == -1:
            raise Exception('no user online')
        else:
            self.stackedWidget.setCurrentWidget(self.wating_page) 
            self.loading_gif.start()
            index = self.user_list.currentRow()
            
            ip = self.get_user_ip_by_name(self.user_list.item(index).text())
            
            try:
                code = self.send_data(ip,self.data['sender'],self.data['algo'],self.data['msg'],self.data['key'])
            except:
                code = -1
            
            self.stackedWidget.setCurrentWidget(self.res_page)
            if code == 200:
                    pixmap = QtGui.QPixmap('s.svg')
                    self.res.setPixmap(pixmap)
                    self.res_text_lab.setText('All good')
            else:
                    pixmap = QtGui.QPixmap('f.svg')
                    self.res.setPixmap(pixmap)
                    self.res_text_lab.setText('something went wrong...')
            
   
    def can(self):
        self.close() 
    
    def Refresh(self):
        self.reff_gif.start()               
        self.user_list.clear()
        self.reff_btn.setEnabled(False)
        print('Refresh')
        
        try:
            self.peer_data = []
            self.peer_data = self.request(self.data['sender'])
            print(self.peer_data)
            self.user_list.addItems(self.get_list_of_names())
        except:
            self.peer_data = []            

        if len(self.peer_data) != 0:
                self.user_list.setCurrentRow(0)
                self.submit.setEnabled(True)
        else:
               self.submit.setEnabled(False)
        self.reff_gif.stop()
        self.reff_btn.setEnabled(True)
    
    def get_gatway_ip(self):
        try:
                gateways = netifaces.gateways()
                defaults = gateways.get("default")
                return defaults[2][0]
        except:
                raise Exception('make sure you are online...')
     
    def request(self,name):
        data = {'name':name,'active':True}
        try:
                x = requests.post(f"http://{self.get_gatway_ip()}:3000/get-peers",json=data)
                if x.status_code == 200:
                        return x.json()
                else:
                        return []
        except Exception as e:
                print(e)
                return []

    def send_data(self,ip,sender,algo,msg,key):
        data = {"sender": sender ,"algorithm": algo ,"message": msg ,"key": key ,"type": "encrypt"}
        url = f'http://{ip}:3000/encrypt'
        try:
                x = requests.post(url, json=data)
                return x.status_code
        except Exception as e:
                print(e)
                return -1

class Ui(QtWidgets.QMainWindow):
   
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('u1.ui', self)
        self.active_style = '''QPushButton{
        background-color:rgb(255, 255, 255); 
        color: rgb(17, 17, 29);       
        font: 75 16pt "Segoe UI";
        border-radius: 10px;
        font-weight: bold;}'''
        self.not_active_style = '''QPushButton{
                font: 75 16pt "Segoe UI";
                background-color:rgb(17, 17, 29);
                color:rgb(255, 255, 255);
                border-radius: 10px;
                font-weight: bold;
                }
                QPushButton:hover{
                background-color:rgb(29, 27, 48);
                }
                QPushButton:pressed{
                background-color:rgb(255, 255, 255);
                color: rgb(17, 17, 29);
                padding-left:5px;
                padding-top:5px;
                background-position:calc(100% - 10px)center;
                }'''
         
        self.text_in.setAcceptRichText(False)
        self.text_in.textChanged.connect(lambda : self.share.hide())

        self.key_c.setValidator(QtGui.QIntValidator())
        self.key_v.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-z]+")))
        self.key_t.setValidator(QtGui.QIntValidator())
        self.key_s.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-z]+")))
        # self.key_d.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-z]+")))
        self.key_d.setMaxLength(8)

        self.btn_caesar.clicked.connect(self.caesar_even)
        self.btn_vigenere.clicked.connect(self.vigenere_even)
        self.btn_transpose.clicked.connect(self.transpose_even)
        self.btn_substitution.clicked.connect(self.substitution_even)
        self.btn_des.clicked.connect(self.des_even)
        

        self.r_attack_v.clicked.connect(self.change_validateur)
        self.r_decode_v.clicked.connect(self.change_validateur)
        self.r_encode_v.clicked.connect(self.change_validateur)

        self.ecode_decod_c.clicked.connect(self.caesar_action)
        self.ecode_decod_v.clicked.connect(self.vigenere_action)
        self.ecode_decod_t.clicked.connect(self.transpose_action)
        self.ecode_decod_s.clicked.connect(self.substitution_action)
        self.ecode_decod_d.clicked.connect(self.des_action)
        
        self.ecode_decod_c.setToolTip('Click to Encrypt/Decrypt')
        self.ecode_decod_v.setToolTip('Click to Encrypt/Decrypt/Attack')
        self.ecode_decod_t.setToolTip('Click to Encrypt/Decrypt')
        self.ecode_decod_s.setToolTip('Click to Encrypt/Decrypt')

        self.server_worker = Server_Worker()
        self.thread = QtCore.QThread()

        self.server_worker.moveToThread(self.thread)
        self.thread.started.connect(self.server_worker.run)
        self.server_worker.res.connect(self.p)
        self.thread.start()


        self.share.setIcon(QtGui.QIcon('share.png'))
        self.share.clicked.connect(self.fun_share)


        map_text_to_number_map_number_to_text = f.gen_alpha_map()
        self.map_text_to_number = {}
        self.map_number_to_text = {} 
        
        self.map_text_to_number.update(map_text_to_number_map_number_to_text[0]) 
        self.map_number_to_text.update(map_text_to_number_map_number_to_text[1])


        self.username = 'Yacine Ammari'

        self.user_name.setText(self.username)

        self.caesar_even()


        self.data_to_send = {'sender':self.username,'algo':'','msg':'','key':''}

        self.request(self.data_to_send['sender'])

        

        self.show()

    def change_validateur(self):
    
        if self.r_attack_v.isChecked():
                self.key_v.setValidator(QtGui.QIntValidator())
                self.key_v.setText('')
                self.key_v.setPlaceholderText('Only Numbers Allowed ...') 
        else:
                self.key_v.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-z]+")))
                self.key_v.setText('')
                self.key_v.setPlaceholderText('Only Letter Allowed...') 
    #=====================side btn events=======================
    
    def caesar_even(self):
        self.btn_caesar.setStyleSheet(self.active_style)
        self.btn_vigenere.setStyleSheet(self.not_active_style)
        self.btn_transpose.setStyleSheet(self.not_active_style)
        self.btn_substitution.setStyleSheet(self.not_active_style)
        self.btn_des.setStyleSheet(self.not_active_style)
        self.btn_p2p.setStyleSheet(self.not_active_style)
        self.stackedWidget.setCurrentWidget(self.caesar_p)
        self.stackedWidget_2.setCurrentWidget(self.algo_page)
        self.text_in.setText('')
        self.text_out.setText('')
        self.key_c.setText('')
        self.share.hide()        
        self.data_to_send = {'sender':self.username,'algo':'ceasar','msg':'','key':''}

    def vigenere_even(self):
        self.btn_caesar.setStyleSheet(self.not_active_style)
        self.btn_vigenere.setStyleSheet(self.active_style)
        self.btn_transpose.setStyleSheet(self.not_active_style)
        self.btn_substitution.setStyleSheet(self.not_active_style)
        self.btn_des.setStyleSheet(self.not_active_style)
        self.btn_p2p.setStyleSheet(self.not_active_style)
        self.stackedWidget.setCurrentWidget(self.vigenere_p)
        self.stackedWidget_2.setCurrentWidget(self.algo_page)
        self.text_in.setText('')
        self.text_out.setText('')
        self.key_v.setText('')
        self.share.hide()
        self.data_to_send = {'sender':self.username,'algo':'vigenere','msg':'','key':''}

    def transpose_even(self):
        self.btn_caesar.setStyleSheet(self.not_active_style)
        self.btn_vigenere.setStyleSheet(self.not_active_style)
        self.btn_transpose.setStyleSheet(self.active_style)
        self.btn_substitution.setStyleSheet(self.not_active_style)
        self.btn_des.setStyleSheet(self.not_active_style)
        self.btn_p2p.setStyleSheet(self.not_active_style)
        self.stackedWidget.setCurrentWidget(self.transpose_p)
        self.stackedWidget_2.setCurrentWidget(self.algo_page)
        self.text_in.setText('')
        self.text_out.setText('')
        self.key_t.setText('')
        self.share.hide()
        self.data_to_send = {'sender':self.username,'algo':'transposition','msg':'','key':''}
        
    def substitution_even(self):
        self.btn_caesar.setStyleSheet(self.not_active_style)
        self.btn_vigenere.setStyleSheet(self.not_active_style)
        self.btn_transpose.setStyleSheet(self.not_active_style)
        self.btn_substitution.setStyleSheet(self.active_style)
        self.btn_des.setStyleSheet(self.not_active_style)
        self.btn_p2p.setStyleSheet(self.not_active_style)
        self.stackedWidget.setCurrentWidget(self.substitution_p)
        self.stackedWidget_2.setCurrentWidget(self.algo_page)
        self.text_in.setText('')
        self.text_out.setText('')
        self.key_s.setText('')
        self.share.hide()
        self.data_to_send = {'sender':self.username,'algo':'substitution','msg':'','key':''}

    def des_even(self):
        self.btn_caesar.setStyleSheet(self.not_active_style)
        self.btn_vigenere.setStyleSheet(self.not_active_style)
        self.btn_transpose.setStyleSheet(self.not_active_style)
        self.btn_substitution.setStyleSheet(self.not_active_style)
        self.btn_des.setStyleSheet(self.active_style)
        self.btn_p2p.setStyleSheet(self.not_active_style)
        self.stackedWidget.setCurrentWidget(self.des_p)
        self.stackedWidget_2.setCurrentWidget(self.algo_page)    
        self.text_in.setText('')
        self.text_out.setText('')
        self.key_d.setText('')
        self.share.hide()
        self.binary_e.setChecked(True)
    
    #============================================

    def get_gatway_ip(self):
        try:
                gateways = netifaces.gateways()
                defaults = gateways.get("default")
                return defaults[2][0]
        except:
                raise Exception('make sure you are online...')

    def request(self,name):
        data = {'name':name,'active':True}
        try:
                x = requests.post(f"http://{self.get_gatway_ip()}:3000/get-peers",json=data)
                if x.status_code == 200:
                        return x.json()
                else:
                        return []
        except Exception as e:
                print(e)
                return []
   
    #===================cipher btn actions=========================

    def caesar_action(self):
        if self.r_encode_c.isChecked():
                encode = True
        else:
                encode = False
        
        text = f.stander_text("".join(self.text_in.toPlainText().split()))
        if (len(text) == 0 or len(text.replace(' ','')) == 0) :
                self.text_out.setText('Text can\'t be empty.')
                return
        
        
        key = f.stander_text("".join(self.key_c.text().split()))
        if (len(key) == 0 or len(key.replace(' ','')) == 0) :
                self.text_out.setText('Key can\'t be empty.')
                return
        self.data_to_send = {'sender':self.username,'algo':'ceasar','msg':'','key':''}
        
        

        if encode:
            t = f.encode_caesar(text,int(key),self.map_text_to_number,self.map_number_to_text)
            self.text_out.setText(t)
            self.data_to_send['msg'] = t
            self.data_to_send['key'] = int(key)
            self.share.show()
            
        else:
            self.text_out.setText(f.decode_caesar(text,int(key),self.map_text_to_number,self.map_number_to_text))

    def vigenere_action(self):
        encode = None
        attack = False
        if self.r_encode_v.isChecked():
                encode = True
        elif self.r_decode_v.isChecked():
                encode = False
        else:
                attack = True
        
        text = f.stander_text("".join(self.text_in.toPlainText().split()))
        if (len(text) == 0 or len(text.replace(' ','')) == 0) :
                self.text_out.setText('Text can\'t be empty.')
                return
        
        # get the key 
        key = f.stander_text("".join(self.key_v.text().split()))
        if (len(key) == 0 or len(key.replace(' ','')) == 0) :
                self.text_out.setText('Key can\'t be empty.')
                return
        self.data_to_send = {'sender':self.username,'algo':'vigenere','msg':'','key':''}
        
        if attack == True:
                self.res_change(f.hack_viginner(text,int(key),self.map_text_to_number,self.map_number_to_text))

        else:
                if encode:
                        t = f.encode_vigenere(text,key,self.map_text_to_number,self.map_number_to_text)
                        self.text_out.setText(t)
                        self.data_to_send['msg'] = t
                        self.data_to_send['key'] = key
                        self.share.show()
                else:
                        self.text_out.setText(f.decode_vigenere(text,key,self.map_text_to_number,self.map_number_to_text))
                                     
    def transpose_action(self):
        if self.r_encode_t.isChecked():
                encode = True
        else:
                encode = False
        text = "".join(self.text_in.toPlainText().split())
        text = f.stander_text2(text)
        if (len(text) == 0 or len(text.replace(' ','')) == 0) :
                self.text_out.setText('Text can\'t be empty.')
                return
        
        
        key = f.stander_text("".join(self.key_t.text().split()))
        if (len(key) == 0 or len(key.replace(' ','')) == 0) :
                self.text_out.setText('Key can\'t be empty.')
                return
        self.data_to_send = {'sender':self.username,'algo':'transposition','msg':'','key':''}
        
        
        if encode:
            t = f.encode_Transposition(text.lower(),int(key))
            self.text_out.setText(t)
            self.data_to_send['msg'] = t
            self.data_to_send['key'] =  int(key)
            self.share.show()
        else:
            self.text_out.setText(f.decode_Transposition(text,int(key)).lower())

    def substitution_action(self):
        if self.r_encode_s.isChecked():
                encode = True
        else:
                encode = False
        
        text = f.stander_text("".join(self.text_in.toPlainText().split()))
        if (len(text) == 0 or len(text.replace(' ','')) == 0) :
                self.text_out.setText('Text can\'t be empty.')
                return
        
        
        key = (self.key_s.text()).lower()
        
        list_key = list(''.join([j for i,j in enumerate(key) if j not in key[:i]]))

        if len(list_key) !=26:
                self.text_out.setText('Ciphertext Alphabet must be of length 26 of unique charcters.')
                return
        
        alpha = list(string.ascii_lowercase)
        self.data_to_send = {'sender':self.username,'algo':'substitution','msg':'','key':''}
        
        
        if encode:
            alpha_map = {}
            for x in range(len(list_key)):
                alpha_map[alpha[x]] = list_key[x]
            t = f.encode_substitution(text,alpha_map)
            self.data_to_send['msg'] = t
            self.data_to_send['key'] = key
            self.text_out.setText(t)
            self.share.show()
        else:
            rev_alpha_map = {}
            for x in range(len(list_key)):
                rev_alpha_map[list_key[x]] = alpha[x]
            self.text_out.setText(f.decode_substitution(text,rev_alpha_map))
    
    def des_action(self):

        if self.r_encode_d.isChecked():
                encode = True
        else:
                encode = False
        
        text = self.text_in.toPlainText()
        if (len(text) == 0 or len(text.replace(' ','')) == 0) :
                self.text_out.setText('Text can\'t be empty.')
                return        
        
        key = self.key_d.text()
        if (len(key) == 0 or len(key.replace(' ','')) == 0) :
                self.text_out.setText('Key can\'t be empty.')
                return
        elif len(key) != 8:
                self.text_out.setText('Key Must be 8 charters Long.')
                return
        be = self.binary_e.isChecked()
        
        if encode:
            self.text_out.setText(des.des_encode(text,key,be))
        else:
            if self.check_bin(text):
                self.text_out.setText(des.des_decode(text,key))
            else:
                self.text_out.setText('in decoding DES text must be a String of 1 and 0 only...')
    
    #============================================
    def check_bin(self,text):
        char_bin = ['1','0']

        for c in text:
                if c not in char_bin:
                        return False
        
        return True
         
    #===================p2p actions=========================
    def fun_share(self): 
        self.window2 = Ui2(self.data_to_send,self)
        self.window2.show()         

    def p(self,val):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("A message was received")
        dlg.setText(f'a message was received from '+str(val['sender']) + ' do you want to see it?')
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dlg.setIcon(QtWidgets.QMessageBox.Question)
        button = dlg.exec()

        if button == QtWidgets.QMessageBox.Yes:
                val['message'] = val['message'].lower()
                
                self.res_p2p.setText('')
                self.btn_caesar.setStyleSheet(self.not_active_style)
                self.btn_vigenere.setStyleSheet(self.not_active_style)
                self.btn_transpose.setStyleSheet(self.not_active_style)
                self.btn_substitution.setStyleSheet(self.not_active_style)
                self.btn_des.setStyleSheet(self.not_active_style)
                self.btn_p2p.setStyleSheet(self.active_style)
                br = '\n'
                self.stackedWidget_2.setCurrentWidget(self.r_page)
                res = '=>Text Received:' + br +val['message'] + br + '=>Key: ' + str(val['key']) +br + '=>From: '+ str(val['sender'])+br +'=>Algorithm: '+str(val['algorithm'])+br+'=>Text Results: '+br


                if val['algorithm'] == 'ceasar':
                    res = res + (f.decode_caesar(val['message'],int(val['key']),self.map_text_to_number,self.map_number_to_text))
                elif val['algorithm'] == 'vigenere':
                         val['key'] = val['key'].lower()
                         res = res +(f.decode_vigenere(val['message'],val['key'],self.map_text_to_number,self.map_number_to_text))
                elif val['algorithm'] == 'substitution':
                    val['key'] = val['key'].lower()
                    rev_alpha_map = {}
                    alpha = list(string.ascii_lowercase)
                    list_key = list(''.join([j for i,j in enumerate(val['key']) if j not in val['key'][:i]]))
                    for x in range(len(list_key)):
                        rev_alpha_map[list_key[x]] = alpha[x]
                    res = res +(f.decode_substitution(val['message'],rev_alpha_map))
                elif val['algorithm'] =='transposition':
                     res = res +(f.decode_Transposition(val['message'],int(val['key']).lower()))
                                
                self.res_p2p.setText(res)
        else:
            pass
    
    def res_change(self,res):
        r = ''
        br = '------------------------'
        for elem in res:
                r = r + '\n' + elem[0]+'\n'+ 'probability of text been france: '+ str(elem[1])+'%'+ '\n' +'text: '+elem[2]+'\n'+br+'\n'
        self.text_out.setText(r)
         


if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = Ui()
        app.exec_()

