SELECT
  guide_id,
  COUNT(user_pseudo_id) as user_count
FROM (
  SELECT
      DISTINCT user_pseudo_id,
      event_params.value.int_value as guide_id  /* 每个用户的引导id */
  FROM
    `analytics_168921341.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'tutorial_complete'
    AND event_params.key = 'guide_id'
    AND _TABLE_SUFFIX BETWEEN '20190305' AND '20190311'  /* 修改为从注册到留存日期范围 */
    AND user_pseudo_id IN (
      SELECT
        DISTINCT user_pseudo_id
      FROM
        `analytics_168921341.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'sign_up'
--         AND geo.country = 'Canada' /* 修改为指定国家 */
        AND platform = 'ANDROID'
        AND _TABLE_SUFFIX BETWEEN '20190305' AND '20190305' /* 修改为注册日期范围 */
      EXCEPT DISTINCT
      SELECT
        user_id
      FROM
        `analytics_168921341.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'user_engagement'
--         AND geo.country = 'Canada' /* 修改为指定国家 */
        AND platform = 'ANDROID'
        AND _TABLE_SUFFIX BETWEEN '20190311' AND '20190311' /* 修改为留存日期范围 */
    )
  )
GROUP BY guide_id
ORDER BY user_count DESC
