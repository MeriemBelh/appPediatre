const navEl = document.querySelector('.nav');
const hamburgerEl = document.querySelector('.hamburger');
const navItemEls = document.querySelectorAll('.nav__item');

hamburgerEl.addEventListener('click', () => {
  navEl.classList.toggle('nav--open');
  hamburgerEl.classList.toggle('hamburger--open');
});

//navItemEls.forEach(navItemEl => {
//  navItemEl.addEventListener('click', () => {
//    navEl.classList.remove('nav--open');
//    hamburgerEl.classList.remove('hamburger--open');
//  });
//});

const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", () => {
  if (window.scrollY > 100) {
    backTopBtn.classList.add("active");
  } else {
    backTopBtn.classList.remove("active");
  }
});

function copyContact(event, contactHref, messageText, messageElementId) {
  event.preventDefault();
  let contactValue = '';
  if (contactHref.startsWith('tel:')) {
    contactValue = contactHref.substring(4); // remove the "tel:" prefix from the href
  } else if (contactHref.startsWith('mailto:')) {
    contactValue = contactHref.substring(7); // remove the "mailto:" prefix from the href
  }
  navigator.clipboard.writeText(contactValue)
    .then(() => {
      const messageElement = document.querySelector(`#${messageElementId}`);
      messageElement.textContent = messageText;
      messageElement.style.display = 'block';
      setTimeout(() => {
        messageElement.style.display = 'none';
        messageElement.textContent = '';
      }, 1000); // 2 second delay
    })
    .catch(() => console.error('Failed to copy contact'));
}
