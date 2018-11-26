from machine import Machine
from planting_module import operations

if __name__ == '__main__':
    node = Machine('xxx.xxx.xxx.xxx', 'xxxx', 'xxxx')
    node.register_all()
    node.list_all_module()
    node.create(path="~/dir", state="dir")
    node.create(path="~/dir/1.txt", state="file")