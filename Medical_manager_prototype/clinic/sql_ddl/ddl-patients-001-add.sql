/*
* Medical Portal Project
*
*/

ALTER TABLE Patients
ADD "direct" BOOLEAN DEFAULT FALSE
;

-- Example usage:
-- SELECT * FROM Patients ORDER BY name;
-- UPDATE Patients SET direct = TRUE WHERE CPR_number = 1001;
-- UPDATE Patients SET direct = FALSE WHERE CPR_number = 1002;
--
-- COMMIT;

