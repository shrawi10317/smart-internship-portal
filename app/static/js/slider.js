let slideIndex = 1;
let autoSlide;

// START
document.addEventListener("DOMContentLoaded", function(){
    showSlides(slideIndex);
    startAutoSlide();
});

// NEXT / PREV
function plusSlides(n){
    showSlides(slideIndex += n);
}

// DOT CLICK
function currentSlide(n){
    showSlides(slideIndex = n);
}

// MAIN FUNCTION
function showSlides(n){

    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");

    if(slides.length === 0) return;

    if(n > slides.length){ slideIndex = 1 }
    if(n < 1){ slideIndex = slides.length }

    // hide all
    for(let i=0;i<slides.length;i++){
        slides[i].classList.remove("active");
    }

    for(let i=0;i<dots.length;i++){
        dots[i].classList.remove("active");
    }

    // show current
    slides[slideIndex-1].classList.add("active");
    dots[slideIndex-1].classList.add("active");
}

// AUTO SLIDE
function startAutoSlide(){
    clearInterval(autoSlide);
    autoSlide = setInterval(() => {
        plusSlides(1);
    }, 3000); // 🔥 FAST & SMOOTH
}