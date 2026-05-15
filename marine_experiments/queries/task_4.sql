SELECT
    p.species_name,
    e.experiment_id,
    p.is_predator,
    CASE
        WHEN p.is_predator = 't'
        THEN e.score * 1.2
        ELSE e.score 
    END AS score
FROM 
    subject
JOIN experiment AS e
    USING (subject_id)
JOIN species AS p
    USING (species_id)
ORDER BY score DESC;