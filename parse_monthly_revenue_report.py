import data_visualizer_helper as visuals
import json
import generate_monthly_revenue_report as revenue_generator
import pandas as pd


def remove_commas(num_string):
    try:
        num_string = num_string[1:]
        # Remove commas from the string
        amount_str_without_commas = num_string.replace(",", "")

        # Convert the string to a float
        amount_float = float(amount_str_without_commas)
        return amount_float

    except:
        print(f"Was not able to convert {num_string} to number")


class RevenueExpenseParser:
    def __init__(self, document):
        self.doc = document
        self.revenue = 0
        self.expenses = 0
        self.profit = 0
        self.payee_totals = {}
        self.fee_totals = {}
        self.tutor_totals = {}
        self.payout = {}

        with open("constant_variables.json", "r") as json_file:
            self.tutoring_constants = json.load(json_file)

        self.tutor_list = self.tutoring_constants["active_tutors"]
        self.active_student_list = self.tutoring_constants["active_students"]
        self.inactive_student_list = self.tutoring_constants["inactive_students"]
        self.default_save_path = self.tutoring_constants["default_download_location"]

    def run(self):
        self.generate_totals()
        visuals.bar_plot_visualization([self.tutor_totals, self.payee_totals, self.fee_totals],
                                       ["Tutor Payments", "Parent Payments Received", "Fees"])
        # visuals.pie_chart_visualization(self.payout)
        print("Juan Payout = ", self.payout["Juan"])
        print("Mateo Payout = ", self.payout["Mateo"])

    def generate_totals(self):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(self.doc, skiprows=[0], usecols=range(1, 7))
        print(f"file {self.default_save_path}/{self.doc} opened successfully. Parsing now...")
        fee_list = ["Bank Fees", "Memberships and Dues", "Website"]
        current_section = "Revenue"
        for i, row in df.iterrows():
            amount = remove_commas(row["Amount"])

            if row["Category"] == "Total":
                if current_section == "Revenue":
                    self.revenue = amount

                elif current_section == "Expenses":
                    self.expenses = amount

            if not pd.isna(row['Payee']) and current_section == "Revenue":
                self.payee_totals.setdefault(row["Payee"], 0)
                self.payee_totals[row["Payee"]] += amount
            else:
                current_section = "Expenses"

            if row["Payee"] in self.tutor_list:
                self.tutor_totals.setdefault(row["Payee"], 0)
                self.tutor_totals[row["Payee"]] += amount

            if row["Category"] in fee_list:
                self.fee_totals.setdefault(row["Category"], 0)
                self.fee_totals[row["Category"]] += amount

            self.profit = self.revenue - self.expenses
            self.payout["Mateo"] = 0.57 * self.profit
            self.payout["Juan"] = 0.43 * self.profit
        #
        # for parent, value in self.payee_totals.items():
        #     print(parent, value)
        # print("\n")
        # for tutor, value in self.tutor_totals.items():
        #     print(tutor, value)
        # print("\n")
        # for fee, value in self.fee_totals.items():
        #     print(fee, value)
        # print("\n")
        # print("revenue: ", self.revenue)
        # print("expenses: ", self.expenses)
        # print("profit: ", self.profit)


if __name__ == '__main__':
    month = 1
    year = 2024
    generator = revenue_generator.RevenueReportGenerator(month, year)
    generator.run()
    doc = generator.output_file
    # doc = "/Users/juanmartinez/Downloads/monthly_revenue_1_2024.csv"
    parser = RevenueExpenseParser(doc)
    parser.run()
