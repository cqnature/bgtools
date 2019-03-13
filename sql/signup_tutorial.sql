SELECT
  COUNT(user_pseudo_id) as user_count
FROM (
  SELECT
     DISTINCT user_pseudo_id
  FROM
    `analytics_168921341.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'tutorial_complete'
    -- AND geo.country = 'United States' /* 修改为指定国家 */
    AND event_params.key = 'guide_id'
    AND event_params.value.int_value = 105
    AND platform = '{0}'
    AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为events数据范围 */
    AND user_pseudo_id IN (
      SELECT
        DISTINCT user_pseudo_id
      FROM
        `analytics_168921341.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'sign_up'
--         AND geo.country = 'United States' /* 修改为指定国家 */
        AND platform = '{0}'
        AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
    )
  )
ORDER BY user_count DESC
