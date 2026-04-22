import sys
import os
import json
import glob
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, QEvent

class EDMissionHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.missions = {}
        self.available_market_stock = {}
        self.max_cargo = 0
        self.last_log_file = None
        self.file_handle = None
        
        # Sürükleme işlemi için değişken
        self.drag_position = None
        self.is_dragging = False
        
        self.init_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setObjectName("main_window")
        
        self.setStyleSheet("""
            QWidget#main_window {
                background-color: transparent;
            }
            QWidget#bg_panel {
                background-color: rgba(0, 0, 0, 120);
                border: 1px solid #ff8200;
                border-radius: 6px;
            }
            QLabel {
                color: #ff8200; 
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: bold;
                padding: 4px;
            }
            QPushButton {
                background-color: #cc0000;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                font-family: Arial;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        
        self.root_layout = QVBoxLayout()
        self.root_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_panel = QWidget()
        self.bg_panel.setObjectName("bg_panel")
        self.main_layout = QVBoxLayout(self.bg_panel)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)

        self.close_btn = QPushButton("X")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(self.close)

        self.top_layout.addStretch()
        self.top_layout.addWidget(self.close_btn)
        
        self.label = QLabel("Yükleniyor...")
        
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.label)

        self.root_layout.addWidget(self.bg_panel)
        self.setLayout(self.root_layout)

        # Arka panel ve alt widget'lar üstünden pencere sürükleme
        self.bg_panel.installEventFilter(self)
        self.label.installEventFilter(self)
        self.close_btn.installEventFilter(self)

    def get_ed_paths(self):
        user_profile = os.environ.get('USERPROFILE')
        base = os.path.join(user_profile, 'Saved Games', 'Frontier Developments', 'Elite Dangerous')
        logs = glob.glob(os.path.join(base, 'Journal.*.log'))
        latest = max(logs, key=os.path.getmtime) if logs else None
        return latest, os.path.join(base, 'Cargo.json'), os.path.join(base, 'Market.json')

    def clean_name(self, name):
        if not name: return ""
        return name.replace("$", "").replace("_Name;", "").replace(";", "").lower().strip()

    def process_journal_event(self, data):
        event = data.get('event')

        if event == 'Loadout':
            self.max_cargo = data.get('CargoCapacity', self.max_cargo)

        elif event == 'MissionAccepted':
            item = data.get('Commodity_Localised') or data.get('Commodity')
            if item:
                station = data.get('DestinationStation', 'Bağış / Mevcut İstasyon')
                self.missions[data['MissionID']] = {
                    'item': self.clean_name(item),
                    'total_req': data.get('Count', 1),
                    'delivered': 0,
                    'station': station
                }

        elif event == 'CargoDepot' and data.get('UpdateType') == 'Deliver':
            m_id = data['MissionID']
            if m_id in self.missions:
                self.missions[m_id]['delivered'] = data.get('Count', 0)

        elif event in ['MissionCompleted', 'MissionAbandoned', 'MissionFailed']:
            self.missions.pop(data.get('MissionID'), None)

    def rebuild_state_from_recent_logs(self, current_log, keep_last_logs=2):
        """Aktif görevi kaçırmamak için son birkaç journal dosyasını baştan tarar."""
        all_logs = sorted(glob.glob(os.path.join(os.path.dirname(current_log), 'Journal.*.log')), key=os.path.getmtime)
        if not all_logs:
            self.missions = {}
            return

        if current_log in all_logs:
            idx = all_logs.index(current_log)
            start = max(0, idx - (keep_last_logs - 1))
            logs_to_parse = all_logs[start:idx + 1]
        else:
            logs_to_parse = all_logs[-keep_last_logs:]

        self.missions = {}

        for log_path in logs_to_parse:
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        try:
                            self.process_journal_event(json.loads(line))
                        except:
                            continue
            except:
                continue

    def tick(self):
        log_file, cargo_file, market_file = self.get_ed_paths()
        if not log_file: return

        if log_file != self.last_log_file:
            self.last_log_file = log_file
            if self.file_handle: self.file_handle.close()

            # Gece yarısı yeni log'a geçildiğinde dünkü aktif görevleri de koru.
            self.rebuild_state_from_recent_logs(log_file, keep_last_logs=2)

            self.file_handle = open(log_file, 'r', encoding='utf-8', errors='ignore')
            self.file_handle.seek(0, os.SEEK_END)

        self.available_market_stock = {}
        if os.path.exists(market_file):
            try:
                with open(market_file, 'r', encoding='utf-8') as f:
                    m_data = json.load(f)
                    for item in m_data.get('Items', []):
                        if item.get('Stock', 0) > 0:
                            name = self.clean_name(item.get('Name_Localised', item['Name']))
                            self.available_market_stock[name] = item['Stock']
            except: pass

        while True:
            line = self.file_handle.readline()
            if not line: break
            try:
                data = json.loads(line)
                self.process_journal_event(data)
            except: continue

        cargo = {}
        cur_c = 0
        if os.path.exists(cargo_file):
            try:
                with open(cargo_file, 'r', encoding='utf-8') as f:
                    c_data = json.load(f)
                    max_c = c_data.get('MaxInventory')
                    if not max_c: max_c = self.max_cargo
                    
                    for i in c_data.get('Inventory', []):
                        n = self.clean_name(i.get('Name_Localised', i['Name']))
                        cargo[n] = i['Count']
                        cur_c += i['Count']
            except: 
                max_c = self.max_cargo
        else:
            max_c = self.max_cargo

        self.update_ui(cargo, cur_c, max_c)

    def update_ui(self, cargo, cur_c, max_c):
        total_required_qty = 0

        if not self.missions:
            display_text = "🚀 ED MISSION TRACKER\nAktif teslimat yok."
        else:
            total_shopping = {}
            mission_lines = ["📋 GÖREV LİSTESİ"]
            mission_lines.append("-" * 35)
            
            for m in self.missions.values():
                remaining = m['total_req'] - m['delivered']
                if remaining > 0:
                    total_shopping[m['item']] = total_shopping.get(m['item'], 0) + remaining
                    mission_lines.append(f"📍 {m['station']} | {m['item'].title()}: {remaining} Adet")

            lines = ["🛒 TOPLAM İHTİYAÇ LİSTESİ"]
            lines.append("-" * 35)
            total_required_qty = sum(total_shopping.values())
            
            for item, total_needed in total_shopping.items():
                curr_in_ship = cargo.get(item, 0)
                stock_count = self.available_market_stock.get(item, 0)
                market_alert = f" 🏪 [MARKETTE VAR: {stock_count}]" if stock_count > 0 else ""
                missing_to_buy = total_needed - curr_in_ship
                buy_hint = f" (➡️ {missing_to_buy} tane al)" if 0 < curr_in_ship < total_needed else ""
                
                icon = "✅" if curr_in_ship >= total_needed else "⚠️"
                lines.append(f"{icon} {item.title()}: {curr_in_ship} / {total_needed}{buy_hint}{market_alert}")
            
            display_text = "\n".join(mission_lines) + "\n\n" + "\n".join(lines)

        if max_c > 0:
            display_text += f"\n\n🚢 KARGO: {cur_c} / {max_c} (%{int((cur_c/max_c)*100)})"
        else:
            display_text += f"\n\n🚢 KARGO: {cur_c} / ?"

        if total_required_qty > 0:
            if max_c > 0:
                capacity_status = "✅ Kargo alanı yeterli" if total_required_qty <= max_c else "❌ Kargo alanı yetersiz"
                display_text += f"\n📦 İHTİYAÇ/KAPASİTE: {total_required_qty}/{max_c} ({capacity_status})"
            else:
                display_text += f"\n📦 İHTİYAÇ/KAPASİTE: {total_required_qty}/? (Kapasite bilgisi yok)"

        self.label.setText(display_text)
        self.adjustSize()

    # --- SÜRÜKLE BIRAK SİSTEMİ (YENİLENDİ) ---
    def mousePressEvent(self, event):
        # Sadece sol tık ile sürüklensin
        if event.button() == Qt.MouseButton.LeftButton:
            # Tıklanan nokta ile pencerenin sol üst köşesi arasındaki farkı al
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.is_dragging = False
            event.accept()

    def mouseMoveEvent(self, event):
        # Sol tık basılı tutularak fare hareket ettiriliyorsa
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            # Pencereyi yeni konuma taşı
            self.move(event.globalPosition().toPoint() - self.drag_position)
            self.is_dragging = True
            event.accept()

    def mouseReleaseEvent(self, event):
        # Fare bırakıldığında sürüklemeyi sıfırla
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            self.is_dragging = False
            event.accept()

    def eventFilter(self, obj, event):
        # Label ve buton üstünden de pencere sürüklenebilsin
        if obj in (self.bg_panel, self.label):
            if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                self.is_dragging = False

            elif event.type() == QEvent.Type.MouseMove and (event.buttons() & Qt.MouseButton.LeftButton) and self.drag_position is not None:
                self.move(event.globalPosition().toPoint() - self.drag_position)
                self.is_dragging = True
                return True

            elif event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
                self.drag_position = None
                self.is_dragging = False

        # Kapatma butonu normal çalışsın, sürüklemeyi tetiklemesin
        elif obj == self.close_btn:
            if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
                self.drag_position = None
                self.is_dragging = False

        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        # Escape tuşu ile kapat
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    hud = EDMissionHUD()
    hud.show()
    sys.exit(app.exec())
