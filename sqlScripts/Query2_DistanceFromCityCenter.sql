WITH date_ranges AS (--This Part should stay the same!!!
    SELECT
        (2000-2000)*12 + 1 AS start_period,
        (2020-2000)*12 + 1 AS end_period
    FROM dual
)--This Part should stay the same!!!
SELECT
    EXTRACT(YEAR FROM StartTime) AS Year,
    EXTRACT(MONTH FROM StartTime) AS Month,
    AVG(Severity) AS AverageSeverity,
    COUNT(Severity) AS TotalNumberOfCrashes,
    AVG(DistanceAffected) AS AverageDistanceAffected,
    AVG(UrbanRuralRelation.DistanceFromCityCenter),
    UrbanRuralRelation.AreaType
FROM
    (
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
            SQRT(((c.Latitude - a.LocStartLatitude) * (c.Latitude - a.LocStartLatitude)) + ((c.Longitude - a.LocStartLongitude) * (c.Longitude - a.LocStartLongitude))) AS DistanceFromCityCenter,
            CASE
                WHEN c.Density < 1000 THEN 'RURAL'
                WHEN c.Density < 2000 THEN 'SUBURBAN'
                ELSE 'CITY'
            END AS AreaType,
            a.Severity Severity,
            a.DistanceAffected DistanceAffected,
            ft.StartTime StartTime
        FROM 
            filtered_time ft
            INNER JOIN MICHAELBENNIE.ACCIDENT a ON ft.AccidentID = a.ID
            INNER JOIN MICHAELBENNIE.LOCATION l ON a.LocStartLatitude = l.StartLatitude AND a.LocStartLongitude = l.StartLongitude
            INNER JOIN "P.KEEFE".USCITIES c ON c.City = l.City AND c.StateID = l.State
            JOIN MICHAELBENNIE.TIME T ON a.ID = T.AccidentID
        WHERE
            c.Density > 0
            AND SQRT(((c.Latitude - a.LocStartLatitude) * (c.Latitude - a.LocStartLatitude)) + ((c.Longitude - a.LocStartLongitude) * (c.Longitude - a.LocStartLongitude))) < 100
    ) UrbanRuralRelation
GROUP BY
    EXTRACT(YEAR FROM StartTime),
    EXTRACT(MONTH FROM StartTime),
    UrbanRuralRelation.AreaType
ORDER BY
    Year,
    Month;