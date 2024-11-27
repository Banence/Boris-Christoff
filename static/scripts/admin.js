function getCsrfToken() {
    // Get CSRF token from meta tag
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return token;
}

function deleteNews(newsId) {
    if (confirm('Are you sure you want to delete this news item?')) {
        fetch(`/admin/news/delete/${newsId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken()  // Add CSRF token
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('News item not found');
                } else if (response.status === 403) {
                    throw new Error('Unauthorized');
                } else if (response.status === 400) {
                    return response.json().then(data => {
                        throw new Error(data.message || 'Bad Request');
                    });
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const newsElement = document.querySelector(`[data-news-id="${newsId}"]`);
                if (newsElement) {
                    newsElement.remove();
                } else {
                    window.location.reload();
                }
                showNotification('News item deleted successfully', 'success');
            } else {
                throw new Error(data.message || 'Error deleting news item');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification(error.message || 'Error deleting news item', 'error');
            if (error.message === 'Unauthorized') {
                window.location.href = '/login';
            }
        });
    }
}

function deleteEvent(eventId) {
    if (confirm('Are you sure you want to delete this event?')) {
        fetch(`/admin/delete-event/${eventId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Event not found');
                } else if (response.status === 403) {
                    throw new Error('Unauthorized');
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const eventElement = document.querySelector(`[data-event-id="${eventId}"]`);
                if (eventElement) {
                    eventElement.remove();
                } else {
                    window.location.reload();
                }
                showNotification('Event deleted successfully', 'success');
            } else {
                throw new Error(data.message || 'Error deleting event');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification(error.message || 'Error deleting event', 'error');
            if (error.message === 'Unauthorized') {
                window.location.href = '/login';
            }
        });
    }
}

function deletePartner(partnerId) {
    if (confirm('Are you sure you want to delete this partner?')) {
        fetch(`/admin/partners/delete/${partnerId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Partner not found');
                } else if (response.status === 403) {
                    throw new Error('Unauthorized');
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const partnerElement = document.querySelector(`[data-partner-id="${partnerId}"]`);
                if (partnerElement) {
                    partnerElement.remove();
                } else {
                    window.location.reload();
                }
                showNotification('Partner deleted successfully', 'success');
            } else {
                throw new Error(data.message || 'Error deleting partner');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification(error.message || 'Error deleting partner', 'error');
            if (error.message === 'Unauthorized') {
                window.location.href = '/login';
            }
        });
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
} 