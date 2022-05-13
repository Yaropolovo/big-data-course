set hive.auto.convert.join=false;
set mapreduce.job.reduces=2;
SELECT users.browser, SUM(IF(users.sex='male', 1, 0)) AS male, SUM(IF(users.sex='female', 1, 0)) AS female
FROM logs join users
ON (logs.ip = users.ip)
GROUP BY users.browser
limit 10;