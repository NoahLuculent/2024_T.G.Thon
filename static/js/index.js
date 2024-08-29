// 화면 전환
document.addEventListener("click", function () {
  const page1 = document.getElementById("page1");
  const page2 = document.getElementById("page2");

  page1.classList.add("hidden");

  setTimeout(function () {
    page1.style.display = "none";
    page2.style.display = "flex";
    page2.classList.remove("hidden");
  }, 500);
});

// 카카오 SDK 초기화
Kakao.init("46e82f2f8a5929e5352cf27290d36421");
console.log(Kakao.isInitialized());

// 카카오 로그인 버튼 클릭 이벤트
document
  .getElementById("kakao-login-btn")
  .addEventListener("click", function (e) {
    e.preventDefault();
    loginWithKakao();
  });

// 카카오 로그인 처리
function loginWithKakao() {
  Kakao.Auth.login({
    success: function (authObj) {
      console.log(authObj);
      Kakao.Auth.setAccessToken(authObj.access_token);
      getInfo();
    },
    fail: function (err) {
      console.error(err);
      alert("카카오 로그인 실패");
    },
  });
}

// 사용자 정보 요청
function getInfo() {
  Kakao.API.request({
    url: "/v2/user/me",
    success: function (res) {
      var id = res.id;
      var profile_nickname = res.kakao_account.profile.nickname;
      localStorage.setItem("nickname", profile_nickname);
      localStorage.setItem("id", id);
      window.location.href = "";
    },
    fail: function (error) {
      alert("카카오 로그인 실패" + JSON.stringify(error));
    },
  });
}

// 로그인 폼 처리
document.querySelector(".login-form").addEventListener("submit", function (e) {
  // e.preventDefault();  // 폼 제출을 막는 코드 주석 처리 또는 제거
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;
  console.log("Email: ", email);
  console.log("Password: ", password);

  // 이 폼은 서버로 정상적으로 전송됩니다.
});
