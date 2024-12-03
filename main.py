from flask import Blueprint, render_template, request, redirect, url_for, flash
from university import University, Faculty, Student
from datetime import datetime
import os

bp = Blueprint('main', __name__)

# Створюємо екземпляр університету
university = University("НуГів.Но")

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        faculty_name = request.form['faculty']
        specialization_name = request.form['specialization']
        card_number = request.form['card_number']
        card_expiry = request.form['card_expiry']
        card_cvv = request.form['card_cvv']
        
        try:
            student = Student(first_name, last_name, email)
            student.set_payment_details(card_number, card_expiry, card_cvv)
            
            faculty = next((f for f in university.list_faculties() if f.name == faculty_name), None)
            if faculty:
                specialization = next((s for s in faculty.list_specializations() if s.name == specialization_name), None)
                if specialization:
                    student.choose_specialization(specialization)
                    
                    # Створюємо папку для заявок, якщо її не існує
                    if not os.path.exists('applications'):
                        os.makedirs('applications')
                    
                    # Створюємо унікальну назву файлу з датою та часом
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"applications/application_{timestamp}_{last_name}_{first_name}.txt"
                    
                    # Записуємо дані у файл
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"Дата подання заявки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Ім'я: {first_name}\n")
                        f.write(f"Прізвище: {last_name}\n")
                        f.write(f"Email: {email}\n")
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