import ftplib
from io import BytesIO
from datetime import datetime
import boto3

def lambda_handler(event, context):
    AWS_BUCKET_NAME = 'short-selling'
    today= datetime.today().strftime('%Y-%m-%d')
    s3 = boto3.client('s3')
    ftp = ftplib.FTP('ftp3.interactivebrokers.com', 'shortstock')
    files = ftp.nlst()
    for f in files:
        if not f.endswith('.txt'):
            # only want .txt files
            continue
        b = BytesIO()
        ftp.retrbinary('RETR ' + f, b.write)
        b.seek(0)
        path = today + ' ' + f
        s3.upload_fileobj(b, AWS_BUCKET_NAME, path)
    ftp.quit()
    return {
        'statusCode': 200,
        'body': 'uploaded ' today + ' files'
    }
