from memeify import text, images, flickr

import boto3
from botocore.client import Config
from boto3.dynamodb.conditions import Key
import psycopg2

import logging
import os
import time
import uuid
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # 'SINGLE', 'DOUBLE', 'LONG'
    click_type = event.get('clickType', 'SINGLE')

    if click_type == 'SINGLE':
        make_new_meme(event, context)

    return

def make_new_meme(event, context):
    ## Environment
    #
    # Required
    flickr_key = os.environ['FLICKR_KEY']
    flickr_secret = os.environ['FLICKR_SECRET']
    aws_region = os.environ['AWS_REGION']
    meme_bucket_name = os.environ['MEMES_BUCKET_NAME']
    #
    #
     # Optional
    font_url = os.environ.get('FONT_URL', None)
    text_url = os.environ.get('TEXT_URL', None)
    #
    ## End Environment

    session = boto3.Session(region_name=aws_region)

    # Generate text
    txt_gen = text.TextGen(text_url)
    txt = txt_gen.make_short_sentence()
    logging.info("Text: '{0}'".format(txt))

    # Pick a photo
    flckr = flickr.Flickr(flickr_key, flickr_secret)
    photo = flckr.pick_photo(txt)

    orig_url = "https://www.flickr.com/photos/{0}/{1}".format(photo['owner'],
                                                              photo['id'])
    logging.info("Photo: '{0}'".format(orig_url))

    photo_bytes = flckr.download_photo_bytes(photo)
    orig_img = images.bytes_to_image(photo_bytes)

    # Put text on image
    line1, line2 = txt_gen.split_meme(txt)
    img_obj = images.build_meme(orig_img, font_url, line1, line2)

    meme_uuid = uuid.uuid4()
    s3_key = 'memes/{0}.png'.format(meme_uuid)

    # Upload final image to S3
    s3 = session.resource('s3')
    meme_bucket = s3.Bucket(meme_bucket_name)

    meme_bucket.upload_fileobj(
        images.image_to_bytes(img_obj),
        s3_key,
        ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
        )

    s3_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(aws_region,
                                                           meme_bucket_name,
                                                           s3_key)
    # Connect to RDS PostgreSQL DB and upload object
    conn_string = "dbname='"+os.environ['RDS_DB_NAME']+"' port='"+os.environ['RDS_PORT']+"' user='"+os.environ['RDS_USERNAME']+"' password='"+os.environ['RDS_PASSWORD']+"' host='"+os.environ['RDS_HOSTNAME']+"'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO meme_meme(unixtime, s3_url) VALUES(%s, %s)", (Decimal(str(time.time())), s3_url))
    conn.commit()
    cursor.close()
    print("working")

    return
