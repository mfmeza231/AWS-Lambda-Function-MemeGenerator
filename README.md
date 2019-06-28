# AWS Lambda Function - Meme Generator
- This Lambda function is triggerd by an Amazon IoT Dash Button and API Gateway (which is done on my website's IoT project page).
- The function then creates a meme using the Flickr API.
- The meme image file is then stored to an S3 bucket.
- Next, the url to the image located in S3 is inserted as part of a record in RDS (PostgreSQL DB).
- The meme is displayed on my website's IoT Project Page.

# Meme Generator App
- The meme generator app was created by following a project tutorial on acloud.guru (https://acloud.guru/series/acg-projects/view/104).
- Modifications were done to integrate the lambda funciton with my website and include another trigger using API Gateway.
