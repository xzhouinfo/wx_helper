import itchat
import random
import get_movie
import requests


@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE], isGroupChat=True)
def group_reply(msg):

    try:
        from_user_name = msg['FromUserName']
        group = itchat.search_chatrooms(userName=from_user_name)
        print(group['NickName'] + "群的 " + msg['ActualNickName'] + " 发来的消息\n" +
              get_text(msg))
        if '@向往 谢谢你' in get_text(msg):
            ketao = ['不客气', '真的不用客气', '真的真的不用客气']
            itchat.send(random.choice(ketao), msg['FromUserName'])

        if msg.isAt:
            if 'ssdy-' in get_text(msg):
                key = get_text(msg).split('-')[-1]
                print(key)
                f = get_movie.get(key)
                print('这是f-------', f)
                if '可以百度离线下载或者用下载软件下载' in f:

                    itchat.send(f, msg['FromUserName'])
                    itchat.send_file('download_link.txt', msg['FromUserName'])
                else:
                    itchat.send(f, msg['FromUserName'])
    except Exception as e:
        print(e)


@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE], isFriendChat=True)
def friends_reply(msg):
    try:
        if msg['Type'] == 'Text':
            if 'ssdy-' in get_text(msg):
                key = get_text(msg).split('-')[-1]
                print(key)
                f = get_movie.get(key)
                print('这是f-------', f)
                if '可以百度离线下载或者用下载软件下载' in f:

                    itchat.send(f, msg['FromUserName'])
                    itchat.send_file('download_link.txt', msg['FromUserName'])
                else:
                    itchat.send(f, msg['FromUserName'])
    except Exception as e:
        print(e)




def get_text(msg):
    if msg['Type'] == 'Text':
        return msg['Text']
    else:
        return 'halo'


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run()