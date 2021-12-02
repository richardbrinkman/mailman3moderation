import email
import html2text
import mailmanclient
import pydoc


def extract_part(parts, content_type='text/plain'):
    content_parts = [part for part in parts if part.get_content_type() == content_type]
    if content_parts:
        return content_parts[0]


def show_message_body(message):
    msg = email.message_from_string(message.msg)
    while msg.is_multipart():
        parts = msg.get_payload()
        msg = extract_part(parts, 'text/plain') or extract_part(parts, 'text/html') or extract_part(parts, 'multipart/alternative')
    payload = msg.get_payload(decode=True)
    if isinstance(payload, bytes):
        payload = payload.decode()
    if msg.get_content_type() == 'text/html':
        payload = html2text.html2text(payload)
    pydoc.pager(payload)


def run():
    try:
        from config import url, password, user
    except ImportError:
        print('Create a config.py file with url, user and password variables')
        return
    client = mailmanclient.Client(url, user, password)
    for maillist in client.lists:
        for message in maillist.held:
            print('List name:', maillist.fqdn_listname)
            print('Member count:', maillist.member_count)
            print('Sender:', message.sender)
            print('Subject:', message.subject)
            print('Reason:', message.reason)
            action = None
            comment = None
            while action is None:
                choice = input('b: show body, h: show header, s: skip, a: accept, r: reject, d: discard: ')
                if choice == 'b':
                    show_message_body(message)
                elif choice == 'h':
                    msg = email.message_from_string(message.msg)
                    pydoc.pager('\n'.join(f'{key}: {value}' for key, value in msg.items()))
                elif choice == 's':
                    action = 'skip'
                elif choice == 'a':
                    action = 'accept'
                elif choice == 'r':
                    action = 'reject'
                    comment = input('Reason to reject: ')
                elif choice == 'd':
                    action = 'discard'
                else:
                    print('Illegal choice')
            if action != 'skip':
                message.moderate(action, comment)
                print()


if __name__ == '__main__':
    run()
