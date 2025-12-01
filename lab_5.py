# audio_player_with_time.py
import os
import sys
import ctypes

def find_qt_plugins():
    """Найти путь к плагинам Qt"""
    search_paths = [
        r"C:\Users\{}\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\PyQt5\Qt5\plugins".format(os.getenv('USERNAME')),
        os.path.join(sys.prefix, "Lib", "site-packages", "PyQt5", "Qt5", "plugins"),
        os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "PyQt5", "Qt5", "plugins"),
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            print(f"Найден путь к плагинам: {path}")
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = path
            return path
    
    print("Не удалось найти плагины Qt автоматически")
    return None

find_qt_plugins()

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtMultimedia import *
    from PyQt5.QtGui import *
    
    print("PyQt5 успешно импортирован!")
    
except Exception as e:
    print(f"Ошибка импорта PyQt5: {e}")
    input("Нажмите Enter для выхода...")
    sys.exit(1)


class AudioPlayerWidget(QWidget):
    """Виджет для проигрывания аудио с отображением времени"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.player = QMediaPlayer()
        self.current_file = None
        
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Информация о файле
        self.file_label = QLabel("Файл не выбран")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        # Время
        time_layout = QHBoxLayout()
        
        self.current_time_label = QLabel("00:00")
        self.current_time_label.setAlignment(Qt.AlignLeft)
        self.current_time_label.setMinimumWidth(50)
        
        self.total_time_label = QLabel("00:00")
        self.total_time_label.setAlignment(Qt.AlignRight)
        self.total_time_label.setMinimumWidth(50)
        
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setRange(0, 100)
        
        time_layout.addWidget(self.current_time_label)
        time_layout.addWidget(self.time_slider)
        time_layout.addWidget(self.total_time_label)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedSize(40, 40)
        
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setFixedSize(40, 40)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(100)
        
        buttons_layout.addWidget(self.play_btn)
        buttons_layout.addWidget(self.stop_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(QLabel("🔊"))
        buttons_layout.addWidget(self.volume_slider)
        
        layout.addWidget(self.file_label)
        layout.addLayout(time_layout)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def connect_signals(self):
        self.play_btn.clicked.connect(self.toggle_play)
        self.stop_btn.clicked.connect(self.stop)
        self.time_slider.sliderMoved.connect(self.seek)
        self.volume_slider.valueChanged.connect(self.set_volume)
        
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.player.stateChanged.connect(self.update_buttons)
    
    def format_time(self, milliseconds):
        """Форматирование времени в MM:SS"""
        if milliseconds <= 0:
            return "00:00"
        
        total_seconds = milliseconds // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        return f"{minutes:02d}:{seconds:02d}"
    
    def load_file(self, file_path):
        """Загрузить аудиофайл"""
        if file_path and os.path.exists(file_path):
            self.current_file = file_path
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            
            file_name = os.path.basename(file_path)
            self.file_label.setText(f"📄 {file_name}")
            
            # Получаем длительность из тегов
            self.get_duration_from_tags(file_path)
            
            return True
        return False
    
    def get_duration_from_tags(self, file_path):
        """Получить длительность из тегов файла (если доступно)"""
        try:
            import mutagen
            audio = mutagen.File(file_path)
            if audio and hasattr(audio.info, 'length'):
                duration_ms = int(audio.info.length * 1000)
                self.total_time_label.setText(self.format_time(duration_ms))
        except:
            pass
    
    def toggle_play(self):
        """Переключить воспроизведение/паузу"""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    
    def stop(self):
        """Остановить воспроизведение"""
        self.player.stop()
    
    def seek(self, position):
        """Перемотать к позиции"""
        if self.player.duration() > 0:
            self.player.setPosition(position)
    
    def set_volume(self, value):
        """Установить громкость"""
        self.player.setVolume(value)
    
    def update_duration(self, duration):
        """Обновить общую длительность"""
        if duration > 0:
            self.time_slider.setRange(0, duration)
            self.total_time_label.setText(self.format_time(duration))
    
    def update_position(self, position):
        """Обновить текущую позицию"""
        if self.player.duration() > 0:
            self.time_slider.setValue(position)
            self.current_time_label.setText(self.format_time(position))
    
    def update_buttons(self, state):
        """Обновить кнопки в зависимости от состояния"""
        if state == QMediaPlayer.PlayingState:
            self.play_btn.setText("⏸")
        else:
            self.play_btn.setText("▶")


class AudioPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Аудио Плеер ")
        self.setGeometry(100, 100, 700, 500)
        
        self.audio_files = []
        self.current_index = 0
        
        self.init_ui()
    
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        
        # Заголовок
        title = QLabel("🎵 Аудио Плеер ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: white;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3498db, stop:1 #9b59b6);
            border-radius: 10px;
        """)
        layout.addWidget(title)
        
        # Виджет плеера
        self.player_widget = AudioPlayerWidget()
        layout.addWidget(self.player_widget)
        
        # Информация о файле
        info_layout = QHBoxLayout()
        
        self.file_info_label = QLabel("Файлов: 0 | Текущий: 0")
        self.file_info_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        
        self.duration_info_label = QLabel("Длительность: --:--")
        self.duration_info_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        
        info_layout.addWidget(self.file_info_label)
        info_layout.addStretch()
        info_layout.addWidget(self.duration_info_label)
        
        layout.addLayout(info_layout)
        
        # Список файлов
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_selected)
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f8f9fa;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        layout.addWidget(self.file_list)
        
        # Кнопки навигации
        nav_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("📁 Загрузить папку")
        self.load_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.load_btn.clicked.connect(self.load_folder)
        
        self.prev_btn = QPushButton("◀ Предыдущий")
        self.prev_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #e67e22;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        self.prev_btn.clicked.connect(self.prev_file)
        
        self.next_btn = QPushButton("Следующий ▶")
        self.next_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #e67e22;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        self.next_btn.clicked.connect(self.next_file)
        
        nav_layout.addWidget(self.load_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        
        layout.addLayout(nav_layout)
        
        # Детальная информация
        self.details_label = QLabel()
        self.details_label.setWordWrap(True)
        self.details_label.setStyleSheet("""
            padding: 10px;
            background-color: #ecf0f1;
            border-radius: 5px;
            font-size: 12px;
        """)
        layout.addWidget(self.details_label)
        
        # Статус
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")
    
    def load_folder(self):
        """Загрузить папку с аудиофайлами"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с аудио")
        
        if folder:
            self.audio_files = []
            self.file_list.clear()
            
            import glob
            audio_extensions = ['*.mp3', '*.wav', '*.ogg', '*.m4a', '*.flac', '*.MP3', '*.WAV', '*.OGG']
            
            for ext in audio_extensions:
                pattern = os.path.join(folder, '**', ext)
                files = glob.glob(pattern, recursive=True)
                self.audio_files.extend(files)
            
            if self.audio_files:
                for file_path in self.audio_files:
                    file_name = os.path.basename(file_path)
                    item = QListWidgetItem(f"🎵 {file_name}")
                    item.setData(Qt.UserRole, file_path)
                    
                    # Добавляем информацию о длительности
                    try:
                        import mutagen
                        audio = mutagen.File(file_path)
                        if audio and hasattr(audio.info, 'length'):
                            duration = audio.info.length
                            minutes = int(duration // 60)
                            seconds = int(duration % 60)
                            item.setText(f"🎵 {file_name} ({minutes:02d}:{seconds:02d})")
                    except:
                        pass
                    
                    self.file_list.addItem(item)
                
                self.file_info_label.setText(f"Файлов: {len(self.audio_files)} | Текущий: 0")
                self.status_bar.showMessage(f"Загружено {len(self.audio_files)} аудиофайлов")
                
                # Выбираем первый файл
                if self.file_list.count() > 0:
                    self.file_list.setCurrentRow(0)
                    self.on_file_selected(self.file_list.item(0))
            else:
                self.status_bar.showMessage("Аудиофайлы не найдены")
                QMessageBox.warning(self, "Внимание", "В выбранной папке не найдено аудиофайлов")
    
    def on_file_selected(self, item):
        """Обработка выбора файла из списка"""
        if item:
            file_path = item.data(Qt.UserRole)
            self.player_widget.load_file(file_path)
            
            # Обновляем информацию
            self.current_index = self.file_list.currentRow()
            self.file_info_label.setText(f"Файлов: {len(self.audio_files)} | Текущий: {self.current_index + 1}")
            
            # Показываем детальную информацию
            self.show_file_details(file_path)
    
    def show_file_details(self, file_path):
        """Показать детальную информацию о файле"""
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            # Форматируем размер
            if file_size < 1024:
                size_str = f"{file_size} байт"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"
            
            # Получаем длительность
            duration_str = "Неизвестно"
            try:
                import mutagen
                audio = mutagen.File(file_path)
                if audio and hasattr(audio.info, 'length'):
                    duration = audio.info.length
                    minutes = int(duration // 60)
                    seconds = int(duration % 60)
                    duration_str = f"{minutes:02d}:{seconds:02d}"
                    
                    # Обновляем информацию о длительности
                    self.duration_info_label.setText(f"Длительность: {duration_str}")
            except:
                pass
            
           
            
        
            self.status_bar.showMessage(f"Загружен: {file_name}")
    
    def prev_file(self):
        """Предыдущий файл"""
        if self.file_list.count() > 0:
            current_row = self.file_list.currentRow()
            prev_row = (current_row - 1) % self.file_list.count()
            self.file_list.setCurrentRow(prev_row)
            self.on_file_selected(self.file_list.item(prev_row))
    
    def next_file(self):
        """Следующий файл"""
        if self.file_list.count() > 0:
            current_row = self.file_list.currentRow()
            next_row = (current_row + 1) % self.file_list.count()
            self.file_list.setCurrentRow(next_row)
            self.on_file_selected(self.file_list.item(next_row))


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Устанавливаем иконку приложения
    app.setWindowIcon(QIcon())
    
    player = AudioPlayerApp()
    player.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()