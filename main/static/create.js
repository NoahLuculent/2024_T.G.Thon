const email = document.getElementById("email");
const password = document.getElementById("password");
const password_check = document.getElementById("password-check");

let signupForm = document.querySelector(".signup-form");

signupForm.addEventListener("submit", (e) => {
  e.defaultPrevented();
  if (password == password_check) {
    // database에서 중복 있는지 확인
  } else {
    alert("비밀번호 재입력");
  }
});
