window.addEventListener('load', function() {
    const assignAll = document.querySelector('#id_assign_all');
    const employeeCheckboxes = document.querySelectorAll('#id_employees input[type=checkbox]');

    if (assignAll) {
        assignAll.addEventListener('change', function() {
            employeeCheckboxes.forEach(cb => {
                cb.checked = assignAll.checked;
            });
        });
    }
});
