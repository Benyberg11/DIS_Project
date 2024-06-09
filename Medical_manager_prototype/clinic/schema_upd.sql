-- schema_upd.sql 20240420

\echo "schema_upd.sql 20240420"

-- Update patient addresses
UPDATE Patients SET name = 'John Doe Updated', address = 'New Address 1, City, Country' WHERE CPR_number = 1001; 
UPDATE Patients SET name = 'Jane Smith Updated', address = 'New Address 2, City, Country' WHERE CPR_number = 1002; 
UPDATE Patients SET name = 'Alice Johnson Updated', address = 'New Address 3, City, Country' WHERE CPR_number = 1003; 
UPDATE Patients SET name = 'Bob Brown Updated', address = 'New Address 4, City, Country' WHERE CPR_number = 1004; 

-- Update doctor information
UPDATE Doctors SET name = 'Dr. Emily Davis Updated', phone = '555-0001', email = 'emily.davis.updated@example.com' WHERE id = 1; 
UPDATE Doctors SET name = 'Dr. Michael Lee Updated', phone = '555-0002', email = 'michael.lee.updated@example.com' WHERE id = 2; 
UPDATE Doctors SET name = 'Dr. Sarah Wilson Updated', phone = '555-0003', email = 'sarah.wilson.updated@example.com' WHERE id = 3; 
UPDATE Doctors SET name = 'Dr. David Kim Updated', phone = '555-0004', email = 'david.kim.updated@example.com' WHERE id = 4;

-- Insert new doctor if not exists
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Doctors WHERE id = 5) THEN
        INSERT INTO Doctors (id, name, password, specialization, phone, email) 
        VALUES (5, 'Dr. Johnny Sins', '$2b$12$cgkBF9hqea9tJiInAJHpz.PzeJKHxVPlpjx/7oKZJ85HIXE1T3l32', 'Gynecologist', '911', 'Sexydoc69@yahoo.com');
    END IF;
END
$$;

-- Activating automatic login
UPDATE Patients SET direct = TRUE WHERE CPR_number = 1001;
UPDATE Patients SET direct = TRUE WHERE CPR_number = 1002;

-- Update existing patient and doctor
UPDATE Patients SET password = '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 
                   name = 'Rafael Nadal', 
                   address = 'New Address 5, City, Country', 
                   phone = '555-1235', 
                   email = 'rafael.nadal@example.com', 
                   birthdate = '1986-06-03', 
                   gender = 'Male' 
WHERE CPR_number = 1004;

UPDATE Doctors SET name = 'Dr. Novak Djokovic', 
                   password = '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e', 
                   specialization = 'Orthopedics', 
                   phone = '555-5679', 
                   email = 'novak.djokovic@example.com' 
WHERE id = 4;

-- Insert new patient if not exists
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Patients WHERE CPR_number = 1005) THEN
        INSERT INTO Patients (CPR_number, password, name, address, phone, email, birthdate, gender) 
        VALUES (1005, '$2b$12$cgkBF9hqea9tJiInAJHpz.PzeJKHxVPlpjx/7oKZJ85HIXE1T3l32', 'Test Patient', '123 Test Street, Test City', '555-1234', 'test.patient@example.com', '1990-01-01', 'Male');
    END IF;
END
$$;

-- Create new medical records
INSERT INTO MedicalRecords (patient_id, doctor_id, record_details, create_date) 
VALUES 
(1005, 5, 'Initial consultation for sports injury.', '2024-06-05');

-- Create new appointments
INSERT INTO Appointments (patient_id, doctor_id, date, time, status) 
VALUES 
(1005, 5, '2024-07-01', '10:00:00', 'scheduled');

-- Create new prescriptions
INSERT INTO Prescriptions (patient_id, doctor_id, medication, dosage, start_date, end_date, notes) 
VALUES 
(1005, 5, 'Ibuprofen', '200 mg', '2024-07-01', '2024-07-07', 'Take as needed for pain relief');

-- Update the password for CPR_number 1001
UPDATE Patients SET password = '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e' WHERE CPR_number = 1001;

-- Update the password for doctor with id 5
UPDATE Doctors SET password = '$2b$12$hFFDXgjT.zIVcjaz83Zx3.t0upmU5AN.JTX8SazXx4oTgHKVFBv7e' WHERE id = 5;
