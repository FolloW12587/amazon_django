INSERT INTO amazon_analytics_requests (request)
SELECT  request
FROM 
(
	SELECT  ttops.id       AS id 
	       ,ttops.request  AS request 
	       ,ttops.position AS position 
	       ,req.id         AS request_id
	FROM amazon_analytics_temporaryrequesttops ttops
	LEFT JOIN amazon_analytics_requests req
	ON req.request = ttops.request 
) wrapper
WHERE request_id is null ;