$(document).ready(function() {
    // Ensure the patientTable is defined before adding event handlers
    if (window.patientTable) {
        console.log('Patient table is defined.  Adding event handlers');
        // ADDING NEW PATIENT PATIENT
        // Function to handle modal display and setup
        function setupModal(response) {
            $('#addPatientModalContainer').html(response);
            modalBtnMappings();
            initAddModal();
            $('#addPatientModal').modal({backdrop: true, keyboard: true});
            $('#addPatientModal').modal('show');
        }

        // Function to clear modal and backdrop
        function clearModal() {
            $('#addPatientModal').modal('dispose');
            $('.modal-backdrop').remove();
            $('#addPatientModal').remove();
        }

        // Function cancel patient addition and clear the modal form
        function modalBtnMappings() {
            $("#cancelPatientBtn").off('click.cancelPatientHandler').on('click.cancelPatientHandler', function() {
                console.log('Cancelling patient addition...');
                clearModal();
            });
        }

        function initAddModal() {
            // Remove any existing click event handler for the addPatientBtn to prevent multiple bindings
            $('#addPatientBtn').off('click.addPatientHandler')
                // Attach a new click event handler for the addPatientBtn
                .on('click.addPatientHandler', function(e) {
                    // Get the form element for patient addition
                    var form = $('#addPatientForm');
                    // URL for the server endpoint where the patient data will be sent
                    var url = addPatientUrl;

                    console.log('Adding patient...');

                    // AJAX call to submit the form data
                    $.ajax({
                        url: url,
                        type: "POST", // HTTP method for form submission
                        headers: {
                            // Include CSRF token for security against cross-site request forgery
                            "X-CSRFToken": csrfToken,
                            // Specify the content type of the data being sent
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        data: form.serialize(), // Serialize form data for sending
                        success: function(response) {
                            // Check if the server response indicates success
                            if (response.success) {
                                console.log('Patient added successfully.');
                                // Close the modal after successful addition
                                $('#addPatientModal').modal('hide');
                                // Update the toast message with server response
                                $('#toastMessage').html(response.message);
                                // Show a toast notification for user feedback
                                $('#patientToast').toast('show');
                                // Reload the patient table to reflect new data
                                window.patientTable.ajax.reload();
                            } else {
                                console.log('Error adding patient.');
                                // Remove the modal backdrop to avoid stacking (in case of multiple modal openings)
                                $('.modal-backdrop').remove();
                                // Re-setup the modal with error details for user to correct
                                setupModal(response);
                            }
                        },
                        // Handle any errors from the AJAX request
                        error: function(xhr, status, error) {
                            console.log('Error adding patient:', error);
                        }
                    });
                });
        }

        // Load and display the patient modal
        $('#loadPatientModalBtn').on('click', function(e) {
            // URL for the server endpoint to retrieve the modal content
            var url = addPatientUrl;
            // AJAX call to obtain the modal content
            $.ajax({
                url: url,
                type: "GET",
                success: function(response) {
                    // Add event handlers to the modal buttons since we are adding dynamically
                    setupModal(response);
                },
                error: function(xhr, status, error) {
                    // Handle any errors from the AJAX request
                    console.error('Error loading add patient modal:', error);
                }
            });
        });


        // DELETE PATIENT
        // Using $(document) to attach event handler since this javascript is being included
        // in a separate file and the patient table is being loaded dynamically
        $(document).on('click', '#patient-table tbody .delete-btn', function(e) {

            console.log("Delete button clicked");

            // Get the row data for the selected row where the delete button was clicked
            var row = window.patientTable.row($(this).closest('tr'));
            var data = row.data();

            // Extract the patient ID from the row data
            var patientID = data.id;

            console.log("Deleting Patient with ID:", patientID);

            // AJAX call to delete the patient
            $.ajax({
                url: deletePatientUrl,
                type: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json"
                },
                data: JSON.stringify({ 'patient_id': patientID }),
                success: function(response) {
                    console.log("Patient deleted successfully");
                    // Update the toast message with server response
                    $('#toastMessage').html(response.message);
                    // Show a toast notification for user feedback
                    $('#patientToast').toast('show');
                    // Remove the row from the data table
                    row.remove().draw(false);
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        });
    }
});