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