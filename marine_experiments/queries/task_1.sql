SELECT
    subject.subject_id,
    subject.subject_name,
    species.species_name,
    TO_CHAR(subject.date_of_birth , 'YYYY-MM') AS date_of_birth
FROM 
    subject 
JOIN species
    USING (species_id)
ORDER BY subject.date_of_birth DESC;
