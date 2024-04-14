WITH date_ranges AS (--This Part should stay the same!!!
    SELECT
        (2000-2000)*12 + 1 AS start_period,
        (2017-2000)*12 + 1 AS end_period
    FROM dual
)--This Part should stay the same!!!
SELECT
    EXTRACT(YEAR FROM t.STARTTIME) AS Year,
    EXTRACT(MONTH FROM t.STARTTIME) AS Month,
    AVG(a.SEVERITY) AS AverageSeverity,
    AVG(a.DISTANCEAFFECTED) AS DistanceAffected
FROM
    MICHAELBENNIE.ACCIDENT a
JOIN
    MICHAELBENNIE.TIME t ON a.ID = t.ACCIDENTID,
    date_ranges dr
WHERE
    ((EXTRACT(YEAR FROM t.STARTTIME)-2000)*12 + EXTRACT(MONTH FROM t.STARTTIME)) BETWEEN dr.start_period AND dr.end_period
GROUP BY
    EXTRACT(YEAR FROM t.STARTTIME),
    EXTRACT(MONTH FROM t.STARTTIME)
ORDER BY
    Year,
    Month;
