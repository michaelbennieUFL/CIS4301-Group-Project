WITH date_ranges AS (
    SELECT
        (2000-2000)*12 + 1 AS start_period,
        (2019-2000)*12 + 1 AS end_period
    FROM dual
)
SELECT
    EXTRACT(YEAR FROM STARTTIME) AS Year,
    EXTRACT(MONTH FROM STARTTIME) AS Month,
    AVG(SEVERITY) AS AverageSeverity,
    COUNT(SEVERITY) AS TotalNumberOfCrashes,
    AVG(DISTANCEAFFECTED) as AverageDistanceAffected,
    WindVehicleRelation
FROM
    (
        SELECT
            a.ID AS AccidentID,
            a.SEVERITY,
            a.DISTANCEAFFECTED,
            T.STARTTIME,
            T.ENDTIME,
            a.LocStartLatitude,
            a.LocStartLongitude,
            a.ENDLATITUDE,
            a.ENDLONGITUDE,
            w.WindDirection,
            ATAN2((a.ENDLATITUDE - a.LocStartLatitude), (a.ENDLONGITUDE - a.LocStartLongitude)) * 180 /3.14159 +
            CASE
                WHEN a.ENDLONGITUDE < a.LocStartLongitude THEN 180
                ELSE 0
            END AS VehicleDirection,
            CASE w.WindDirection
                WHEN 'N' THEN 0
                WHEN 'NNE' THEN 22.5
                WHEN 'NE' THEN 45
                WHEN 'ENE' THEN 67.5
                WHEN 'E' THEN 90
                WHEN 'ESE' THEN 112.5
                WHEN 'SE' THEN 135
                WHEN 'SSE' THEN 157.5
                WHEN 'S' THEN 180
                WHEN 'SSW' THEN 202.5
                WHEN 'SW' THEN 225
                WHEN 'WSW' THEN 247.5
                WHEN 'W' THEN 270
                WHEN 'WNW' THEN 292.5
                WHEN 'NW' THEN 315
                WHEN 'NNW' THEN 337.5
            END AS windDegrees,
            CASE
                WHEN ABS(CASE w.WindDirection
                            WHEN 'N' THEN 0
                            -- Additional wind directions mapped to degrees
                            ELSE NULL
                         END - (ATAN2((a.ENDLATITUDE - a.LocStartLatitude), (a.ENDLONGITUDE - a.LocStartLongitude)) * 180 / 3.14159 +
                               CASE
                                   WHEN a.ENDLONGITUDE < a.LocStartLongitude THEN 180
                                   ELSE 0
                               END)) <= 45 THEN 'towards the vehicle'
                WHEN ABS(ABS(CASE w.WindDirection
                                WHEN 'N' THEN 0
                                WHEN 'N' THEN 0
                                WHEN 'NNE' THEN 22.5
                                WHEN 'NE' THEN 45
                                WHEN 'ENE' THEN 67.5
                                WHEN 'E' THEN 90
                                WHEN 'ESE' THEN 112.5
                                WHEN 'SE' THEN 135
                                WHEN 'SSE' THEN 157.5
                                WHEN 'S' THEN 180
                                WHEN 'SSW' THEN 202.5
                                WHEN 'SW' THEN 225
                                WHEN 'WSW' THEN 247.5
                                WHEN 'W' THEN 270
                                WHEN 'WNW' THEN 292.5
                                WHEN 'NW' THEN 315
                                WHEN 'NNW' THEN 337.5
                                ELSE NULL
                             END - (ATAN2((a.ENDLATITUDE - a.LocStartLatitude), (a.ENDLONGITUDE - a.LocStartLongitude)) * 180 / 3.14159 +
                                   CASE
                                       WHEN a.ENDLONGITUDE < a.LocStartLongitude THEN 180
                                       ELSE 0
                                   END)) - 360) >= 135 THEN 'against the vehicle'
                ELSE 'perpendicular to the vehicle'
            END AS WindVehicleRelation
        FROM
            MICHAELBENNIE.ACCIDENT a
        JOIN
            MICHAELBENNIE.WEATHER w ON a.ID = w.AccidentID
        JOIN
            MICHAELBENNIE.TIME T ON w.ACCIDENTID = T.ACCIDENTID,
            date_ranges dr
        WHERE
            a.ENDLATITUDE IS NOT NULL
            AND a.ENDLONGITUDE IS NOT NULL
            AND NOT (a.ENDLATITUDE = a.LocStartLatitude AND a.ENDLONGITUDE = a.LocStartLongitude)
            AND ((EXTRACT(YEAR FROM T.STARTTIME)-2000)*12 + EXTRACT(MONTH FROM T.STARTTIME)) BETWEEN dr.start_period AND dr.end_period
    )
GROUP BY
    EXTRACT(YEAR FROM STARTTIME),
    EXTRACT(MONTH FROM STARTTIME),
    WindVehicleRelation
ORDER BY
    Year,
    Month;
