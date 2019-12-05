import logging
import boto3
from botocore.exceptions import ClientError

# 업로드할 폴더 경로
path_dir = "C:\\Users\\JJunJang\\Desktop\\Dataset\\img_resize\\"

def delete_object(bucket_name, object_name):

    # Delete the object
    s3 = boto3.client('s3')

    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def main():
    """Exercise delete_object()"""

    # Assign these values before running the program
    test_bucket_name = 'takealookdb'
    test_object_name = 'tt0116684.jpg'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Delete the object
    if delete_object(test_bucket_name, test_object_name):
        logging.info(f'{test_object_name} was deleted from {test_bucket_name}')


if __name__ == '__main__':
    main()