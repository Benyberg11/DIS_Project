--
-- schema_ins.sql
-- Populate medical portal schema with data.
--
\echo Emptying the medical portal database. Deleting all tuples.
--
-- Dependency level 2
-- Referential integrity to level 1 and 0
--
-- schema_ins.sql

-- Empty the medical portal database. Deleting all tuples.
DELETE FROM Prescriptions;
DELETE FROM Appointments;
DELETE FROM MedicalRecords;
DELETE FROM Patients;
DELETE FROM Doctors;

-- Adding data
-- Insert new doctors
INSERT INTO Doctors (id, name, password, specialization, phone, email) 
VALUES 
(1, 'Dr. Emily Davis', '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 'Cardiology', '555-0001', 'emily.davis@example.com'),
(2, 'Dr. Michael Lee', '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 'Neurology', '555-0002', 'michael.lee@example.com'),
(3, 'Dr. Sarah Wilson', '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 'Orthopedics', '555-0003', 'sarah.wilson@example.com'),
(4, 'Dr. David Kim', '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 'Pediatrics', '555-0004', 'david.kim@example.com');
-- Adding patients
INSERT INTO Patients (CPR_number, password, name, address, phone, email, birthdate, gender) 
VALUES 
(1001, '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 'John Doe', '123 Main St, Anytown', '555-5551', 'johndoe@example.com', '1990-01-01', 'Male'),
(1002, '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 'Jane Smith', '456 Oak St, Anytown', '555-5552', 'janesmith@example.com', '1985-05-15', 'Female'),
(1003, '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 'Alice Johnson', '789 Pine St, Anytown', '555-5553', 'alicejohnson@example.com', '1975-09-30', 'Female'),
(1004, '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 'Bob Brown', '321 Elm St, Anytown', '555-5554', 'bobbrown@example.com', '1980-12-20', 'Male');

-- Adding medical records
INSERT INTO MedicalRecords (patient_id, doctor_id, record_details, create_date) 
VALUES 
(1001, 1, 'Initial consultation.', '2024-06-05'),
(1002, 2, 'Follow-up visit.', '2024-06-06'),
(1003, 3, 'Routine check-up.', '2024-06-07'),
(1004, 4, 'Physical therapy session.', '2024-06-08');

-- Adding appointments
INSERT INTO Appointments (patient_id, doctor_id, date, time, status) 
VALUES 
(1001, 1, '2024-07-01', '10:00:00', 'scheduled'),
(1002, 2, '2024-07-02', '11:00:00', 'scheduled'),
(1003, 3, '2024-07-03', '09:00:00', 'scheduled'),
(1004, 4, '2024-07-04', '14:00:00', 'scheduled');

-- Adding prescriptions
INSERT INTO Prescriptions (patient_id, doctor_id, medication, dosage, start_date, end_date, notes) 
VALUES 
(1001, 1, 'Ibuprofen', '200 mg', '2024-07-01', '2024-07-07', 'Take as needed for pain relief'),
(1002, 2, 'Amoxicillin', '500 mg', '2024-07-02', '2024-07-09', 'Take three times a day for infection'),
(1003, 3, 'Metformin', '500 mg', '2024-07-03', '2024-07-10', 'Take twice a day for blood sugar control'),
(1004, 4, 'Lisinopril', '10 mg', '2024-07-04', '2024-07-11', 'Take once a day for blood pressure');


