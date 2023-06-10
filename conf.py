import boto3
import yaml

conf = yaml.load(open('conf.yml', 'r'), yaml.CLoader)

s3_conf = conf["s3"]
mm_conf = conf["mattermost"]
mm_auth = mm_conf["auth"]

session = boto3.Session(
    aws_access_key_id = s3_conf["aws-access-key-id"],
    aws_secret_access_key = s3_conf["aws-secret-key-id"]
)
s3 = session.resource('s3')