document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Bandwidth slider functionality
    document.querySelectorAll('.bandwidth-slider').forEach(slider => {
        slider.addEventListener('input', function() {
            const mac = this.dataset.mac;
            const value = this.value;
            
            fetch('/api/clients/bandwidth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': document.querySelector('meta[name="api-key"]').content
                },
                body: JSON.stringify({
                    mac: mac,
                    limit: value + 'mbit'
                })
            }).then(response => {
                if (!response.ok) throw new Error('Network error');
                showToast('Bandwidth limit updated');
            }).catch(error => {
                console.error('Error:', error);
                showToast('Update failed', 'danger');
            });
        });
    });

    // Block client buttons
    document.querySelectorAll('.block-client').forEach(button => {
        button.addEventListener('click', function() {
            const mac = this.dataset.mac;
            if (confirm(`Block device ${mac}?`)) {
                fetch('/api/clients/block', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': document.querySelector('meta[name="api-key"]').content
                    },
                    body: JSON.stringify({ mac: mac })
                }).then(response => {
                    if (!response.ok) throw new Error('Network error');
                    showToast('Device blocked');
                    setTimeout(() => location.reload(), 1000);
                }).catch(error => {
                    console.error('Error:', error);
                    showToast('Block failed', 'danger');
                });
            }
        });
    });

    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        new bootstrap.Toast(toast, { delay: 3000 }).show();
        setTimeout(() => toast.remove(), 3000);
    }
});