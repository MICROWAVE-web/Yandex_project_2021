import random
import sys
import urllib.request

import requests
import validators
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QEventLoop, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QLabel, QVBoxLayout, QPushButton, \
    QApplication
from pytube import YouTube
from youtube_dl import YoutubeDL

from uiandpy import chooses
from uiandpy import downloading
from uiandpy import loading
from uiandpy import stylesearch
from uiandpy import stylesheets


class Social:
    def __init__(self, url=''):
        if validators.url(url):
            self.url = url
        self.youtubeDL = YoutubeDL

    def download(self, url, downloading_object, **kwargs):
        """
        Функция загрузки стримов,
        принимает url типа str
        & объект загрузки
        :return: Ничего не возвращает
        """
        ydl_opts = {
            'progress_hooks': [downloading_object.hook],
            'outtmpl': f'{DOWNLOAD_DIRECTORY}/{kwargs["name"]}.{kwargs["exc"]}'
        }
        with self.youtubeDL(ydl_opts) as ydl:
            ydl.download([url])


class Youtube(Social):
    def __init__(self, url=''):
        super().__init__(url)
        if validators.url(url):
            try:
                self.yt = YouTube(url)
            except Exception:
                self.yt = None
        else:
            self.yt = None

    def streams(self):

        return self.yt.streams.filter(progressive=True)

    def video_streams(self):
        return self.yt.streams.filter(type='video', mime_type='video/mp4',
                                      progressive=True).order_by('resolution')

    def audio_streams(self):
        return self.yt.streams.filter(type='audio', mime_type='audio/mp4').order_by('abr')

    def download(self, url, parant_object, **kwargs):
        pause(300)
        urllib.request.urlretrieve(url, f'{DOWNLOAD_DIRECTORY}/{kwargs["name"]}.{kwargs["exc"]}')
        parant_object.ui.progressBar.setValue(int(parant_object.simple_procent))


class VK(Social):
    def video_streams(self):
        output_streams = []
        with self.youtubeDL() as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            for stream in info_dict['formats']:
                if str(stream.get('format_id')).startswith('cache') or str(
                        stream.get('format_id')).startswith('url'):
                    output_streams.append(stream)
                elif stream.get('format_id') in [str(i) for i in range(1000)] and \
                        stream.get('ext') in ['m4a', 'mp4'] and stream.get('asr') and stream.get(
                    'fps') \
                        and not str(stream.get('format_id')).startswith('hls'):
                    output_streams.append(stream)
        return output_streams


class SoundCloud(Social):
    def audio_streams(self):
        output_streams = []
        with self.youtubeDL() as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            for stream in info_dict['formats']:
                if stream.get('format_id') == f'http_mp3_{stream.get("abr")}':
                    output_streams.append(stream)
        return output_streams


class FaceBook(Social):
    def streams(self):
        output_streams = []
        with self.youtubeDL() as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            if info_dict.get('entries'):
                for stream in info_dict['entries'][0]['formats']:
                    if stream.get('acodec') == 'mp4a.40.5':  # аудио дорожка
                        output_streams.append(stream)
                    elif stream.get('format_id') in ['dash_sd_src',
                                                     'dash_sd_src_no_ratelimit',
                                                     'sd']:  # Порядке возростания качества
                        output_streams.append(stream)
            else:
                for stream in info_dict['formats']:
                    if stream.get('acodec') == 'mp4a.40.5':  # аудио дорожка
                        output_streams.append(stream)
                    elif stream.get('format_id') in ['dash_sd_src',
                                                     'dash_sd_src_no_ratelimit',
                                                     'sd']:  # Порядке возростания качества
                        output_streams.append(stream)
        return output_streams

    def video_streams(self):
        output_streams = []
        with self.youtubeDL() as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            if info_dict.get('entries'):
                for stream in info_dict['entries'][0]['formats']:
                    if stream.get('format_id') in ['dash_sd_src',
                                                   'dash_sd_src_no_ratelimit',
                                                   'sd']:  # Порядке возростания качества
                        output_streams.append(stream)
            else:
                for stream in info_dict['formats']:
                    if stream.get('format_id') in ['dash_sd_src',
                                                   'dash_sd_src_no_ratelimit',
                                                   'sd']:  # Порядке возростания качества
                        output_streams.append(stream)
        return output_streams

    def audio_streams(self):
        output_streams = []
        with self.youtubeDL() as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            if info_dict.get('entries'):
                for stream in info_dict['entries'][0]['formats']:
                    if stream.get('acodec') == 'mp4a.40.5':  # аудио дорожка
                        output_streams.append(stream)
            else:
                for stream in info_dict['formats']:
                    if stream.get('acodec') == 'mp4a.40.5':  # аудио дорожка
                        output_streams.append(stream)
        return output_streams


DOWNLOAD_DIRECTORY = 'downloads'

SOCIAL_LIST = {
    'FaceBook': (['fb.watch', 'www.facebook.com'], FaceBook, ['', 'icons/facebook.png']),
    'SoundCloud': (['soundcloud.com'], SoundCloud, ['', 'icons/soundcloud.png']),
    'VK': (['vk.com'], VK, ['', 'icons/vk.png']),
    'Youtube': (['youtu.be', 'www.youtube.com'], Youtube, ['', 'icons/youtube.png'])
}


def pause(val):
    loop = QEventLoop()
    QTimer.singleShot(val, loop.quit)
    loop.exec_()


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('icons/logo.svg'))
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.windowses = {}
        self.register(Introducing(), "intro")
        self.register(Search(), "search")
        self.register(Loading(), "loading")
        self.register(Chooses(), 'chooses')
        self.register(Downloading(), 'downloading')
        self.goto("intro")
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(200)
        self.opening()

    def register(self, widget, name):
        self.windowses[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.windowses:
            widget = self.windowses[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())

    def opening(self):
        try:
            self.animation.finished.disconnect(self.close)
        except Exception:
            pass
        self.animation.stop()
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def ending(self, close=False):
        self.animation.stop()
        if close:
            self.animation.finished.connect(self.close)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()


class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class Introducing(PageWindow):
    def __init__(self):
        super(Introducing, self).__init__()
        self.ui = stylesheets.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.5)
        self.setWindowTitle("Linker Beta — Intro")
        self.ui.label_2.setPixmap(QtGui.QPixmap("icons/logo.svg"))
        self.initUI()

    def initUI(self):
        self.ui.pushButton.clicked.connect(self.go_next_search)

    def go_next_search(self):
        _parent_window.ending()
        self.goto("search")
        _parent_window.opening()


class Search(PageWindow):
    def __init__(self):
        super().__init__()
        self.opacity_effect = QGraphicsOpacityEffect()
        self.previous = 'nothing :)'
        self.ui = stylesearch.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.soc_icon = QLabel()
        self.ui.soc_icon.move(-80, 10)

        self.ui.soc_icon.setMaximumWidth(60)
        self.ui.soc_icon.setMaximumHeight(60)
        self.ui.soc_icon.setScaledContents(True)
        self.anim = QPropertyAnimation(self.ui.soc_icon, b'pos')
        self.anim.setEasingCurve(QEasingCurve(QEasingCurve.OutBounce))
        self.anim.setDuration(1500)
        self.anim.setStartValue(QtCore.QPoint(-80, 10))
        self.anim.setEndValue(QtCore.QPoint(380, 10))
        self.setWindowTitle("Linker Beta — Search")
        self.link = ''
        self.initUI()

    def initUI(self):
        self.ui.lineEdit.textChanged.connect(
            lambda: self.social_icons_animation(self.ui.lineEdit.text()))
        self.ui.pushButton.clicked.connect(self.go_next_chooses)
        self.ui.pushButton_2.clicked.connect(self.go_back_intro)
        self.opacity_effect.setOpacity(0.5)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton.setGraphicsEffect(self.opacity_effect)

    def social_icons_animation(self, text):
        for soc in SOCIAL_LIST.keys():
            for domain in SOCIAL_LIST[soc][0]:
                if domain in text and self.previous not in domain:
                    for i in reversed(range(self.ui.horizontalLayout.count())):
                        self.ui.horizontalLayout.itemAt(i).widget().setParent(None)
                    self.ui.horizontalLayout.addWidget(self.ui.soc_icon)
                    self.ui.soc_icon.setPixmap(QPixmap(SOCIAL_LIST[soc][-1][-1]))
                    self.anim.start()
                    self.previous = domain
                    break
                elif text == '':
                    for i in reversed(range(self.ui.horizontalLayout.count())):
                        self.ui.horizontalLayout.itemAt(i).widget().setParent(None)
                    self.previous = 'nothing :)'
        try:
            response = requests.head(text)
            if response.status_code == 200 or 303:
                self.ui.label_2.setText('')
                self.opacity_effect.setOpacity(1)
                self.ui.pushButton.setEnabled(True)
                self.ui.pushButton.setGraphicsEffect(self.opacity_effect)
                self.link = text
            else:
                self.ui.label_2.setText('Введённая ссылка не действительна! ')
                self.opacity_effect.setOpacity(0.5)
                self.ui.pushButton.setEnabled(False)
                self.ui.pushButton.setGraphicsEffect(self.opacity_effect)
                self.link = ''
        except Exception:
            self.ui.label_2.setText('Ошибка доступа к ресурсу - измените ссылку')
            self.opacity_effect.setOpacity(0.5)
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton.setGraphicsEffect(self.opacity_effect)
            self.link = ''

    def go_next_chooses(self):
        _parent_window.ending()
        self.goto("loading")
        _parent_window.opening()
        _parent_window.windowses['loading'].start_search_streams(self.link)

    def go_back_intro(self):
        _parent_window.ending()
        self.goto("intro")
        _parent_window.opening()


class Loading(PageWindow):
    def __init__(self):
        super().__init__()
        self.ui = loading.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Linker Beta — Loading")
        gif = QtGui.QMovie('icons/loading.gif')
        self.ui.label_2.setMovie(gif)
        self.ui.label_2.setScaledContents(True)
        self.ui.label_2.setStyleSheet('border-radius: 20px;')
        self.chosen_social = None
        gif.start()

    def start_search_streams(self, link: str):
        """
        Поиск и валидация стримов по ссылке
        """
        streams = []
        for soc in SOCIAL_LIST.keys():
            for domain in SOCIAL_LIST[soc][0]:
                if domain in link:
                    if soc == 'FaceBook':
                        social = FaceBook(link)
                        self.chosen_social = social
                        streams = list(social.streams())
                        break
                    elif soc == 'VK':
                        social = VK(link)
                        self.chosen_social = social
                        streams = list(social.video_streams())
                        break
                    elif soc == 'Youtube':
                        social = Youtube(link)
                        self.chosen_social = social
                        streams = list(social.video_streams()) + list(social.audio_streams())
                        break
                    elif soc == 'SoundCloud':
                        social = SoundCloud(link)
                        self.chosen_social = social
                        streams = list(social.audio_streams())
                        break
        if len(streams) == 0:
            self.ui.label_3.setText('Не удалось найти подходящий стрим, возвращаю...')
            loop = QEventLoop()
            QTimer.singleShot(5000, loop.quit)
            loop.exec_()
            _parent_window.ending()
            self.goto("search")
            _parent_window.opening()
        else:
            output = []
            for stream in streams:
                if stream.__class__.__name__ == 'Stream':
                    output.append(stream.__dict__)
                else:
                    output.append(stream)
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            _parent_window.windowses['chooses'].set_chooses(output, self.chosen_social)
            _parent_window.ending()
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec_()
            self.goto("chooses")
            _parent_window.opening()


class Chooses(PageWindow):
    def __init__(self):
        super().__init__()
        self.obj_chosen_social = None
        self.items = {}
        self.main_streams = []
        self.ui = chooses.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Linker Beta — Chooses")
        self.opacity_effect = QGraphicsOpacityEffect()
        self.vbox = QVBoxLayout()
        self.opacity_effect.setOpacity(0.5)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton.setGraphicsEffect(self.opacity_effect)
        self.ui.pushButton.clicked.connect(self.go_next_downloader)
        self.ui.pushButton_2.clicked.connect(self.go_back_search)

    def go_back_search(self):
        """
        Возвращение на экран ввода ссылки
        """
        _parent_window.ending()
        self.goto("search")
        _parent_window.opening()

    def set_chooses(self, streams: dict, obj_chosen_social):
        """
        Перебор словаря стримов, и вывод кнопок вариантов загрузки
        """
        self.obj_chosen_social = obj_chosen_social
        for index, stream in enumerate(streams):
            self.main_streams.append(stream)
            new_item = []
            for key in dict(stream).keys():
                if key == 'ext':
                    new_item.append(f' Тип - {stream["ext"]}')
                elif key == 'type':
                    new_item.append(f' Тип - {stream["type"]}')
                elif key == 'resolution' and str(stream["resolution"]).lower() != 'none':
                    new_item.append(f' Разрешение - {stream["resolution"]}')
                elif key == 'abr':
                    new_item.append(f' Битрейт - {stream["abr"]}')
                elif key == 'format':
                    new_item.append(f' Формат - {stream["format"]}')
                elif key == 'res':
                    new_item.append(f' Разрешение - {stream["res"]}')
                elif key == 'fps':
                    new_item.append(f' Кадр/сек - {stream["fps"]}')
                elif key == 'vcodec' and stream["vcodec"] != 'none':
                    new_item.append(f' Видео-кодек - {stream["vcodec"]}')
                elif key == 'acodec':
                    new_item.append(f' Видео-кодек - {stream["acodec"]}')
            self.items[index] = [QPushButton(str(', '.join(new_item))), False]
            self.items[index][0].setStyleSheet(
                '.QPushButton {color: black; padding: 20px; border-radius: 15px; background-color: '
                'rgb(255, 255, '
                '255);} .QPushButton:pressed {background-color: rgb(240,240,240);}')
            self.items[index][0].setObjectName(f'm_PushButton_{index}')
            self.items[index][0].clicked.connect(
                lambda ch, l_index=index: self.change_button_color(l_index))
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)
        for keys in self.items.keys():
            self.widget = QWidget()
            self.vbox.addWidget(self.items[keys][0])
            self.widget.setLayout(self.vbox)
            self.ui.scrollArea.setWidget(self.widget)

    def change_button_color(self, n: int):
        """
        Изменеие цвета кнопки на её нажатие, и отметка файла под 'скачивание'
        """
        if self.items[n][1]:
            self.items[n][1] = False
            self.items[n][0].setStyleSheet(
                '.QPushButton {color: black; padding: 20px; border-radius: 15px; background-color: '
                'rgb(255, 255, '
                '255);} .QPushButton:pressed {background-color: rgb(240,240,240);}')
        else:
            self.items[n][1] = True
            self.items[n][0].setStyleSheet(
                '.QPushButton {color: black; padding: 20px; border: 1px solid rgb(8,96,'
                '242); border-radius: 15px; '
                'background-color: rgb(255,255,255);} .QPushButton:pressed {background-color: rgb('
                '240,240,240);}')
        for key in self.items.keys():  # Переключение кнопки активное/пассивное состояние
            if self.items[key][1]:
                self.opacity_effect.setOpacity(1)
                self.ui.pushButton.setEnabled(True)
                self.ui.pushButton.setGraphicsEffect(self.opacity_effect)
                break
            self.opacity_effect.setOpacity(0.5)
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton.setGraphicsEffect(self.opacity_effect)

    def go_next_downloader(self):
        """
        Переход на страницу загрузки файлов
        """
        streams = []
        for key in self.items.keys():
            if self.items[key][1]:
                streams.append(self.main_streams[key])
        _parent_window.ending()
        self.goto("downloading")
        _parent_window.opening()
        _parent_window.windowses['downloading'].resetting()
        _parent_window.windowses['downloading'].downloading(streams, self.obj_chosen_social)


class Downloading(PageWindow):
    """
    Класс экрана скачивания файлов
    """

    def __init__(self):
        super().__init__()
        self.ui = downloading.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Linker Beta — Downloading")
        self.breaking_object = None
        self.ui.label_2.setPixmap(QtGui.QPixmap("icons/download.png"))
        self.ui.pushButton_2.clicked.connect(self.break_and_go_back_search)
        self.ui.pushButton_3.clicked.connect(self.go_back_search)
        self.ui.pushButton_3.hide()
        self.ui.pushButton_2.show()
        self.stop_downloading = False

    def downloading(self, streams, obj_chosen_social):
        """
        :param streams: Список стримов на скасивание
        :param obj_chosen_social: Объект необходимой соц. сети
        :return: Ничего не возвращает
        :
        Основная функция класса скачивания файлов,
        """
        self.stream_count = len(streams)
        self.simple_procent = 0
        code = random.choice([str(i) for i in range(100, 999)])
        for index, stream in enumerate(streams, start=1):
            if self.stop_downloading:
                print('breaking')
                break
            exc = 'mp4'
            typeS = 'video'
            if stream.get('type') == 'audio' or stream.get('ext') == 'mp3':
                exc = 'mp3'
                typeS = 'audio'
            self.simple_procent = round(index / self.stream_count, 2) * 100
            obj_chosen_social.download(stream.get('url'), self, name=f'{typeS}-{str(index)}-{code}',
                                       exc=exc)
        print('Successfully')
        self.ui.pushButton_3.show()
        self.ui.pushButton_2.hide()

    def hook(self, progress: dict):
        """
        :param progress: Словарь мета-данных загрузки
        :return: Ничего не возвращает
        :
        'Хукер' для отображения процентов загрузки файлов,
        (Работает, только с VK, Soundcloud и FaceBook)
        """
        if progress['status'] == 'finished':
            self.ui.progressBar.setValue(100)
            # что-то типа 'усешно'
        if progress['status'] == 'downloading':
            self.ui.progressBar.setValue(
                round(float(progress['_percent_str'].split('%')[0].strip())))
            pause(100)

    def resetting(self):
        """
        Сброс настроек & флагов при повторной загрузке в одном сеансе
        """
        self.ui.progressBar.setValue(0)
        self.ui.pushButton_3.hide()
        self.ui.pushButton_2.show()
        self.stop_downloading = False

    def break_and_go_back_search(self):
        """
        Функция для кнопки 'Отмена'

        Отмена загрузки следующего файла, и переход на страницу ввода ссылки
        """
        self.stop_downloading = True
        _parent_window.ending()
        self.goto("search")
        _parent_window.opening()

    def go_back_search(self):
        """
        Функция для кнопки 'Скачать ещё'

        Переход на страницу ввода ссылки после успешного сохранения файлов
        """
        _parent_window.ending()
        self.goto("search")
        _parent_window.opening()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    _parent_window = Window()
    _parent_window.setFixedSize(730, 459)
    _parent_window.show()
    sys.exit(app.exec_())
'''
ФИКС ЗАВИСАНИЯ ЭКРАНА ПРИ ЗАГРУЗКЕ!
'''
