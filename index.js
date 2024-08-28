// 처음 화면에서 로그인 화면으로 전환
document.addEventListener("click", function () {
  const page1 = document.getElementById("page1");
  const page2 = document.getElementById("page2");

  page1.classList.add("hidden");

  setTimeout(function () {
    page1.style.display = "none";
    page2.style.display = "flex";
    page2.classList.remove("hidden");
  }, 500); // CSS transition 시간에 맞추기
});

// 카카오 SDK 초기화
Kakao.init('46e82f2f8a5929e5352cf27290d36421');
console.log(Kakao.isInitialized()); // SDK 초기화 확인 (true 출력 시 성공)

// 카카오 로그인 버튼 클릭 이벤트
document.getElementById('kakao-login-btn').addEventListener('click', function (e) {
  e.preventDefault(); // 기본 동작 막기
  loginWithKakao();
});

// 카카오 로그인 처리 함수
function loginWithKakao() {
  Kakao.Auth.login({
    success: function (authObj) {
      console.log(authObj); // 인증 정보 출력
      Kakao.Auth.setAccessToken(authObj.access_token); // access 토큰 값 저장

      // 사용자 정보 요청
      Kakao.API.request({
        url: '/v2/user/me',
        success: function (res) {
          console.log(res); // 사용자 정보 출력
          alert('카카오 로그인 성공');
          window.location.href = "view.html"; // 로그인 성공 시 view.html로 이동
        },
        fail: function (error) {
          console.error(error);
        }
      });
    },
    fail: function (err) {
      console.error(err);
      alert('카카오 로그인 실패');
    }
  });
}

// 로그인 폼 처리
document.querySelector(".login-form").addEventListener("submit", function (e) {
  e.preventDefault();
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;

  console.log("Email: ", email);
  console.log("Password: ", password);

  // 이후 API로 전송하는 부분이 필요함
  // Flask 서버 구축 후 데이터 전송 및 처리
  // 데이터베이스에는 편지지, 우편함 페이지 주소가 포함되어 있어야 함
});
