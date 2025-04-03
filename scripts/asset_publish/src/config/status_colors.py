# -*- coding: utf-8 -*-

class StatusColor:
    """定义不同状态对应的颜色"""

    WAIT = "rgb(192,192,192)"  # 等待中
    PAUSE = "rgb(255,158,62)"  # 暂停
    RETAKE = "rgb(255,62,62)"  # 有反馈
    CHECK = "rgb(14,134,254)"  # 审核
    READY = "rgb(134,14,254)"  # 准备就绪
    REWORK = "rgb(150,150,150)"  # 返工
    APPROVE = "rgb(0,143,20)"

    @classmethod
    def get_color(cls, status):
        return getattr(cls, status.upper(), None)
