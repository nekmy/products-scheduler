from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from app.widgets.gantt_widget import GanttWidget
from core.scheduler import Scheduler
from core.schedule_repository import ScheduleRepository


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        self.repository = ScheduleRepository(
            repository_dir="..\\datas\\datas_sample_20260103_00"
        )
        self.scheduler = self.repository.read_scheduler()

        gantt_widget = GanttWidget(self.scheduler)
        main_layout.addWidget(gantt_widget)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
