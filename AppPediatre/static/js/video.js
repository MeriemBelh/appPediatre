const section = document.querySelector("section");
const body = document.querySelector("body");
const mainVideo = document.querySelector(".main-video video");
const videos = document.querySelectorAll(".videos");
const close = document.querySelector(".close");
const titleElement = document.querySelector(".main-video .title");

videos.forEach((video) => {
    video.addEventListener("click", (e) => {
        const target = e.currentTarget;
        section.classList.add("active");
        body.classList.add("active");

        videos.forEach((video) => {
            video.classList.add("active");
        });

        let src = target.querySelector("video").src;
        let title = target.querySelector("video").getAttribute("data-title");

        mainVideo.src = src;
        titleElement.textContent = title;
    });
});

close.addEventListener("click", () => {
    section.classList.remove("active");
    body.classList.remove("active");
    mainVideo.src = "";
    titleElement.textContent = "";

    videos.forEach((video) => {
        video.classList.remove("active");
    });
});





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
