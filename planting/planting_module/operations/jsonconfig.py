# #!/usr/bin/env python
# # -*- coding: utf8 -*-

# import os
# # from planting.planting_module import ModuleBase
# from functools import reduce
# import json
# from collections import OrderedDict
# # from sftp_client import SFTPClient

# import os
# print os.sys.path

# # with SFTPClient(host, username, password, license_key='license_key') as ssh_client:
# #     ssh_client.download('./server_path.txt', '~/variables.conf')
# #     # ssh_client.upload('./server_path2.txt', ~/local_path.txt)
# #     print client.list_directory('./')


# #     sftp_client = ssh_client.open_sftp()
# #     remote_file = sftp_client.open('~/variables.conf')
# #     print
# #     try:
# #         for line in remote_file:
# #             pass
# #             # process line
# #     finally:
# #         remote_file.close()
# import paramiko
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('10.40.50.132', username='linuxadmin', password='Hello=111!')

# sftp = ssh.open_sftp()
# remote_file = sftp.file('/home/linuxadmin/variables.conf', mode='r+')
# content = remote_file.read()
# remote_file.close()

# content = content.replace('platform', 'aaa')
# print content
# print '\n',type(content),'\n'

# content = content.replace('platform', 'aaa')

# json_content = json.loads(content, object_pairs_hook=OrderedDict)
# print json_content
# print '\n',type(json_content),'\n'


# json_content['_face_aaa_ip'] = '127.0.0.5'
# print json_content
# print '\n',type(json_content),'\n'

# remote_temp_file = sftp.file('/home/linuxadmin/variables_1.conf', mode='w+')
# remote_temp_file.write(json.dumps(json_content, indent=4, sort_keys=False))
# remote_temp_file.close()

# # stdin, stdout, stderr = ssh.exec_command('ll')
# # output = stdout.readlines()
# # print '\n'.join(output)
# # print output