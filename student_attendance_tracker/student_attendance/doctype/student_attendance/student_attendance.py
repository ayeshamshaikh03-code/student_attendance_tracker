

class StudentAttendance(Document):
    def validate(self):
        """Ensure no duplicate attendance for the same student on the same date"""
        if frappe.db.exists("Student Attendance", {
            "student_name": self.student_name,
            "date": self.date,
            "name": ["!=", self.name]
        }):
            frappe.throw(f"Attendance already marked for {self.student_name} on {self.date}")

        # Auto calculate monthly attendance % (simple logic placeholder)
        self.calculate_attendance_percentage()

    def calculate_attendance_percentage(self):
        """Calculate attendance % for the student in the current month"""
        from datetime import datetime

        month_start = self.date.replace(day=1)
        month_end = self.date.replace(
            day=28
        ) + frappe.utils.date_diff(frappe.utils.add_months(month_start, 1), month_start) * frappe.utils.timedelta(days=1)

        records = frappe.get_all("Student Attendance",
            filters={
                "student_name": self.student_name,
                "date": ["between", [month_start, month_end]]
            },
            fields=["status"]
        )

        total_days = len(records)
        present_days = sum(1 for r in records if r["status"] == "Present")

        if total_days > 0:
            percentage = (present_days / total_days) * 100
            frappe.msgprint(f"Attendance % for {self.student_name} this month: {percentage:.2f}%")
