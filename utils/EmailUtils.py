#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   EmailUtils.py
@Time    :   2022/08/11 19:34:21
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   None
'''


import yagmail
import yaml
import traceback
class AutoEmail():
    def __init__(self):
        pass
    def smtp_infor(self,user:str,password:str,host:str)->yagmail.SMTP:
        """Open POP3/SMTP e.g. 163 email 
        load the email user and password and host
        Note that: password is authorization temp password, not is your presonal password !!!

        Parameters
        ----------
        user : str
            Email user name
        password : str
            Authorization temp password, not is your presonal password !!!
        host : str
            It is the default email host 

        Returns
        -------
        yagmail.SMTP
            yagmail_server: sender information
        """
        self.yagmail_server = yagmail.SMTP(user=user, password=password, host=host)
        return self.yagmail_server
        
    def send(self, email_name:str, email_title:str, email_content:list, email_attachment:list=None):
        """send the email to the email_name, you can send to your own email address.
        
        Parameters
        ----------
        email_name : str
            Recipient, can be your own email address
        email_title : str
            what is it ?? title of the email
        email_content : list
            content
        email_attachment : list
            useful files (attachment)---> attachment path
        """
        try:
            self.yagmail_server.send(to=email_name, subject=email_title, contents=email_content, attachments=email_attachment)
            print("Sent email successfully")
        except Exception:
            print("Failed to send email")
            print(traceback.format_exc())



def config2email(email_config,email_attachment):
    email_config = yaml.load(open(email_config), Loader=yaml.FullLoader)
    email_send = AutoEmail()
    email_send.smtp_infor(email_config['user'],email_config['password'],email_config['port'])
    email_send.send(email_config['recipient'],email_config['email_title'], email_config['email_content'], email_attachment)


def config2email_error(email_config,error_infor):
    email_config = yaml.load(open(email_config), Loader=yaml.FullLoader)
    email_send = AutoEmail()
    email_send.smtp_infor(email_config['user'],email_config['password'],email_config['port'])
    email_send.send(email_config['recipient'],email_config['email_title'], error_infor)