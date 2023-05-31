//slider 1

let slideIndex = 1;
let timer = setInterval(() => {
  plusSlides(1);
}, 5000);

showSlides(slideIndex);

function plusSlides(n) {
  clearTimeout(timer); // reset the timer
  timer = setInterval(() => {
    plusSlides(1);
  }, 5000);
  showSlides(slideIndex += n);
}



function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}

//slider 2
$(document).ready(function () {
			$("#news-slider").owlCarousel({
				items: 3,
				navigation: true,
				navigationText: ["", ""],
				autoPlay: true
			});
		});


//profile
function menuToggle() {
  const toggleMenu = document.querySelector('.menu');
  toggleMenu.classList.toggle('active');
}

function closeMenu(event) {
  const toggleMenu = document.querySelector('.menu');
  if (event.target.closest('.action') == null) {
    toggleMenu.classList.remove('active');
  }
}

document.addEventListener('click', closeMenu);
