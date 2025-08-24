// student_attendance.js
// Client-side script for Student Attendance DocType

frappe.ui.form.on('Student Attendance', {
    status: function(frm) {
        if (frm.doc.status === "Absent") {
            frappe.msgprint("Please add remarks for absence.");
            frm.set_df_property("remarks", "reqd", 1);
        } else {
            frm.set_df_property("remarks", "reqd", 0);
        }
    },

    validate: function(frm) {
        if (frm.doc.status === "Absent" && !frm.doc.remarks) {
            frappe.throw("Remarks are mandatory when marking a student as Absent.");
        }
    }
});
