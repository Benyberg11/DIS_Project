\i clinic/schema_drop.sql

-- schema.sql

CREATE TABLE IF NOT EXISTS Patients (
    CPR_number INTEGER PRIMARY KEY,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    birthdate DATE NOT NULL,
    gender TEXT NOT NULL,
    direct BOOLEAN DEFAULT FALSE 
);

CREATE TABLE IF NOT EXISTS Doctors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    specialization TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS MedicalRecords (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    record_details TEXT NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients (CPR_number),
    FOREIGN KEY (doctor_id) REFERENCES Doctors (id)
);

CREATE TABLE IF NOT EXISTS Appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    status TEXT NOT NULL,
    comment TEXT,
    FOREIGN KEY (patient_id) REFERENCES Patients (CPR_number),
    FOREIGN KEY (doctor_id) REFERENCES Doctors (id)
);

CREATE TABLE IF NOT EXISTS Prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    medication TEXT NOT NULL,
    dosage TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    notes TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patients (CPR_number),
    FOREIGN KEY (doctor_id) REFERENCES Doctors (id)
);


-- Indexes and constraints
CREATE INDEX idx_patient_id ON MedicalRecords(patient_id);
CREATE INDEX idx_doctor_id ON MedicalRecords(doctor_id);
CREATE INDEX idx_appointment_patient ON Appointments(patient_id);
CREATE INDEX idx_appointment_doctor ON Appointments(doctor_id);
CREATE INDEX idx_prescription_patient ON Prescriptions(patient_id);
CREATE INDEX idx_prescription_doctor ON Prescriptions(doctor_id);

-- Comments
COMMENT ON TABLE Patients IS 'Table containing patient details';
COMMENT ON TABLE Doctors IS 'Table containing doctor details';
COMMENT ON TABLE MedicalRecords IS 'Table containing medical records of patients';
COMMENT ON TABLE Appointments IS 'Table containing appointments between patients and doctors';
COMMENT ON TABLE Prescriptions IS 'Table containing prescriptions issued by doctors to patients';

\i clinic/sql_ddl/vw_patient_summary.sql
\i clinic/sql_ddl/vw_doctor_patient_appointments.sql
\i clinic/sql_ddl/vw_prescription_summary.sql

