import boto3

import re, os

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
            files.append(file_name)

    if files == []: print("No files found!")

    return files


def upload_file(file, bucket, prefix=""):
    upload_client = boto3.client(
            's3',
            aws_access_key_id = secrets.access_key_id,
            aws_secret_access_key = secrets.access_key
        )
    
    try:
        response = upload_client.upload_file(file, bucket, os.path.basename(file))
    except Exception as e:
        print(e)
        return False
    
    return True

def filter_files(re_filter, bucket="*", prefix=""):
    files = []

    for obj in bucket.objects.filter(Prefix=prefix):
        file_name = obj.key.split("/")[-1]
        if obj.key != ( prefix + "/" ) and file_name != "": # ignore the root directory
            files.append(file_name)

    res_files = []
    for file in files:
        found = re.search(re_filter, file)
        if found:
            res_files.append(file)
    
    if res_files == []: print("No files found!")

    return res_files

def delete_files_by_filter(re_filter, bucket="*", prefix=""):
    files_to_delete = filter_files(example_filter, bucket, prefix)
    
    deletion_client = boto3.client(
        's3',
        aws_access_key_id = secrets.access_key_id,
        aws_secret_access_key = secrets.access_key
    )

    # we have only filename and not the path:
    file_paths = []
    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key.split("/")[-1] in files_to_delete:
            file_paths.append(obj.key)

    
    for file in file_paths:
        try:
            res = deletion_client.delete_object(Bucket=bucket.name, Key=file)
        except Exception as e:
            print(e)
            return False

    return True

if __name__ == "__main__":

    running = True

    print("Welcome to S3 AWS CLI")

    bucket_name = input("Give me the name of the bucket > ")
    prefix_name = input("Give me the prefix > ")
    bucket = s3.Bucket(bucket_name)
    prefix = prefix_name

    print("Usage: list_files, upload_files, filter_files, delete_files, exit")

    while running:
        order = input("What do you want to do: ")

        match order:
            case "help":
                print("Usage: list_files, upload_files, filter_files, delete_files, exit")
            
            case "list_files":
                files = list_files(bucket, prefix)
                for file in files:
                    print(file)

            case "upload_files":
                path = input("What file? ")
                res = upload_file(path, bucket.name, prefix)
                if res == True:
                    print("Done.") #no need to print false as the user will see an error

            case "filter_files":
                given_filter = input("What RE? ")
                files = filter_files(given_filter, bucket, prefix)
                for file in files:
                    print(file)

            case "delete_files":
                given_filter = input("What RE? ")
                res = delete_files_by_filter(example_filter, bucket, prefix)
                if res == True:
                    print("Done")

            
            case "exit": running = False




    
    