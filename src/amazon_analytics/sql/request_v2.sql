SELECT  requests.request                                                                                                                        AS request_name 
       ,wrapper.at_start                                                                                                                        AS at_start 
       ,wrapper.at_end                                                                                                                          AS at_end 
       ,CASE WHEN wrapper.tops_count < reports_count_table.rep_count THEN 1000001  ELSE wrapper.maximum END                                     AS lowest_position 
       ,wrapper.minimum                                                                                                                         AS highest_position 
       ,CASE WHEN wrapper.tops_count < reports_count_table.rep_count THEN 1000001 - wrapper.minimum  ELSE wrapper.maximum - wrapper.minimum END AS diff_min_max --diff_btw_max_and_min 
       ,wrapper.at_start - wrapper.at_end                                                                                                       AS diff_start_end --diff_btw_pos_at_start_and_at_end
       ,abs(wrapper.at_start - wrapper.at_end)                                                                                                  AS abs_diff --abs_diff_btw_pos_at_start_and_at_end 
FROM 
(
	SELECT  tops.request_id 
	       ,MAX(tops.position)                                                                 AS maximum 
	       ,MIN(tops.position)                                                                 AS minimum 
	       ,COUNT(tops.position)                                                               AS tops_count 
	       ,coalesce(SUM(CASE WHEN period_date = %s THEN tops.position ELSE null END),1000001) AS at_start -- '2021-02-27' 
	       ,coalesce(SUM(CASE WHEN period_date = %s THEN tops.position ELSE null END),1000001) AS at_end -- '2021-03-13'
	FROM amazon_analytics_requesttops tops
	RIGHT JOIN amazon_analytics_reports reports -- Получаю строки позиций за конкретный период
	ON tops.report_id = reports.id AND reports.period_date >= %s AND reports.period_date <= %s -- '2021-02-27' '2021-03-13'
	GROUP BY  tops.request_id -- Группирую их по id запроса 
) wrapper
LEFT JOIN -- Добавляю столбец с количеством отчетов за период 
(
	SELECT  COUNT(*) AS rep_count
	FROM amazon_analytics_reports
	WHERE period_date >= %s -- '2021-02-27' 
	AND period_date <= %s -- '2021-03-13'  
) reports_count_table
ON wrapper.request_id > 0
LEFT JOIN amazon_analytics_requests requests -- Добавляю запросам текстовое представление
ON wrapper.request_id = requests.id
ORDER BY diff_min_max DESC --diff_btw_max_and_min
LIMIT {limit};


-- SELECT  tops.request_id 
--        ,tops.position AS pos 
--        ,reports.id    AS report_id
-- FROM amazon_analytics_requesttops tops
-- RIGHT OUTER JOIN amazon_analytics_reports reports
-- ON tops.report_id = reports.id AND reports.period_date >= '2021-02-27' AND reports.period_date <= '2021-03-13'
-- WHERE tops.request_id = 809019
-- ORDER BY pos asc nulls first 
-- LIMIT 10;

-- SELECT  *
-- FROM amazon_analytics_reports reports
-- LEFT JOIN amazon_analytics_requesttops tops
-- ON reports.id = tops.report_id AND tops.request_id = 809019;