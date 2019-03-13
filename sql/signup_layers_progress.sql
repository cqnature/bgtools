SELECT
  max_layer,
  COUNT(user_pseudo_id) as user_count
FROM (
  SELECT
      user_pseudo_id,
      max(event_params.value.int_value) as max_layer  /* 只要已解锁的最大矿层数 */
  FROM
    `analytics_168921341.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'activate_manto'
    AND event_params.key = 'manto_id'
    AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}'
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
        AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为events数据范围 */
    )
  GROUP BY user_pseudo_id /* 按用户id去重，每个id只保留最大矿层进度数 */
  )
GROUP BY max_layer
ORDER BY max_layer
