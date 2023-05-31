const togglePassword = document.querySelectorAll('.toggle-password');

togglePassword.forEach(function (element) {
  element.addEventListener('click', function () {
    const input = document.querySelector(this.getAttribute('data_input'));
    if (input.type === "password") {
      input.type = "text";
      this.classList.remove('fa-eye-slash');
      this.classList.add('fa-eye');
    } else {
      input.type = "password";
      this.classList.remove('fa-eye');
      this.classList.add('fa-eye-slash');
    }
  });
});