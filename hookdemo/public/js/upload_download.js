if (frm.fields_dict.custom_equipment) {
    setTimeout(() => {
        let footer = $(frm.fields_dict.custom_equipment.grid.wrapper).find(".grid-footer");
        footer.css({
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center"
        });

        let right_wrapper = $('<div class="custom-right-btns"></div>');

        // -------- Download Button --------
        let download_btn = $('<button class="btn btn-sm btn-primary" style="margin-left: 8px;">Download Equipment</button>')
            .on('click', function () {
                frappe.prompt([{
                    label: 'Choose Format',
                    fieldname: 'format',
                    fieldtype: 'Select',
                    options: ['CSV', 'Excel'],
                    default: 'CSV'
                }], (values) => {
                    let rows = frm.doc.custom_equipment || [];
                    if (!rows.length) {
                        frappe.msgprint("No equipment data to download");
                        return;
                    }

                    if (values.format === 'CSV') {
                        let csv = "Vin/Serial No,Billing Rate (Excl)\n";
                        rows.forEach(row => {
                            csv += `${row.vinserial_no || ""},${row.billing_rate_excl || 0}\n`;
                        });
                        let blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
                        let link = document.createElement("a");
                        link.href = URL.createObjectURL(blob);
                        link.download = "contract_custom_equipment.csv";
                        link.click();
                    } else {
                        frappe.require("https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js", function () {
                            let data = rows.map(row => ({
                                "Vin/Serial No": row.vinserial_no || "",
                                "Billing Rate (Excl)": row.billing_rate_excl || 0
                            }));
                            let worksheet = XLSX.utils.json_to_sheet(data);
                            let workbook = XLSX.utils.book_new();
                            XLSX.utils.book_append_sheet(workbook, worksheet, "Custom Equipment");
                            XLSX.writeFile(workbook, "contract_custom_equipment.xlsx");
                        });
                    }
                }, 'Download Format');
            });

        // -------- Upload Button --------
        let upload_btn = $('<button class="btn btn-sm btn-secondary" style="margin-left: 8px;background:transparent !important;">Upload Equipment</button>')
            .on('click', function () {
                frappe.require("https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js", function () {
                    let input = document.createElement("input");
                    input.type = "file";
                    input.accept = ".csv,.xlsx,.xls";

                    input.onchange = async (e) => {
                        let file = e.target.files[0];
                        if (!file) return;

                        let extension = file.name.split('.').pop().toLowerCase();
                        let reader = new FileReader();

                        // ---- CSV Upload ----
                        if (extension === 'csv') {
                            reader.onload = async function (event) {
                                let csv = event.target.result;
                                let lines = csv.split("\n").map(r => r.trim()).filter(r => r);
                                if (!lines.length) {
                                    frappe.throw("⚠️ Uploaded CSV file is empty.");
                                    return;
                                }

                                let header = lines[0].trim();
                                if (header !== "Vin/Serial No,Billing Rate (Excl)") {
                                    frappe.throw("⚠️ Invalid CSV header. Expected 'Vin/Serial No,Billing Rate (Excl)'");
                                    return;
                                }

                                frm.clear_table("custom_equipment");

                                for (let r of lines.slice(1)) {
                                    if (!r.trim()) continue;
                                    let cols = r.split(",");
                                    let vin = cols[0]?.trim();

                                    let exists = await frappe.db.exists("Equipment Stock", vin);
                                    if (!exists) {
                                        frappe.throw(`⚠️ VIN Serial No <b>${vin}</b> does not exist in Equipment Stock.`);
                                    }

                                    let child = frm.add_child("custom_equipment");
                                    child.vinserial_no = vin;
                                    child.billing_rate_excl = parseFloat(cols[1] || 0);
                                }

                                frm.refresh_field("custom_equipment");
                                frappe.msgprint("✅ Custom equipment data uploaded successfully.");
                            };
                            reader.readAsText(file);
                        } else {
                            // ---- Excel Upload ----
                            reader.onload = async function (event) {
                                let data = new Uint8Array(event.target.result);
                                let workbook = XLSX.read(data, { type: "array" });
                                let sheetName = workbook.SheetNames[0];
                                let sheet = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], { defval: "" });

                                if (!sheet.length) {
                                    frappe.throw("⚠️ Uploaded Excel file is empty.");
                                    return;
                                }

                                if (!sheet[0].hasOwnProperty("Vin/Serial No") || !sheet[0].hasOwnProperty("Billing Rate (Excl)")) {
                                    frappe.throw("⚠️ Excel must have columns: 'Vin/Serial No', 'Billing Rate (Excl)'");
                                    return;
                                }

                                frm.clear_table("custom_equipment");

                                for (let row of sheet) {
                                    let vin = row["Vin/Serial No"]?.trim();

                                    let exists = await frappe.db.exists("Equipment Stock", vin);
                                    if (!exists) {
                                        frappe.throw(`⚠️ VIN Serial No <b>${vin}</b> does not exist in Equipment Stock.`);
                                    }

                                    let child = frm.add_child("custom_equipment");
                                    child.vinserial_no = vin;
                                    child.billing_rate_excl = parseFloat(row["Billing Rate (Excl)"] || 0);
                                }

                                frm.refresh_field("custom_equipment");
                                frappe.msgprint("✅ Custom equipment data uploaded successfully.");
                            };
                            reader.readAsArrayBuffer(file);
                        }
                    };
                    input.click();
                });
            });

        if (footer.find(".custom-right-btns").length === 0) {
            right_wrapper.append(download_btn).append(upload_btn);
            footer.append(right_wrapper);
        }
    }, 500);
}