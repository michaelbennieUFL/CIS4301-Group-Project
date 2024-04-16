WITH date_ranges AS (
    SELECT
        (2000-2000)*12 + 1 AS start_period,
        (2019-2000)*12 + 1 AS end_period
    FROM dual
)
SELECT /*+ PARALLEL(Accident, 4) PARALLEL(RoadCondition, 4) PARALLEL(TIME, 4) */
    EXTRACT(YEAR FROM STARTTIME) AS Year,
    EXTRACT(MONTH FROM STARTTIME) AS Month,
    AVG(SEVERITY) AS AverageSeverity,
    COUNT(SEVERITY) AS TotalNumberOfCrashes,
    AVG(DISTANCEAFFECTED) as AverageDistanceAffected,
    TrafficCategory
FROM (
WITH filtered_time AS(
    SELECT
        t.ACCIDENTID,
        t.STARTTIME
    FROM
        MICHAELBENNIE.TIME t,
        date_ranges dr
    WHERE
        ((EXTRACT(YEAR FROM t.STARTTIME)-2000)*12 + EXTRACT(MONTH FROM t.STARTTIME)) BETWEEN dr.start_period AND dr.end_period
)
SELECT
    CASE
        WHEN (rc.Bump + rc.Amenity + rc.NoExit + rc.TrafficSignal + rc.Railway + rc.TrafficCalming + rc.GiveWay + rc.TurningLoop + rc.Roundabout + rc.Crossing + rc.Station + rc.Stop + rc.Junction) = 0 THEN '0'
        WHEN (rc.Bump + rc.Amenity + rc.NoExit + rc.TrafficSignal + rc.Railway + rc.TrafficCalming + rc.GiveWay + rc.TurningLoop + rc.Roundabout + rc.Crossing + rc.Station + rc.Stop + rc.Junction) BETWEEN 1 AND 4 THEN '1-4'
        WHEN (rc.Bump + rc.Amenity + rc.NoExit + rc.TrafficSignal + rc.Railway + rc.TrafficCalming + rc.GiveWay + rc.TurningLoop + rc.Roundabout + rc.Crossing + rc.Station + rc.Stop + rc.Junction) BETWEEN 5 AND 8 THEN '5-8'
        ELSE '9+'
    END AS TrafficCategory,
    a.SEVERITY as SEVERITY,
    a.DISTANCEAFFECTED as DISTANCEAFFECTED,
    ft.STARTTIME as STARTTIME
FROM
    filtered_time ft
INNER JOIN michaelbennie.accident a ON ft.ACCIDENTID = a.ID
INNER JOIN "H.ZENG".roadcondition rc ON rc.LocStartLatitude = a.LocStartLatitude
                                     AND rc.LocStartLongitude = a.LocStartLongitude
)
GROUP BY
    EXTRACT(YEAR FROM STARTTIME),
    EXTRACT(MONTH FROM STARTTIME),
    TrafficCategory
ORDER BY
    Year,
    Month;



