class University:
    def __init__(self, name: str):
        self.name = name
        self.faculties = []
        self._init_faculties()

    def _init_faculties(self):
        faculty_specs = {
            "Факультет військової справи": ["Кіллер", "Ніндзя", "Самурай", "Лицар"],
            "Факульет магії": ["Чарівник", "Шаман", "Іллюзіоніст"],
            "Факультет транспорту": ["Водій мусоровозу", "Таксист", "Машиніст трамваю"],
            "Факультет сидіння": ["Кіберспортсмен", "Анімешник", "Біт-мейкер", "Стрімер", "Репер"],
            "Факультет спорту": ["Кроссфітер", "Пауерліфтер", "Еголіфтер", "Бодібілдер"],
            "Факультет світогляду": ["Веган", "Анархіст", "Панк"],
            "Факультет інформаційного добробуту": ["Детектив", "Шпигун", "Сищик", "Хакер"]
        }
        
        for faculty_name, specs in faculty_specs.items():
            faculty = Faculty(faculty_name, self)
            for spec in specs:
                faculty.add_specialization(Specialization(spec, faculty))
            self.add_faculty(faculty)

    def add_faculty(self, faculty: "Faculty"):
        self.faculties.append(faculty)

    def list_faculties(self):
        return self.faculties


class Faculty:
    def __init__(self, name: str, university: University):
        self.name = name
        self.university = university
        self.specializations = []

    def add_specialization(self, specialization: "Specialization"):
        self.specializations.append(specialization)

    def list_specializations(self):
        return self.specializations


class Specialization:
    def __init__(self, name: str, faculty: Faculty):
        self.name = name
        self.faculty = faculty
        self.students = []
        self.teachers = []
        self.card_number = None
        self.card_expiry = None
        self.card_cvv = None 


class Person:
    def __init__(self, first_name: str, last_name: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = None
        self.address = None
        self.birth_date = None
        self.card_number = None
        self.card_expiry = None
        self.card_cvv = None
    
    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }

    def set_payment_details(self, card_number: str, expiry: str, cvv: str):
        if not self._validate_card_number(card_number):
            raise ValueError("Невірний номер карти")
        if not self._validate_expiry(expiry):
            raise ValueError("Невірний формат терміну дії (потрібен формат MM/YY)")
        if not self._validate_cvv(cvv):
            raise ValueError("Невірний CVV код")
            
        self.card_number = ''.join(card_number.split())
        self.card_expiry = expiry
        self.card_cvv = cvv
        
    def _validate_card_number(self, number: str) -> bool:
        number = ''.join(number.split())
        return len(number) == 16 and number.isdigit()
    
    def _validate_expiry(self, expiry: str) -> bool:
        if not len(expiry) == 5 or expiry[2] != '/':
            return False
        month, year = expiry.split('/')
        return (month.isdigit() and year.isdigit() and
                1 <= int(month) <= 12 and len(year) == 2)
    
    def _validate_cvv(self, cvv: str) -> bool:
        return len(cvv) == 3 and cvv.isdigit()
        
    def get_card_info(self) -> dict:
        if not self.card_number:
            return None
        return {
            "card_number": self.card_number,
            "expiry": self.card_expiry,
            "cvv": self.card_cvv
        }

    def set_phone(self, phone: str):
        if not phone.startswith('+380') or len(phone) != 13 or not phone[1:].isdigit():
            raise ValueError("Невірний формат номера телефону. Використовуйте формат +380XXXXXXXXX")
        self.phone = phone


class Student(Person):
    def __init__(self, first_name: str, last_name: str, email: str):
        super().__init__(first_name, last_name, email)
        self.specialization = None

class Teacher(Person):
    def __init__(self, first_name: str, last_name: str, email: str):
        super().__init__(first_name, last_name, email)
        self.specialization = None
