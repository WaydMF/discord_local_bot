import boto3

client = boto3.client('s3', region_name="eu-west-2")


def get_ffmpeg():
    print("Getting ffmpeg")

    client.download_file(
        Bucket="local-bot-tf-state",
        Key="ffmpeg/ffmpeg.exe",
        Filename="local_bot/ffmpeg.exe"
    )
    client.download_file(
        Bucket="local-bot-tf-state",
        Key="ffmpeg/ffplay.exe",
        Filename="local_bot/ffplay.exe"
    )
    client.download_file(
        Bucket="local-bot-tf-state",
        Key="ffmpeg/ffprobe.exe",
        Filename="local_bot/ffprobe.exe"
    )

    client.download_file(
        Bucket="local-bot-tf-state",
        Key="ffmpeg/ffmpeg.exe",
        Filename="ffmpeg.exe"
    )
    client.download_file(
        Bucket="local-bot-tf-state",
        Key="ffmpeg/ffplay.exe",
        Filename="ffplay.exe"
    )
    client.download_file(
        Bucket="local-bot-tf-state",
        Key="ffmpeg/ffprobe.exe",
        Filename="ffprobe.exe"
    )

