import boto3
import StringIO
import zipfile
import mimetypes

try:
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:090877040118:ReactTopic')

    portfolio_bucket = s3.Bucket('beacloud.ninja')
    build_bucket = s3.Bucket('build.beacloud.ninja')

    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj('buildreactquiz.zip', portfolio_zip)

    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

    topic.publish(Subject="Code Deployed", Message="Code has been deployed")
except:
    topic.publish(Subject="Code Deploy Failed", Message="Code was NOT deployed")
    raise
