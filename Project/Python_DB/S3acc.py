import boto3
import json

ACCESS_KEY = 'AKIAX2R4V25UA7N2724I'
SECRET_KEY = ''


s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)

bucket_name = "takealookdb"

# s3.upload_file(filename, bucket_name, filename)

# S3 Policy 설정 부여하기
bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPerm',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': "arn:aws:s3:::%s/*" % bucket_name
    }]
}
# Convert the policy to a JSON string
bucket_policy = json.dumps(bucket_policy)

# Set the new policy on the given bucket
s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
policy_res = s3.get_bucket_policy(Bucket="takealookdb")
print(policy_res)

# [S3 Policy 설정 삭제하기]

# s3.delete_bucket_policy(Bucket='netmgr-bucket')
acl_res = s3.get_bucket_acl(Bucket="takealookdb")



