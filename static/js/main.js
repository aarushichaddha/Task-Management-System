// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.opacity = '0';
                setTimeout(() => msg.remove(), 500); // Wait for transition
            });
        }, 5000);
    }

    // Confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Simple date validation for add/edit task
    const taskForms = document.querySelectorAll('#addTaskForm, #editTaskForm');
    taskForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const dueDateInput = form.querySelector('#due_date');
            if (dueDateInput && dueDateInput.value) {
                // We can allow past dates (e.g., for logging retroactive tasks)
                // but if we wanted to restrict to future dates, we could do:
                /*
                const selectedDate = new Date(dueDateInput.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                if (selectedDate < today) {
                    alert('Due date cannot be in the past.');
                    e.preventDefault();
                }
                */
            }
        });
    });
});
