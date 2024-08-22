from abc import ABC, abstractmethod


class CanInterface(ABC):
    @abstractmethod
    def connect(self):
        """建立CAN总线的连接"""
        pass

    @abstractmethod
    def close(self):
        """关闭CAN接口连接"""
        pass

    @abstractmethod
    def send(self, data, arb_id, is_extended=None, is_error=False, is_remote=False, is_fd=False):
        """
        发送CAN消息

        :return:
        """
        pass

    @abstractmethod
    def receive(self, channel, timeout=None):
        """
        接收CAN消息

        :return: 返回接收到的消息元组 (message_id, data, timestamp)
        """
        pass
