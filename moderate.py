import email
import html2text
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
            action = None
            while action is None:
                choice = input('b: show body, h: show header, s: skip, a: accept, r: reject, d: discard: ')
                if choice == 'b':
                    msg = email.message_from_string(message.msg)
                    payload = str(msg.get_payload(decode=True))
                    if msg.get_content_type() == 'text/html':
                        payload = html2text.html2text(payload)
                    pydoc.pager(payload)
                elif choice == 'h':
                    msg = email.message_from_string(message.msg)
                    pydoc.pager('\n'.join(f'{key}: {value}' for key, value in msg.items()))
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
                print()
