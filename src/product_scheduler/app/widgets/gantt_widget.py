from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QGraphicsScene,
    QGraphicsView,
)
from PySide6.QtGui import QPainter, QColor, QPen

from product_scheduler.core.elements.job import Job
from product_scheduler.core.schedule import Schedule
from product_scheduler.app.widgets.job_rect_item import JobRectItem


class GanttScene(QGraphicsScene):
    """
    ガントチャートの表示を行うscene
    """

    def __init__(
        self,
        n_lines: int,
        time_bucket_width: int,
        line_height: int,
        job_rect_height: int,
    ):
        """ """
        super().__init__(0, 0, 2000, 1000)
        self.n_lines = n_lines
        self.time_bucket_width = time_bucket_width
        self.line_height = line_height
        self.job_rect_height = job_rect_height

    def drawBackground(self, painter: QPainter, rect):
        painter.setPen(QPen(QColor(0, 0, 0, 30), 2))
        # lineの区切り線

        for i in range(0, self.n_lines + 1):
            y = i * self.line_height
            painter.drawLine(rect.x(), y, rect.x() + rect.width(), y)
        # time_bucketの区切り線
        display_first_j = int(rect.x() // self.time_bucket_width)
        display_last_j = int((rect.x() + rect.width()) // self.time_bucket_width)
        for j in range(display_first_j, display_last_j + 1):
            x = j * self.time_bucket_width
            painter.drawLine(x, rect.y(), x, rect.y() + rect.height())
        return

    def add_job(self, job: Job):
        """
        jobの追加

        :param self: 説明
        :param job: 説明
        """
        x, y = self.id_to_pos(job.assigned_resources, job.start_time_bucket_id)
        w = 1
        h = self.job_rect_height
        job_rect_item = JobRectItem(self, x, y, w, h, job.name)
        self.addItem(job_rect_item)

    def pos_to_id(self, pos):
        line_id = int(pos.y()) // self.line_height
        time_bucket_id = int(pos.x()) // self.time_bucket_width
        return line_id, time_bucket_id

    def id_to_pos(self, line_id, time_bucket_id):
        x = time_bucket_id * self.time_bucket_width
        y = line_id * self.line_height + (self.line_height - self.job_rect_height) / 2
        return x, y


class GanttWidget(QWidget):
    TIME_BUCKET_WIDTH = 100
    LINE_HEIGHT = 100
    JOB_RECT_HEIGHT = 50

    def __init__(self, scheduler: Schedule):
        super().__init__()
        self.scheduler = scheduler
        self.gantt_scene = GanttScene(
            self.scheduler.n_resources,
            self.TIME_BUCKET_WIDTH,
            self.LINE_HEIGHT,
            self.JOB_RECT_HEIGHT,
        )
        self.gantt_view = QGraphicsView(self.gantt_scene)
        layout = QHBoxLayout()
        layout.addWidget(self.gantt_view)
        self.setLayout(layout)

        for job_id, job in self.scheduler._jobs.items():
            self.gantt_scene.add_job(job)
