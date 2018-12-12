# #!/usr/bin/env python
# # -*- coding: utf8 -*-

# import os
# from functools import reduce
# import json
# from collections import OrderedDict
# import os
# # print(os.sys.path)
# import paramiko

# class FileConfig(object):

#     def __init__(self, machine, config_path):
#         pass

#     def __enter__(self):
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect('10.40.50.132', username='linuxadmin', password='Hello=111!')

#         sftp = ssh.open_sftp()
#         remote_file = sftp.file('/home/linuxadmin/variables.conf', mode='r+')
#         content = remote_file.read()
#         remote_file.close()

#         return content

#     def __exit__(self):
#         remote_temp_file = sftp.file('/home/linuxadmin/variables_1.conf', mode='w+')
#         remote_temp_file.write(json.dumps(json_content, indent=4, sort_keys=False))
#         remote_temp_file.close()

# class FileConfigClient(object):

#     def __init__(self, machine):
#         pass
        
#     def ssh_client(self):
#         pass

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



# # stdin, stdout, stderr = ssh.exec_command('ll')
# # output = stdout.readlines()
# # print '\n'.join(output)
# # print output