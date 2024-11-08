import boto3
import re

import secrets

s3 = boto3.resource(
    's3',
    aws_access_key_id = secrets.access_key_id,
    aws_secret_access_key = secrets.access_key
    )


def list_files(bucket, prefix=""):
    files = []
    for obj in bucket.objects.filter(Prefix=prefix):
        file_name = obj.key.split("/")[-1]
        if obj.key != ( prefix + "/" ) and file_name != "": # do not print the root directory
            print(file_name)
            files.append(file_name)

    return files



def upload_file(file, target):
    pass

def filter_files(re_filter, bucket="*", prefix=""):
    files = []
    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key != ( prefix + "/" ): # ignore the root directory
            files.append(obj.key)

    for file in files:
        match = re.search(re_filter, file)
        if not match:
            files.remove(file)
        else:
            print(file)

    return files

    

def delete_files_by_filter(re_filter, bucket="*", prefix=""):
    pass

if __name__ == "__main__":

    bucket = s3.Bucket('developer-task')
    prefix = "a-wing"
    
    _ = list_files(bucket, prefix)

    example_filter = "^i"

    _ = filter_files(example_filter, bucket, prefix)