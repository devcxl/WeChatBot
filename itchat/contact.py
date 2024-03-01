class Contact:
    """
    联系人
    """

    def __init__(self, raw):
        self.raw = raw
        pass

    @property
    def id(self):
        """
        联系人ID
        """
        return self.raw.get('ID')

    @property
    def remark_name(self):
        """
        备注名称
        """
        return self.raw.get('RemarkName')

    def delete(self):
        """
        删除联系人
        :return:
        """


class SingleContact(Contact):
    """
    单独联系人
    """

    def __init__(self, raw):
        super().__init__(raw)

    @property
    def phone(self):
        """
        电话号码
        """
        return self.raw.get('ID')

    @property
    def sex(self):
        """
        # 男性  1
        # 女性  2
        """
        return self.raw.get('Sex')

    @property
    def province(self):
        """
        省份
        """
        return self.raw.get('Province')

    @property
    def city(self):
        """
        城市
        """
        return self.raw.get('City')

    @property
    def signature(self):
        """
        个性签名
        """
        return self.raw.get('Signature')


class GroupContact(Contact):
    """
    群组联系人
    """

    def __init__(self, raw):
        super().__init__(raw)

    def get_members(self):
        """
        获取群组中的成员
        :return:
        """
        pass
