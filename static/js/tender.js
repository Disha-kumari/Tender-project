/* ======================================================
   MRPL Tender Commercial Evaluation
   tender.js — workflow navigation + all button actions
   for view_tender.html
====================================================== */

(function () {

    "use strict";

    var workflowContainer = document.getElementById("workflowContainer");

    var TENDER_ID = workflowContainer
        ? workflowContainer.dataset.tenderId
        : null;

    var INITIAL_STEP = workflowContainer
        ? parseInt(workflowContainer.dataset.initialStep, 10) || 1
        : 1;

    // ==================================================
    // STEP NAVIGATION
    // ==================================================

    function showPage(n) {

        document.querySelectorAll(".workflow-page").forEach(function (page) {
            page.classList.remove("active");
        });

        var target = document.getElementById("page" + n);

        if (target) {
            target.classList.add("active");
        }

        document.querySelectorAll(".step-dot-wrap").forEach(function (dot) {
            var step = Number(dot.dataset.step);
            dot.classList.toggle("current", step === n);
            dot.classList.toggle("done", step < n);
        });

        var stepper = document.getElementById("workflowStepper");

        if (stepper) {
            stepper.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }

    // Expose globally since buttons call showPage(n) via inline onclick
    window.showPage = showPage;

    // ==================================================
    // STEP 3 — UPLOAD VENDOR QUOTATION PDF
    // ==================================================

    function selectQuotationFile(vendorId) {

        var fileInput = document.getElementById("vendor" + vendorId);

        if (!fileInput) {
            alert("Could not find the file picker for this vendor.");
            return;
        }

        // Opens the browser's native "choose file" dialog. The actual
        // upload is kicked off automatically by the change listener
        // below once a file is picked.
        fileInput.click();
    }

    window.selectQuotationFile = selectQuotationFile;

    function uploadQuotation(vendorId) {

        if (!TENDER_ID) {
            alert("Could not determine which tender this is. Please reload the page.");
            return;
        }

        var fileInput = document.getElementById("vendor" + vendorId);

        if (!fileInput || fileInput.files.length === 0) {
            alert("Please choose a PDF file first.");
            return;
        }

        var file = fileInput.files[0];

        if (!file.name.toLowerCase().endsWith(".pdf")) {
            alert("Only PDF files are allowed.");
            return;
        }

        var statusEl = document.getElementById("status" + vendorId);

        if (statusEl) {
            statusEl.textContent = "Uploading...";
        }

        // Build a real form and move the file input (with its selected
        // file already attached) into it, then submit natively. This is
        // more reliable for file uploads than doing it over fetch().
        var form = document.createElement("form");
        form.method = "POST";
        form.enctype = "multipart/form-data";
        form.action = "/upload_quotation/" + TENDER_ID;
        form.style.display = "none";

        var vendorIdField = document.createElement("input");
        vendorIdField.type = "hidden";
        vendorIdField.name = "vendor_id";
        vendorIdField.value = vendorId;
        form.appendChild(vendorIdField);

        fileInput.name = "quotation_file";
        form.appendChild(fileInput);

        document.body.appendChild(form);
        form.submit();
    }

    window.uploadQuotation = uploadQuotation;

    // As soon as a file is chosen in the native dialog, upload it right
    // away -- no second click needed.
    document.querySelectorAll(".vendor-file").forEach(function (input) {

        input.addEventListener("change", function () {

            var vendorId = input.id.replace("vendor", "");

            if (input.files.length > 0) {

                var statusEl = document.getElementById("status" + vendorId);

                if (statusEl) {
                    statusEl.textContent = input.files[0].name;
                }

                uploadQuotation(vendorId);
            }
        });
    });

    // ==================================================
    // STEP 7 — SAVE NEGOTIATION
    // ==================================================

    function saveNegotiation() {

        var form = document.getElementById("negotiationForm");

        if (!form) {
            alert("Negotiation form not found on this page.");
            return;
        }

        form.submit();
    }

    window.saveNegotiation = saveNegotiation;

    // ==================================================
    // STEP 8 — GENERATE / DOWNLOAD REPORT
    // ==================================================

    function generateReport() {

        if (!TENDER_ID) {
            alert("Could not determine which tender this is. Please reload the page.");
            return;
        }

        window.location.href = "/generate_report/" + TENDER_ID;
    }

    window.generateReport = generateReport;

    function downloadReport() {

        if (!TENDER_ID) {
            alert("Could not determine which tender this is. Please reload the page.");
            return;
        }

        // Deterministic filename set by generate_report() in app.py.
        // If it 404s, the report hasn't been generated yet.
        window.location.href = "/download_report/Report_" + TENDER_ID + ".pdf";
    }

    window.downloadReport = downloadReport;

    // ==================================================
    // INITIAL STATE
    // ==================================================

    document.addEventListener("DOMContentLoaded", function () {
        showPage(INITIAL_STEP);
    });

})();
