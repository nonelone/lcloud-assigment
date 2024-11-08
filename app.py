import boto3

import secrets

s3 = boto3.resource(
    's3',
    aws_access_key_id = secrets.access_key_id,
    aws_secret_access_key = secrets.access_key
    )


def list_files(bucket, prefix=""):
    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key != ( prefix + "/" ): # do not print the root directory
            print(obj.key)

def upload_file(file, target):
    pass

def filter_files(filter, bucket="*"):
    pass

def delete_files_by_filter(filter, bucket="*"):
    pass

if __name__ == "__main__":
    
    bucket = s3.Bucket('developer-task')
    prefix = "a-wing"
    
    list_files(bucket, prefix)