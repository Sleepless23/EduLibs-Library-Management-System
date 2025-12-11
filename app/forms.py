from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo

class BookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=10, max=13)])
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    genre = StringField('Genre', validators=[Length(max=50)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Book')

class StudentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    class_name = StringField('Course', validators=[DataRequired(), Length(max=50)])
    school = StringField('School', validators=[DataRequired(), Length(max=100)])
    contact = StringField('Contact', validators=[Length(max=100)])
    submit = SubmitField('Save Student')

class BorrowForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    book_id = SelectField('Book', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Borrow Book')

class ReturnForm(FlaskForm):
    submit = SubmitField('Return Book')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    class_name = StringField('Class', validators=[DataRequired(), Length(max=50)])
    school = StringField('School', validators=[DataRequired(), Length(max=100)])
    contact = StringField('Contact', validators=[Length(max=100)])
    submit = SubmitField('Sign Up')