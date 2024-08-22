from abc import ABC, abstractmethod


class FlexRayInterface(ABC):
    @abstractmethod
    def connect(self):
        """建立FlexRay总线的连接"""
        pass

    @abstractmethod
    def close(self):
        """关闭FlexRay接口连接"""
        pass

    @abstractmethod
    def send_fr_message(self):
        """发送FlexRay消息"""
        pass

    @abstractmethod
    def receive_fr_message(self, channel, timeout=None):
        """接收FlexRay消息"""
        pass
