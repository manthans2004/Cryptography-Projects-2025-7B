from __future__ import annotations

import os
import random
from pathlib import Path
from typing import List, Optional

from PyQt5 import QtCore, QtGui, QtWidgets

from crypto_utils import encrypt_token_with_passphrase, decrypt_token_with_passphrase
from steganography_utils import hide_bytes_in_image, reveal_bytes_from_image
from user_manager import (
	UserProfile,
	get_or_create_user_directory,
	get_user,
	save_user_profile,
)

APP_TITLE = "MLS-2FA (PoC)"
IMAGES_DIR = Path("images")
SUCCESS_TOKEN = "MLS_SUCCESS_TOKEN"


class ImageButton(QtWidgets.QLabel):
	clicked = QtCore.pyqtSignal()

	def __init__(self, pixmap: QtGui.QPixmap, path: str, parent=None):
		super().__init__(parent)
		self.setPixmap(pixmap)
		self.setScaledContents(True)
		self.path = path
		self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

	def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
		if event.button() == QtCore.Qt.LeftButton:
			self.clicked.emit()


class ClickableImage(QtWidgets.QLabel):
	clicked_at = QtCore.pyqtSignal(float, float)  # relative x,y in [0,1]

	def __init__(self, pixmap: QtGui.QPixmap, parent=None):
		super().__init__(parent)
		self.setPixmap(pixmap)
		self.setScaledContents(True)
		self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

	def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
		if event.button() != QtCore.Qt.LeftButton:
			return
		w = self.width()
		h = self.height()
		x = max(0, min(event.x(), w)) / max(1, w)
		y = max(0, min(event.y(), h)) / max(1, h)
		self.clicked_at.emit(x, y)


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle(APP_TITLE)
		self.resize(960, 640)

		central = QtWidgets.QWidget()
		self.setCentralWidget(central)

		layout = QtWidgets.QVBoxLayout(central)
		layout.addStretch(1)

		title = QtWidgets.QLabel("MLS-2FA Proof of Concept")
		title.setObjectName("Heading")
		title.setAlignment(QtCore.Qt.AlignCenter)
		font = title.font()
		font.setPointSize(18)
		font.setBold(True)
		title.setFont(font)
		layout.addWidget(title)

		btn_row = QtWidgets.QHBoxLayout()
		layout.addLayout(btn_row)

		self.register_btn = QtWidgets.QPushButton("Register a New User")
		self.login_btn = QtWidgets.QPushButton("Login")
		self.admin_btn = QtWidgets.QPushButton("Admin Debug")
		self.register_btn.setMinimumHeight(48)
		self.login_btn.setMinimumHeight(48)
		self.admin_btn.setMinimumHeight(48)
		self.admin_btn.setStyleSheet("background-color: #dc2626; color: white;")
		btn_row.addStretch(1)
		btn_row.addWidget(self.register_btn)
		btn_row.addSpacing(12)
		btn_row.addWidget(self.login_btn)
		btn_row.addSpacing(12)
		btn_row.addWidget(self.admin_btn)
		btn_row.addStretch(1)

		layout.addStretch(2)

		self.register_btn.clicked.connect(self.open_registration)
		self.login_btn.clicked.connect(self.open_login)
		self.admin_btn.clicked.connect(self.open_admin_debug)

	def open_registration(self):
		dialog = RegistrationWizard(self)
		dialog.exec_()

	def open_login(self):
		dialog = LoginWizard(self)
		dialog.exec_()

	def open_admin_debug(self):
		dialog = AdminDebugDialog(self)
		dialog.exec_()




class RegistrationWizard(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register User")
        self.resize(1000, 720)

        self.username: Optional[str] = None
        self.selected_image_path: Optional[str] = None
        self.secret_x: Optional[float] = None
        self.secret_y: Optional[float] = None
        self.passphrase: Optional[str] = None

        self.stack = QtWidgets.QStackedWidget()
        self.btn_prev = QtWidgets.QPushButton("Back")
        self.btn_next = QtWidgets.QPushButton("Next")
        self.btn_prev.clicked.connect(self.go_prev)
        self.btn_next.clicked.connect(self.go_next)

        root = QtWidgets.QVBoxLayout(self)
        root.addWidget(self.stack)
        nav = QtWidgets.QHBoxLayout()
        nav.addStretch(1)
        nav.addWidget(self.btn_prev)
        nav.addWidget(self.btn_next)
        root.addLayout(nav)

        self.page_username = self._build_username_page()
        self.page_image_grid = self._build_image_grid_page()
        self.page_secret_spot = self._build_secret_spot_page()
        self.page_passphrase = self._build_passphrase_page()

        for page in [self.page_username, self.page_image_grid, self.page_secret_spot, self.page_passphrase]:
            self.stack.addWidget(page)

        self.update_nav()

    def update_nav(self):
        idx = self.stack.currentIndex()
        self.btn_prev.setEnabled(idx > 0)
        self.btn_next.setText("Finish" if idx == self.stack.count() - 1 else "Next")

    def go_prev(self):
        self.stack.setCurrentIndex(max(0, self.stack.currentIndex() - 1))
        self.update_nav()

    def go_next(self):
        idx = self.stack.currentIndex()
        if idx == 0:
            if not self.username_input.text().strip():
                QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please enter a username.")
                return
            self.username = self.username_input.text().strip()
            self.stack.setCurrentIndex(1)
        elif idx == 1:
            if not self.selected_image_path:
                QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please select an image.")
                return
            self._load_secret_spot_image()
            self.stack.setCurrentIndex(2)
        elif idx == 2:
            if self.secret_x is None or self.secret_y is None:
                QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please click on the image to set your secret spot.")
                return
            self.stack.setCurrentIndex(3)
        elif idx == 3:
            if not self.passphrase_input.text():
                QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please enter a stego passphrase.")
                return
            self.passphrase = self.passphrase_input.text()
            self._finalize_registration()
            self.accept()
        self.update_nav()

    def _build_username_page(self) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(w)
        label = QtWidgets.QLabel("Enter a username:")
        label.setObjectName("accent")
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("alice")
        self.username_input.setMaxLength(64)
        lay.addWidget(label)
        lay.addWidget(self.username_input)
        lay.addStretch(1)
        return w

    def _build_image_grid_page(self) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        label = QtWidgets.QLabel("Select your secret base image (20 images):")
        label.setObjectName("accent")
        v.addWidget(label)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        container = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(container)
        grid.setSpacing(8)

        image_paths = self._load_sample_images(limit=20)
        if len(image_paths) < 20:
            warn = QtWidgets.QLabel("Warning: fewer than 20 images found in 'images/' directory.")
            warn.setStyleSheet("color: #c0392b;")
            v.addWidget(warn)

        self.image_buttons: List[ImageButton] = []
        row = col = 0
        for path in image_paths:
            pix = QtGui.QPixmap(path)
            if pix.isNull():
                continue
            thumb = pix.scaled(150, 150, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            btn = ImageButton(thumb, path)
            btn.setProperty("thumbnail", True)
            btn.clicked.connect(lambda p=path, b=btn: self._select_image(p, b))
            self.image_buttons.append(btn)
            grid.addWidget(btn, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1

        scroll.setWidget(container)
        v.addWidget(scroll)
        return w

    def _build_secret_spot_page(self) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        label = QtWidgets.QLabel("Click on the image to set your secret spot (stored as percentages).")
        label.setObjectName("accent")
        v.addWidget(label)
        self.secret_image_holder = QtWidgets.QWidget()
        self.secret_image_layout = QtWidgets.QVBoxLayout(self.secret_image_holder)
        self.secret_image_layout.setContentsMargins(0, 0, 0, 0)
        v.addWidget(self.secret_image_holder, 1)
        self.coords_label = QtWidgets.QLabel("No spot selected.")
        v.addWidget(self.coords_label)
        return w

    def _build_passphrase_page(self) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        label = QtWidgets.QLabel("Enter your Stego-Key (passphrase):")
        label.setObjectName("accent")
        self.passphrase_input = QtWidgets.QLineEdit()
        self.passphrase_input.setEchoMode(QtWidgets.QLineEdit.Password)
        v.addWidget(label)
        v.addWidget(self.passphrase_input)
        v.addStretch(1)
        return w

    def _select_image(self, path: str, btn: ImageButton):
        self.selected_image_path = path
        for b in self.image_buttons:
            b.setStyleSheet("")
        btn.setStyleSheet("border: 3px solid #27ae60;")

    def _load_secret_spot_image(self):
        for i in reversed(range(self.secret_image_layout.count())):
            item = self.secret_image_layout.itemAt(i)
            w = item.widget()
            if w:
                w.setParent(None)
        pix = QtGui.QPixmap(self.selected_image_path)
        view = ClickableImage(pix)
        view.clicked_at.connect(self._on_spot_clicked)
        self.secret_image_layout.addWidget(view)

    def _on_spot_clicked(self, x: float, y: float):
        self.secret_x = x
        self.secret_y = y
        self.coords_label.setText(f"Selected spot: x={x:.3f}, y={y:.3f}")

    def _finalize_registration(self):
        assert self.username and self.selected_image_path and self.secret_x is not None and self.secret_y is not None and self.passphrase

        user_dir = get_or_create_user_directory(self.username)
        stego_out = user_dir / "stego_image.png"

        cipher = encrypt_token_with_passphrase(SUCCESS_TOKEN, self.passphrase)
        hide_bytes_in_image(self.selected_image_path, cipher, str(stego_out))

        all_images = [str(p) for p in self._load_sample_images(limit=200)]
        decoys = [p for p in all_images if p != self.selected_image_path]
        random.shuffle(decoys)
        decoys = decoys[:19]

        profile = UserProfile(
            username=self.username,
            stego_image_path=str(stego_out),
            secret_coordinates={"x": float(self.secret_x), "y": float(self.secret_y)},
            decoy_images=decoys,
        )
        save_user_profile(profile)
        QtWidgets.QMessageBox.information(self, APP_TITLE, f"User '{self.username}' registered successfully.")

    def _load_sample_images(self, limit: int = 20) -> List[str]:
        if not IMAGES_DIR.exists():
            IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        paths: List[str] = []
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.bmp"):
            paths.extend([str(p) for p in IMAGES_DIR.glob(ext)])
        random.shuffle(paths)
        return paths[:limit]


class LoginWizard(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.resize(1000, 720)

        self.username: Optional[str] = None
        self.profile: Optional[UserProfile] = None
        self.selected_grid_image_path: Optional[str] = None
        self.clicked_x: Optional[float] = None
        self.clicked_y: Optional[float] = None
        self.passphrase: Optional[str] = None

        self.stack = QtWidgets.QStackedWidget()
        self.btn_prev = QtWidgets.QPushButton("Back")
        self.btn_next = QtWidgets.QPushButton("Next")
        self.btn_prev.clicked.connect(self.go_prev)
        self.btn_next.clicked.connect(self.go_next)

        root = QtWidgets.QVBoxLayout(self)
        root.addWidget(self.stack)
        nav = QtWidgets.QHBoxLayout()
        nav.addStretch(1)
        nav.addWidget(self.btn_prev)
        nav.addWidget(self.btn_next)
        root.addLayout(nav)

        self.page_username = self._build_username_page()
        self.page_grid = self._build_grid_page()
        self.page_spot = self._build_spot_page()
        self.page_pass = self._build_passphrase_page()

        for page in [self.page_username, self.page_grid, self.page_spot, self.page_pass]:
            self.stack.addWidget(page)

        self.update_nav()

    def update_nav(self):
        idx = self.stack.currentIndex()
        self.btn_prev.setEnabled(idx > 0)
        self.btn_next.setText("Login" if idx == self.stack.count() - 1 else "Next")

    def go_prev(self):
        self.stack.setCurrentIndex(max(0, self.stack.currentIndex() - 1))
        self.update_nav()

    def go_next(self):
        idx = self.stack.currentIndex()
        if idx == 0:
            name = self.username_input.text().strip()
            if not name:
                QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please enter a username.")
                return
            self.profile = get_user(name)
            if not self.profile:
                QtWidgets.QMessageBox.critical(self, APP_TITLE, "User not found. Please register first.")
                return
            self.username = name
            self._load_grid_images()
            self.stack.setCurrentIndex(1)
        elif idx == 1:
            if not self.selected_grid_image_path:
                QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please select an image from the grid.")
                return
            if self.selected_grid_image_path != self.profile.stego_image_path:
                QtWidgets.QMessageBox.critical(self, APP_TITLE, "Login Failed! Wrong image selected.")
                self.reject()
                return
            self._load_spot_image()
            self.stack.setCurrentIndex(2)
        elif idx == 2:
            if self.clicked_x is None or self.clicked_y is None:
                QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please click on the image.")
                return
            if not self._spot_within_tolerance(self.clicked_x, self.clicked_y):
                QtWidgets.QMessageBox.critical(self, APP_TITLE, "Login Failed! Wrong spot.")
                self.reject()
                return
            self.stack.setCurrentIndex(3)
        elif idx == 3:
            if not self.passphrase_input.text():
                QtWidgets.QMessageBox.warning(self, APP_TITLE, "Please enter your Stego-Key.")
                return
            self.passphrase = self.passphrase_input.text()
            self._attempt_decrypt_and_finish()
        self.update_nav()

    def _build_username_page(self) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        label = QtWidgets.QLabel("Enter username:")
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("alice")
        self.username_input.setMaxLength(64)
        v.addWidget(label)
        v.addWidget(self.username_input)
        v.addStretch(1)
        return w

    def _build_grid_page(self) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        self.grid_info = QtWidgets.QLabel("Select your registered image from the grid:")
        self.grid_info.setObjectName("accent")
        v.addWidget(self.grid_info)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        self.grid_container = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(8)
        scroll.setWidget(self.grid_container)
        v.addWidget(scroll)
        return w

    def _build_spot_page(self) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        label = QtWidgets.QLabel("Click your secret spot on the image:")
        label.setObjectName("accent")
        v.addWidget(label)
        self.spot_holder = QtWidgets.QWidget()
        self.spot_layout = QtWidgets.QVBoxLayout(self.spot_holder)
        self.spot_layout.setContentsMargins(0, 0, 0, 0)
        v.addWidget(self.spot_holder, 1)
        self.spot_coords = QtWidgets.QLabel("No click yet.")
        v.addWidget(self.spot_coords)
        return w

    def _build_passphrase_page(self) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        label = QtWidgets.QLabel("Enter your Stego-Key (passphrase):")
        label.setObjectName("accent")
        self.passphrase_input = QtWidgets.QLineEdit()
        self.passphrase_input.setEchoMode(QtWidgets.QLineEdit.Password)
        v.addWidget(label)
        v.addWidget(self.passphrase_input)
        v.addStretch(1)
        return w

    def _load_grid_images(self):
        # Mix stego image with 19 decoys from profile
        assert self.profile is not None
        all_paths: List[str] = [self.profile.stego_image_path] + list(self.profile.decoy_images)
        random.shuffle(all_paths)
        # Clear previous
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            w = item.widget()
            if w:
                w.setParent(None)
        row = col = 0
        self.grid_buttons: List[ImageButton] = []
        for path in all_paths:
            pix = QtGui.QPixmap(path)
            if pix.isNull():
                continue
            thumb = pix.scaled(150, 150, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            btn = ImageButton(thumb, path)
            btn.clicked.connect(lambda p=path, b=btn: self._choose_grid_image(p, b))
            self.grid_buttons.append(btn)
            self.grid_layout.addWidget(btn, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1

    def _choose_grid_image(self, path: str, btn: ImageButton):
        self.selected_grid_image_path = path
        for b in self.grid_buttons:
            b.setStyleSheet("")
        btn.setStyleSheet("border: 3px solid #27ae60;")

    def _load_spot_image(self):
        for i in reversed(range(self.spot_layout.count())):
            item = self.spot_layout.itemAt(i)
            w = item.widget()
            if w:
                w.setParent(None)
        pix = QtGui.QPixmap(self.profile.stego_image_path)
        view = ClickableImage(pix)
        view.clicked_at.connect(self._on_spot_clicked)
        self.spot_layout.addWidget(view)

    def _on_spot_clicked(self, x: float, y: float):
        self.clicked_x = x
        self.clicked_y = y
        self.spot_coords.setText(f"Clicked: x={x:.3f}, y={y:.3f}")

    def _spot_within_tolerance(self, x: float, y: float, tol: float = 0.02) -> bool:
        assert self.profile is not None
        saved = self.profile.secret_coordinates
        return (abs(x - float(saved["x"])) <= tol) and (abs(y - float(saved["y"])) <= tol)

    def _attempt_decrypt_and_finish(self):
        assert self.profile is not None and self.passphrase is not None
        cipher = reveal_bytes_from_image(self.profile.stego_image_path)
        if cipher is None:
            QtWidgets.QMessageBox.critical(self, APP_TITLE, "Login Failed! No hidden data.")
            self.reject()
            return
        ok, plaintext = decrypt_token_with_passphrase(cipher, self.passphrase)
        if not ok or plaintext != SUCCESS_TOKEN:
            QtWidgets.QMessageBox.critical(self, APP_TITLE, "Login Failed! Wrong key.")
            self.reject()
            return
        QtWidgets.QMessageBox.information(self, APP_TITLE, "Login Successful!")
        self.accept()


class AdminDebugDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Debug - Ciphertext Inspector")
        self.resize(800, 600)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # Header
        header = QtWidgets.QLabel("🔍 Admin Debug: Ciphertext Inspector")
        header.setObjectName("Heading")
        header.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(header)
        
        # Username selection
        user_layout = QtWidgets.QHBoxLayout()
        user_layout.addWidget(QtWidgets.QLabel("Select User:"))
        self.user_combo = QtWidgets.QComboBox()
        self.user_combo.setMinimumWidth(200)
        self._load_users()
        user_layout.addWidget(self.user_combo)
        user_layout.addStretch(1)
        layout.addLayout(user_layout)
        
        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.reveal_btn = QtWidgets.QPushButton("🔓 Reveal Ciphertext")
        self.reveal_btn.setStyleSheet("background-color: #dc2626; color: white; font-weight: bold;")
        self.reveal_btn.clicked.connect(self.reveal_ciphertext)
        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.reveal_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)
        
        # Results area
        self.results = QtWidgets.QTextEdit()
        self.results.setReadOnly(True)
        self.results.setPlaceholderText("Click 'Reveal Ciphertext' to see the encrypted data...")
        self.results.setStyleSheet("font-family: 'Courier New', monospace; background-color: #0c1117; color: #e5e7eb;")
        layout.addWidget(self.results)
        
    def _load_users(self):
        """Load all registered users into the combo box"""
        try:
            from user_manager import load_user_db
            db = load_user_db()
            users = list(db.keys())
            if not users:
                self.user_combo.addItem("No users found")
                self.reveal_btn.setEnabled(False)
            else:
                self.user_combo.addItems(users)
        except Exception as e:
            self.user_combo.addItem("Error loading users")
            self.reveal_btn.setEnabled(False)
    
    def reveal_ciphertext(self):
        """Extract and display the ciphertext from the selected user's stego image"""
        username = self.user_combo.currentText()
        if not username or username == "No users found" or username == "Error loading users":
            return
            
        try:
            from user_manager import get_user
            from steganography_utils import reveal_bytes_from_image
            import base64
            
            profile = get_user(username)
            if not profile:
                self.results.setText("❌ User profile not found!")
                return
                
            # Extract ciphertext from stego image
            ciphertext = reveal_bytes_from_image(profile.stego_image_path)
            if ciphertext is None:
                self.results.setText("❌ No hidden data found in stego image!")
                return
            
            # Display results
            result_text = f"""
🔍 Ciphertext Analysis for User: {username}

📁 Stego Image Path: {profile.stego_image_path}
📍 Secret Coordinates: x={profile.secret_coordinates['x']:.3f}, y={profile.secret_coordinates['y']:.3f}
🔢 Decoy Images: {len(profile.decoy_images)} files

🔐 RAW CIPHERTEXT (Base64):
{base64.b64encode(ciphertext).decode('utf-8')}

🔐 RAW CIPHERTEXT (Hex):
{ciphertext.hex()}

📊 Ciphertext Length: {len(ciphertext)} bytes

⚠️  WARNING: This is the encrypted token that was hidden in the image.
   The actual decrypted content is: "MLS_SUCCESS_TOKEN"
   Only the correct passphrase can decrypt this ciphertext.
"""
            self.results.setText(result_text)
            
        except Exception as e:
            self.results.setText(f"❌ Error extracting ciphertext: {str(e)}")


def main():
	import sys
	app = QtWidgets.QApplication(sys.argv)
	# Modernize visuals: Fusion style + custom QSS
	app.setStyle("Fusion")
	qss_path = Path("style.qss")
	if qss_path.exists():
		with qss_path.open("r", encoding="utf-8") as f:
			app.setStyleSheet(f.read())
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()