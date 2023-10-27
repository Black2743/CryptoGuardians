var table = document.getElementById("myTable");
var lastColumnIndex = 5;

for (var i = 1; i < table.rows.length; i++) {
    tableColorData[i] = table.rows[i].className;
}




//**************************************************** */
function populateTable(jsonData) {
    var table = document.getElementById("myTable");
    var newRow = table.insertRow(-1);

    var cell1 = newRow.insertCell(0);
    cell1.innerHTML = table.rows.length - 1;
    var cell2 = newRow.insertCell(1);
    cell2.innerHTML = jsonData.incident;

    var cell3 = newRow.insertCell(2);
    cell3.innerHTML = jsonData.time;

    var cell4 = newRow.insertCell(3);
    cell4.innerHTML = jsonData.camera_name;

    var cell5 = newRow.insertCell(4);
    cell5.innerHTML = jsonData.location;

    var cell6 = newRow.insertCell(5);
    cell6.className = "no-color-change";

    var showPhotoLink = document.createElement('a');
    showPhotoLink.href = "#";
    showPhotoLink.innerHTML = "Показать фото";

    var modal = document.getElementById('myModal');
    var modalImage = document.getElementById('modalImage');
    showPhotoLink.onclick = function() {
        modal.style.display = "block";
        modalImage.src = jsonData.photo;
    };

    var photoDiv = document.createElement('div');
    photoDiv.id = "photo" + (table.rows.length - 1);
    photoDiv.className = "hidden";

    var photoImage = document.createElement('img');
    photoImage.src = jsonData.photo;
    photoImage.alt = jsonData.incident;

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    photoDiv.appendChild(photoImage);
    cell6.appendChild(showPhotoLink);
    cell6.appendChild(photoDiv);

    if (jsonData.color) {
        newRow.classList.add(jsonData.color);
    }


    if (jsonData.color) {
        newRow.classList.add(jsonData.color);
    }
}



fetch("log.json")
    .then(response => response.json())
    .then(data => {
        if (Array.isArray(data)) {
            data.forEach(item => {
                populateTable(item);

            });
        } else {
            console.error('JSON файл не содержит массив объектов');
        }
    })
    .catch(error => console.error('Ошибка при загрузке JSON файла:', error));