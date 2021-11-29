import mailmanclient
import pydoc


if __name__ == '__main__':
    try:
        from config import url, password, user
    except ImportError:
        print('Create a config.py file with url, user and password variables')
        quit(1)

    client = mailmanclient.Client(url, user, password)
    for maillist in client.lists:
        for message in maillist.held:
            print('List name:', maillist.fqdn_listname)
            print('Member count:', maillist.member_count)
            print('Sender:', message.sender)
            print('Subject:', message.subject)
            print('Reason:', message.reason)
            choice = input('m: show message, s: skip, a: accept, r: reject, d: discard: ')
            action = None
            while action is None:
                if choice == 'm':
                    pydoc.pager(message.msg)
                elif choice == 's':
                    action = 'skip'
                    comment = None
                elif choice == 'a':
                    action = 'accept'
                    comment = None
                elif choice == 'r':
                    action = 'reject'
                    comment = input('Reason to reject: ')
                elif choice == 'd':
                    action = 'discard'
                    comment = None
                else:
                    print('Illegal choice')
            if action != 'skip':
                message.moderate(action, comment)
