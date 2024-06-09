from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, DateField, TimeField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email, DataRequired, Regexp
from datetime import datetime, timedelta, time

def validate_future_date(form, field):
    if field.data < datetime.date.today():
        raise ValidationError("The date cannot be in the past.")
    if field.data.weekday() > 4:  # Monday is 0 and Sunday is 6
        raise ValidationError("Appointments cannot be scheduled on weekends.")

def generate_time_choices():
    times = []
    for hour in range(8, 15):
        if hour == 11:
            continue
        for minute in [0, 20, 40]:
            time_str = f"{hour:02}:{minute:02}"
            times.append((time_str, time_str))
    return times

class CancelAppointmentForm(FlaskForm):
    appointment_id = HiddenField('Appointment ID', validators=[DataRequired()])
    submit = SubmitField('Cancel')

class ScheduleAppointmentForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = SelectField('Time', choices=[
        ('08:00', '08:00'), ('08:20', '08:20'), ('08:40', '08:40'),
        ('09:00', '09:00'), ('09:20', '09:20'), ('09:40', '09:40'),
        ('10:00', '10:00'), ('10:20', '10:20'), ('10:40', '10:40'),
        ('12:00', '12:00'), ('12:20', '12:20'), ('12:40', '12:40'),
        ('13:00', '13:00'), ('13:20', '13:20'), ('13:40', '13:40'),
        ('14:00', '14:00')
    ], validators=[DataRequired()])
    doctor = SelectField('Doctor', choices=[], coerce=int, validators=[DataRequired()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Schedule')

    def __init__(self, *args, **kwargs):
        super(ScheduleAppointmentForm, self).__init__(*args, **kwargs)
        self.time.choices = self.get_time_choices()

    def get_time_choices(self):
        choices = []
        start_time = datetime.strptime('08:00', '%H:%M')
        end_time = datetime.strptime('14:00', '%H:%M')
        exclude_start = datetime.strptime('11:00', '%H:%M')
        exclude_end = datetime.strptime('12:00', '%H:%M')

        while start_time < end_time:
            if not (exclude_start <= start_time < exclude_end):
                choices.append((start_time.strftime('%H:%M'), start_time.strftime('%H:%M')))
            start_time += timedelta(minutes=20)

        return choices

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=1, max=20)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class AddPatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    CPR_number = StringField('CPR Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(),
        Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message="Invalid email address")
    ])
    birthdate = DateField('Birthdate', validators=[DataRequired()], format='%Y-%m-%d')
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    submit = SubmitField('Add')

class DirectPatientLoginForm(FlaskForm):
    p = IntegerField('CPR_number', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PatientLoginForm(FlaskForm):
    id = IntegerField('CPR_number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DoctorLoginForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PrescriptionForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    medication = StringField('Medication', validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Prescribe')

class MedicalRecordForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    record_details = TextAreaField('Record Details', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddPrescriptionForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    medication = StringField('Medication', validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    submit = SubmitField('Prescribe')