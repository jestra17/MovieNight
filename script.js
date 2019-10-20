var slideIndex = 1;
showSlides(slideIndex, "mySlides", "dot");
showSlides(slideIndex,"mySlides2","dot1")

// Next/previous controls
function plusSlides(n, slidesString, dotsString) {
  showSlides(slideIndex += n, slidesString, dotsString);
}

// Thumbnail image controls
function currentSlide(n, slidesString, dotsString) {
  showSlides(slideIndex = n, slidesString, dotsString);
}

function showSlides(n, slidesString, dotsString ) {
  var i;
  var slides = document.getElementsByClassName(slidesString);
  var dots = document.getElementsByClassName(dotsString);
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}


