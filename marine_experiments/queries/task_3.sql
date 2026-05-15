SELECT
    x.type_name,
    p.species_name,
    ROUND(AVG(e.score),1) AS average_score
FROM
    subject AS s
JOIN experiment AS e
    USING (subject_id)
JOIN species AS p
    USING (species_id)
JOIN experiment_type AS x
    USING (experiment_type_id)
GROUP BY x.type_name, p.species_name
HAVING ROUND(AVG(e.score),1) > 5
ORDER BY average_score DESC;