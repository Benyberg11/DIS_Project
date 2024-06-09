CREATE OR REPLACE VIEW vw_prescription_summary AS
SELECT 
    p.CPR_number AS patient_id, 
    p.name AS patient_name, 
    pr.prescription_id, 
    pr.medication, 
    pr.dosage, 
    pr.start_date, 
    pr.end_date, 
    pr.notes, 
    d.name AS doctor_name
FROM 
    Prescriptions pr
JOIN 
    Patients p ON pr.patient_id = p.CPR_number
JOIN 
    Doctors d ON pr.doctor_id = d.id
ORDER BY 
    p.CPR_number, pr.start_date;
