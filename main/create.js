let email = document.getElementById("email");
let password = document.getElementById("password");
let password_check = document.getElementById("password-check");

let signupForm = document.querySelector(".signup-form");

signupForm.addEventListener("submit", (e) => {
  e.defaultPrevented();
  if (password == password_check) {
    // database에서 중복 있는지 확인
  } else {
    alert("비밀번호 재입력");
  }
});
