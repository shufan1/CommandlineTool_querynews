# CommandlineTool_querynews

This is a command line built in the AWS cloud enviornment. It takes keywords from Terminal and query the Global Event, Language and Tone Database with AWS Athena.<br>
![image](https://user-images.githubusercontent.com/39500675/137047385-9fa6fa59-8b79-4f42-8a3f-921193e51b2e.png)
## Example:
```
chmod +x news_cli.py
./news_cli.py --yearmonth 201410 --name "BARACK OBAMA" --orderby globaleventid --order ascending
```
![image](https://user-images.githubusercontent.com/39500675/137047604-c8344c93-91c6-4a4b-a1f0-a78b9d3776d3.png)

## Sceheme:
![image](https://user-images.githubusercontent.com/39500675/137047902-da75d41e-c4fd-49eb-9fa6-889fe4a81fee.png)


## preparing the data in S3:
1. create database in AWS Glue
2. Create an S3 bucket for putting output
3. In Athena, in settings, point output directory to your S3 bucket, e.g. s3://myathenagdelt/**!!! Athena and S3 must be in the same region**
4. In Athena, add the **_event_** table by selecting data from the open S3 bucket:
  ```
  CREATE EXTERNAL TABLE IF NOT EXISTS gdelt.events (
  `globaleventid` INT,`day` INT,`monthyear` INT,`year` INT,`fractiondate` FLOAT,
  `actor1code` string,`actor1name` string,`actor1countrycode` string,`actor1knowngroupcode` string,
  `actor1ethniccode` string,`actor1religion1code` string,`actor1religion2code` string,
  `actor1type1code` string,`actor1type2code` string,`actor1type3code` string,
  `actor2code` string,`actor2name` string,`actor2countrycode` string,`actor2knowngroupcode` string,
  `actor2ethniccode` string,`actor2religion1code` string,`actor2religion2code` string,
  `actor2type1code` string,`actor2type2code` string,`actor2type3code` string,
  `isrootevent` BOOLEAN,`eventcode` string,`eventbasecode` string,`eventrootcode` string,
  `quadclass` INT,`goldsteinscale` FLOAT,`nummentions` INT,`numsources` INT,`numarticles` INT,`avgtone` FLOAT,
  `actor1geo_type` INT,`actor1geo_fullname` string,`actor1geo_countrycode` string,`actor1geo_adm1code` string,
  `actor1geo_lat` FLOAT,`actor1geo_long` FLOAT,`actor1geo_featureid` INT,
  `actor2geo_type` INT,`actor2geo_fullname` string,`actor2geo_countrycode` string,`actor2geo_adm1code` string,
  `actor2geo_lat` FLOAT,`actor2geo_long` FLOAT,`actor2geo_featureid` INT,
  `actiongeo_type` INT,`actiongeo_fullname` string,`actiongeo_countrycode` string,`actiongeo_adm1code` string,
  `actiongeo_lat` FLOAT,`actiongeo_long` FLOAT,`actiongeo_featureid` INT,
  `dateadded` INT,`sourceurl` string) 
  ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
  WITH SERDEPROPERTIES ('serialization.format' = '	','field.delim' = '	') LOCATION 's3://gdelt-open-data/events/';
  ```
5. This result should show up in your S3 bucket
6. upload eventcode.csv to a folder under S3 (e.g.s3://myathenagdelt/cameocodes)  , and add it to gdelt database with the name gdelt.eventcode.
   This eventcode.csv is downloaded from https://github.com/tenthe/CAMEO-Event-Data-Codebook





**note:
This CLI Tool only handles small query. Limited to top 20 query, no order
