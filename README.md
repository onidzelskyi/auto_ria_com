auto.ria.com car image grabber
==============================

Crawl car images with car' info and collect info in db and google cloud bucket

Get Google cloud storage credentials
====================================

Create Service account keys
Go to APIs & Services -> Credentials.
Create Service account key.
Download key as a json file and store it locally
Add an environment variable with path to key file

```
GOOGLE_APPLICATION_CREDENTIALS=google.json
```

Get bucket path

```
gcloud auth login
gcloud projects list
gsutil ls -p muuze-195611'
```

Export mongodb collection to csv
================================
```
mongoexport --db=ukrgo_items --collection=ukrgo_items  --out=/Users/alex/Downloads/ukrgo.json --jsonArray
```

Convert image url to GCP bucket file name
=========================================
```code:pytonn
import hashlib

hashlib.sha1(b'http://dp.ukrgo.com/pictures/ukrgo_id_20275480.jpg').hexdigest()

>>> ec2b2751289ed2c1ef35efc917c609dad0012d2e
```

MySQL
=====

Connect to Google Cloud SQL instance
```
mysql -h 35.194.38.30 -u root -p
```

Save data in json file
======================
```
scrapy crawl cars -o data.json
```