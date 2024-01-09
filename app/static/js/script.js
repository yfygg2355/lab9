function closeAlert() {
    var alertMessage = document.getElementById('alertMessage');
    alertMessage.style.display = 'none';
}


document.getElementById('picture').addEventListener('change', function() {
    var fileName = this.value.split('\\').pop();
    document.getElementById('custom-file-label').innerText = fileName;
});

