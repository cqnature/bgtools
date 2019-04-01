SELECT
  user_pseudo_id,
  event_timestamp,
  event_params.value.int_value AS af_event_id
FROM
  `analytics_195246954.events_*` AS T,
  T.event_params
WHERE
  event_name = 'af_ad_view'
  AND event_params.key = 'af_event_id'
  AND event_params.value.int_value = 0 /* 修改为event id，主场景为0，其他依次为1/2/3 */
  AND geo.country = 'United States' /* 修改为指定国家 */
  AND platform = '{0}'
  AND _TABLE_SUFFIX BETWEEN '{2}'
  AND '{2}'
  AND user_pseudo_id IN (
  SELECT
    DISTINCT user_pseudo_id
  FROM
    `analytics_195246954.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'first_open'
    AND geo.country = 'United States' /* 修改为指定国家 */
    AND platform = '{0}'
    AND _TABLE_SUFFIX BETWEEN '{1}'
    AND '{1}' INTERSECT DISTINCT /* 保留留存用户 */
  SELECT
    DISTINCT user_pseudo_id
  FROM
    `analytics_195246954.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'user_engagement'
    AND geo.country = 'United States' /* 修改为指定国家 */
    AND platform = '{0}'
    AND _TABLE_SUFFIX BETWEEN '{2}'
    AND '{2}' )