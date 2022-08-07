import boto3

client = boto3.client('s3', region_name="eu-west-2")


def get_ffmpeg():
    print("Getting ffmpeg")

    client.download_file(
        Bucket="local-bot-tf-state",
        Key="ffmpeg.exe",
        Filename="ffmpeg.exe"
    )
