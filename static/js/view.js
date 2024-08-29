document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const letterList = document.getElementById("letter-list");
  const filter = document.getElementById("filter");
  let letters = Array.from(document.querySelectorAll(".letter"));

  // 모든 편지의 원래 위치를 기억하기 위해 인덱스를 부여
  letters.forEach((letter, index) => {
    letter.dataset.originalIndex = index;
  });

  searchInput.addEventListener("input", function () {
    const searchValue = this.value.toLowerCase();
    letters.forEach((letter) => {
      const sender = letter.getAttribute("data-sender");
      if (sender.includes(searchValue)) {
        letter.style.display = "";
      } else {
        letter.style.display = "none";
      }
    });
  });

  // 정렬 기능
  filter.addEventListener("change", function () {
    const sortedLetters = sortLetters(this.value);
    renderLetters(sortedLetters);
  });

  // 즐겨찾기 기능
  function toggleFavorite(star) {
    star.classList.toggle("favorited");
    const letter = star.closest(".letter");

    if (star.classList.contains("favorited")) {
      letterList.prepend(letter); // 목록의 가장 위로 이동
    } else {
      const originalIndex = parseInt(letter.dataset.originalIndex);
      const beforeLetter = letters.find(
        (l) => parseInt(l.dataset.originalIndex) === originalIndex - 1
      );
      if (beforeLetter) {
        beforeLetter.insertAdjacentElement("afterend", letter);
      } else {
        letterList.appendChild(letter);
      }
    }
  }

  // 모든 즐겨찾기 버튼에 이벤트 리스너 추가
  document.querySelectorAll(".star").forEach((star) => {
    star.addEventListener("click", function () {
      toggleFavorite(this);
    });
  });

  // 편지 정렬 함수
  function sortLetters(order) {
    if (order === "oldest") {
      return letters.sort((a, b) => {
        const timeA = parseExtendedTime(
          a.querySelector(".letter-timer").getAttribute("data-time")
        );
        const timeB = parseExtendedTime(
          b.querySelector(".letter-timer").getAttribute("data-time")
        );
        return timeA - timeB; // 오래된 것부터 정렬
      });
    } else {
      return letters.sort((a, b) => {
        const timeA = parseExtendedTime(
          a.querySelector(".letter-timer").getAttribute("data-time")
        );
        const timeB = parseExtendedTime(
          b.querySelector(".letter-timer").getAttribute("data-time")
        );
        return timeB - timeA; // 최신 것부터 정렬
      });
    }
  }

  function renderLetters(sortedLetters) {
    letterList.innerHTML = ""; // 기존 편지 목록 초기화
    sortedLetters.forEach((letter) => {
      letterList.appendChild(letter); // 정렬된 편지를 리스트에 추가
    });
  }

  function parseExtendedTime(timeString) {
    let months = 0,
      days = 0,
      hours = 0,
      minutes = 0,
      seconds = 0;
    const parts = timeString.split(" ");

    parts.forEach((part) => {
      if (part.includes("months")) months = parseInt(part);
      if (part.includes("days")) days = parseInt(part);
      if (part.includes("hours")) hours = parseInt(part);
      if (part.includes("minutes")) minutes = parseInt(part);
      if (part.includes("secs")) seconds = parseInt(part);
      if (part.includes(":")) {
        const timeParts = part.split(":");
        hours = parseInt(timeParts[0]);
        minutes = parseInt(timeParts[1]);
        seconds = parseInt(timeParts[2]);
      }
    });

    return (
      (((months * 30 + days) * 24 + hours) * 3600 + minutes) * 60 + seconds
    );
  }

  function formatExtendedTime(seconds) {
    const months = Math.floor(seconds / (30 * 24 * 3600));
    seconds %= 30 * 24 * 3600;
    const days = Math.floor(seconds / (24 * 3600));
    seconds %= 24 * 3600;
    const hours = Math.floor(seconds / 3600);
    seconds %= 3600;
    const minutes = Math.floor(seconds / 60);
    seconds %= 60;

    return `${months}months ${days}days ${hours}hours ${minutes}minutes ${seconds}secs`;
  }
  function updateTimers() {
    letters.forEach((letter) => {
      const timerElement = letter.querySelector(".letter-timer");
      const openButton = letter.querySelector(".open-button");
      let remainingTime = parseExtendedTime(
        timerElement.getAttribute("data-time")
      );

      if (remainingTime > 0) {
        remainingTime -= 1;
        const formattedTime = formatExtendedTime(remainingTime);
        timerElement.setAttribute("data-time", formattedTime);
        timerElement.innerHTML = `${formattedTime} left`;

        openButton.classList.add("hidden"); // 버튼 숨김
      } else {
        if (!timerElement.classList.contains("revealed")) {
          timerElement.classList.add("revealed");
          // 익명 파트 쓰는 부분
          const senderName = letter.getAttribute("data-sender");
          timerElement.innerHTML = `${senderName}이(가) 보낸 편지가 도착했습니다`;

          // 편지 미리보기를 표시
          const previewElement = letter.querySelector(".letter-preview");
          previewElement.classList.remove("hidden");

          // 열람 가능 버튼 표시
          openButton.classList.remove("hidden");

          // 알림 추가
          alert(
            `편지 제목: ${
              letter.querySelector(".letter-title").innerText
            }가 도착했습니다!`
          );
          clearInterval(timerInterval);
        }
      }
    });
  }

  /*
    const previewElement = letter.querySelector(".letter-preview");
    previewElement.classList.remove("hidden"); // 미리보기 표시 */

  setInterval(updateTimers, 1000); // 1초마다 타이머 업데이트
});
