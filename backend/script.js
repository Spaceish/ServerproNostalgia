function refreshKey() {
    fetch('/key-rec')
        .then(response => response.json())
        .then(data => {
            const newKey = data.key;
            console.log(newKey);
            document.getElementById('key').innerText = newKey;
        })
        .catch(error => {
            console.error(error);
        });
}