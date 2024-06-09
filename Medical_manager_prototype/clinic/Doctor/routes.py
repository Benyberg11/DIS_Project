from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from clinic import app, conn, bcrypt
from clinic.forms import AddPatientForm, ScheduleAppointmentForm, PrescriptionForm, MedicalRecordForm, AddPrescriptionForm
from clinic.models import insert_patient, select_doctor_patients, select_medical_records_for_doctor, select_appointments_for_doctor, select_prescriptions_for_doctor, update_medical_record, delete_patient, delete_appointment, delete_prescription
import datetime
from clinic import roles, mysession
from flask_wtf import FlaskForm

Doctor = Blueprint('Doctor', __name__)

@Doctor.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_authenticated:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('Login.login'))

    medical_records = select_medical_records_for_doctor(current_user.get_id())
    appointments = select_appointments_for_doctor(current_user.get_id())
    prescriptions = select_prescriptions_for_doctor(current_user.get_id())

    form = FlaskForm()

    return render_template('dashboard.html', medical_records=medical_records, appointments=appointments, prescriptions=prescriptions, mysession=mysession, roles=roles, form=form)


@Doctor.route("/appointments", methods=['GET', 'POST'])
@login_required
def appointments():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if mysession["role"] != roles[1]: 
        flash('Viewing appointments is doctor only.', 'danger')
        return redirect(url_for('Login.login'))

    mysession["state"] = "appointments"
    print(mysession)

    appointments = select_appointments_for_doctor(current_user.get_id())
    print(appointments)
    role = mysession["role"]
    print('role: ' + role)

    return render_template('appointments.html', title='Appointments', appointments=appointments, role=role, mysession=mysession, roles=roles)

@Doctor.route("/addpatient", methods=['GET', 'POST'])
@login_required
def addpatient():
    mysession["state"] = "addpatient"
    form = AddPatientForm()
    if form.validate_on_submit():
        success = insert_patient(
            form.name.data,
            form.CPR_number.data,
            form.password.data,
            form.address.data,
            form.phone.data,
            form.email.data,
            form.birthdate.data,
            form.gender.data
        )
        if success:
            flash('Patient added successfully!', 'success')
            return redirect(url_for('Doctor.dashboard'))
        else:
            flash('Failed to add patient. Please try again.', 'danger')
    return render_template('addpatient.html', title='Add patient', form=form, mysession=mysession, roles=roles)

@Doctor.route("/account")
@login_required
def account():
    if not current_user.is_authenticated:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('Login.login'))

    print(f"Session state: {mysession}")
    print(f"Role: {mysession['role']}")
    print(f"Roles: {roles}")

    if mysession["role"] == roles[1]: 
        patients = select_doctor_patients(current_user.get_id())
        return render_template('account.html', acc=patients, title='Doctor Account', mysession=mysession, roles=roles)
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('Login.home'))

@Doctor.route("/add_prescription", methods=['GET', 'POST'])
@login_required
def add_prescription():
    form = AddPrescriptionForm()
    
    cur = conn.cursor()
    cur.execute("SELECT CPR_number, name FROM Patients")
    patients = cur.fetchall()
    form.patient_id.choices = [(patient[0], patient[1]) for patient in patients]
    cur.close()

    if form.validate_on_submit():
        patient_id = form.patient_id.data
        medication = form.medication.data
        dosage = form.dosage.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        notes = form.notes.data
        
        try:
            cur = conn.cursor()
            sql = """
            INSERT INTO Prescriptions (patient_id, doctor_id, medication, dosage, start_date, end_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (patient_id, current_user.id, medication, dosage, start_date, end_date, notes))
            conn.commit()
            cur.close()
            flash('Prescription added successfully!', 'success')
            return redirect(url_for('Doctor.dashboard'))
        except Error as e:
            conn.rollback()
            flash(f'Database error: {e}', 'danger')
    
    return render_template('add_prescription.html', title='Add Prescription', form=form, mysession=mysession, roles=roles)

@Doctor.route("/remove_patient", methods=['POST'])
@login_required
def remove_patient():
    if not current_user.is_authenticated:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('Login.login'))

    patient_id = request.form.get('patient_id')
    if patient_id:
        delete_patient(patient_id)
        flash('Patient and all related records have been removed!', 'success')
    else:
        flash('Failed to remove patient. Please try again.', 'danger')
    return redirect(url_for('Doctor.dashboard'))

@Doctor.route("/cancel_appointment", methods=['POST'])
@login_required
def cancel_appointment():
    if not current_user.is_authenticated:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('Login.login'))

    appointment_id = request.form.get('appointment_id')
    if appointment_id:
        delete_appointment(appointment_id)
        flash('Appointment has been canceled!', 'success')
    else:
        flash('Failed to cancel appointment. Please try again.', 'danger')
    return redirect(url_for('Doctor.dashboard'))

@Doctor.route("/remove_prescription", methods=['POST'])
@login_required
def remove_prescription():
    if not current_user.is_authenticated:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('Login.login'))

    prescription_id = request.form.get('prescription_id')
    if prescription_id:
        delete_prescription(prescription_id)
        flash('Prescription has been removed!', 'success')
    else:
        flash('Failed to remove prescription. Please try again.', 'danger')
    return redirect(url_for('Doctor.dashboard'))

@Doctor.route("/update_medical_record", methods=['POST'])
@login_required
def update_medical_record():
    record_id = request.form.get('record_id')
    record_details = request.form.get('record_details')

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
        flash('Medical record updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating medical record: {e}', 'danger')

    return redirect(url_for('Doctor.dashboard'))