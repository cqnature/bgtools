SELECT
  C.af_ad_scene,
  C.ad_view_count,
  D.daily_user_count,
  C.ad_view_count/D.daily_user_count AS daily_average_ad_view_count
FROM (
  SELECT
    af_ad_scene,
    COUNT(user_pseudo_id) AS ad_view_count
  FROM (
    SELECT
      A.user_pseudo_id,
      B.af_ad_scene
    FROM (
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
        AND _TABLE_SUFFIX BETWEEN '{1}'
        AND '{1}' ) AS A,
      (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.string_value AS af_ad_scene
      FROM
        `analytics_195246954.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_ad_view'
        AND event_params.key = 'af_ad_scene'
        AND geo.country = 'United States' /* 修改为指定国家 */
        AND platform = '{0}'
        AND _TABLE_SUFFIX BETWEEN '{1}'
        AND '{1}' ) AS B
    WHERE
      A.user_pseudo_id = B.user_pseudo_id
      AND A.event_timestamp = B.event_timestamp )
  GROUP BY
    af_ad_scene) AS C,
  (
  SELECT
    COUNT(DISTINCT user_pseudo_id) AS daily_user_count
  FROM
    `analytics_195246954.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'user_engagement'
    AND geo.country = 'United States' /* 修改为指定国家 */
    AND platform = '{0}'
    AND _TABLE_SUFFIX BETWEEN '{1}'
    AND '{1}') AS D
