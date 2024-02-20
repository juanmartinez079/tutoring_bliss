import csv
import os
import json
import pandas as pd
import generate_active_student_csv as active_students
import data_visualizer_helper as visuals
from datetime import datetime
import tutorbird_helper as tb


class StudentBookingParser:
    def __init__(self, document):
        self.doc = document

        with open("constant_variables.json", "r") as json_file:
            self.tutoring_constants = json.load(json_file)

        self.tutor_list = self.tutoring_constants["active_tutors"]
        self.student_list = self.tutoring_constants["active_students"]
        self.default_save_path = self.tutoring_constants["default_download_location"]

    def run(self):
        self.review_attendance()
        # visuals.bar_plot_visualization([attendance, payments],
        #                                ["Student Attendance", "Tutor Payments Due"])

    def review_attendance(self):
        # student_attendance = {}
        # for student in self.student_list:
        #     student_attendance.setdefault(student, 0)
        # Load the CSV file into a DataFrame
        # df = pd.read_csv(self.doc, skiprows=[0], usecols=range(1, 7))
        df = pd.read_csv(self.doc)
        print(f"file {self.default_save_path}/{self.doc} opened successfully. Parsing now...")

        # iterate through each row in the CSV
        for i, row in df.iterrows():
            student = f"{row["First Name"]} {row["Last Name"]}"
            # Define the format of the input string
            date_format = "%m/%d/%Y"
            last_lesson = None
            next_lesson = None

            today = datetime.now()

            if not pd.isna(row['Last Lesson']):
                last_lesson = row["Last Lesson"]
                last_lesson = last_lesson.split()[0]
                last_lesson = datetime.strptime(last_lesson, date_format)

            if not pd.isna(row['Next Lesson']):
                next_lesson = row["Next Lesson"]
                next_lesson = next_lesson.split()[0]
                next_lesson = datetime.strptime(next_lesson, date_format)

            if next_lesson is None:
                # figure out how many days ago the last lesson was
                time_delta = today - last_lesson
                days_since_last_lesson = time_delta.days

                if days_since_last_lesson > 7:
                    print(f"{student} does not have a next lesson booked.")
                    print(f"It has been {days_since_last_lesson} day(s) since {student}'s last lesson\n")
                else:
                    print(f"{student} recently took a lesson {days_since_last_lesson} day(s) ago.")
                    print("They do not have a follow up session booked\n")

            else:
                # figure out how many days ago the last lesson was
                time_delta = today - last_lesson
                days_since_last_lesson = time_delta.days

                time_delta = next_lesson - today
                days_until_next_lesson = time_delta.days
                print(f"{student} has a lesson booked in {days_until_next_lesson} days.")
                print(f"Their last session was {days_since_last_lesson} day(s) ago.\n")
            # print(student, "last lesson: ", last_lesson, "next lesson: ", next_lesson)


if __name__ == "__main__":
    # generator = active_students.ActiveStudentReportGenerator()
    # generator.run()
    # doc = generator.output_file
    doc = tb.select_file()
    parser = StudentBookingParser(doc)
    parser.run()
