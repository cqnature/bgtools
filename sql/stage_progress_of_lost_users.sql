SELECT stage,
       wave,
       count(user_pseudo_id) AS user_count
FROM
  (SELECT C.user_pseudo_id,
          C.event_timestamp,
          D.stage,
          E.wave
   FROM
     (SELECT A.user_pseudo_id,
             max(A.event_timestamp) AS event_timestamp
      FROM
        (SELECT user_pseudo_id,
                event_timestamp,
                event_params.value.int_value AS stage
         FROM `analytics_195246954.events_*` AS T,
              T.event_params
         WHERE event_name = 'af_stage_progress'
           AND event_params.key = 'af_stage'
           AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
           AND user_pseudo_id IN
             (SELECT DISTINCT user_pseudo_id
              FROM `analytics_195246954.events_*` AS T,
                   T.event_params
              WHERE event_name = 'first_open'
                AND geo.country = 'United States' /* 修改为指定国家 */
                AND platform = '{0}'
                AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}'
              EXCEPT DISTINCT /* 排除留存用户 */ SELECT DISTINCT user_pseudo_id
              FROM `analytics_195246954.events_*` AS T,
                   T.event_params
              WHERE event_name = 'user_engagement'
                AND geo.country = 'United States' /* 修改为指定国家 */
                AND platform = '{0}'
                AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' ) ) AS A,

        (SELECT user_pseudo_id,
                event_timestamp,
                event_params.value.int_value AS wave
         FROM `analytics_195246954.events_*` AS T,
              T.event_params
         WHERE event_name = 'af_stage_progress'
           AND event_params.key = 'af_wave' ) AS B
      WHERE A.user_pseudo_id = B.user_pseudo_id
        AND A.event_timestamp = B.event_timestamp
      GROUP BY A.user_pseudo_id) AS C,

     (SELECT user_pseudo_id,
             event_timestamp,
             event_params.value.int_value AS stage
      FROM `analytics_195246954.events_*` AS T,
           T.event_params
      WHERE event_name = 'af_stage_progress'
        AND event_params.key = 'af_stage' ) AS D,

     (SELECT user_pseudo_id,
             event_timestamp,
             event_params.value.int_value AS wave
      FROM `analytics_195246954.events_*` AS T,
           T.event_params
      WHERE event_name = 'af_stage_progress'
        AND event_params.key = 'af_wave' ) AS E
   WHERE C.user_pseudo_id = D.user_pseudo_id
     AND C.user_pseudo_id = E.user_pseudo_id
     AND C.event_timestamp = D.event_timestamp
     AND C.event_timestamp = E.event_timestamp )
GROUP BY stage,
         wave
ORDER BY stage,
         wave
