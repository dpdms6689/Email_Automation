import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

def send_email(smtp_info, msg):
    with smtplib.SMTP(smtp_info["smtp_server"], smtp_info["smtp_port"]) as server:
        server.starttls()
        server.login(smtp_info["smtp_user_id"], smtp_info["smtp_user_pw"])
        response = server.sendmail(msg['From'], msg['To'], msg.as_string())

        if not response:
            print('이메일을 성공적으로 보냈습니다.')
        else:
            print(response)

def make_multimsg(msg_dict):
    multi = MIMEMultipart(_subtype='mixed')

    for key, value in msg_dict.items():
        if key == 'text':
            with open(value['filename'], encoding='utf-8') as fp:
                msg = MIMEText(fp.read(), _subtype=value['subtype'])
        elif key == 'image':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=value['subtype'])
        elif key == 'audio':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEAudio(fp.read(), _subtype=value['subtype'])
        else:
            with open(value['filename'], 'rb') as fp:
                msg = MIMEBase(value['maintype'], value['subtype'])
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)

        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(value['filename']))
        multi.attach(msg)

    return multi

smtp_info = {
    'smtp_server': 'smtp.naver.com',
    'smtp_port': 587,
    'smtp_user_id': 'dpdms6689@naver.com',
    'smtp_user_pw': 'chldPdms1234!'
}

msg_dict = {
    'text': {'filename': 'C:/Users/user15/Desktop/최예은/이메일 전송 자동화/hello.txt', 'subtype': 'plain'},
    'image': {'filename': 'C:/Users/user15/Desktop/최예은/이메일 전송 자동화/test_8.jpg', 'subtype': 'jpeg'},
    'audio': {'filename': 'C:/Users/user15/Desktop/최예은/이메일 전송 자동화/test.mp3', 'subtype': 'mpeg'}
}

msg = MIMEMultipart()
msg['From'] = 'dpdms6689@naver.com'
msg['To'] = 'soonsung0728@naver.com'
msg['Subject'] = 'dpdms6689@naver.com'

# 메일 본문 내용 추가
msg.attach(MIMEText('여러 형식의 파일이 첨부된 이메일입니다.', 'plain', 'utf-8'))

# 첨부 파일 추가
multi = make_multimsg(msg_dict)
msg.attach(multi)

try:
    send_email(smtp_info, msg)
except Exception as e:
    print(f"오류 발생: {e}")
