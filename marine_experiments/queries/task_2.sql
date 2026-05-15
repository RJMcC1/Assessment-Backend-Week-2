SELECT 
    e.experiment_id,
    s.subject_id,
    p.species_name AS species,
    e.experiment_date,
    x.type_name AS experiment_type,
    CONCAT(ROUND((e.score / x.max_score) * 100, 2), '%') AS score
FROM
    subject AS s
JOIN experiment AS e
    USING (subject_id)
JOIN species AS p
    USING (species_id)
JOIN experiment_type AS x
    ON e.experiment_type_id = x.experiment_type_id
ORDER BY e.experiment_date DESC;
