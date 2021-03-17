SELECT  request_str 
       ,position1
       ,position2 
       ,position1 - position2      AS diff 
       ,abs(position1 - position2) AS abs_diff
FROM 
(
	SELECT  req.request                       AS request_str 
	       ,coalesce(tops1.position,1000001)  AS position1 
	       ,coalesce(topssd.position,1000001) AS position2 
	       ,reports1.name                     AS name1 
	       ,topssd.name                       AS name2
	FROM amazon_analytics_requesttops tops1
	RIGHT JOIN 
	(
		SELECT  *
		FROM amazon_analytics_reports
		WHERE period_date = %s --'2021-03-11'  
	) reports1
	ON tops1.report_id = reports1.id
	FULL OUTER JOIN 
	(
		SELECT  tops2.report_id 
		       ,tops2.request_id 
		       ,tops2.position 
		       ,reports2.name AS name
		FROM amazon_analytics_requesttops tops2
		RIGHT JOIN 
		(
			SELECT  *
			FROM amazon_analytics_reports
			WHERE period_date = %s --'2021-03-14'  
		) reports2
		ON tops2.report_id = reports2.id 
	) topssd
	ON tops1.request_id = topssd.request_id
	LEFT JOIN amazon_analytics_requests req
	ON tops1.request_id=req.id or topssd.request_id=req.id 
) wrapper
ORDER BY abs_diff desc
LIMIT {limit};