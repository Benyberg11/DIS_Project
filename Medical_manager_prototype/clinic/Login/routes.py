from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from clinic import app, conn, bcrypt
from clinic.forms import PatientLoginForm, DoctorLoginForm, DirectPatientLoginForm, ChangePasswordForm
from clinic.models import Patients, select_patient, select_patient_direct, select_patients_direct, select_doctor, select_patient_doctors, select_doctor_patients
from clinic import roles, mysession

Login = Blueprint('Login', __name__)

@Login.route("/")
@Login.route("/home")
def home():
    mysession["state"] = "home or /"
    print(f"Home session: {mysession}")
    role = mysession["role"]
    print(f"Role: {role}")
    return render_template('home.html', posts=[], role=role, mysession=mysession, roles=roles)

@Login.route("/about")
def about():
    mysession["state"] = "about"
    print(mysession)
    return render_template('about.html', title='About', mysession=mysession, roles=roles)

@Login.route("/direct", methods=['GET', 'POST'])
def direct():
    mysession["state"] = "direct"
    print(mysession)
    role = None

    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))

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
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    direct_users = select_patients_direct()
    print("L2 direct", direct_users)

    return render_template('direct.html', title='Direct Login', is_doctor=is_doctor, form=form, radio_direct=direct_users, role=role, mysession=mysession, roles=roles)

@Login.route("/login", methods=['GET', 'POST'])
def login():
    mysession["state"] = "login"
    print(f"Session state: {mysession}")
    role = None

    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))

    is_doctor = request.args.get('is_doctor', 'false').lower() == 'true'
    print(f"Is doctor: {is_doctor}")
    
    form = DoctorLoginForm() if is_doctor else PatientLoginForm()

    if form.validate_on_submit():
        print(f"Form data: ID={form.id.data}, Password={form.password.data}, Is doctor={is_doctor}")
        
        user = select_doctor(form.id.data) if is_doctor else select_patient(form.id.data)
        print(f"User fetched from DB: {user}")

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
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            print("No user found")
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    return render_template('login.html', title='Login', is_doctor=is_doctor, form=form, role=role, mysession=mysession, roles=roles)

@Login.route("/logout")
def logout():
    mysession["state"] = "logout"
    print(mysession)
    logout_user()
    return redirect(url_for('Login.home'))

@Login.route("/account")
@login_required
def account():
    mysession["state"] = "account"
    print(mysession)
    role = mysession["role"]
    print('Role:', role)
    form = ChangePasswordForm()
    if role == roles[2]:  # patient
        doctors = select_patient_doctors(current_user.get_id())
        return render_template('account.html', title='Patient Account', acc=doctors, form=form, role=role, mysession=mysession, roles=roles)
    elif role == roles[1]:  # doctor
        patients = select_doctor_patients(current_user.get_id())
        return render_template('account.html', title='Doctor Account', acc=patients, form=form, role=role, mysession=mysession, roles=roles)
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('Login.home'))

@Login.route("/account/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        cur = conn.cursor()
        if mysession["role"] == roles[1]:  # doctor
            sql = "UPDATE doctors SET password = %s WHERE id = %s"
        else:  # patient
            sql = "UPDATE patients SET password = %s WHERE cpr_number = %s"
        cur.execute(sql, (hashed_password, mysession["id"]))
        conn.commit()
        cur.close()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('Login.account'))
    return render_template('change_password.html', title='Change Password', form=form, mysession=mysession, roles=roles)

@Login.route("/forgot_password", methods=['POST'])
def forgot_password():
    email = request.form.get('email')
    if email:
        flash(f'A password reset link has been sent to {email}', 'info')
    else:
        flash('Please enter a valid email address.', 'danger')
    return redirect(url_for('Login.login'))
