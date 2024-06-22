import json
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtGui
import os

class fenprincipale(QMainWindow):
    def __init__(self):
        super(fenprincipale, self).__init__()
        self.setWindowIcon(QtGui.QIcon('Slorpy.ico'))

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.ouvrir_nouvel_onglet)
        self.tabs.currentChanged.connect(self.update_url_barre)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.fermer_onglet)

        self.setCentralWidget(self.tabs)
        self.showMaximized()

        # Navbar:
        navbar = QToolBar()
        self.addToolBar(navbar)

        accueil_btn = QAction('Accueil', self)
        accueil_btn.triggered.connect(self.url_accueil)
        navbar.addAction(accueil_btn)

        retour_btn = QAction('Retour', self)
        retour_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(retour_btn)

        rafraichir_btn = QAction('Rafraîchir', self)
        rafraichir_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(rafraichir_btn)

        avancer_btn = QAction('Avancer', self)
        avancer_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(avancer_btn)

        historique_btn = QAction('Historique', self)
        historique_btn.triggered.connect(self.afficher_historique)
        navbar.addAction(historique_btn)

        self.url_barre = QLineEdit()
        self.url_barre.returnPressed.connect(self.navigation)
        navbar.addWidget(self.url_barre)

        self.ouvrir_nouvel_onglet()

    def url_accueil(self):
        self.tabs.currentWidget().setUrl(QUrl('http://google.com'))

    def navigation(self):
        url = self.url_barre.text()
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, url):
        self.url_barre.setText(url.toString())
        self.ajouter_historique(url)

    def update_url_barre(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl)

    def ajouter_historique(self, url):
        historique = []
        historique_path = os.path.expanduser('~/.historique.json')
        if os.path.exists(historique_path):
            with open(historique_path, 'r') as f:
                try:
                    historique = json.load(f)
                except json.JSONDecodeError:
                    historique = []

        domaine = QUrl(url).host().replace('www.', '').split('.')[0]
        historique.append(domaine)
        with open(historique_path, 'w') as f:
            json.dump(historique, f)

    def afficher_historique(self):
        historique_window = QDialog(self)
        historique_window.setWindowTitle('Historique')
        layout = QVBoxLayout()

        historique_list = QListWidget()
        historique_path = os.path.expanduser('~/.historique.json')
        if os.path.exists(historique_path):
            with open(historique_path, 'r') as f:
                try:
                    historique = json.load(f)
                    for site in historique:
                        historique_list.addItem(site)
                except json.JSONDecodeError:
                    pass

        layout.addWidget(historique_list)
        historique_window.setLayout(layout)
        historique_window.exec_()

    def ouvrir_nouvel_onglet(self, i=-1):
        if i == -1:
            navigateur = QWebEngineView()
            navigateur.setUrl(QUrl('http://google.com'))
            i = self.tabs.addTab(navigateur, "Nouvel Onglet")
            self.tabs.setCurrentIndex(i)
            navigateur.urlChanged.connect(self.update_url)

    def fermer_onglet(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

app = QApplication(sys.argv)
QApplication.setApplicationName('Slorpy')
fenetre = fenprincipale()
app.exec()
