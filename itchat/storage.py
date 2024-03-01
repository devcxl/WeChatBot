import os
import pickle


class LocalStorage:
    def __init__(self, directory='data'):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save(self, key, obj):
        """序列化对象并保存到文件"""
        file_path = os.path.join(self.directory, f'{key}.pickle')
        with open(file_path, 'wb') as f:
            pickle.dump(obj, f)

    def load(self, key):
        """从文件反序列化对象"""
        file_path = os.path.join(self.directory, f'{key}.pickle')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        else:
            raise FileNotFoundError(f"No such file: {file_path}")

    def delete(self, key):
        """删除序列化的对象文件"""
        file_path = os.path.join(self.directory, f'{key}.pickle')
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"No such file: {file_path}")
