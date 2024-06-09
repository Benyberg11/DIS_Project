CREATE OR REPLACE VIEW vw_doctor_patient_appointments AS
SELECT 
    d.id AS doctor_id, 
    d.name AS doctor_name, 
    p.CPR_number AS patient_id, 
    p.name AS patient_name, 
    a.appointment_id, 
    a.date, 
    a.time, 
    a.status
FROM 
    Doctors d
JOIN 
    Appointments a ON d.id = a.doctor_id
JOIN 
    Patients p ON a.patient_id = p.CPR_number
ORDER BY 
    d.id, a.date, a.time;

