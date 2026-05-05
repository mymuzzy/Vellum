import sys, os, shutil, random, string
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QScrollArea, QFrame, QSplitter,
    QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit,
    QListWidget, QListWidgetItem, QMessageBox, QSizePolicy,
    QStackedWidget, QGroupBox, QFormLayout, QProgressBar,
    QDialog, QDialogButtonBox, QTextEdit, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer, QMimeData
from PyQt6.QtGui import QPixmap, QImage, QCursor
import fitz
from tools import PDFTools

APP_NAME = "Vellum"

FONT_SCALES = {
    "Whisper":  0.72,
    "Petite":   0.88,
    "Standard": 1.0,
    "Grande":   1.20,
    "Colossal": 1.50,
}
BASE_FIELD = 11
BASE_BTN   = 13
BASE_LABEL = 11
BASE_TITLE = 13



# BVelow Changed 36 line -   font-family:'SF Pro Display','Segoe UI',Arial,sans-serif}
#  
DARK = """
QMainWindow,QDialog{background:#2b2b2b}
QWidget{background:#2b2b2b;color:#e0e0e0;
  font-family: sans-serif, Arial, Helvetica}
QFrame#leftPanel{background:#222;border:none}
QFrame#rightPanel{background:#222;border:none}
QFrame#midPanel{background:#1a1a1a;border:none}
QScrollArea{background:transparent;border:none}
QScrollBar:vertical{background:#2b2b2b;width:8px;border-radius:4px}
QScrollBar::handle:vertical{background:#555;border-radius:4px;min-height:24px}
QScrollBar:horizontal{background:#2b2b2b;height:8px;border-radius:4px}
QScrollBar::handle:horizontal{background:#555;border-radius:4px;min-width:24px}
QPushButton{background:#3a3a3a;color:#e0e0e0;
  border:1px solid #505050;border-radius:6px;
  padding:6px 12px;min-height:28px}
QPushButton:hover{background:#484848;border-color:#6a9fd8}
QPushButton:pressed{background:#2a2a2a}
QPushButton:checked{background:#4a7fb5;border-color:#6aafdf;color:#fff}
QPushButton#accentBtn{background:#4a7fb5;color:#fff;border-color:#3a6fa5}
QPushButton#accentBtn:hover{background:#5a8fc5}
QPushButton#dangerBtn{background:#7a2a2a;color:#fff;border-color:#9a3a3a}
QPushButton#dangerBtn:hover{background:#9a3a3a}
QPushButton#reloadBtn{background:#2d5a27;color:#afffad;
  border:1px solid #3d7a37;border-radius:6px;padding:6px 12px}
QPushButton#reloadBtn:hover{background:#3d7a37}
QPushButton#toolHeader{background:#1e1e1e;color:#8ab4d4;
  border:none;border-radius:0;text-align:left;
  font-weight:bold;padding:8px 10px;
  border-bottom:1px solid #383838;min-height:34px}
QPushButton#smallBtn{background:#3a3a3a;color:#e0e0e0;
  border:1px solid #505050;border-radius:4px;
  padding:2px 6px;min-height:24px;max-height:28px;
  font-size:14px;font-weight:bold}
QPushButton#smallBtn:hover{background:#5a8fc5;border-color:#6aafdf;color:#fff}
QPushButton#scopeBtn{background:#3a3a3a;color:#ccc;
  border:1px solid #505050;border-radius:5px;
  padding:5px 10px;min-height:28px}
QPushButton#scopeBtn:checked{background:#4a7fb5;color:#fff;border-color:#6aafdf}
QPushButton#scopeBtn:hover{background:#484848;border-color:#6a9fd8}
QComboBox{background:#3a3a3a;color:#e0e0e0;
  border:1px solid #505050;border-radius:5px;
  padding:4px 8px;min-height:28px}
QComboBox::drop-down{border:none;width:22px}
QComboBox::down-arrow{border-left:5px solid transparent;
  border-right:5px solid transparent;
  border-top:7px solid #aaa;margin-right:6px}
QComboBox QAbstractItemView{background:#3a3a3a;color:#e0e0e0;
  selection-background-color:#4a7fb5;
  border:1px solid #505050;padding:4px;min-width:160px}
QSpinBox,QDoubleSpinBox,QLineEdit{background:#3a3a3a;color:#e0e0e0;
  border:1px solid #505050;border-radius:5px;
  padding:4px 6px;min-height:28px}
QSpinBox::up-button,QDoubleSpinBox::up-button{
  subcontrol-origin:border;subcontrol-position:top right;
  width:22px;height:14px;background:#484848;
  border:1px solid #606060;border-radius:3px;margin:2px 2px 0 2px}
QSpinBox::down-button,QDoubleSpinBox::down-button{
  subcontrol-origin:border;subcontrol-position:bottom right;
  width:22px;height:14px;background:#484848;
  border:1px solid #606060;border-radius:3px;margin:0 2px 2px 2px}
QSpinBox::up-arrow,QDoubleSpinBox::up-arrow{
  border-left:4px solid transparent;
  border-right:4px solid transparent;
  border-bottom:6px solid #ccc;width:0;height:0}
QSpinBox::down-arrow,QDoubleSpinBox::down-arrow{
  border-left:4px solid transparent;
  border-right:4px solid transparent;
  border-top:6px solid #ccc;width:0;height:0}
QSpinBox::up-button:hover,QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover,QDoubleSpinBox::down-button:hover{
  background:#5a8fc5;border-color:#6aafdf}
QCheckBox{color:#e0e0e0;spacing:8px;min-height:24px}
QCheckBox::indicator{width:15px;height:15px;
  border:1px solid #606060;border-radius:3px;background:#3a3a3a}
QCheckBox::indicator:checked{background:#4a7fb5;border-color:#4a7fb5}
QListWidget{background:#272727;border:1px solid #404040;
  border-radius:5px;color:#e0e0e0}
QListWidget::item{padding:5px 8px;min-height:26px}
QListWidget::item:selected{background:#4a7fb5;color:#fff}
QListWidget::item:hover{background:#3a3a3a}
QTextEdit{background:#272727;color:#e0e0e0;
  border:1px solid #404040;border-radius:5px;padding:4px}
QGroupBox{border:1px solid #383838;border-radius:6px;
  margin-top:8px;padding-top:6px;color:#aaa}
QGroupBox::title{subcontrol-origin:margin;left:8px;
  padding:0 4px;color:#8ab4d4}
QProgressBar{background:#3a3a3a;border:1px solid #505050;
  border-radius:4px;color:#e0e0e0;text-align:center;min-height:18px}
QProgressBar::chunk{background:#4a7fb5;border-radius:4px}
QSplitter::handle{background:#383838}
QSplitter::handle:horizontal{width:5px}
QSplitter::handle:horizontal:hover{background:#6a9fd8}
QLabel#sectionTitle{color:#8ab4d4;font-weight:bold}
"""
# Below change 132 line -   font-family:'SF Pro Display','Segoe UI',Arial,sans-serif}
LIGHT = """
QMainWindow,QDialog{background:#f0f0f0}
QWidget{background:#f0f0f0;color:#1a1a1a;
  font-family: sans-serif, Arial, Helvetica}
QFrame#leftPanel{background:#e4e4e4;border:none}
QFrame#rightPanel{background:#e4e4e4;border:none}
QFrame#midPanel{background:#d8d8d8;border:none}
QScrollArea{background:transparent;border:none}
QScrollBar:vertical{background:#e0e0e0;width:8px;border-radius:4px}
QScrollBar::handle:vertical{background:#aaa;border-radius:4px;min-height:24px}
QScrollBar:horizontal{background:#e0e0e0;height:8px;border-radius:4px}
QScrollBar::handle:horizontal{background:#aaa;border-radius:4px;min-width:24px}
QPushButton{background:#dcdcdc;color:#1a1a1a;
  border:1px solid #b0b0b0;border-radius:6px;
  padding:6px 12px;min-height:28px}
QPushButton:hover{background:#c8c8c8;border-color:#4a7fb5}
QPushButton:pressed{background:#b8b8b8}
QPushButton:checked{background:#4a7fb5;border-color:#3a6fa5;color:#fff}
QPushButton#accentBtn{background:#4a7fb5;color:#fff;border-color:#3a6fa5}
QPushButton#accentBtn:hover{background:#5a8fc5}
QPushButton#dangerBtn{background:#c0392b;color:#fff;border-color:#a93226}
QPushButton#dangerBtn:hover{background:#e74c3c}
QPushButton#reloadBtn{background:#2ecc71;color:#fff;
  border:1px solid #27ae60;border-radius:6px;padding:6px 12px}
QPushButton#reloadBtn:hover{background:#27ae60}
QPushButton#toolHeader{background:#d0d0d0;color:#2a5f8f;
  border:none;border-radius:0;text-align:left;
  font-weight:bold;padding:8px 10px;
  border-bottom:1px solid #bbb;min-height:34px}
QPushButton#smallBtn{background:#dcdcdc;color:#1a1a1a;
  border:1px solid #b0b0b0;border-radius:4px;
  padding:2px 6px;min-height:24px;max-height:28px;
  font-size:14px;font-weight:bold}
QPushButton#smallBtn:hover{background:#4a7fb5;border-color:#3a6fa5;color:#fff}
QPushButton#scopeBtn{background:#dcdcdc;color:#333;
  border:1px solid #b0b0b0;border-radius:5px;
  padding:5px 10px;min-height:28px}
QPushButton#scopeBtn:checked{background:#4a7fb5;color:#fff;border-color:#3a6fa5}
QPushButton#scopeBtn:hover{background:#c8c8c8;border-color:#4a7fb5}
QComboBox{background:#dcdcdc;color:#1a1a1a;
  border:1px solid #b0b0b0;border-radius:5px;
  padding:4px 8px;min-height:28px}
QComboBox::drop-down{border:none;width:22px}
QComboBox::down-arrow{border-left:5px solid transparent;
  border-right:5px solid transparent;
  border-top:7px solid #555;margin-right:6px}
QComboBox QAbstractItemView{background:#dcdcdc;color:#1a1a1a;
  selection-background-color:#4a7fb5;
  border:1px solid #b0b0b0;padding:4px;min-width:160px}
QSpinBox,QDoubleSpinBox,QLineEdit{background:#dcdcdc;color:#1a1a1a;
  border:1px solid #b0b0b0;border-radius:5px;
  padding:4px 6px;min-height:28px}
QSpinBox::up-button,QDoubleSpinBox::up-button{
  subcontrol-origin:border;subcontrol-position:top right;
  width:22px;height:14px;background:#c8c8c8;
  border:1px solid #a0a0a0;border-radius:3px;margin:2px 2px 0 2px}
QSpinBox::down-button,QDoubleSpinBox::down-button{
  subcontrol-origin:border;subcontrol-position:bottom right;
  width:22px;height:14px;background:#c8c8c8;
  border:1px solid #a0a0a0;border-radius:3px;margin:0 2px 2px 2px}
QSpinBox::up-arrow,QDoubleSpinBox::up-arrow{
  border-left:4px solid transparent;
  border-right:4px solid transparent;
  border-bottom:6px solid #333;width:0;height:0}
QSpinBox::down-arrow,QDoubleSpinBox::down-arrow{
  border-left:4px solid transparent;
  border-right:4px solid transparent;
  border-top:6px solid #333;width:0;height:0}
QSpinBox::up-button:hover,QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover,QDoubleSpinBox::down-button:hover{
  background:#4a7fb5;border-color:#3a6fa5}
QCheckBox{color:#1a1a1a;spacing:8px;min-height:24px}
QCheckBox::indicator{width:15px;height:15px;
  border:1px solid #a0a0a0;border-radius:3px;background:#dcdcdc}
QCheckBox::indicator:checked{background:#4a7fb5;border-color:#4a7fb5}
QListWidget{background:#e8e8e8;border:1px solid #c0c0c0;
  border-radius:5px;color:#1a1a1a}
QListWidget::item{padding:5px 8px;min-height:26px}
QListWidget::item:selected{background:#4a7fb5;color:#fff}
QListWidget::item:hover{background:#d0d0d0}
QTextEdit{background:#e8e8e8;color:#1a1a1a;
  border:1px solid #c0c0c0;border-radius:5px;padding:4px}
QGroupBox{border:1px solid #c0c0c0;border-radius:6px;
  margin-top:8px;padding-top:6px;color:#555}
QGroupBox::title{subcontrol-origin:margin;left:8px;
  padding:0 4px;color:#2a5f8f}
QProgressBar{background:#dcdcdc;border:1px solid #b0b0b0;
  border-radius:4px;color:#1a1a1a;text-align:center;min-height:18px}
QProgressBar::chunk{background:#4a7fb5;border-radius:4px}
QSplitter::handle{background:#c0c0c0}
QSplitter::handle:horizontal{width:5px}
QSplitter::handle:horizontal:hover{background:#4a7fb5}
QLabel#sectionTitle{color:#2a5f8f;font-weight:bold}
"""


def rand_suffix(n=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


def unique_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    i = 1
    while True:
        c = f"{base}_{i}{ext}"
        if not os.path.exists(c):
            return c
        i += 1
        if i > 999:
            return f"{base}_{rand_suffix(3)}{ext}"


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ══════════════════════════════════════════
# DRAG-DROP LIST (Merge tool)
# ══════════════════════════════════════════
class DropListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.CopyAction)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
        else:
            super().dragEnterEvent(e)

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
        else:
            super().dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            for url in e.mimeData().urls():
                p = url.toLocalFile()
                if p.lower().endswith('.pdf'):
                    self.addItem(QListWidgetItem(p))
            e.acceptProposedAction()
        else:
            super().dropEvent(e)


# ══════════════════════════════════════════
# PASSWORD DIALOG
# ══════════════════════════════════════════
class PasswordDialog(QDialog):
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password Required")
        self.setMinimumWidth(340)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(QLabel(
            f"🔒  '{filename}' is password protected.\nEnter password to decrypt:"))
        self.pwd_field = QLineEdit()
        self.pwd_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_field.setPlaceholderText("Password…")
        self.pwd_field.setMinimumHeight(32)
        lay.addWidget(self.pwd_field)
        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        lay.addWidget(bb)
        self.pwd_field.returnPressed.connect(self.accept)

    def password(self):
        return self.pwd_field.text()


# ══════════════════════════════════════════
# PAGE THUMBNAIL
# ══════════════════════════════════════════
class PageThumb(QLabel):
    from PyQt6.QtCore import pyqtSignal
    clicked_sig = pyqtSignal(int, object)

    def __init__(self, idx, pixmap, parent=None):
        super().__init__(parent)
        self.idx = idx
        self.selected = False
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._unsel = "border:2px solid transparent;border-radius:4px;margin:4px;background:#2a2a2a"
        self._sel   = "border:2px solid #4a7fb5;border-radius:4px;margin:4px;background:#1a3a5c"
        self.setStyleSheet(self._unsel)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def set_selected(self, v):
        self.selected = v
        self.setStyleSheet(self._sel if v else self._unsel)

    def mousePressEvent(self, e):
        self.clicked_sig.emit(self.idx, e)


# ══════════════════════════════════════════
# PDF VIEWER
# ══════════════════════════════════════════
class PDFViewer(QScrollArea):
    from PyQt6.QtCore import pyqtSignal
    page_changed      = pyqtSignal(int, int)
    selection_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.lay = QVBoxLayout(self.container)
        self.lay.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.lay.setSpacing(8)
        self.lay.setContentsMargins(20, 20, 20, 20)
        self.setWidget(self.container)
        self.thumbs         = []
        self.selected_pages = set()
        self.zoom           = 1.0
        self.pdf_path       = None
        self.verticalScrollBar().valueChanged.connect(self._on_scroll)

    def load_pdf(self, path, zoom=None):
        self.pdf_path = path
        if zoom is not None:
            self.zoom = zoom
        self._clear()
        try:
            doc = fitz.open(path)
        except Exception as ex:
            print(f"ERROR: Cannot open PDF for viewer: {ex}")
            return
        try:
            for i in range(len(doc)):
                try:
                    page = doc[i]
                    mat  = fitz.Matrix(self.zoom * 1.5, self.zoom * 1.5)
                    pix  = page.get_pixmap(matrix=mat, alpha=False)
                    img  = QImage(pix.samples, pix.width, pix.height,
                                  pix.stride, QImage.Format.Format_RGB888)
                    t = PageThumb(i, QPixmap.fromImage(img))
                    t.clicked_sig.connect(self._on_click)
                    self.thumbs.append(t)
                    self.lay.addWidget(t)
                except Exception as ex:
                    print(f"ERROR: Rendering page {i}: {ex}")
        finally:
            doc.close()
        QTimer.singleShot(100, lambda: self.page_changed.emit(1, len(self.thumbs)))

    def _clear(self):
        self.thumbs.clear()
        self.selected_pages.clear()
        while self.lay.count():
            item = self.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _on_click(self, idx, event):
        try:
            mods  = event.modifiers()
            ctrl  = Qt.KeyboardModifier.ControlModifier
            shift = Qt.KeyboardModifier.ShiftModifier
            if mods & ctrl:
                if idx in self.selected_pages:
                    self.selected_pages.discard(idx)
                    self.thumbs[idx].set_selected(False)
                else:
                    self.selected_pages.add(idx)
                    self.thumbs[idx].set_selected(True)
            elif mods & shift and self.selected_pages:
                last = max(self.selected_pages)
                for j in range(min(last, idx), max(last, idx) + 1):
                    self.selected_pages.add(j)
                    self.thumbs[j].set_selected(True)
            else:
                if self.selected_pages == {idx}:
                    self.selected_pages.clear()
                    self.thumbs[idx].set_selected(False)
                else:
                    for j in list(self.selected_pages):
                        self.thumbs[j].set_selected(False)
                    self.selected_pages = {idx}
                    self.thumbs[idx].set_selected(True)
            self.selection_changed.emit()
        except Exception as ex:
            print(f"ERROR: Page click handler: {ex}")

    def _on_scroll(self, _):
        try:
            if not self.thumbs:
                return
            bar  = self.verticalScrollBar()
            frac = bar.value() / max(1, bar.maximum())
            cur  = min(int(frac * len(self.thumbs)) + 1, len(self.thumbs))
            self.page_changed.emit(cur, len(self.thumbs))
        except Exception as ex:
            print(f"ERROR: Scroll handler: {ex}")

    def set_zoom(self, z):
        try:
            sel = set(self.selected_pages)
            self.zoom = z
            if self.pdf_path:
                self.load_pdf(self.pdf_path)
                for idx in sel:
                    if idx < len(self.thumbs):
                        self.thumbs[idx].set_selected(True)
                        self.selected_pages.add(idx)
                self.selection_changed.emit()
        except Exception as ex:
            print(f"ERROR: Set zoom: {ex}")

    def get_selected(self):
        return sorted(self.selected_pages)

    def get_total(self):
        return len(self.thumbs)

    def deselect_all(self):
        try:
            for t in self.thumbs:
                t.set_selected(False)
            self.selected_pages.clear()
            self.selection_changed.emit()
        except Exception as ex:
            print(f"ERROR: Deselect all: {ex}")

    def select_all(self):
        try:
            for i, t in enumerate(self.thumbs):
                t.set_selected(True)
                self.selected_pages.add(i)
            self.selection_changed.emit()
        except Exception as ex:
            print(f"ERROR: Select all: {ex}")


# ══════════════════════════════════════════
# IMPORT WIDGET
# ══════════════════════════════════════════
class ImportWidget(QWidget):
    from PyQt6.QtCore import pyqtSignal
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(16)
        
        instr = QLabel("INSTRUCTION: \n\n- Drag and drop PDF files onto the viewer area to open them, or use the 'Browse Files' button below.\n- Import a PDF to view & edit.\n- Use left panel tools to crop, rotate, split, merge & more.\n- Export your final file from the right panel.\n- If you import mutiple files so please use merge tool to merge them into one file, which is on the left panel.")
        instr.setAlignment(Qt.AlignmentFlag.AlignLeft)
        instr.setStyleSheet("font-size:13px;font-weight:bold;color:#8ab4d4;background:transparent;padding:10px 14px 0px 14px")
        instr.setWordWrap(True)


        icon  = QLabel("📄")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size:60px;background:transparent")
        title = QLabel("Drop PDF files here")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size:22px;font-weight:bold;color:#8ab4d4;background:transparent")

        sub = QLabel("or")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("color:#888;background:transparent")
        self.btn = QPushButton("  Browse Files")
        self.btn.setObjectName("accentBtn")
        self.btn.setFixedSize(180, 44)

        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.addWidget(instr)
        lay.addStretch()
        lay.addWidget(icon)
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)
        lay.addStretch()


    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        try:
            paths = [u.toLocalFile() for u in e.mimeData().urls()
                     if u.toLocalFile().lower().endswith('.pdf')]
            if paths:
                self.files_dropped.emit(paths)
        except Exception as ex:
            print(f"ERROR: ImportWidget drop: {ex}")


def _hsep():
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setStyleSheet("color:#404040;max-height:1px")
    return f


# ══════════════════════════════════════════
# DROP ZONE WIDGET (for Decrypt tool)
# ══════════════════════════════════════════
class _DropZone(QLabel):
    from PyQt6.QtCore import pyqtSignal
    file_dropped = pyqtSignal(str)

    def __init__(self, text="Drop file here", parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            "border:2px dashed #505050;border-radius:6px;"
            "color:#888;padding:8px;background:#1a1a1a")

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        try:
            for url in e.mimeData().urls():
                p = url.toLocalFile()
                if p.lower().endswith('.pdf'):
                    self.file_dropped.emit(p)
                    break
        except Exception as ex:
            print(f"ERROR: DropZone drop: {ex}")


# ══════════════════════════════════════════
# MAIN WINDOW
# ══════════════════════════════════════════
class VellumMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.tools          = PDFTools()
        self.cur_pdf        = None
        self.temp_dir       = None
        self.history        = []
        self.dark_mode      = True
        self.font_scale     = 1.0
        self.export_folder  = None
        self.page_rotations = {}   # {page_index: cumulative_angle}
        self._build_ui()
        self._apply_theme()
        try:
            scr = QApplication.primaryScreen().geometry()
            w, h = scr.width() // 2, scr.height() // 2
            self.resize(w, h)
            self.move((scr.width() - w) // 2, (scr.height() - h) // 2)
        except Exception as ex:
            print(f"ERROR: Window positioning: {ex}")
            self.resize(900, 650)

    # ══════════════════════════════════════════
    # BUILD UI
    # ══════════════════════════════════════════
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(5)
        root.addWidget(self.splitter)
        self.splitter.addWidget(self._build_left())
        self.splitter.addWidget(self._build_mid())
        self.splitter.addWidget(self._build_right())
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 0)
        self.splitter.setSizes([270, 530, 240])

    # ── LEFT PANEL ──────────────────────────────
    def _build_left(self):
        panel = QFrame()
        panel.setObjectName("leftPanel")
        panel.setMinimumWidth(230)
        lay = QVBoxLayout(panel)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        brand = QLabel(f"  ✦ {APP_NAME}")
        brand.setObjectName("sectionTitle")
        brand.setStyleSheet(
            "font-size:16px;font-weight:bold;color:#8ab4d4;"
            "padding:10px 10px 8px 10px;background:#1a1a1a")
        lay.addWidget(brand)
        lay.addWidget(_hsep())
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        inner = QWidget()
        ilay  = QVBoxLayout(inner)
        ilay.setSpacing(0)
        ilay.setContentsMargins(0, 0, 0, 0)
        sections = [
            ("🔓  Decrypt PDF",   self._build_decrypt(),  "Unlock password-protected PDFs"),
            ("✂   Crop Pages",    self._build_crop(),     "Crop margins from page edges"),
            ("📝  Add Footer",    self._build_footer(),   "Add page numbers or custom text footer"),
            ("🔗  Merge PDFs",    self._build_merge(),    "Combine multiple PDFs into one"),
            ("✂️  Split PDF",     self._build_split(),    "Extract page ranges to new files"),
            ("🔄  Rotate Pages",  self._build_rotate(),   "Rotate pages left or right 90°"),
            ("⤡   Resize Pages",  self._build_resize(),   "Scale content to reference page width"),
            ("🗜  Compress PDF",  self._build_compress(), "Reduce file size using Ghostscript"),
            ("🗑  Delete Pages",  self._build_delete(),   "Delete selected pages from PDF"),
            ("⇅   Reorder Pages",   self._build_reorder(),  "Move pages up, down or to a position"),
        ]
        for title, widget, tip in sections:
            self._add_section(ilay, title, widget, tip)
        ilay.addStretch()
        scroll.setWidget(inner)
        lay.addWidget(scroll, 1)
        return panel

    def _add_section(self, parent_lay, title, content, tooltip=""):
        header = QPushButton(f"  {title}")
        header.setObjectName("toolHeader")
        header.setCheckable(True)
        header.setChecked(False)
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        header.setMinimumHeight(36)
        header.setToolTip(tooltip)
        parent_lay.addWidget(header)
        content.setVisible(False)
        parent_lay.addWidget(content)
        header.toggled.connect(content.setVisible)

    # ── TOOL WRAPPERS ────────────────────────────
    def _tool_wrap(self):
        w = QWidget()
        w.setStyleSheet("background:#202020;border-left:3px solid #3a3a3a")
        lay = QVBoxLayout(w)
        lay.setSpacing(8)
        lay.setContentsMargins(10, 10, 10, 12)
        return w, lay

    def _lbl(self, txt):
        l = QLabel(txt)
        l.setWordWrap(True)
        l.setMinimumWidth(72)
        l.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        return l

    def _field_row(self, label_txt, *widgets, tip=""):
        row = QHBoxLayout()
        row.setSpacing(6)
        if label_txt:
            lbl = self._lbl(label_txt)
            if tip:
                lbl.setToolTip(tip)
            row.addWidget(lbl)
        for w in widgets:
            if tip and hasattr(w, 'setToolTip'):
                w.setToolTip(tip)
            row.addWidget(w, 1)
        return row

    # ── DECRYPT ──────────────────────────────────
    def _build_decrypt(self):
        w, lay = self._tool_wrap()
        info = QLabel("Browse or drop an encrypted PDF.\nEnter password and decrypt.")
        info.setStyleSheet("color:#aaa;font-size:10px")
        info.setWordWrap(True)
        lay.addWidget(info)
        self.decrypt_drop = _DropZone("Drop encrypted PDF here")
        self.decrypt_drop.setMinimumHeight(54)
        self.decrypt_drop.file_dropped.connect(self._decrypt_file_dropped)
        lay.addWidget(self.decrypt_drop)
        browse = QPushButton("📂  Browse Encrypted PDF")
        browse.clicked.connect(self._decrypt_browse)
        lay.addWidget(browse)
        self.decrypt_path_lbl = QLabel("No file selected")
        self.decrypt_path_lbl.setStyleSheet("color:#aaa;font-size:10px")
        self.decrypt_path_lbl.setWordWrap(True)
        lay.addWidget(self.decrypt_path_lbl)
        self.decrypt_pwd = QLineEdit()
        self.decrypt_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.decrypt_pwd.setPlaceholderText("Password…")
        self.decrypt_pwd.setMinimumHeight(30)
        lay.addLayout(self._field_row("Password:", self.decrypt_pwd))
        btn = QPushButton("🔓  Decrypt & Load")
        btn.setObjectName("accentBtn")
        btn.clicked.connect(self._do_decrypt)
        lay.addWidget(btn)
        return w

    # ── CROP ─────────────────────────────────────
    def _build_crop(self):
        w, lay = self._tool_wrap()
        self.crop_left   = QDoubleSpinBox()
        self.crop_right  = QDoubleSpinBox()
        self.crop_top    = QDoubleSpinBox()
        self.crop_bottom = QDoubleSpinBox()
        for sp in (self.crop_left, self.crop_right, self.crop_top, self.crop_bottom):
            sp.setRange(0, 500)
            sp.setSuffix(" pt")
            sp.setMinimumWidth(110)
        lay.addLayout(self._field_row("Left ↔",   self.crop_left,   tip="Remove pts from left"))
        lay.addLayout(self._field_row("Right ↔",  self.crop_right,  tip="Remove pts from right"))
        lay.addLayout(self._field_row("Top ↕",    self.crop_top,    tip="Remove pts from top"))
        lay.addLayout(self._field_row("Bottom ↕", self.crop_bottom, tip="Remove pts from bottom"))
        self.crop_scope = QComboBox()
        self.crop_scope.addItems(["Selected Pages", "All Pages"])
        self.crop_scope.setMinimumWidth(130)
        lay.addLayout(self._field_row("Scope:", self.crop_scope))
        b = QPushButton("✂  Apply Crop")
        b.setObjectName("accentBtn")
        b.clicked.connect(self._do_crop)
        lay.addWidget(b)
        return w

    # ── FOOTER ───────────────────────────────────
    def _build_footer(self):
        w, lay = self._tool_wrap()
        pr = QHBoxLayout()
        pr.setSpacing(6)
        for label, tmpl in [("Page X of Y", "Page {n} of {total}"),
                             ("+ Filename",  "{filename} — Page {n} of {total}"),
                             ("Custom",      None)]:
            btn = QPushButton(label)
            btn.setMinimumHeight(30)
            if tmpl:
                btn.clicked.connect(lambda _, t=tmpl: self.footer_text.setText(t))
            else:
                btn.clicked.connect(lambda: self.footer_text.setFocus())
            pr.addWidget(btn)
        lay.addLayout(pr)
        self.footer_text = QLineEdit("Page {n} of {total}")
        self.footer_text.setPlaceholderText("{n}=page  {total}=total  {filename}=name")
        self.footer_text.setMinimumWidth(150)
        lay.addLayout(self._field_row("Text:", self.footer_text,
                                      tip="Use {n}, {total}, {filename}"))
        self.footer_align = QComboBox()
        self.footer_align.addItems(["Left", "Center", "Right"])
        self.footer_align.setCurrentText("Right")
        self.footer_align.view().setMinimumWidth(120)
        lay.addLayout(self._field_row("Align:", self.footer_align))
        self.footer_font = QComboBox()
        self.footer_font.addItems(["Helvetica", "Times-Roman", "Courier"])
        self.footer_font.view().setMinimumWidth(150)
        lay.addLayout(self._field_row("Font:", self.footer_font))
        self.footer_size = QSpinBox()
        self.footer_size.setRange(6, 36)
        self.footer_size.setValue(10)
        self.footer_size.setMinimumWidth(90)
        lay.addLayout(self._field_row("Size:", self.footer_size))
        # Gap row
        gap_lbl = self._lbl("Gap (cm):")
        gap_lbl.setToolTip("Space between content and footer in cm")
        self.footer_gap_spin = QDoubleSpinBox()
        self.footer_gap_spin.setRange(0.0, 10.0)
        self.footer_gap_spin.setValue(0.0)
        self.footer_gap_spin.setDecimals(1)
        self.footer_gap_spin.setSingleStep(0.5)
        self.footer_gap_spin.setMinimumWidth(80)
        gap_up   = QPushButton("▲")
        gap_up.setObjectName("smallBtn")
        gap_up.setFixedSize(30, 30)
        gap_down = QPushButton("▼")
        gap_down.setObjectName("smallBtn")
        gap_down.setFixedSize(30, 30)
        gap_up.clicked.connect(lambda: self.footer_gap_spin.setValue(
            min(self.footer_gap_spin.value() + 0.5, 10.0)))
        gap_down.clicked.connect(lambda: self.footer_gap_spin.setValue(
            max(self.footer_gap_spin.value() - 0.5, 0.0)))
        gap_row = QHBoxLayout()
        gap_row.setSpacing(4)
        gap_row.addWidget(gap_lbl)
        gap_row.addWidget(self.footer_gap_spin, 1)
        gap_row.addWidget(gap_up)
        gap_row.addWidget(gap_down)
        lay.addLayout(gap_row)
        # Scope toggle buttons
        scope_lbl = self._lbl("Scope:")
        self.footer_all_btn = QPushButton("◼  All Pages")
        self.footer_all_btn.setObjectName("scopeBtn")
        self.footer_all_btn.setCheckable(True)
        self.footer_all_btn.setChecked(True)
        self.footer_sel_btn = QPushButton("◻  Selected")
        self.footer_sel_btn.setObjectName("scopeBtn")
        self.footer_sel_btn.setCheckable(True)
        self.footer_sel_btn.setChecked(False)
        self.footer_all_btn.clicked.connect(lambda: self._footer_scope_toggle(True))
        self.footer_sel_btn.clicked.connect(lambda: self._footer_scope_toggle(False))
        sr = QHBoxLayout()
        sr.setSpacing(6)
        sr.addWidget(scope_lbl)
        sr.addWidget(self.footer_all_btn, 1)
        sr.addWidget(self.footer_sel_btn, 1)
        lay.addLayout(sr)
        b = QPushButton("📝  Apply Footer")
        b.setObjectName("accentBtn")
        b.clicked.connect(self._do_footer)
        lay.addWidget(b)
        return w

    def _footer_scope_toggle(self, all_pages):
        self.footer_all_btn.setChecked(all_pages)
        self.footer_sel_btn.setChecked(not all_pages)
        if all_pages:
            self.viewer.select_all()

    # ── MERGE ────────────────────────────────────
    def _build_merge(self):
        w, lay = self._tool_wrap()
        add_btn = QPushButton("➕  Add Files")
        add_btn.clicked.connect(self._merge_add)
        lay.addWidget(add_btn)
        info = QLabel("Drag & drop PDFs here or use Add Files:")
        info.setStyleSheet("color:#aaa;font-size:10px")
        lay.addWidget(info)
        self.merge_list = DropListWidget()
        self.merge_list.setMinimumHeight(80)
        self.merge_list.setMaximumHeight(130)
        lay.addWidget(self.merge_list)
        br = QHBoxLayout()
        br.setSpacing(6)
        for label, fn in [("▲ Up", self._merge_up),
                           ("▼ Down", self._merge_down),
                           ("✕ Remove", self._merge_rm)]:
            b = QPushButton(label)
            b.setMinimumHeight(30)
            b.clicked.connect(fn)
            br.addWidget(b)
        lay.addLayout(br)
        go = QPushButton("🔗  Create Merged PDF")
        go.setObjectName("accentBtn")
        go.clicked.connect(self._do_merge)
        lay.addWidget(go)
        return w

    # ── SPLIT ────────────────────────────────────
    def _build_split(self):
        w, lay = self._tool_wrap()
        info = QLabel("Enter ranges e.g.  1-3, 5, 7-9")
        info.setStyleSheet("color:#aaa;font-size:10px")
        lay.addWidget(info)
        self.split_field = QLineEdit()
        self.split_field.setPlaceholderText("e.g. 1-3, 5, 7-9")
        self.split_field.setMinimumWidth(150)
        lay.addLayout(self._field_row("Ranges:", self.split_field,
                                      tip="Comma-separated pages or ranges"))
        self.split_mode = QComboBox()
        self.split_mode.addItems([
            "Extract to Single File",
            "Split Each Range Separately",
            "Split Every Page",
        ])
        self.split_mode.view().setMinimumWidth(220)
        lay.addLayout(self._field_row("Mode:", self.split_mode))
        b = QPushButton("✂️  Apply Split")
        b.setObjectName("accentBtn")
        b.clicked.connect(self._do_split)
        lay.addWidget(b)
        return w

    # ── ROTATE ───────────────────────────────────
    def _build_rotate(self):
        w, lay = self._tool_wrap()
        info = QLabel("Rotate selected or all pages 90°:")
        info.setStyleSheet("color:#aaa;font-size:10px")
        lay.addWidget(info)
        br = QHBoxLayout()
        br.setSpacing(8)
        lb = QPushButton("◀  Left")
        lb.setObjectName("accentBtn")
        rb = QPushButton("Right  ▶")
        rb.setObjectName("accentBtn")
        lb.setMinimumHeight(34)
        rb.setMinimumHeight(34)
        lb.setToolTip("Rotate 90° counter-clockwise")
        rb.setToolTip("Rotate 90° clockwise")
        lb.clicked.connect(lambda: self._do_rotate(90))
        rb.clicked.connect(lambda: self._do_rotate(270))
        br.addWidget(lb)
        br.addWidget(rb)
        lay.addLayout(br)
        self.rotate_scope = QComboBox()
        self.rotate_scope.addItems(["Selected Pages", "All Pages"])
        self.rotate_scope.setMinimumWidth(140)
        lay.addLayout(self._field_row("Scope:", self.rotate_scope))
        return w

    # ── RESIZE ───────────────────────────────────
    def _build_resize(self):
        w, lay = self._tool_wrap()
        info = QLabel("Scale content to reference width.\n"
                      "Height scales proportionally. No white borders.")
        info.setStyleSheet("color:#aaa;font-size:10px")
        info.setWordWrap(True)
        lay.addWidget(info)
        self.resize_ref = QSpinBox()
        self.resize_ref.setRange(1, 9999)
        self.resize_ref.setValue(1)
        self.resize_ref.setMinimumWidth(90)
        lay.addLayout(self._field_row("Ref Page:", self.resize_ref,
                                      tip="Page whose width all others scale to"))
        self.resize_scope = QComboBox()
        self.resize_scope.addItems(["All Pages", "Selected Pages"])
        self.resize_scope.setMinimumWidth(140)
        lay.addLayout(self._field_row("Scope:", self.resize_scope))
        b = QPushButton("⤡  Apply Resize")
        b.setObjectName("accentBtn")
        b.clicked.connect(self._do_resize)
        lay.addWidget(b)
        return w

    # ── COMPRESS ─────────────────────────────────
    def _build_compress(self):
        w, lay = self._tool_wrap()
        info = QLabel(" Iterates DPI until target reached.\n When Clicked - WAIT for few seconds.")
        info.setStyleSheet("color:#aaa;font-size:10px")
        info.setWordWrap(True)
        lay.addWidget(info)
        self.compress_target = QDoubleSpinBox()
        self.compress_target.setRange(0.01, 999)
        self.compress_target.setValue(1.0)
        self.compress_target.setSuffix(" MB")
        self.compress_target.setDecimals(2)
        self.compress_target.setMinimumWidth(120)
        lay.addLayout(self._field_row(" Target:", self.compress_target,
                                      tip="Target file size in megabytes"))
        self.compress_bar = QProgressBar()
        self.compress_bar.setVisible(False)
        self.compress_status = QLabel("")
        self.compress_status.setWordWrap(True)
        self.compress_status.setStyleSheet("color:#aaa;font-size:10px")
        lay.addWidget(self.compress_bar)
        lay.addWidget(self.compress_status)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        builtin_btn = QPushButton("🐍 In-built")
        builtin_btn.setObjectName("accentBtn")
        builtin_btn.clicked.connect(self._do_compress_builtin)
        gs_btn = QPushButton("👻 Ghostscript")
        gs_btn.setObjectName("accentBtn")
        gs_btn.clicked.connect(self._do_compress_ghostscript)
        btn_row.addWidget(builtin_btn)
        btn_row.addWidget(gs_btn)
        lay.addLayout(btn_row)
        return w

    # ── DELETE ───────────────────────────────────
    def _build_delete(self):
        w, lay = self._tool_wrap()
        info = QLabel("Ctrl+Click / Shift+Click to multi-select,\nthen press Delete.")
        info.setWordWrap(True)
        info.setStyleSheet("color:#aaa;font-size:10px")
        lay.addWidget(info)
        b = QPushButton("🗑  Delete Selected Pages")
        b.setObjectName("dangerBtn")
        b.clicked.connect(self._do_delete)
        lay.addWidget(b)
        return w
    
    # ── REORDER ───────────────────────────────────
    def _build_reorder(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(6)
        lay.setContentsMargins(8, 6, 8, 6)

        move_row = QHBoxLayout()
        self.btn_move_up = QPushButton("▲  Move Up")
        self.btn_move_dn = QPushButton("▼  Move Down")
        self.btn_move_up.clicked.connect(self._move_pages_up)
        self.btn_move_dn.clicked.connect(self._move_pages_down)
        move_row.addWidget(self.btn_move_up)
        move_row.addWidget(self.btn_move_dn)

        goto_row = QHBoxLayout()
        goto_lbl = QLabel("Position:")
        goto_lbl.setFixedWidth(58)
        self.goto_spin = QSpinBox()
        self.goto_spin.setMinimum(1)
        self.goto_spin.setMaximum(9999)
        self.goto_spin.setFixedWidth(64)
        self.btn_goto = QPushButton("Move Here")
        self.btn_goto.clicked.connect(self._move_pages_to)
        goto_row.addWidget(goto_lbl)
        goto_row.addWidget(self.goto_spin)
        goto_row.addWidget(self.btn_goto)

        lay.addLayout(move_row)
        lay.addLayout(goto_row)
        return w


    # ── MIDDLE PANEL ─────────────────────────────
    def _build_mid(self):
        panel = QFrame()
        panel.setObjectName("midPanel")
        lay   = QVBoxLayout(panel)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.stacked = QStackedWidget()

        import_container = QWidget()
        import_lay = QVBoxLayout(import_container)
        import_lay.setContentsMargins(0, 0, 0, 0); import_lay.setSpacing(12)
        instr_label = QLabel("Step 1: Import PDF files\nDrag & drop or browse to select PDF(s)")
        instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instr_label.setStyleSheet("color:#8ab4d4;font-size:13px;background:transparent;padding:16px")
        instr_label.setWordWrap(True)

        # Index 0: import screen
        self.import_w = ImportWidget()
        self.import_w.btn.clicked.connect(self._browse)
        self.import_w.files_dropped.connect(self._load_files)

        import_lay.addWidget(instr_label)
        import_lay.addWidget(self.import_w, 1)

        # Index 1: viewer
        self.viewer = PDFViewer()
        self.viewer.page_changed.connect(self._update_page_ind)

        self.stacked.addWidget(self.import_w)   # index 0
        self.stacked.addWidget(self.viewer)      # index 1
        lay.addWidget(self.stacked, 1)


        self.stacked.addWidget(import_container)
        self.stacked.addWidget(self.viewer)
        lay.addWidget(self.stacked, 1)


        pi = QWidget()
        pi.setStyleSheet("background:#161616")
        pl = QHBoxLayout(pi)
        pl.setContentsMargins(8, 3, 8, 3)
        pl.addStretch()
        self.page_ind = QLabel("— of —")
        self.page_ind.setStyleSheet(
            "color:#8ab4d8;font-size:11px;background:transparent")
        pl.addWidget(self.page_ind)
        lay.addWidget(pi)
        return panel

    # ── RIGHT PANEL ───────────────────────────────
    def _build_right(self):
        panel = QFrame()
        panel.setObjectName("rightPanel")
        panel.setMinimumWidth(200)
        lay = QVBoxLayout(panel)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(6)

        tr = QHBoxLayout()
        tr.setSpacing(6)
        tr.setContentsMargins(0, 0, 0, 0)
        sel_all_btn = QPushButton("▢ Select All")
        sel_all_btn.setMinimumHeight(28)
        sel_all_btn.clicked.connect(self._safe_select_all)
        desel_btn = QPushButton("◻ Deselect All")
        desel_btn.setMinimumHeight(28)
        desel_btn.clicked.connect(self._safe_deselect_all)
        tr.addWidget(sel_all_btn)
        tr.addWidget(desel_btn)
        lay.addLayout(tr)

        credit = QLabel("Developed by Muzkkir")
        credit.setStyleSheet(
            "font-size:8px;color:#666;background:transparent;"
            "font-weight:normal;text-align:center")
        credit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(credit)
        lay.addWidget(_hsep())

        rsc = QScrollArea()
        rsc.setWidgetResizable(True)
        rsc.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        ri  = QWidget()
        ril = QVBoxLayout(ri)
        ril.setSpacing(8)
        ril.setContentsMargins(0, 0, 4, 0)

        # File Info
        props_title = QLabel("Properties")
        props_title.setObjectName("sectionTitle")
        props_title.setStyleSheet(
            "font-size:11px;font-weight:bold;color:#8ab4d4;background:transparent")
        ril.addWidget(props_title)
        fi = QGroupBox("File Info")
        fl = QFormLayout(fi)
        fl.setSpacing(4)
        self.lbl_name  = QLabel("—")
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setMinimumHeight(40)
        self.lbl_pages = QLabel("—")
        self.lbl_size  = QLabel("—")
        self.lbl_size.setWordWrap(True)
        self.lbl_size.setMinimumHeight(40)
        fl.addRow("Name:",  self.lbl_name)
        fl.addRow("Pages:", self.lbl_pages)
        fl.addRow("Size:",  self.lbl_size)
        fi.setMinimumHeight(140)
        ril.addWidget(fi)

        # Zoom
        zg = QGroupBox("Zoom")
        zl = QVBoxLayout(zg)
        zl.setSpacing(6)
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems(["10%", "25%", "50%", "75%", "100%",
                                   "125%", "150%", "200%", "300%", "Custom"])
        self.zoom_combo.setCurrentText("50%")
        self.zoom_combo.view().setMinimumWidth(50)
        self.zoom_combo.currentTextChanged.connect(self._on_zoom)
        self.zoom_spin = QSpinBox()
        self.zoom_spin.setRange(10, 1000)
        self.zoom_spin.setValue(100)
        self.zoom_spin.setSuffix("%")
        self.zoom_spin.setVisible(False)
        self.zoom_spin.editingFinished.connect(self._apply_custom_zoom)
        zl.addWidget(self.zoom_combo)
        zl.addWidget(self.zoom_spin)
        ril.addWidget(zg)

        # Appearance
        ag = QGroupBox("Appearance")
        al = QFormLayout(ag)
        al.setSpacing(6)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.view().setMinimumWidth(80)
        self.theme_combo.currentTextChanged.connect(self._on_theme)
        self.font_combo = QComboBox()
        self.font_combo.addItems(list(FONT_SCALES.keys()))
        self.font_combo.setCurrentText("Standard")
        self.font_combo.view().setMinimumWidth(120)
        self.font_combo.currentTextChanged.connect(self._on_font)
        al.addRow("Theme:",     self.theme_combo)
        al.addRow("Text Size:", self.font_combo)
        ril.addWidget(ag)

        # Export
        eg = QGroupBox("Export")
        el = QFormLayout(eg)
        el.setSpacing(6)
        self.exp_folder_lbl = QLabel("—")
        self.exp_folder_lbl.setWordWrap(True)
        fb = QPushButton("📁  Choose Folder")
        fb.setMinimumHeight(30)
        fb.clicked.connect(self._choose_folder)
        self.exp_prefix = QLineEdit()
        self.exp_prefix.setPlaceholderText("e.g. MyDoc")
        self.exp_prefix.setMinimumWidth(110)
        self.exp_suffix = QLineEdit()
        self.exp_suffix.setPlaceholderText("e.g. _final")
        self.exp_suffix.setMinimumWidth(110)
        el.addRow("Folder:", self.exp_folder_lbl)
        el.addRow("",        fb)
        el.addRow("Prefix:", self.exp_prefix)
        el.addRow("Suffix:", self.exp_suffix)
        ril.addWidget(eg)

        # History & Notes
        hg = QGroupBox("History & Notes")
        hl = QVBoxLayout(hg)
        hl.setSpacing(6)
        self.undo_btn = QPushButton("↩  Undo Last")
        self.undo_btn.setEnabled(False)
        self.undo_btn.clicked.connect(self._undo)
        hl.addWidget(self.undo_btn)
        notes_hdr = QHBoxLayout()
        notes_lbl = QLabel("📋 Scratch Pad")
        notes_lbl.setStyleSheet("color:#8ab4d4;font-size:10px;font-weight:bold")
        cp_btn = QPushButton("⎘ Copy")
        cp_btn.setFixedHeight(24)
        cp_btn.setToolTip("Copy scratch pad text")
        cp_btn.clicked.connect(self._notes_copy)
        pa_btn = QPushButton("⎙ Paste")
        pa_btn.setFixedHeight(24)
        pa_btn.setToolTip("Paste into scratch pad")
        pa_btn.clicked.connect(self._notes_paste)
        notes_hdr.addWidget(notes_lbl)
        notes_hdr.addStretch()
        notes_hdr.addWidget(cp_btn)
        notes_hdr.addWidget(pa_btn)
        hl.addLayout(notes_hdr)
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Rough notes, temp info, copy-paste area…")
        self.notes_edit.setMinimumHeight(80)
        self.notes_edit.setMaximumHeight(160)
        hl.addWidget(self.notes_edit)
        ril.addWidget(hg)

        ril.addStretch()
        rsc.setWidget(ri)
        lay.addWidget(rsc, 1)

        self.save_btn = QPushButton("💾  Export PDF")
        self.save_btn.setObjectName("accentBtn")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self._export)
        lay.addWidget(self.save_btn)
        return panel

    # ══════════════════════════════════════════
    # TEMP / FILE MANAGEMENT
    # ══════════════════════════════════════════
    def _ensure_temp(self):
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            self.temp_dir = os.path.join(SCRIPT_DIR, f"vellum_temp_{rand_suffix(8)}")
            os.makedirs(self.temp_dir, exist_ok=True)

    def _copy_to_temp(self, src):
        self._ensure_temp()
        dst = os.path.join(self.temp_dir, os.path.basename(src))
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        return dst

    def _make_temp_out(self, suffix="out"):
        self._ensure_temp()
        ts = datetime.now().strftime("%H%M%S%f")[:12]
        return os.path.join(self.temp_dir, f"vellum_{suffix}_{ts}.pdf")

    def _need_pdf(self):
        if not self.cur_pdf or not os.path.exists(self.cur_pdf):
            QMessageBox.warning(self, APP_NAME, "Please import a PDF file first.")
            return False
        return True

    def _get_sel(self):
        s = self.viewer.get_selected()
        if not s:
            QMessageBox.warning(self, APP_NAME,
                                "Select at least one page in the viewer.")
        return s or None

    def _validate_numeric(self, value, min_val, max_val, field_name):
        try:
            if value < min_val or value > max_val:
                print(f"ERROR: {field_name} out of range. "
                      f"Expected {min_val}–{max_val}, got {value}")
                return False
            return True
        except Exception as ex:
            print(f"ERROR: Validating {field_name}: {ex}")
            return False

    def _validate_positive(self, value, field_name):
        if value <= 0:
            print(f"ERROR: {field_name} must be > 0, got {value}")
            return False
        return True

    # ══════════════════════════════════════════
    # SMART RELOAD
    # ══════════════════════════════════════════
    def _apply_op(self, new_path):
        """Save current to history, set new as current, smart reload."""
        if self.cur_pdf:
            self.history.append(self.cur_pdf)
            self.undo_btn.setEnabled(True)
        self.cur_pdf = new_path
        self._smart_reload()

    def _smart_reload(self):
        """Reload PDF viewer and refresh all panels after every operation."""
        if not self.cur_pdf or not os.path.exists(self.cur_pdf):
            return
        try:
            self.viewer.load_pdf(self.cur_pdf, self.viewer.zoom)
        except Exception as ex:
            print(f"ERROR: Failed to reload viewer: {ex}")
        self._refresh_right_panel()
        self._refresh_tool_limits()

    def _refresh_right_panel(self):
        """Update filename, page count, file size in right panel."""
        if not self.cur_pdf or not os.path.exists(self.cur_pdf):
            return
        try:
            name = os.path.basename(self.cur_pdf)
            try:
                doc   = fitz.open(self.cur_pdf)
                pages = len(doc)
                doc.close()
            except Exception:
                pages = 0
            try:
                size_bytes = os.path.getsize(self.cur_pdf)
                size_str = (f"{size_bytes / (1024*1024):.2f} MB  "
                            f"({size_bytes / 1024:.0f} KB)")
            except Exception:
                size_str = "—"
            self.lbl_name.setText(name)
            self.lbl_pages.setText(str(pages))
            self.lbl_size.setText(size_str)
        except Exception as ex:
            print(f"ERROR: Refresh right panel: {ex}")

    def _refresh_tool_limits(self):
        """Update field max values based on current PDF page count."""
        try:
            doc   = fitz.open(self.cur_pdf)
            pages = len(doc)
            doc.close()
            if pages > 0:
                self.resize_ref.setMaximum(pages)
                mid_point = max(1, pages // 2)
                self.split_field.setPlaceholderText(
                    f"e.g. 1-{mid_point}, {mid_point+1}-{pages}")
        except Exception as ex:
            print(f"ERROR: Refresh tool limits: {ex}")

    # ══════════════════════════════════════════
    # BROWSE / LOAD
    # ══════════════════════════════════════════
    def _browse(self):
        try:
            paths, _ = QFileDialog.getOpenFileNames(
                self, "Open PDF", "", "PDF Files (*.pdf)")
            if paths:
                self._load_files(paths)
        except Exception as ex:
            print(f"ERROR: Browse: {ex}")

    def _load_files(self, paths):
        try:
            if not paths:
                return
            if len(paths) == 1:
                self._load_single(paths[0])
            else:
                for p in paths:
                    self.merge_list.addItem(QListWidgetItem(p))
                QMessageBox.information(
                    self, APP_NAME,
                    f"Added {len(paths)} files to the Merge list.\n"
                    "Open the Merge PDFs section and click Create Merged PDF.")
        except Exception as ex:
            print(f"ERROR: Load files: {ex}")

    def _load_single(self, path):
        try:
            doc = fitz.open(path)
            if doc.needs_pass:
                doc.close()
                dlg = PasswordDialog(os.path.basename(path), self)
                if dlg.exec() != QDialog.DialogCode.Accepted:
                    return
                pwd = dlg.password()
                doc = fitz.open(path)
                if not doc.authenticate(pwd):
                    doc.close()
                    QMessageBox.critical(self, APP_NAME, "Incorrect password.")
                    return
                tmp_dec = self._make_temp_out("decrypted")
                doc.save(tmp_dec, garbage=4, deflate=True)
                doc.close()
                path = tmp_dec
            else:
                doc.close()
        except Exception as ex:
            QMessageBox.critical(self, APP_NAME, f"Cannot open file:\n{ex}")
            return

        try:
            tmp = self._copy_to_temp(path)
            self.cur_pdf        = tmp
            self.export_folder  = os.path.dirname(os.path.abspath(path))
            self.page_rotations = {}
            self.exp_folder_lbl.setText(self.export_folder)
            self.exp_prefix.setText(
                os.path.splitext(os.path.basename(path))[0])
            # Set zoom to 50% on import
            self.zoom_combo.blockSignals(True)
            self.zoom_combo.setCurrentText("50%")
            self.zoom_combo.blockSignals(False)
            self.viewer.zoom = 0.5
            self.viewer.deselect_all()
            self._smart_reload()
            self.stacked.setCurrentWidget(self.viewer)
            self.save_btn.setEnabled(True)
        except Exception as ex:
            QMessageBox.critical(self, APP_NAME, f"Failed to load file:\n{ex}")
            print(f"ERROR: Load single: {ex}")

    def _update_page_ind(self, cur, total):
        try:
            self.page_ind.setText(f"{cur} of {total}")
        except Exception:
            pass

    # ══════════════════════════════════════════
    # DECRYPT TOOL
    # ══════════════════════════════════════════
    def _decrypt_browse(self):
        try:
            path, _ = QFileDialog.getOpenFileName(
                self, "Open Encrypted PDF", "", "PDF Files (*.pdf)")
            if path:
                self.decrypt_path_lbl.setText(os.path.basename(path))
                self.decrypt_path_lbl.setProperty("full_path", path)
        except Exception as ex:
            print(f"ERROR: Decrypt browse: {ex}")

    def _decrypt_file_dropped(self, path):
        try:
            self.decrypt_path_lbl.setText(os.path.basename(path))
            self.decrypt_path_lbl.setProperty("full_path", path)
        except Exception as ex:
            print(f"ERROR: Decrypt file dropped: {ex}")

    def _do_decrypt(self):
        try:
            path = self.decrypt_path_lbl.property("full_path") or ""
            if not path or not os.path.exists(path):
                QMessageBox.warning(self, APP_NAME,
                                    "Select an encrypted PDF first.")
                return
            pwd = self.decrypt_pwd.text()
            if not pwd:
                QMessageBox.warning(self, APP_NAME, "Enter a password.")
                return
            doc = fitz.open(path)
            if not doc.needs_pass:
                doc.close()
                QMessageBox.information(self, APP_NAME,
                    "This PDF is not encrypted. Loading directly.")
                self._load_single(path)
                return
            if not doc.authenticate(pwd):
                doc.close()
                QMessageBox.critical(self, APP_NAME, "Incorrect password.")
                return
            out = self._make_temp_out("decrypted")
            doc.save(out, garbage=4, deflate=True)
            doc.close()
            self.cur_pdf        = out
            self.export_folder  = os.path.dirname(os.path.abspath(path))
            self.page_rotations = {}
            self.exp_folder_lbl.setText(self.export_folder)
            self.exp_prefix.setText(
                os.path.splitext(os.path.basename(path))[0] + "_decrypted")
            self.zoom_combo.blockSignals(True)
            self.zoom_combo.setCurrentText("50%")
            self.zoom_combo.blockSignals(False)
            self.viewer.zoom = 0.5
            self.viewer.deselect_all()
            self._smart_reload()
            self.stacked.setCurrentWidget(self.viewer)
            self.save_btn.setEnabled(True)
            self.decrypt_pwd.clear()
        except Exception as ex:
            QMessageBox.critical(self, "Decrypt Error", str(ex))
            print(f"ERROR: Decrypt failed: {ex}")

    # ══════════════════════════════════════════
    # TOOL ACTIONS
    # ══════════════════════════════════════════
    def _do_crop(self):
        if not self._need_pdf():
            return
        try:
            l = self.crop_left.value()
            r = self.crop_right.value()
            t = self.crop_top.value()
            b = self.crop_bottom.value()
        except Exception as ex:
            print(f"ERROR: Reading crop values: {ex}")
            return
        sel = (self.viewer.get_selected()
               if self.crop_scope.currentText() == "Selected Pages" else None)
        if self.crop_scope.currentText() == "Selected Pages" and not sel:
            QMessageBox.warning(self, APP_NAME,
                                "Select at least one page or switch scope to All Pages.")
            return
        out = self._make_temp_out("crop")
        try:
            self.tools.crop_pdf(self.cur_pdf, out, l, r, t, b, sel)
            self._apply_op(out)
        except Exception as ex:
            QMessageBox.critical(self, "Crop Error", str(ex))
            print(f"ERROR: Crop failed: {ex}")

    def _do_footer(self):
        if not self._need_pdf():
            return
        if not (self._validate_numeric(self.footer_size.value(), 6, 36, "Font Size") and
                self._validate_numeric(self.footer_gap_spin.value(), 0, 10, "Gap")):
            return
        use_all = self.footer_all_btn.isChecked()
        sel     = None if use_all else self.viewer.get_selected()
        if not use_all and not sel:
            QMessageBox.warning(self, APP_NAME,
                                "Select pages or switch to All Pages.")
            return
        out = self._make_temp_out("footer")
        try:
            self.tools.add_footer(
                self.cur_pdf, out,
                text_template  = self.footer_text.text(),
                alignment      = self.footer_align.currentText().lower(),
                font_name      = self.footer_font.currentText(),
                font_size      = self.footer_size.value(),
                gap_cm         = self.footer_gap_spin.value(),
                page_indices   = sel,
                filename       = os.path.basename(self.cur_pdf),
                page_rotations = self.page_rotations,
            )
            self._apply_op(out)
        except Exception as ex:
            QMessageBox.critical(self, "Footer Error", str(ex))
            print(f"ERROR: Footer failed: {ex}")

    def _merge_add(self):
        try:
            paths, _ = QFileDialog.getOpenFileNames(
                self, "Add PDFs", "", "PDF Files (*.pdf)")
            for p in paths:
                self.merge_list.addItem(QListWidgetItem(p))
        except Exception as ex:
            print(f"ERROR: Merge add: {ex}")

    def _merge_up(self):
        try:
            r = self.merge_list.currentRow()
            if r > 0:
                it = self.merge_list.takeItem(r)
                self.merge_list.insertItem(r - 1, it)
                self.merge_list.setCurrentRow(r - 1)
        except Exception as ex:
            print(f"ERROR: Merge up: {ex}")

    def _merge_down(self):
        try:
            r = self.merge_list.currentRow()
            if r < self.merge_list.count() - 1:
                it = self.merge_list.takeItem(r)
                self.merge_list.insertItem(r + 1, it)
                self.merge_list.setCurrentRow(r + 1)
        except Exception as ex:
            print(f"ERROR: Merge down: {ex}")

    def _merge_rm(self):
        try:
            r = self.merge_list.currentRow()
            if r >= 0:
                self.merge_list.takeItem(r)
        except Exception as ex:
            print(f"ERROR: Merge remove: {ex}")

    def _do_merge(self):
        try:
            paths = [self.merge_list.item(i).text()
                     for i in range(self.merge_list.count())]
            if len(paths) < 2:
                QMessageBox.warning(self, APP_NAME, "Add at least 2 files.")
                return
            out = self._make_temp_out("merged")
            self.tools.merge_pdfs(paths, out)
            self.export_folder = os.path.dirname(os.path.abspath(paths[0]))
            self.exp_folder_lbl.setText(self.export_folder)
            self.exp_prefix.setText(
                os.path.splitext(os.path.basename(paths[0]))[0] + "_merged")
            self.page_rotations = {}
            self._apply_op(out)
            self.stacked.setCurrentWidget(self.viewer)
            self.save_btn.setEnabled(True)
            self.merge_list.clear()
        except Exception as ex:
            QMessageBox.critical(self, "Merge Error", str(ex))
            print(f"ERROR: Merge failed: {ex}")

    def _do_split(self):
        if not self._need_pdf():
            return
        raw  = self.split_field.text().strip()
        mode = self.split_mode.currentText()
        if not raw:
            QMessageBox.warning(self, APP_NAME, "Enter page ranges.")
            return
        try:
            indices = self._parse_ranges(raw)
        except Exception as ex:
            QMessageBox.critical(self, "Range Error", str(ex))
            return
        if not indices:
            QMessageBox.warning(self, APP_NAME, "No valid pages found.")
            return
        out = self._make_temp_out("split")
        try:
            if "Every Page" in mode:
                paths = self.tools.split_every_page(self.cur_pdf, self.temp_dir)
                QMessageBox.information(self, APP_NAME,
                    f"Split into {len(paths)} files in temp folder.")
            elif "Separately" in mode:
                paths = self.tools.split_ranges_separately(
                    self.cur_pdf, self.temp_dir, raw)
                QMessageBox.information(self, APP_NAME,
                    f"Created {len(paths)} files in temp folder.")
            else:
                self.tools.split_indices(self.cur_pdf, out, indices)
                self._apply_op(out)
        except Exception as ex:
            QMessageBox.critical(self, "Split Error", str(ex))
            print(f"ERROR: Split failed: {ex}")

    def _parse_ranges(self, text):
        indices = []
        for part in text.split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-", 1)
                indices.extend(range(int(a.strip()) - 1, int(b.strip())))
            elif part.isdigit():
                indices.append(int(part) - 1)
        return sorted(set(indices))

    def _do_rotate(self, angle):
        if not self._need_pdf():
            return
        try:
            all_pages = self.rotate_scope.currentText() == "All Pages"
            sel       = None if all_pages else self.viewer.get_selected()
            if not all_pages and not sel:
                QMessageBox.warning(self, APP_NAME,
                                    "Select pages or use All Pages scope.")
                return
            out = self._make_temp_out("rotate")
            self.tools.rotate_pages(self.cur_pdf, out, angle, sel)
            # Rotation is now baked into content — clear stale rotation tracking
            # so footer/resize see these pages as plain rotation=0 pages.
            try:
                doc   = fitz.open(self.cur_pdf)
                total = len(doc)
                doc.close()
            except Exception:
                total = 0
            targets = range(total) if all_pages else sel
            for i in targets:
                self.page_rotations.pop(i, None)
            self._apply_op(out)
        except Exception as ex:
            QMessageBox.critical(self, "Rotate Error", str(ex))
            print(f"ERROR: Rotate failed: {ex}")


    def _do_resize(self):
        if not self._need_pdf():
            return
        try:
            doc       = fitz.open(self.cur_pdf)
            max_pages = len(doc)
            doc.close()
        except Exception:
            max_pages = 1
        if not self._validate_numeric(self.resize_ref.value(), 1, max_pages,
                                      "Reference Page"):
            return
        ref = self.resize_ref.value() - 1
        sel = (self.viewer.get_selected()
               if self.resize_scope.currentText() == "Selected Pages" else None)
        out = self._make_temp_out("resize")
        try:
            self.tools.resize_to_ref_width(self.cur_pdf, out, ref, sel)
            self._apply_op(out)
        except Exception as ex:
            QMessageBox.critical(self, "Resize Error", str(ex))
            print(f"ERROR: Resize failed: {ex}")

    def _do_compress_builtin(self):
        if not self._need_pdf():
            return
        if not self._validate_positive(self.compress_target.value(), "Target Size"):
            return
        out = self._make_temp_out("compressed_builtin")
        self.compress_bar.setVisible(True)
        self.compress_bar.setValue(0)
        self.compress_status.setText("Compressing (In-built)…")
        QApplication.processEvents()
        try:
            rp, mb = self.tools.compress_pdf_builtin(
                self.cur_pdf, out,
                self.compress_target.value(),
                progress_cb=self._comp_cb)
            self.compress_bar.setValue(100)
            self.compress_status.setText(f"Done: {mb:.2f} MB")
            self._apply_op(rp)
        except Exception as ex:
            self.compress_status.setText(f"Error: {ex}")
            QMessageBox.critical(self, "Compress Error", str(ex))
            print(f"ERROR: Built-in compression failed: {ex}")
        finally:
            self.compress_bar.setVisible(False)

    def _do_compress_ghostscript(self):
        if not self._need_pdf():
            return
                
        # ── Ghostscript availability check ──────────────
        if not self.tools._find_ghostscript():
            QMessageBox.information(
                self, "Ghostscript Not Installed",
                "Ghostscript was not found on this system.\n\n"
                "To install it:\n\n"
                "  macOS  →  brew install ghostscript\n"
                "  Ubuntu →  sudo apt install ghostscript\n"
                "  Windows→  https://ghostscript.com/releases/gsdnld.html\n\n"
                "After installing, restart Vellum and try again.\n\n"
                "Alternatively, use the 🐍 In-built compressor — it\n"
                "requires no external tools."
            )
            return
        # ────────────────────────────────────────────────
        if not self._validate_positive(self.compress_target.value(), "Target Size"):
            return
        out = self._make_temp_out("compressed_gs")
        self.compress_bar.setVisible(True)
        self.compress_bar.setValue(0)
        self.compress_status.setText("Compressing (Ghostscript)…")
        QApplication.processEvents()
        try:
            rp, mb = self.tools.compress_pdf(
                self.cur_pdf, out,
                self.compress_target.value(),
                progress_cb=self._comp_cb)
            self.compress_bar.setValue(100)
            self.compress_status.setText(f"Done: {mb:.2f} MB")
            self._apply_op(rp)
        except Exception as ex:
            self.compress_status.setText(f"Error: {ex}")
            QMessageBox.critical(self, "Compress Error", str(ex))
            print(f"ERROR: Ghostscript compression failed: {ex}")
        finally:
            self.compress_bar.setVisible(False)

    def _comp_cb(self, v, msg=""):
        try:
            self.compress_bar.setValue(v)
            if msg:
                self.compress_status.setText(msg)
            QApplication.processEvents()
        except Exception:
            pass

    def _do_delete(self):
        if not self._need_pdf():
            return
        sel = self._get_sel()
        if not sel:
            return
        try:
            d   = fitz.open(self.cur_pdf)
            tot = len(d)
            d.close()
        except Exception:
            QMessageBox.critical(self, APP_NAME, "Cannot open PDF.")
            return
        if len(sel) >= tot:
            QMessageBox.warning(self, APP_NAME,
                                "Cannot delete all pages.")
            return
        out = self._make_temp_out("delete")
        try:
            self.tools.delete_pages(self.cur_pdf, out, sel)
            for i in sel:
                self.page_rotations.pop(i, None)
            self._apply_op(out)
            self.viewer.deselect_all()
        except Exception as ex:
            QMessageBox.critical(self, "Delete Error", str(ex))
            print(f"ERROR: Delete failed: {ex}")
    

    # ===
    # Reorder Page
    # ===
    def _move_pages_up(self):
        if not self._need_pdf():
            return
        sel = self._get_sel()
        if not sel:
            return
        try:
            doc = fitz.open(self.cur_pdf)
            n = doc.page_count
            doc.close()
        except Exception:
            return
        order = list(range(n))
        for idx in sorted(sel):
            if idx <= 0:
                continue
            order[idx], order[idx - 1] = order[idx - 1], order[idx]
        out = self._make_temp_out("reorder")
        try:
            self.tools.reorder_pages(self.cur_pdf, out, order)
            self._apply_op(out)
            self.viewer.deselect_all()
        except Exception as ex:
            QMessageBox.critical(self, "Reorder Error", str(ex))
            print(f"ERROR reorder up: {ex}")

    def _move_pages_down(self):
        if not self._need_pdf():
            return
        sel = self._get_sel()
        if not sel:
            return
        try:
            doc = fitz.open(self.cur_pdf)
            n = doc.page_count
            doc.close()
        except Exception:
            return
        order = list(range(n))
        for idx in sorted(sel, reverse=True):
            if idx >= n - 1:
                continue
            order[idx], order[idx + 1] = order[idx + 1], order[idx]
        out = self._make_temp_out("reorder")
        try:
            self.tools.reorder_pages(self.cur_pdf, out, order)
            self._apply_op(out)
            self.viewer.deselect_all()
        except Exception as ex:
            QMessageBox.critical(self, "Reorder Error", str(ex))
            print(f"ERROR reorder down: {ex}")

    def _move_pages_to(self):
        if not self._need_pdf():
            return
        sel = self._get_sel()
        if not sel:
            return
        try:
            doc = fitz.open(self.cur_pdf)
            n = doc.page_count
            doc.close()
        except Exception:
            return
        target = max(0, min(self.goto_spin.value() - 1, n - 1))
        sel_sorted = sorted(sel)
        remaining = [i for i in range(n) if i not in sel]
        insert_at = min(target, len(remaining))
        new_order = remaining[:insert_at] + sel_sorted + remaining[insert_at:]
        out = self._make_temp_out("reorder")
        try:
            self.tools.reorder_pages(self.cur_pdf, out, new_order)
            self._apply_op(out)
            self.viewer.deselect_all()
        except Exception as ex:
            QMessageBox.critical(self, "Reorder Error", str(ex))
            print(f"ERROR reorder goto: {ex}")


    # ══════════════════════════════════════════
    # EXPORT
    # ══════════════════════════════════════════
    def _choose_folder(self):
        try:
            f = QFileDialog.getExistingDirectory(
                self, "Choose Export Folder", self.export_folder or "")
            if f:
                self.export_folder = f
                self.exp_folder_lbl.setText(f)
        except Exception as ex:
            print(f"ERROR: Choose folder: {ex}")

    def _export(self):
        try:
            if not self.cur_pdf or not os.path.exists(self.cur_pdf):
                QMessageBox.warning(self, APP_NAME, "No PDF to export.")
                return
            prefix    = self.exp_prefix.text().strip()
            suffix    = self.exp_suffix.text().strip()
            base_name = os.path.splitext(os.path.basename(self.cur_pdf))[0]
            ts        = datetime.now().strftime("%d%m%Y_%H%M%S")
            
            #parts     = [p for p in [prefix, base_name, ts, suffix] if p]
            if prefix:
                parts = [p for p in [prefix, suffix] if p]
            else:
                parts = [p for p in [base_name, ts, suffix] if p]
            fname     = "_".join(parts) + ".pdf"
            
            folder    = self.export_folder
            if not folder or not os.path.isdir(folder):
                folder = os.path.expanduser("~")
            out = unique_path(os.path.join(folder, fname))
            shutil.copy2(self.cur_pdf, out)
            if os.path.exists(out):
                QMessageBox.information(self, APP_NAME,
                    f"✅ Exported successfully:\n{out}")
            else:
                QMessageBox.critical(self, APP_NAME,
                    "Export failed — file not found after copy.")
        except Exception as ex:
            QMessageBox.critical(self, "Export Error", str(ex))
            print(f"ERROR: Export failed: {ex}")

    # ══════════════════════════════════════════
    # ZOOM / THEME / FONT
    # ══════════════════════════════════════════
    def _on_zoom(self, text):
        try:
            if text == "Custom":
                self.zoom_spin.setVisible(True)
                return
            self.zoom_spin.setVisible(False)
            self.viewer.set_zoom(int(text.replace("%", "")) / 100)
        except Exception as ex:
            print(f"ERROR: Zoom change: {ex}")

    def _apply_custom_zoom(self):
        try:
            if self.zoom_combo.currentText() == "Custom":
                self.viewer.set_zoom(self.zoom_spin.value() / 100)
        except Exception as ex:
            print(f"ERROR: Custom zoom: {ex}")

    def _on_theme(self, t):
        self.dark_mode = (t == "Dark")
        self._apply_theme()

    def _apply_theme(self):
        try:
            QApplication.instance().setStyleSheet(DARK if self.dark_mode else LIGHT)
            self._apply_font_scale()
        except Exception as ex:
            print(f"ERROR: Apply theme: {ex}")

    def _on_font(self, t):
        self.font_scale = FONT_SCALES.get(t, 1.0)
        self._apply_font_scale()

    def _apply_font_scale(self):
        try:
            s  = self.font_scale
            ff = max(8,  int(BASE_FIELD * s))
            fb = max(9,  int(BASE_BTN   * s))
            fl = max(8,  int(BASE_LABEL * s))
            ft = max(10, int(BASE_TITLE * s))
            extra = (
                f"QWidget{{font-size:{fl}px}}"
                f"QPushButton{{font-size:{fb}px}}"
                f"QLabel{{font-size:{fl}px}}"
                f"QComboBox{{font-size:{ff}px}}"
                f"QSpinBox{{font-size:{ff}px}}"
                f"QDoubleSpinBox{{font-size:{ff}px}}"
                f"QLineEdit{{font-size:{ff}px}}"
                f"QGroupBox::title{{font-size:{ft}px}}"
                f"QLabel#sectionTitle{{font-size:{ft}px}}"
            )
            base = DARK if self.dark_mode else LIGHT
            QApplication.instance().setStyleSheet(base + extra)
        except Exception as ex:
            print(f"ERROR: Apply font scale: {ex}")

    # ══════════════════════════════════════════
    # NOTES
    # ══════════════════════════════════════════
    def _notes_copy(self):
        try:
            txt = self.notes_edit.toPlainText()
            if txt:
                QApplication.clipboard().setText(txt)
        except Exception as ex:
            print(f"ERROR: Notes copy: {ex}")

    def _notes_paste(self):
        try:
            txt = QApplication.clipboard().text()
            if txt:
                self.notes_edit.insertPlainText(txt)
        except Exception as ex:
            print(f"ERROR: Notes paste: {ex}")

    # ══════════════════════════════════════════
    # UNDO
    # ══════════════════════════════════════════
    def _undo(self):
        try:
            if not self.history:
                return
            prev = self.history.pop()
            if os.path.exists(prev):
                self.cur_pdf = prev
                self._smart_reload()
            self.undo_btn.setEnabled(bool(self.history))
        except Exception as ex:
            print(f"ERROR: Undo: {ex}")

    def _safe_select_all(self):
        try:
            if self.cur_pdf and os.path.exists(self.cur_pdf):
                self.viewer.select_all()
        except Exception as ex:
            print(f"ERROR: Select All: {ex}")

    def _safe_deselect_all(self):
        try:
            if self.cur_pdf and os.path.exists(self.cur_pdf):
                self.viewer.deselect_all()
        except Exception as ex:
            print(f"ERROR: Deselect All: {ex}")

    # ══════════════════════════════════════════
    # FULL RELOAD — wipes everything
    # ══════════════════════════════════════════
    def _full_reload(self):
        try:
            r = QMessageBox.question(
                self, APP_NAME,
                "Reset everything to start screen?\nAll unsaved changes will be lost.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if r != QMessageBox.StandardButton.Yes:
                return

            self.cur_pdf        = None
            self.export_folder  = None
            self.history        = []
            self.page_rotations = {}

            self.viewer._clear()
            self.stacked.setCurrentIndex(0)     # back to import screen
            self.save_btn.setEnabled(False)
            self.undo_btn.setEnabled(False)

            # Reset tool fields
            self.crop_left.setValue(0)
            self.crop_right.setValue(0)
            self.crop_top.setValue(0)
            self.crop_bottom.setValue(0)
            self.crop_scope.setCurrentIndex(0)
            self.footer_text.setText("Page {n} of {total}")
            self.footer_align.setCurrentText("Right")
            self.footer_font.setCurrentIndex(0)
            self.footer_size.setValue(10)
            self.footer_gap_spin.setValue(0.0)
            self._footer_scope_toggle(True)
            self.split_field.clear()
            self.split_mode.setCurrentIndex(0)
            self.rotate_scope.setCurrentIndex(0)
            self.resize_ref.setValue(1)
            self.resize_scope.setCurrentIndex(0)
            self.compress_target.setValue(1.0)
            self.compress_status.setText("")
            self.compress_bar.setVisible(False)
            self.lbl_name.setText("—")
            self.lbl_pages.setText("—")
            self.lbl_size.setText("—")
            self.page_ind.setText("— of —")
            self.exp_folder_lbl.setText("—")
            self.exp_prefix.clear()
            self.zoom_combo.setCurrentText("50%")
            self.zoom_spin.setVisible(False)
            self.zoom_spin.setValue(100)
            self.notes_edit.clear()
            self.decrypt_path_lbl.setText("No file selected")
            self.decrypt_path_lbl.setProperty("full_path", "")
            self.decrypt_pwd.clear()
            self.merge_list.clear()
        except Exception as ex:
            print(f"ERROR: Full reload: {ex}")

    # ══════════════════════════════════════════
    # CLOSE
    # ══════════════════════════════════════════
    def closeEvent(self, e):
        try:
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception:
            pass
        e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    win = VellumMainWindow()
    win.show()
    sys.exit(app.exec())
