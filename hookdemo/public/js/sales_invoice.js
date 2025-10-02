// frappe.ui.form.on("Sales Invoice", {
//     refresh: function(frm) {
//         frappe.msgprint("My Name is Ahmad Saeed");
//     },

//     onload: function(frm) {
//         // Apply filter for customer field only once
//         frm.fields_dict['customer'].set_query = function(doc) {
//             return {
//                 filters: {
//                     customer_group: "Commercial",
//                     customer_type: "Company"
//                 }
//             };
//         };
//     }
// });
