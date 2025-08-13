import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime

class StudentApp:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Alunos Moderno")
        master.geometry("600x400")
        master.config(bg="#2C3E50")

        self.students = []
        self.current_frame = None

        self.create_frames()
        self.show_frame(self.home_frame)

    def create_frames(self):
        # Frame da Home
        self.home_frame = tk.Frame(self.master, bg="#2C3E50")
        self.home_frame.pack(fill="both", expand=True)

        label_home = tk.Label(self.home_frame, text="Bem-vindo ao Sistema de Gerenciamento de Alunos", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 16))
        label_home.pack(pady=20)

        button_register = tk.Button(self.home_frame, text="Cadastrar Aluno", command=self.show_registration_frame, bg="#3498DB", fg="#FFFFFF", width=30)
        button_register.pack(pady=5)

        button_view = tk.Button(self.home_frame, text="Ver Alunos", command=self.show_curriculum_frame, bg="#3498DB", fg="#FFFFFF", width=30)
        button_view.pack(pady=5)

        button_grades = tk.Button(self.home_frame, text="Inserir Notas", command=self.show_grades_frame, bg="#3498DB", fg="#FFFFFF", width=30)
        button_grades.pack(pady=5)

        button_edit = tk.Button(self.home_frame, text="Editar Aluno", command=self.show_edit_frame, bg="#3498DB", fg="#FFFFFF", width=30)
        button_edit.pack(pady=5)

        # Frame de Cadastro
        self.registration_frame = tk.Frame(self.master, bg="#2C3E50")

        tk.Label(self.registration_frame, text="Nome:", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.entry_name = tk.Entry(self.registration_frame, width=40)
        self.entry_name.pack(pady=5)

        tk.Label(self.registration_frame, text="Data de Nascimento (DD/MM/YYYY):", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.entry_birthdate = tk.Entry(self.registration_frame, width=40)
        self.entry_birthdate.pack(pady=5)
        self.entry_birthdate.bind("<FocusOut>", self.format_birthdate)

        tk.Label(self.registration_frame, text="Número de Telefone (XX-XXXXX-XXXX):", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.entry_phone = tk.Entry(self.registration_frame, width=40)
        self.entry_phone.pack(pady=5)
        self.entry_phone.bind("<FocusOut>", self.format_phone)
        self.entry_phone.insert(0, "XX-XXXXX-XXXX")  # Máscara padrão

        tk.Label(self.registration_frame, text="Escolha sua foto:", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.button_upload = tk.Button(self.registration_frame, text="Upload Foto", command=self.upload_photo, bg="#3498DB", fg="#FFFFFF")
        self.button_upload.pack(pady=5)

        self.button_register = tk.Button(self.registration_frame, text="Cadastrar", command=self.register_student, bg="#2ECC71", fg="#FFFFFF")
        self.button_register.pack(pady=20)

        self.photo_path = None

        # Frame do Currículo
        self.curriculum_frame = tk.Frame(self.master, bg="#2C3E50")
        
        self.curriculum_canvas = tk.Canvas(self.curriculum_frame, bg="#ECF0F1")
        self.curriculum_scroll = tk.Scrollbar(self.curriculum_frame, orient="vertical", command=self.curriculum_canvas.yview)
        self.curriculum_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.curriculum_list = tk.Frame(self.curriculum_canvas, bg="#ECF0F1")
        self.curriculum_canvas.create_window((0, 0), window=self.curriculum_list, anchor='nw')

        self.curriculum_canvas.configure(yscrollcommand=self.curriculum_scroll.set)
        self.curriculum_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        button_back_curriculum = tk.Button(self.curriculum_frame, text="← Voltar", command=self.show_home_frame, bg="#E74C3C", fg="#FFFFFF")
        button_back_curriculum.pack(pady=20)

        # Frame de Inserir Notas
        self.grades_frame = tk.Frame(self.master, bg="#2C3E50")
        tk.Label(self.grades_frame, text="Inserir Notas", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.grades_frame, text="Selecione o aluno:", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.student_var = tk.StringVar(self.grades_frame)
        self.student_menu = tk.OptionMenu(self.grades_frame, self.student_var, *self.get_student_names())
        self.student_menu.pack(pady=5)

        tk.Label(self.grades_frame, text="Nota:", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.entry_grade = tk.Entry(self.grades_frame, width=7)
        self.entry_grade.pack(pady=5)

        self.button_save_grade = tk.Button(self.grades_frame, text="Salvar Nota", command=self.save_grade, bg="#2ECC71", fg="#FFFFFF")
        self.button_save_grade.pack(pady=20)

        button_back_grades = tk.Button(self.grades_frame, text="← Voltar", command=self.show_home_frame, bg="#E74C3C", fg="#FFFFFF")
        button_back_grades.pack(pady=20)

        # Frame de Editar Aluno
        self.edit_frame = tk.Frame(self.master, bg="#2C3E50")
        tk.Label(self.edit_frame, text="Editar Aluno", bg="#2C3E50", fg="#ECF0F1", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.edit_frame, text="Selecione o aluno:", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.edit_student_var = tk.StringVar(self.edit_frame)
        self.edit_student_menu = tk.OptionMenu(self.edit_frame, self.edit_student_var, *self.get_student_names())
        self.edit_student_menu.pack(pady=5)

        tk.Label(self.edit_frame, text="Novo Nome:", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.entry_edit_name = tk.Entry(self.edit_frame, width=40)
        self.entry_edit_name.pack(pady=5)

        tk.Label(self.edit_frame, text="Nova Nota:", bg="#2C3E50", fg="#ECF0F1").pack(pady=10)
        self.entry_edit_grade = tk.Entry(self.edit_frame, width=7)
        self.entry_edit_grade.pack(pady=5)

        self.button_update_student = tk.Button(self.edit_frame, text="Atualizar Aluno", command=self.update_student, bg="#2ECC71", fg="#FFFFFF")
        self.button_update_student.pack(pady=20)

        button_back_edit = tk.Button(self.edit_frame, text="← Voltar", command=self.show_home_frame, bg="#E74C3C", fg="#FFFFFF")
        button_back_edit.pack(pady=20)

    def get_student_names(self):
        return [student["name"] for student in self.students] if self.students else ["Nenhum aluno cadastrado"]

    def show_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def show_home_frame(self):
        self.show_frame(self.home_frame)

    def show_registration_frame(self):
        self.show_frame(self.registration_frame)

    def show_curriculum_frame(self):
        self.populate_curriculum()
        self.show_frame(self.curriculum_frame)

    def show_grades_frame(self):
        self.populate_grades_menu()
        self.show_frame(self.grades_frame)

    def show_edit_frame(self):
        self.populate_edit_menu()
        self.show_frame(self.edit_frame)

    def upload_photo(self):
        self.photo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not self.photo_path:
            return
        messagebox.showinfo("Foto selecionada", "Foto carregada com sucesso!")

    def format_birthdate(self, event=None):
        raw_date = self.entry_birthdate.get().replace("/", "")
        if raw_date.isdigit():
            if len(raw_date) > 8:
                raw_date = raw_date[:8]
            formatted_date = ""
            if len(raw_date) >= 2:
                formatted_date += raw_date[:2] + "/"
            if len(raw_date) >= 4:
                formatted_date += raw_date[2:4] + "/"
            if len(raw_date) >= 8:
                formatted_date += raw_date[4:8]

            self.entry_birthdate.delete(0, tk.END)
            self.entry_birthdate.insert(0, formatted_date)

    def format_phone(self, event=None):
        raw_phone = self.entry_phone.get().replace("-", "")
        if raw_phone.isdigit():
            if len(raw_phone) > 11:
                raw_phone = raw_phone[:11]
            formatted_phone = ""
            if len(raw_phone) >= 2:
                formatted_phone += raw_phone[:2] + "-"
            if len(raw_phone) >= 7:
                formatted_phone += raw_phone[2:7] + "-"
            if len(raw_phone) >= 11:
                formatted_phone += raw_phone[7:11]

            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(0, formatted_phone)

    def register_student(self):
        name = self.entry_name.get()
        birthdate = self.entry_birthdate.get()
        phone = self.entry_phone.get().replace("-", "")

        if not name or not birthdate or not phone or not self.photo_path:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        try:
            datetime.strptime(birthdate, '%d/%m/%Y')
        except ValueError:
            messagebox.showwarning("Atenção", "Data de nascimento inválida. Use o formato DD/MM/AAAA.")
            return

        if len(phone) != 11 or not phone.isdigit():
            messagebox.showwarning("Atenção", "Número de telefone inválido. Use o formato XX-XXXXX-XXXX.")
            return

        self.students.append({
            "name": name,
            "birthdate": birthdate,
            "phone": phone,
            "photo": self.photo_path,
            "grade": None  # Adicionando campo de nota
        })

        self.show_home_frame()
        self.entry_name.delete(0, tk.END)
        self.entry_birthdate.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.photo_path = None

    def populate_curriculum(self):
        for widget in self.curriculum_list.winfo_children():
            widget.destroy()

        for student in self.students:
            student_info = f"Nome: {student['name']}, Data Nascimento: {student['birthdate']}, Telefone: {student['phone']}, Nota: {student['grade'] if student['grade'] is not None else 'Não informada'}"
            label_student = tk.Label(self.curriculum_list, text=student_info, bg="#ECF0F1", fg="#2C3E50")
            label_student.pack(pady=5)

            if student['photo']:
                img = Image.open(student['photo'])
                img = img.resize((50, 50), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label_photo = tk.Label(self.curriculum_list, image=photo, bg="#ECF0F1")
                label_photo.image = photo
                label_photo.pack(pady=5)

        # Atualiza a área de rolagem
        self.curriculum_list.update_idletasks()
        self.curriculum_canvas.config(scrollregion=self.curriculum_canvas.bbox("all"))

    def populate_grades_menu(self):
        menu = self.student_menu['menu']
        menu.delete(0, 'end')
        for student in self.get_student_names():
            menu.add_command(label=student, command=lambda value=student: self.student_var.set(value))

    def populate_edit_menu(self):
        menu = self.edit_student_menu['menu']
        menu.delete(0, 'end')
        for student in self.get_student_names():
            menu.add_command(label=student, command=lambda value=student: self.edit_student_var.set(value))
        self.populate_edit_fields()

    def populate_edit_fields(self):
        student_name = self.edit_student_var.get()
        for student in self.students:
            if student["name"] == student_name:
                self.entry_edit_name.delete(0, tk.END)
                self.entry_edit_name.insert(0, student["name"])
                self.entry_edit_grade.delete(0, tk.END)
                self.entry_edit_grade.insert(0, student["grade"] if student["grade"] else "")
                break

    def save_grade(self):
        student_name = self.student_var.get()
        grade = self.entry_grade.get()

        if not student_name or not grade:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        if not grade.isdigit() or int(grade) < 0 or int(grade) > 10:
            messagebox.showwarning("Atenção", "Nota inválida. A nota deve ser um número entre 0 e 10.")
            return

        for student in self.students:
            if student["name"] == student_name:
                student["grade"] = grade
                break

        messagebox.showinfo("Sucesso", "Nota salva com sucesso!")
        self.show_home_frame()
        self.entry_grade.delete(0, tk.END)

    def update_student(self):
        student_name = self.edit_student_var.get()
        new_name = self.entry_edit_name.get()
        new_grade = self.entry_edit_grade.get()

        if not student_name or (not new_name and not new_grade):
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        if new_grade and (not new_grade.isdigit() or int(new_grade) < 0 or int(new_grade) > 10):
            messagebox.showwarning("Atenção", "Nota inválida. A nota deve ser um número entre 0 e 10.")
            return

        for student in self.students:
            if student["name"] == student_name:
                if new_name:
                    student["name"] = new_name
                if new_grade:
                    student["grade"] = new_grade
                break

        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        self.show_home_frame()
        self.entry_edit_name.delete(0, tk.END)
        self.entry_edit_grade.delete(0, tk.END)
        self.edit_student_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
