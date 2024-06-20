from pathlib import Path
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QFileDialog
from PySide2.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QIcon
from PySide2.QtCore import Qt
from ui.ui import Ui_Form
from konversi.akselerasi import setup_shortcuts
from konversi.konversi import jalan_ubah_ukuran_png_multi

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # ikon aplikasi        
        self.setWindowIcon(QIcon("assets/bunga.png"))

        # Membuat QLabel
        self.label = QLabel(self.ui.frame)
        self.label.setAlignment(Qt.AlignCenter)  # Mengatur gambar agar berada di tengah

        # Inisialisasi QPixmap
        self.pixmap = None

        # Inisialisasi file_path
        self.file_path = None
        self.jalur_simpan = None
        
        # Membuat layout untuk frame dan menetapkan QLabel ke dalam frame
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.label)
        self.ui.frame.setLayout(frame_layout)

        # Mengatur widget untuk menerima drag dan drop
        self.setAcceptDrops(True)
        
        # Menghubungkan event resize agar gambar disesuaikan saat ukuran jendela berubah
        self.ui.frame.resizeEvent = self.on_resize
        setup_shortcuts(self)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.file_path = Path(url.toLocalFile()).expanduser()  # Menggunakan pathlib.Path().expanduser()
                if self.file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                    self.pixmap = QPixmap(str(self.file_path))  # Menggunakan str(self.file_path) untuk mendapatkan path string
                    self.on_resize(None)
                    # self.show_hello_world()  # Panggil show_hello_world
                    break

    def on_resize(self, event):
        if self.pixmap is not None:
            # Mendapatkan ukuran baru dari frame QFrame
            new_size = self.ui.frame.size()
            
            # Mengubah ukuran QPixmap agar sesuai dengan QFrame
            scaled_pixmap = self.pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Menetapkan QPixmap yang diubah ukurannya ke QLabel
            self.label.setPixmap(scaled_pixmap)
    
    def show_hello_world(self):
        if self.file_path:
            jalan_ubah_ukuran_png_multi(self.file_path, self.jalur_simpan)
    
    def show_folder_and_directory(self):
        # Membuka dialog untuk memilih folder
        folder_path = QFileDialog.getExistingDirectory(self, "Pilih Folder", "/")
        if folder_path:
            # print(f"Direktori folder yang dipilih: {folder_path}")
            self.jalur_simpan = folder_path
if __name__=="__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
