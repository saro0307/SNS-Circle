const searchInput = document.getElementById('search-input');
const searchIcon = document.getElementById('search-icon');
const iconImg = document.getElementById('icon-img');

searchInput.addEventListener('focus', () => {
     if (searchInput.value == '') {
        iconImg.style = "display: none";
    }
});

searchInput.addEventListener('blur', () => {
    if (searchInput.value === '') {
        iconImg.style = "display: grid";
    }
});

searchIcon.addEventListener('click', () => {
    if (searchInput.value === '') {
        searchInput.focus();
    } 
});

searchInput.addEventListener('input', () => {
    if (searchInput.value == '') {
        iconImg.src = '../static/images/search.png';
    }
    else {
        iconImg.style = "display: none";
    }
});

document.querySelector('.card-gallery-container').addEventListener('wheel', function (event) {
        event.preventDefault();
        this.scrollLeft += event.deltaY;
    });
