document.addEventListener('DOMContentLoaded', function() {
  let write_new = document.getElementById("write_new");
  let check_mine = document.getElementById("check_mine");

  // "새 편지 작성" 버튼 클릭 시 write.html로 이동
  write_new.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "write.html";
  });

  // "내게 온 편지 확인" 버튼 클릭 시 view.html로 이동
  check_mine.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "view.html";
  });
});
