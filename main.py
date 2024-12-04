from flask import Blueprint, render_template, request, redirect, url_for, flash
from university import University, Faculty, Person, Student, Teacher
from datetime import datetime
import os

bp = Blueprint('main', __name__)

university = University("НуГів.Но")

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_type = request.form['user_type']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        faculty_name = request.form['faculty']
        specialization_name = request.form['specialization']
        card_number = request.form['card_number']
        card_expiry = request.form['card_expiry']
        card_cvv = request.form['card_cvv']
        
        try:
            if user_type == 'student':
                person = Student(first_name, last_name, email)
            else:
                person = Teacher(first_name, last_name, email)
                
            person.set_payment_details(card_number, card_expiry, card_cvv)
            person.set_phone(phone)
            
            faculty = next((f for f in university.list_faculties() if f.name == faculty_name), None)
            if faculty:
                specialization = next((s for s in faculty.list_specializations() if s.name == specialization_name), None)
                if specialization:
                    if isinstance(person, Student):
                        specialization.students.append(person)
                        person.specialization = specialization
                    else:
                        specialization.teachers.append(person)
                        person.specialization = specialization
                    
                    if not os.path.exists('applications'):
                        os.makedirs('applications')
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"applications/application_{timestamp}_{last_name}_{first_name}.txt"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"Дата подання заявки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Тип користувача: {user_type}\n")
                        f.write(f"Ім'я: {first_name}\n")
                        f.write(f"Прізвище: {last_name}\n")
                        f.write(f"Email: {email}\n")
                        f.write(f"Телефон: {phone}\n")
                        f.write(f"Факультет: {faculty_name}\n")
                        f.write(f"Спеціалізація: {specialization_name}\n")
                        f.write(f"Номер карти: {card_number}\n")
                        f.write(f"Термін дії карти: {card_expiry}\n")
                        f.write(f"CVV: {card_cvv}\n")
                    
                    flash('Заявка успішно подана! Ми з вами обов\'язково зв\'яжемось!')
                    return redirect(url_for('main.index'))
            
        except ValueError as e:
            flash(str(e))
            
    return render_template('index.html', faculties=university.list_faculties())
