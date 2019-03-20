SELECT DISTINCT user_pseudo_id
FROM `analytics_195246954.events_*` AS T,
     T.event_params
WHERE event_name = 'first_open'
  AND geo.country = 'United States' /* 修改为指定国家 */
  AND platform = '{0}'
  AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}'
EXCEPT DISTINCT
SELECT user_pseudo_id
FROM `analytics_195246954.events_*` AS T,
     T.event_params
WHERE event_name = 'user_engagement'
  AND geo.country = 'United States' /* 修改为指定国家 */
  AND platform = '{0}'
  AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}'
