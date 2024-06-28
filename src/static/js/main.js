let ws = new WebSocket("ws://127.0.0.1:8000/pages/ws");
let timer;
let wpm = 0;
const decreaseInterval = 1000; // Интервал для уменьшения WPM

// Функция для обновления отображения WPM
function updateWPM() {
  document.getElementById("result").innerText = "WPM: " + wpm.toFixed(2);
}

// Функция для уменьшения WPM со временем
function decreaseWPM() {
  if (wpm > 0) {
    wpm -= 0.1; // Уменьшение WPM на 0.1 каждую секунду
    updateWPM();
  }
}

// Функция для перезапуска страницы
function Restart() {
  ws.send("restart");
  document.getElementById("word").value = "";
  currentInput = "";
  wpm = 0;
  updateWPM();
  clearInterval(timer);
}

// Обработка сообщений от WebSocket
ws.onmessage = function (event) {
  try {
    var data = JSON.parse(event.data);
    if (data.initial_text) {
      document.getElementById("text").innerText = data.initial_text;
    } else {
      var is_end = data.isEnd;
      wpm = data.wpm; // Обновляем WPM на основе данных с сервера

      // Если данные по WPM получены, обновляем значение
      if (data.wpm !== undefined) {
        wpm = data.wpm;
        updateWPM();
      }

      setTimeout(() => {
        if (typeof wpm !== "undefined") {
          updateWPM();
        }
      }, 100); // Обновляем отображение WPM через 100 мс

      // Сбрасываем таймер, если пользователь начал вводить текст
      clearInterval(timer);
      timer = setInterval(decreaseWPM, decreaseInterval);

      // Проверка на конец строки
      if (is_end) {
        var element = document.getElementById("word");
        document.getElementById("prev-result").innerText =
          "Prev WPM: " + wpm.toFixed(2);

        if (element) {
          document.getElementById("word").value = "";
          ws.send("restart");
          currentInput = "";
          wpm = 0;
          updateWPM();
          clearInterval(timer);
        }
      }

      // Обновление цвета текста в зависимости от правильности ввода
      if (data.is_correct) {
        document.getElementById("word").style.color = "white";
      } else {
        document.getElementById("word").style.color = "red";
      }
    }
  } catch (e) {
    console.error("Error parsing JSON:", e);
  }
};

// Функция для отправки текста на сервер
function sendMessage(event) {
  ws.send(event.target.value);
}

// Добавляем обработчик ввода текста
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("word").addEventListener("word", sendMessage);
});
