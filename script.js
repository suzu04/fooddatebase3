document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('.toggle-button');

    toggleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const nextGroup = btn.nextElementSibling;
            if (nextGroup) {
                nextGroup.style.display = nextGroup.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
});



