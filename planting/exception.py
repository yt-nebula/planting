class AnsibleException(Exception):
    def __init__(self, err='ansible exception'):
        Exception.__init__(self, err)


class AnsibleFailException(AnsibleException):
    def __init__(self, err='ansible task failed'):
        Exception.__init__(self, err)


class AnsibleUnreachableException(AnsibleException):
    def __init__(self, err='host unreachable'):
        Exception.__init__(self, err)
