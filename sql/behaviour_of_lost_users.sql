SELECT
  A.max_level,
  A.user_pseudo_id,
  B.compound_count,
  C.buy_count,
  D.max_stage,
  E.tap_count,
  F.ad_view_count,
  G.unlock_chef_count,
  H.upgrade_chef_count,
  I.complete_mission_count,
  J.guide8_trigger_count,
  K.guide8_complete_count,
  L.guide11_trigger_count,
  M.guide11_complete_count,
  N.guide12_trigger_count,
  O.guide12_complete_count
FROM (
  SELECT
    user_pseudo_id,
    max_level
  FROM (
    SELECT
      user_pseudo_id,
      MAX(event_params.value.int_value) AS max_level
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'level_up'
      AND event_params.key = 'level'
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
        AND '{1}' EXCEPT DISTINCT
      SELECT
        DISTINCT user_pseudo_id
      FROM
        `analytics_195246954.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'user_engagement'
        AND geo.country = 'United States'
        AND platform = '{0}'
        AND _TABLE_SUFFIX BETWEEN '{2}'
        AND '{2}')
    GROUP BY
      user_pseudo_id)
  WHERE
    user_pseudo_id IN (
    SELECT
      DISTINCT user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'user_engagement'
      AND geo.country = 'United States' /* 修改为指定国家 */
      AND platform = '{0}'
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{3}' )
    AND max_level = {4} ) AS A
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS compound_count
  FROM
    `analytics_195246954.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'af_compound_food'
    AND event_params.key = 'level'
    AND _TABLE_SUFFIX BETWEEN '{1}'
    AND '{2}'
  GROUP BY
    user_pseudo_id ) AS B
ON
  A.user_pseudo_id = B.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS buy_count
  FROM
    `analytics_195246954.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'af_shop_buy_food'
    AND event_params.key = 'af_food_id'
    AND _TABLE_SUFFIX BETWEEN '{1}'
    AND '{2}'
  GROUP BY
    user_pseudo_id ) AS C
ON
  A.user_pseudo_id = C.user_pseudo_id
LEFT JOIN (
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
    AND '{2}'
  GROUP BY
    user_pseudo_id ) AS D
ON
  A.user_pseudo_id = D.user_pseudo_id
LEFT JOIN (
  SELECT
    X.user_pseudo_id,
    SUM(X.tap_count) AS tap_count
  FROM (
    SELECT
      user_pseudo_id,
      event_params.value.int_value AS tap_count,
      event_timestamp
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_click_tap_button'
      AND event_params.key = 'af_count'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}' ) AS X,
    (
    SELECT
      user_pseudo_id,
      event_timestamp
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_click_tap_button'
      AND event_params.key = 'level'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}' ) AS Y
  WHERE
    X.user_pseudo_id = Y.user_pseudo_id
    AND X.event_timestamp = Y.event_timestamp
  GROUP BY
    user_pseudo_id ) AS E
ON
  A.user_pseudo_id = E.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS ad_view_count
  FROM
    `analytics_195246954.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'af_ad_view'
    AND event_params.key = 'af_event_id'
    AND event_params.value.int_value = 0
    AND _TABLE_SUFFIX BETWEEN '{1}'
    AND '{2}'
  GROUP BY
    user_pseudo_id ) AS F
ON
  A.user_pseudo_id = F.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(chef_id) AS unlock_chef_count
  FROM (
    SELECT
      DISTINCT event_params.value.int_value AS chef_id,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_unlock_chef'
      AND event_params.key = 'af_chef_id'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS G
ON
  A.user_pseudo_id = G.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(chef_id) AS upgrade_chef_count
  FROM (
    SELECT
      DISTINCT event_params.value.int_value AS chef_id,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_upgrade_chef'
      AND event_params.key = 'af_chef_id'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS H
ON
  A.user_pseudo_id = H.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS complete_mission_count
  FROM (
    SELECT
      event_timestamp,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_track_scene'
      AND event_params.key = 'af_scene'
      AND event_params.value.string_value = 'complete_mission_type_all'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS I
ON
  A.user_pseudo_id = I.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS guide8_trigger_count
  FROM (
    SELECT
      event_timestamp,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_track_scene'
      AND event_params.key = 'af_scene'
      AND event_params.value.string_value = 'guide8_begin'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS J
ON
  A.user_pseudo_id = J.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS guide8_complete_count
  FROM (
    SELECT
      event_timestamp,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_track_scene'
      AND event_params.key = 'af_scene'
      AND event_params.value.string_value = 'guide8_end'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS K
ON
  A.user_pseudo_id = K.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS guide11_trigger_count
  FROM (
    SELECT
      event_timestamp,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_track_scene'
      AND event_params.key = 'af_scene'
      AND event_params.value.string_value = 'guide11_begin'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS L
ON
  A.user_pseudo_id = L.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS guide11_complete_count
  FROM (
    SELECT
      event_timestamp,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_track_scene'
      AND event_params.key = 'af_scene'
      AND event_params.value.string_value = 'guide11_end'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS M
ON
  A.user_pseudo_id = M.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS guide12_trigger_count
  FROM (
    SELECT
      event_timestamp,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_track_scene'
      AND event_params.key = 'af_scene'
      AND event_params.value.string_value = 'guide12_begin'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS N
ON
  A.user_pseudo_id = N.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(event_timestamp) AS guide12_complete_count
  FROM (
    SELECT
      event_timestamp,
      user_pseudo_id
    FROM
      `analytics_195246954.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_track_scene'
      AND event_params.key = 'af_scene'
      AND event_params.value.string_value = 'guide12_end'
      AND _TABLE_SUFFIX BETWEEN '{1}'
      AND '{2}')
  GROUP BY
    user_pseudo_id) AS O
ON
  A.user_pseudo_id = O.user_pseudo_id
