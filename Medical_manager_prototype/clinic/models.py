from datetime import datetime
from clinic import conn, login_manager, bcrypt
from flask_login import UserMixin
from psycopg2 import sql, Error

@login_manager.user_loader
def load_user(user_id):
    try:
        cur = conn.cursor()

        schema = 'patients'
        id_field = 'cpr_number'
        if str(user_id).isdigit() and int(user_id) <= 1000:
            schema = 'doctors'
            id_field = 'id'

        user_sql = sql.SQL("""
        SELECT * FROM {}
        WHERE {} = %s
        """).format(sql.Identifier(schema), sql.Identifier(id_field))

        cur.execute(user_sql, (int(user_id),))
        user_data = cur.fetchone()
        cur.close()
        
        if user_data:
            print(f"Loaded user from {schema}: {user_data}")
            return Doctors(user_data) if schema == 'doctors' else Patients(user_data)
        else:
            print("No user found with id:", user_id)
            return None
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

class Patients(tuple, UserMixin):
    def __init__(self, user_data):
        self.CPR_number = user_data[0]
        self.password = user_data[1]
        self.name = user_data[2]
        self.address = user_data[3]
        self.phone = user_data[4]
        self.email = user_data[5]
        self.birthdate = user_data[6]
        self.gender = user_data[7]
        self.role = "patient"

    def get_id(self):
        return self.CPR_number

class Doctors(tuple, UserMixin):
    def __init__(self, doctor_data):
        self.id = doctor_data[0]
        self.name = doctor_data[1]
        self.password = doctor_data[2]
        self.specialization = doctor_data[3]
        self.phone = doctor_data[4]
        self.email = doctor_data[5]
        self.role = "doctor"

    def get_id(self):
        return self.id

class MedicalRecord(tuple):
    def __init__(self, record_data):
        self.id = record_data[0]
        self.patient_id = record_data[1]
        self.doctor_id = record_data[2]
        self.record_details = record_data[3]
        self.create_date = record_data[4]

class Appointment(tuple):
    def __init__(self, appointment_data):
        self.appointment_id = appointment_data[0]
        self.patient_id = appointment_data[1]
        self.doctor_id = appointment_data[2]
        self.date = appointment_data[3]
        self.time = appointment_data[4]
        self.status = appointment_data[5]

class Prescription(tuple):
    def __init__(self, prescription_data):
        self.prescription_id = prescription_data[0]
        self.patient_id = prescription_data[1]
        self.doctor_id = prescription_data[2]
        self.medication = prescription_data[3]
        self.dosage = prescription_data[4]
        self.start_date = prescription_data[5]
        self.end_date = prescription_data[6]
        self.notes = prescription_data[7]

def insert_patient(name, CPR_number, password, address, phone, email, birthdate, gender):
    try:
        cur = conn.cursor()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        sql = """
        INSERT INTO Patients (name, CPR_number, password, address, phone, email, birthdate, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (name, CPR_number, hashed_password, address, phone, email, birthdate, gender))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Database error: {e}")
        return False

def select_patient(CPR_number):
    cur = conn.cursor()
    sql = """
    SELECT * FROM Patients
    WHERE CPR_number = %s
    """
    cur.execute(sql, (CPR_number,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return Patients(user_data)
    return None

def select_patient_direct(CPR_number):
    try:
        cur = conn.cursor()
        sql = """
        SELECT * FROM Patients
        WHERE CPR_number = %s
        AND DIRECT IS TRUE
        """
        cur.execute(sql, (CPR_number,))
        user = Patients(cur.fetchone()) if cur.rowcount > 0 else None
        cur.close()
        return user
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

def select_doctor(id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT * FROM Doctors
        WHERE id = %s
        """
        cur.execute(sql, (id,))
        user_data = cur.fetchone()
        cur.close()
        user = Doctors(user_data) if user_data else None
        print(f"Doctor data: {user_data}")
        return user
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

def insert_medical_record(patient_id, doctor_id, record_details):
    try:
        cur = conn.cursor()
        sql = """
        INSERT INTO MedicalRecords(patient_id, doctor_id, record_details, create_date)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (patient_id, doctor_id, record_details, datetime.utcnow()))
        conn.commit()
        cur.close()
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")

def update_medical_record(record_id, record_details):
    try:
        cur = conn.cursor()
        sql = """
        UPDATE MedicalRecords
        SET record_details = %s
        WHERE id = %s
        """
        cur.execute(sql, (record_details, record_id))
        conn.commit()
        cur.close()
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")

def select_medical_records(patient_id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT * FROM MedicalRecords
        WHERE patient_id = %s
        """
        cur.execute(sql, (patient_id,))
        records = cur.fetchall()
        cur.close()
        return records
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

def select_doctor_patients(doctor_id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT p.name, p.CPR_number, p.address
        FROM Patients p
        JOIN MedicalRecords m ON p.CPR_number = m.patient_id
        WHERE m.doctor_id = %s
        """
        cur.execute(sql, (doctor_id,))
        patients = cur.fetchall()
        cur.close()
        return patients
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

def select_patient_doctors(patient_id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT d.name, d.specialization, d.phone
        FROM Doctors d
        JOIN MedicalRecords m ON d.id = m.doctor_id
        WHERE m.patient_id = %s
        """
        cur.execute(sql, (patient_id,))
        doctors = cur.fetchall()
        cur.close()
        return doctors
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return []

def select_medical_records_for_doctor(doctor_id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT mr.*, p.name as patient_name, p.CPR_number
        FROM MedicalRecords mr
        JOIN Patients p ON mr.patient_id = p.CPR_number
        WHERE mr.doctor_id = %s
        """
        cur.execute(sql, (doctor_id,))
        records = cur.fetchall()
        cur.close()
        return [dict(id=record[0], patient_id=record[1], patient_name=record[-2], record_details=record[3], create_date=record[4]) for record in records]
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

def select_appointments_for_doctor(doctor_id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT a.*, p.name as patient_name
        FROM Appointments a
        JOIN Patients p ON a.patient_id = p.CPR_number
        WHERE a.doctor_id = %s
        """
        cur.execute(sql, (doctor_id,))
        appointments = cur.fetchall()
        cur.close()
        return [dict(appointment_id=appointment[0], patient_name=appointment[-1], date=appointment[3], time=appointment[4], status=appointment[5], comment=appointment[6]) for appointment in appointments]
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

def select_prescriptions_for_doctor(doctor_id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT pr.*, p.name as patient_name
        FROM Prescriptions pr
        JOIN Patients p ON pr.patient_id = p.CPR_number
        WHERE pr.doctor_id = %s
        """
        cur.execute(sql, (doctor_id,))
        prescriptions = cur.fetchall()
        cur.close()
        return [dict(prescription_id=prescription[0], patient_name=prescription[-1], medication=prescription[3], dosage=prescription[4], start_date=prescription[5], end_date=prescription[6], notes=prescription[7]) for prescription in prescriptions]
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

def delete_patient(patient_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Patients WHERE CPR_number = %s", (patient_id,))
        cur.execute("DELETE FROM MedicalRecords WHERE patient_id = %s", (patient_id,))
        cur.execute("DELETE FROM Appointments WHERE patient_id = %s", (patient_id,))
        cur.execute("DELETE FROM Prescriptions WHERE patient_id = %s", (patient_id,))
        conn.commit()
        cur.close()
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")

def delete_appointment(appointment_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Appointments WHERE appointment_id = %s", (appointment_id,))
        conn.commit()
        cur.close()
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")

def delete_prescription(prescription_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Prescriptions WHERE prescription_id = %s", (prescription_id,))
        conn.commit()
        cur.close()
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")

def select_patients_direct():
    try:
        cur = conn.cursor()
        sql = """
        SELECT name, CPR_number, address
        FROM Patients
        WHERE DIRECT IS TRUE
        """
        cur.execute(sql)
        direct_patients = cur.fetchall()
        cur.close()
        return direct_patients
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return None

def select_appointments_for_patient(patient_id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT a.appointment_id, d.name AS doctor_name, a.date, a.time, a.status
        FROM Appointments a
        JOIN Doctors d ON a.doctor_id = d.id
        WHERE a.patient_id = %s
        """
        cur.execute(sql, (patient_id,))
        appointments = cur.fetchall()
        cur.close()
        return appointments
    except Error as e:
        print(f"Database error: {e}")
        return []

def select_prescriptions_for_patient(patient_id):
    try:
        cur = conn.cursor()
        sql = """
        SELECT prescription_id, medication, dosage, start_date, end_date, notes
        FROM Prescriptions
        WHERE patient_id = %s
        """
        cur.execute(sql, (patient_id,))
        prescriptions = cur.fetchall()
        cur.close()
        return prescriptions
    except Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return []

def insert_appointment(patient_id, doctor_id, date, time, comment):
    try:
        cur = conn.cursor()
        sql = """
        INSERT INTO Appointments (patient_id, doctor_id, date, time, comment, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (patient_id, doctor_id, date, time, comment, 'Scheduled'))
        conn.commit()
        cur.close()
        return True
    except Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return False

def get_available_doctors(date, time):
    try:
        cur = conn.cursor()
        sql = """
        SELECT d.id, d.name, d.password, d.specialization, d.phone, d.email
        FROM Doctors d
        LEFT JOIN Appointments a ON d.id = a.doctor_id AND a.date = %s AND a.time = %s
        WHERE a.appointment_id IS NULL
        """
        cur.execute(sql, (date, time))
        doctors = cur.fetchall()
        cur.close()
        return [Doctors(doctor) for doctor in doctors]
    except Exception as e:
        print(f"Database error: {e}")
        return []
