WITH date_ranges AS (
    SELECT
        (2000-2000)*12 + 1 AS start_period,
        (2019-2000)*12 + 1 AS end_period
    FROM dual
), filtered_time AS (
    SELECT
        t.ACCIDENTID,
        t.ENDTIME,
        t.STARTTIME
    FROM
        MICHAELBENNIE.TIME t,
        date_ranges dr
    WHERE
        ((EXTRACT(YEAR FROM t.STARTTIME)-2000)*12 + EXTRACT(MONTH FROM t.STARTTIME)) BETWEEN dr.start_period AND dr.end_period
)
SELECT
    EXTRACT(YEAR FROM STARTTIME) AS Year,
    EXTRACT(MONTH FROM STARTTIME) AS Month,
    AVG(SEVERITY) AS AverageSeverity,
    COUNT(SEVERITY) AS TotalNumberOfCrashes,
    AVG(DISTANCEAFFECTED) as AverageDistanceAffected,
    SPEEDRANGE
FROM (
    SELECT
        CASE
            WHEN Distance < 10 THEN '0-10'
            WHEN Distance >= 10 AND Distance < 20 THEN '10-20'
            WHEN Distance >= 20 AND Distance < 30 THEN '20-30'
            WHEN Distance >= 30 AND Distance < 40 THEN '30-40'
            WHEN Distance >= 40 AND Distance < 50 THEN '40-50'
            ELSE '50+'
        END AS SPEEDRANGE,
        SEVERITY,
        DISTANCEAFFECTED,
        STARTTIME
    FROM (
        SELECT
            a.SEVERITY,
            ft.STARTTIME,
            a.DISTANCEAFFECTED,
            (LOG(4,(
                extract(day from (ft.ENDTIME-ft.STARTTIME))*24
                +extract(hour from (ft.ENDTIME-ft.STARTTIME))
                +extract(minute from (ft.ENDTIME-ft.STARTTIME))/60
                +extract(second from (ft.ENDTIME-ft.STARTTIME))/3600
            ))*200+3)*7917.5 * ASIN(SQRT(
                SIN(((ENDLATITUDE - LOCSTARTLATITUDE) * 0.017453292519943295) / 2) * SIN(((ENDLATITUDE - LOCSTARTLATITUDE) * 0.017453292519943295) / 2) +
                COS(LOCSTARTLATITUDE * 0.017453292519943295) * COS(ENDLATITUDE * 0.017453292519943295) *
                SIN(((ENDLONGITUDE - LOCSTARTLONGITUDE) * 0.017453292519943295) / 2) * SIN(((ENDLONGITUDE - LOCSTARTLONGITUDE) * 0.017453292519943295) / 2)
            )) AS Distance
        FROM filtered_time ft
        INNER JOIN michaelbennie.accident a ON ft.ACCIDENTID = a.ID
    ) Distances
) Grouped
GROUP BY
    EXTRACT(YEAR FROM STARTTIME),
    EXTRACT(MONTH FROM STARTTIME),
    SPEEDRANGE
ORDER BY
    Year,
    Month;
