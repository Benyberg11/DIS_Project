from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from clinic import app, conn, bcrypt
from clinic.forms import PatientLoginForm, DoctorLoginForm, DirectPatientLoginForm, ScheduleAppointmentForm, CancelAppointmentForm
from clinic.models import Patients, select_patient, select_patient_direct, select_patients_direct, select_doctor, select_patient_doctors, select_appointments_for_patient, select_prescriptions_for_patient, get_available_doctors
from clinic import roles, mysession
from datetime import datetime

Patient = Blueprint('Patient', __name__)

@Patient.route("/")
@Patient.route("/home")
def home():
    mysession["state"] = "home or /"
    print("Home session:", mysession)
    role = mysession["role"]
    print('Role:', role)
    return render_template('home.html', posts=[], role=role, mysession=mysession, roles=roles)

@Patient.route("/about")
def about():
    mysession["state"] = "about"
    print(mysession)
    return render_template('about.html', title='About', mysession=mysession, roles=roles)

@Patient.route("/direct", methods=['GET', 'POST'])
def direct():
    mysession["state"] = "direct"
    print(mysession)
    role = None

    if current_user.is_authenticated:
        return redirect(url_for('Patient.home'))

    is_doctor = True if request.args.get('is_doctor') == 'true' else False
    form = DirectPatientLoginForm()

    if form.validate_on_submit():
        user = select_patient_direct(form.p.data)
        print("L2 user", user)

        if user is not None:
            print("L3 role:" + user.role)
            mysession["role"] = roles[2]  
            mysession["id"] = form.p.data
            print("L3", mysession)
            print("L3", roles)

            login_user(user, remember=form.remember.data)
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Patient.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    direct_users = select_patients_direct()
    print("L2 direct", direct_users)

    return render_template('direct.html', title='Direct Login', is_doctor=is_doctor, form=form, radio_direct=direct_users, role=role, mysession=mysession, roles=roles)

@Patient.route("/login", methods=['GET', 'POST'])
def login():
    mysession["state"] = "login"
    print(f"Session state: {mysession}")
    role = None

    if current_user.is_authenticated:
        return redirect(url_for('Patient.home'))

    is_doctor = True if request.args.get('is_doctor') == 'true' else False
    form = DoctorLoginForm() if is_doctor else PatientLoginForm()

    if form.validate_on_submit():
        user = select_doctor(form.id.data) if is_doctor else select_patient(form.id.data)

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == 'doctor':
                mysession["role"] = roles[1]  # doctor
            elif user.role == 'patient':
                mysession["role"] = roles[2]  # patient
            else:
                mysession["role"] = roles[0]  # none

            mysession["id"] = str(user.get_id())
            print(f"Session after setting user: {mysession}")
            print(f"Roles: {roles}")

            login_user(user, remember=form.remember.data)
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Patient.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    return render_template('login.html', title='Login', is_doctor=is_doctor, form=form, role=role, mysession=mysession, roles=roles)

@Patient.route("/logout")
def logout():
    mysession["state"] = "logout"
    print(mysession)
    logout_user()
    return redirect(url_for('Patient.home'))

@Patient.route("/account")
@login_required
def account():
    mysession["state"] = "account"
    print(mysession)
    role = mysession["role"]
    print('role: ' + role)
    if role == roles[2]: 
        doctors = select_patient_doctors(current_user.get_id())
        return render_template('account.html', title='Account', doctors=doctors, role=role, mysession=mysession, roles=roles)
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('Patient.home'))

@Patient.route("/appointments", methods=['GET', 'POST'])
@login_required
def appointments():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Patient.login'))

    if mysession["role"] != roles[2]:  
        flash('Viewing appointments is patient only.', 'danger')
        return redirect(url_for('Patient.login'))

    mysession["state"] = "appointments"
    print(mysession)

    appointments = select_appointments_for_patient(current_user.get_id())
    print(appointments)
    role = mysession["role"]
    print('role: ' + role)

    form = CancelAppointmentForm()

    return render_template('appointments.html', title='Appointments', appointments=appointments, form=form, role=role, mysession=mysession, roles=roles)

@Patient.route("/cancel_appointment", methods=['POST'])
@login_required
def cancel_appointment():
    form = CancelAppointmentForm()
    print("Form Data Received:", request.form)  # Debugging line to print form data
    if form.validate_on_submit():
        appointment_id = form.appointment_id.data
        print("Appointment ID to Cancel:", appointment_id)  # Debugging line
        try:
            cur = conn.cursor()
            sql = "DELETE FROM Appointments WHERE appointment_id = %s AND patient_id = %s"
            cur.execute(sql, (appointment_id, current_user.get_id()))
            conn.commit()
            cur.close()
            flash('Appointment cancelled successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f"Error cancelling appointment: {e}", 'danger')
            print(f"Database error: {e}")
    else:
        flash(f"Form validation failed: {form.errors}", 'danger')

    return redirect(url_for('Patient.appointments'))

@Patient.route("/prescriptions", methods=['GET', 'POST'])
@login_required
def prescriptions():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Patient.login'))

    if mysession["role"] != roles[2]:  
        flash('Viewing prescriptions is patient only.', 'danger')
        return redirect(url_for('Patient.login'))

    mysession["state"] = "prescriptions"
    print(mysession)

    prescriptions = select_prescriptions_for_patient(current_user.get_id())
    print("Prescriptions fetched from database:", prescriptions)
    role = mysession["role"]
    print('Role:', role)

    return render_template('prescriptions.html', title='Prescriptions', prescriptions=prescriptions, role=role, mysession=mysession, roles=roles)

@Patient.route("/schedule_appointment", methods=['GET', 'POST'])
@login_required
def schedule_appointment():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Patient.login'))

    if mysession["role"] != roles[2]:  
        flash('Scheduling appointments is patient only.', 'danger')
        return redirect(url_for('Patient.login'))

    form = ScheduleAppointmentForm()
    form.doctor.choices = [(doctor.id, doctor.name) for doctor in get_available_doctors(None, None)]

    if form.validate_on_submit():
        date = form.date.data
        time = form.time.data
        doctor_id = form.doctor.data
        comment = form.comment.data
        
        # Make sure the date is not in the past
        if date < datetime.now().date():
            flash('Cannot schedule an appointment in the past.', 'danger')
        else:
            # Schedule the appointment
            try:
                cur = conn.cursor()
                sql = """
                INSERT INTO Appointments (patient_id, doctor_id, date, time, comment, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (current_user.get_id(), doctor_id, date, time, comment, 'Scheduled'))
                conn.commit()
                cur.close()
                flash('Appointment scheduled successfully!', 'success')
            except Exception as e:
                conn.rollback()
                flash(f"Error scheduling appointment: {e}", 'danger')
                print(f"Database error: {e}")

            return redirect(url_for('Patient.appointments'))

    return render_template('schedule_appointment.html', title='Schedule Appointment', form=form, role=mysession["role"], mysession=mysession, roles=roles)

