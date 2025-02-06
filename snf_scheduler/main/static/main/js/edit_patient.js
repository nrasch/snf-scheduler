$(document).ready(function() {
    // Ensure the patientTable is defined before adding event handlers
    if (window.patientTable) {

        // Function to handle modal display and setup
        function setupEditModal(response) {
            $('#editPatientModalContainer').html(response);
            editModalBtnMappings();
            $('#editPatientModal').modal({backdrop: true, keyboard: true});
            $('#editPatientModal').modal('show');
        }

        // Function to clear modal and backdrop
        function clearEditModal() {
            $('#editPatientModal').modal('hide');
        }

        // Function cancel patient edit and clear the modal form
        function editModalBtnMappings() {
            // Add click event handler for the cancel button
            $("#cancelEditPatientBtn").off('click.cancelPatientHandler').on('click.cancelPatientHandler', function() {
                console.log('Cancelling patient edit...');
                clearEditModal();
            });

            // Add click event handler for the edit button
            $("#editPatientBtn").off('click.editPatientHandler').on('click.editPatientHandler', function() {
                editPatient();
            });
        }

        // Add event handler to display the modal for patient edits
        // Using event delegation to handle dynamically added elements
        $(document).on('click', '#patient-table tbody .edit-btn', function(e) {
            // Fetch the row data for the patient being edited
            var data = window.patientTable.row($(this).closest('tr')).data();

            // Assign the patient ID to a global variable for use in the edit function
            patientID = data.id;

            // URL for the server endpoint to retrieve the modal content
            var url = editPatientUrl.replace('0', patientID);

            // AJAX call to obtain the modal content
            $.ajax({
                url: url,
                type: "GET",
                success: function(response) {
                    // Add event handlers to the modal buttons since we are editing dynamically
                    setupEditModal(response);
                },
                error: function(xhr, status, error) {
                    // Handle any errors from the AJAX request
                    console.error('Error loading edit patient modal:', error);
                }
            });
        });


        // Function to initialize the modal for patient edit
        function editPatient() {
            // Get the form element for patient edit
            var form = $('#editPatientForm');

            // Modify the URL to include the patient ID
            var url = editPatientUrl.replace('0', patientID);

            // AJAX call to submit the form data
            $.ajax({
                url: url,
                type: "POST", // HTTP method for form submission
                headers: {
                    // Include CSRF token for security against cross-site request forgery
                    "X-CSRFToken": csrfToken
                },
                data: form.serialize(), // Serialize form data for sending
                success: function(response) {
                    // Check if the server response indicates success
                    if (response.success) {
                        console.log('Patient edited successfully.');
                        // Close the modal after successful edit
                        $('#editPatientModal').modal('hide');
                        // Update the toast message with server response
                        $('#toastMessage').html(response.message);
                        // Show a toast notification for user feedback
                        $('#patientToast').toast('show');
                        // Reload the patient table to reflect new data
                        window.patientTable.ajax.reload();
                    } else {
                        console.log('Error editing patient.');
                        // Remove the modal backdrop to avoid stacking (in case of multiple modal openings)
                        $('.modal-backdrop').remove();
                        // Re-setup the modal with error details for user to correct
                        setupEditModal(response);
                    }
                },
                // Handle any errors from the AJAX request
                error: function(xhr, status, error) {
                    console.log('Error editing patient:', error);
                }
            });

        } // end function editPatient() {
    } // end if (window.patientTable) {
});