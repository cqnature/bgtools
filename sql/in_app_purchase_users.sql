SELECT
  user_pseudo_id,
  event_params.value.string_value as item_name,
  event_timestamp
FROM
  `analytics_195246954.events_*` AS T,
  T.event_params
WHERE
  event_name = 'in_app_purchase'
  AND event_params.key = 'product_id'
  AND geo.country = 'United States'
  AND platform = '{0}'
  AND _TABLE_SUFFIX BETWEEN '{1}'
  AND '{2}'
  AND user_pseudo_id IN (
  SELECT
    DISTINCT user_pseudo_id
  FROM
    `analytics_195246954.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'first_open'
    AND geo.country = 'United States'
    AND platform = '{0}'
    AND _TABLE_SUFFIX BETWEEN '{1}'
    AND '{1}' )
