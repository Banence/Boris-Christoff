function updatePartner(partnerId) {
    const form = document.getElementById('update-partner-form');
    const formData = new FormData(form);
    
    fetch(`/admin/update-partner/${partnerId}`, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = '/admin/upload-partner';
        } else {
            alert('Error: ' + (data.error || 'Unknown error occurred'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the partner');
    });
}

function deletePartner(partnerId) {
    if (confirm('Are you sure you want to delete this partner?')) {
        fetch(`/admin/partners/delete/${partnerId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById(`partner-${partnerId}`).remove();
            } else {
                alert('Error: ' + (data.error || 'Unknown error occurred'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the partner');
        });
    }
} 