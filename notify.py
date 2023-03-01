# https://firebase.google.com/docs/cloud-messaging/send-message#python
import os
import sys
import traceback
import firebase_admin
from firebase_admin import messaging

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_GOOGLE_APPLICATION_CREDENTIALS_name.json"

# firebase setup
# check if GOOGLE_APPLICATION_CREDENTIALS env variables exists
if os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None) == None:
    print('GOOGLE_APPLICATION_CREDENTIALS Not Found.')
    print('Check environment variable.')
    exit()
firebase_admin.initialize_app()
#======================================================================================================
def exception_detail(e):
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    return errMsg
#======================================================================================================
def send_message(notification, token_list):
    if token_list == []:
        return False, 'token_list empty'
    if notification.get('title') not in [None, '']:
        notify = messaging.Notification(title=notification.get('title'), body=notification.get('content', ''))
        android_notify = messaging.AndroidNotification(
            title=notification.get('title'), 
            body=notification.get('content', ''),
            default_sound=True
        )
    else:
        notify = messaging.Notification(body=notification.get('content', ''))
        android_notify = messaging.AndroidNotification(
            body=notification.get('content', ''),
            default_sound=True
        )

    multi_msg = messaging.MulticastMessage(
        notification=notify,
        tokens=token_list, 
        data={} if 'route' not in notification else {'direct': notification['route']},
        android=messaging.AndroidConfig(notification=android_notify, priority='high'),
        apns=messaging.APNSConfig(payload=messaging.APNSPayload(messaging.Aps(
            sound=messaging.CriticalSound('default', volume=1.0)
        )))
    )
    response = messaging.send_multicast(multi_msg)
    failed_tokens = []
    if response.failure_count > 0:
        responses = response.responses
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(token_list[idx])
        print('List of tokens that caused failures: {0}'.format(failed_tokens))
    return True, 'send to {} devices, with {} successed, with {} failed.'.format(
        len(token_list), response.success_count, response.failure_count)
#======================================================================================================
if __name__ == "__main__":
    notification = {
        "title": "python notify",
        "content": "notification content"
    }
    token_list = ["your_token"]
    state, value = send_message(notification, token_list)
    print(value)