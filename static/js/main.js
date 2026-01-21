document.addEventListener('DOMContentLoaded', function () {
    const tables = document.querySelectorAll('.data-table');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            if (index < headers.length - 1) {
                const resizer = document.createElement('div');
                resizer.className = 'resizer';
                header.appendChild(resizer);
                makeResizable(header, resizer);
            }
        });
    });
});

function makeResizable(header, resizer) {
    let x = 0;
    let w = 0;
    let table = header.closest('table');
    let colIndex = Array.from(header.parentNode.children).indexOf(header);

    const mouseDownHandler = function (e) {
        x = e.clientX;
        w = header.offsetWidth;

        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    };

    const mouseMoveHandler = function (e) {
        const dx = e.clientX - x;
        const newWidth = w + dx;
        header.style.width = `${newWidth}px`;

        const rows = table.querySelectorAll('tr');
        rows.forEach(row => {
            const cells = row.children;
            if (cells.length > colIndex) {
                cells[colIndex].style.width = `${newWidth}px`;
            }
        });
    };

    const mouseUpHandler = function () {
        document.removeEventListener('mousemove', mouseMoveHandler);
        document.removeEventListener('mouseup', mouseUpHandler);
    };

    resizer.addEventListener('mousedown', mouseDownHandler);
}
