import csv
import os
import json
import generate_tutor_payroll_report as payroll_generator


class TutorPayrollParser:
    def __init__(self, doc):
        self.doc = doc

        with open("constant_variables.json", "r") as json_file:
            self.tutoring_constants = json.load(json_file)

        self.tutor_list = self.tutoring_constants["active_tutors"]
        self.student_list = self.tutoring_constants["active_students"]
        self.default_save_path = self.tutoring_constants["default_download_location"]

    def run(self):
        total, attendance, payments = self.generate_totals()
        print("Total Payroll: \n")
        print(total)
        print("Student Attendance: \n")
        print(attendance)
        print("Individual Tutor Payments: \n")
        print(payments)

        self.visualize_percentages(total, attendance, payments)

    def generate_totals(self):
        print("generating totals")
        tutor_payments = {}
        student_attendance = {}
        current_student = ""
        os.chdir(self.default_save_path)
        with open(self.doc, 'r') as payroll_file:
            csv_reader = csv.reader(payroll_file)
            print(f"file {self.default_save_path}/{self.doc} opened successfully. Parsing now...")
            for row in csv_reader:
                print(row)
                tutor = [name for name in self.tutor_list if name in row]
                student = [name for name in self.student_list if name in row[2]]
                balance_row = "Tutor Balance" in row
                # if it is a tutor row
                if not tutor == []:
                    current_student = tutor[0]

                # if it is a balance row
                if balance_row:
                    balance = row[-1]
                    balance = float(balance[1:])
                    tutor_payments.setdefault(current_student, balance)

                # if it is a row with any other info
                if not student == []:
                    student = student[0]
                    if student in student_attendance:
                        student_attendance[student] += 1
                    else:
                        student_attendance.setdefault(student, 1)

            total_payment_due = sum(tutor_payments.values())
            return total_payment_due, student_attendance, tutor_payments

    def visualize_percentages(self, total, attendance, payments):
        return


if __name__ == "__main__":
    generator = payroll_generator.PayrollReportGenerator('1/1/2024', '2/6/2024')
    generator.run()
    doc = generator.output_file
    parser = TutorPayrollParser(doc)
    parser.run()
