INSERT INTO amazon_analytics_requesttops (request_id, report_id, position)
SELECT  req.id          AS request_id 
       ,ttops.report_id AS report_id 
       ,ttops.position  AS position
FROM amazon_analytics_temporaryrequesttops ttops
LEFT JOIN amazon_analytics_requests req
ON req.request = ttops.request ;