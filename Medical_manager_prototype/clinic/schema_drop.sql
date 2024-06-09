DROP VIEW IF EXISTS vw_patient_summary;
DROP VIEW IF EXISTS vw_doctor_patient_appointments;
DROP VIEW IF EXISTS vw_prescription_summary;

DROP INDEX IF EXISTS idx_prescription_doctor;
DROP INDEX IF EXISTS idx_prescription_patient;
DROP INDEX IF EXISTS idx_appointment_doctor;
DROP INDEX IF EXISTS idx_appointment_patient;
DROP INDEX IF EXISTS idx_doctor_id;
DROP INDEX IF EXISTS idx_patient_id;

DROP TABLE IF EXISTS Prescriptions;
DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS MedicalRecords;
DROP TABLE IF EXISTS Doctors;
DROP TABLE IF EXISTS Patients;

-- ROLLBACK; commit;

