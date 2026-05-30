from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsTextItem,
)
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import QPointF


class JobRectItem(QGraphicsRectItem):

    def __init__(self, gantt_scene, x, y, w, h, text):
        self.gantt_scene = gantt_scene
        super().__init__(0, 0, w, h)
        self.setFlags(
            QGraphicsRectItem.ItemIsMovable
            | QGraphicsRectItem.ItemIsSelectable
            | QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("skyBlue")))
        self.text_item = QGraphicsTextItem(parent=self)
        html_text = '<span style="color: #000000; font-family: Arial; font-size: 20pt; font-weight: bold;">{0}</span>'.format(
            text
        )
        self.text_item.setHtml(html_text)

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange and self.scene():
            line_id, time_bucket_id = self.gantt_scene.pos_to_id(value)
            return QPointF(*self.gantt_scene.id_to_pos(line_id, time_bucket_id))
        return super().itemChange(change, value)
