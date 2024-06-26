# -*- coding: utf-8 -*-
import sys
import datetime
import cv2
import numpy as np
import os
import face_recognition
from PyQt5.QtGui import QImage
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer, QDate
from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtWidgets import QApplication, QLabel





image_folder = 'C:/Users/berika/PycharmProjects/PYQT/images'
class Window(QWidget):
    # -*- coding: utf-8 -*-
    def __init__(self):
        super().__init__()

        

        # window
        self.setWindowTitle("Face Recognition")
        layout = QVBoxLayout(self)

        self.frame_label = QLabel(self)
        self.frame_label.setMinimumSize(1150, 800)
        #self.frame_label.setMaximumSize(1150, 800)
        layout.addWidget(self.frame_label)

        

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 840)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 680)

        

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(30)

        
        
        """
        self.zaman_timer = QTimer()
        self.zaman_timer.timeout.connect(self.zaman)
        self.zaman_timer.start(1000)"""
        self.label_tarih = QLabel(self)
        self.label_saat = QLabel(self)
        self.label_isim = QLabel(self)

        self.yuzLabel()
        self.baslik()
        self.yuzAra()
        self.labelTarih()
        self.labelIsim()
        #self.face_rec()  # face_rec fonksiyonunu başlat
        #self.updateFrame()

        
        
        self.encoding_dict = {}  # Yüz kodlarını içeren sözlük
        self.loadEncodings()
    def loadEncodings(self):
        # -*- coding: utf-8 -*-
        for image_name in os.listdir(image_folder):
            if image_name.endswith('.jpg') or image_name.endswith('.png') :
                image_path = os.path.join(image_folder, image_name)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                name = os.path.splitext(image_name)[0]
                self.encoding_dict[name] = encoding

        
        
        
        

    
    
    def updateFrame(self):
        # -*- coding: utf-8 -*-
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(frame_rgb)
            face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                if len(self.encoding_dict) == 0:
                    break

                matches = face_recognition.compare_faces(list(self.encoding_dict.values()), face_encoding)

                name = "UNKNOWN"

                face_distances = face_recognition.face_distance(list(self.encoding_dict.values()), face_encoding)
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = list(self.encoding_dict.keys())[best_match_index]
            
                face_names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                cv2.rectangle(frame_rgb, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame_rgb, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165, 0), 2)
                

                self.isim_value_label.setText(name)

            frame_qimage: QImage = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
            frame_pixmap = QPixmap.fromImage(frame_qimage)
            self.frame_label.setPixmap(frame_pixmap.scaled(self.frame_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.zaman()

    def labelTarih(self):
        tarih_label = QLabel("Tarih: ", self)
        tarih_label.resize(50, 200)
        tarih_label.move(700, 100)
        self.label_tarih = QLabel(self)
        self.label_tarih.resize(200, 200)
        self.label_tarih.move(750, 100)
        self.label_tarih.setStyleSheet("color: green;font-size: 20px;")

        self.label_saat = QLabel("Saat: ",self)
        self.label_saat.resize(200, 200)
        self.label_saat.move(700, 150)
        self.label_saat = QLabel(self)
        self.label_saat.resize(200, 200)
        self.label_saat.move(750, 150)
        self.label_saat.setStyleSheet("color: green;font-size: 20px;")

    def zaman(self):
        now = QDate.currentDate()
        current_date = now.toString("ddd dd MMMM yyyy")
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.label_tarih.setText(current_date)
        self.label_saat.setText(current_time)


    def labelIsim(self):
        # -*- coding: utf-8 -*-
        self.isim_label = QLabel("İsim: ", self)
        self.isim_label.resize(50, 200)
        self.isim_label.move(700, 200)
        self.isim_value_label = QLabel("UNKNOWN", self)
        self.isim_value_label.resize(250, 200)
        self.isim_value_label.move(750, 200)
        self.isim_label.setStyleSheet("color: black")  # Label rengini turuncu olarak ayarla
        self.isim_value_label.setStyleSheet("color: green;font-size: 20px;")
        font = QFont()  # Uygun bir font oluşturun
        font.setPointSize(12)  # Örnek olarak punto boyutunu ayarlayın
        self.isim_value_label.setFont(font)



        # show gui
        self.show()

    def yuzAra(self):
        solButon = QPushButton("Yüz Ara", self)
        solButon.resize(450, 25)
        solButon.move(25, 700)
        solButon.clicked.connect(self.solTik)
        sagButon: QPushButton = QPushButton("Kapat", self)
        sagButon.resize(450, 25)
        sagButon.move(500, 700)
        sagButon.clicked.connect(self.close)

    def solTik(self):
        message_box = QMessageBox()
        #print("Yüz aranıyor...")
        message_box.setText("Şu anda yüz arama işlemindesiniz.")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.setDefaultButton(QMessageBox.Ok)
        choice = message_box.exec_()

    def yuzLabel(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.frame_label = QLabel(self)
        self.frame_label.setGeometry(30, 140, 551, 361)

        #layout = QVBoxLayout(self)
        #layout.addWidget(self.frame_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(30)
        

        #yuz_label =  QLabel("shfgsdhfdsh               xvcxcbbbbbbb                    dxbfbfdndfnd000000000", self)
        #yuz_label.resize(10, 50)
        #yuz_label.move(10, 20)
        #font = yuz_label.font()
        #font.setPointSize(10)
        #yuz_label.setFont(font)
        #yuz_label.setGeometry(30, 140, 551, 361)

        
    def closeEvent(self, event):
        self.cap.release()
        event.accept()
    


    def baslik(self):
        baslik_label = QLabel("YÜZ TANIMA SİSTEMİ", self)
        baslik_label.setGeometry(370, 30, 401, 51)
        font = baslik_label.font()
        font.setPointSize(16)
        font.setBold(True)
        baslik_label.setFont(font)
        baslik_label.setStyleSheet("color: orange;")
        
        
    
    
    """
    def face_rec(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(frame_rgb)  # Yüz konumlarını tespit et

        # Tespit edilen yüz konumlarına çerçeve ekle
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame_rgb, (left, top), (right, bottom), (0, 0, 255), 2)

        # PyQt5 QLabel'e çerçeveli kareyi ekle
            frame_qimage = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
            frame_pixmap = QPixmap.fromImage(frame_qimage)
            self.frame_label.setPixmap(frame_pixmap.scaled(self.frame_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # Belirli bir süre sonra tekrar face_rec fonksiyonunu çağır
        QTimer.singleShot(30, self.face_rec)"""




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())



# Şimdiye kadar adele buffon ve angelina jolşe,pogba,lukaku,mane,umtiti,şaban
# ramos,oneal,barış,winnick takıldı