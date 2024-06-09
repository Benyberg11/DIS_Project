CREATE OR REPLACE VIEW vw_patient_summary AS
SELECT 
    p.CPR_number, 
    p.name, 
    p.address,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT r.id) AS total_medical_records, 
    COUNT(DISTINCT pr.prescription_id) AS total_prescriptions
FROM 
    Patients p
LEFT JOIN 
    Appointments a ON p.CPR_number = a.patient_id
LEFT JOIN 
    MedicalRecords r ON p.CPR_number = r.patient_id
LEFT JOIN 
    Prescriptions pr ON p.CPR_number = pr.patient_id
GROUP BY 
    p.CPR_number, p.name, p.address;


