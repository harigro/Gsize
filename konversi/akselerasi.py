from PySide2.QtWidgets import QShortcut
from PySide2.QtGui import QKeySequence
from PySide2.QtCore import Qt

def setup_shortcuts(main_window):
    # Menambahkan akselerator Ctrl+K untuk membuka folder dan menampilkan direktori di terminal
    shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_K), main_window)
    shortcut.activated.connect(main_window.show_folder_and_directory)  # Memanggil metode dari instance main_window

    shortcut2 = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_T), main_window)
    shortcut2.activated.connect(main_window.show_hello_world)
