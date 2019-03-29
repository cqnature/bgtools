SELECT
  A.max_level,
  A.user_pseudo_id,
  B.compound_count,
  C.buy_count,
  D.max_stage,
  E.tap_count,
  F.ad_view_count
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
        AND '{2}' )
    GROUP BY
      user_pseudo_id)
  WHERE
    max_level = {3} ) AS A
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
    AND event_params.value.int_value = {3}
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
      AND event_params.value.int_value = {3}
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
