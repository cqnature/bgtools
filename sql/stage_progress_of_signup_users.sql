SELECT
  max_stage,
  COUNT(user_pseudo_id) AS user_count
FROM (
  SELECT
    user_pseudo_id,
    MAX(event_params.value.int_value) AS max_stage
  FROM
    `analytics_195246954.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'af_stage_progress'
    AND event_params.key = 'af_stage'
    AND _TABLE_SUFFIX BETWEEN '{1}'
    AND '{1}'
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
      AND '{1}'
  )
  GROUP BY
    user_pseudo_id)
GROUP BY
  max_stage
ORDER BY
  max_stage
