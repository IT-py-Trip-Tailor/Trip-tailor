var slideIndex = 0;
var slides = document.getElementsByClassName("slider-img");
var slider = document.getElementById("slider");
var isDragging = false;
var startPos;

// Отображение текущего слайда
function showSlide(n) {
    if (n >= slides.length) {
        slideIndex = 0;
    }
    if (n < 0) {
        slideIndex = slides.length - 1;
    }

    for (var i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex].style.display = "block";
}

showSlide(slideIndex); // Отображение исходного слайда

// Добавление слушателей событий
slider.addEventListener('mousedown', (e) => {
    isDragging = true;
    startPos = e.clientX;
});

slider.addEventListener('mouseup', (e) => {
    if (!isDragging) return;
    isDragging = false;
    if (startPos < e.clientX) {
        showSlide(--slideIndex);
    } else {
        showSlide(++slideIndex);
    }
});

slider.addEventListener('mouseleave', () => {
    isDragging = false;
});
