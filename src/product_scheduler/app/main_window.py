from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from product_scheduler.app.widgets.gantt_widget import GanttWidget
from product_scheduler.core.schedule import Schedule
from product_scheduler.core.interfaces.schedule_factory import ScheduleFactory


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        self.repository = ScheduleFactory(
            repository_dir="..\\datas\\datas_sample_20260103_00"
        )
        self.scheduler = self.repository.build()

        gantt_widget = GanttWidget(self.scheduler)
        main_layout.addWidget(gantt_widget)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
