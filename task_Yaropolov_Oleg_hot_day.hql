with t as (
SELECT `date`, count(1) as visits
FROM logs
GROUP BY `date`)
SELECT *
FROM t
ORDER BY visits DESC limit 10;