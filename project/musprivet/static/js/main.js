// 2й уровень навигации появление при HOVER
let navSecondLevel = document.querySelector('.nav__link_2level');
navSecondLevel.addEventListener('mouseover', () => {
  document.querySelector('.nav__list-2level').classList.toggle('hidden');
})

// Функция для добавления стилей ссылкам папе, маме, жене, мужу и т.д. на главной странице
const colorsArray = ['ready-variants__link_green', 'ready-variants__link_red', 'ready-variants__link_verygreen', 'ready-variants__link_yellow', 'ready-variants__link_siren', 'ready-variants__link_puppy', 'ready-variants__link_softblue', 'ready-variants__link_browny', 'ready-variants__link_blue', 'ready-variants__link_strongyellow', 'ready-variants__link_orange', 'ready-variants__link_chery'];
const readyVariantsLink = Array.from(document.querySelectorAll('.ready-variants__link'));
readyVariantsLink.forEach((a)=> {
  a.classList.remove('ready-variants__link_siren');
})
for (let i = 0; i < readyVariantsLink.length; i++) {
if (colorsArray[i] === undefined) {colorsArray[i] = colorsArray[i-1];
}
  readyVariantsLink[i].classList.add(colorsArray[i]);
}

// СТРЕЛОЧКА НАВЕРХ
document.addEventListener("DOMContentLoaded", function () {
  const backToTop = document.getElementById("back-to-top");

  // Показать/скрыть кнопку при прокрутке страницы
  window.addEventListener("scroll", function () {
    if (window.pageYOffset > 300) {
      backToTop.style.display = "block";
    } else {
      backToTop.style.display = "none";
    }
  });

  // Плавная прокрутка при клике на кнопку
  backToTop.addEventListener("click", function (event) {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});


// ВКЛАДКИ на странице рекламный ролик

function openCity(evt, cityName) {
  // Declare all variables

  // Get all elements with class="tabcontent" and hide them
  let tabcontent = document.getElementsByClassName("tabcontent");
  for (let i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  let tablinks = document.getElementsByClassName("tablinks");
  for (let i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "flex";
  evt.currentTarget.className += " active";
}

// Открыть первую вкладку по умолчанию
if (document.getElementById("defaultOpen")) {
  document.getElementById("defaultOpen").click();
}




// Защита аудио
// var element = document.querySelector('audio');

// var observer = new MutationObserver(function(mutations) {
//   mutations.forEach(function(mutation) {
//     if ('attributes' === mutation.type &&
//       'controlslist' === mutation.attributeName &&
//       !element.getAttribute('controlslist')
//     ) {
//       alert('Попытка изменить атрибут "controlslist"');
//       element.setAttribute('controlslist', 'nodownload');
//     }
//   });
// });

// observer.observe(element, {
//   attributes: true
// });

// setTimeout(function() {
//   element.setAttribute('controlslist', '');
// }, 2000)

// $('audio').bind('contextmenu', function(e) {return false; });



// Кастомный AUDIO
// Поиск тега аудио
document.addEventListener('DOMContentLoaded', () => {
  let audios = document.querySelectorAll('.custom-audio');
  audios = Array.from(audios);
  audios.forEach(audio => {
    audio.addEventListener('pause', () => {
      playPausa.classList.remove('pause');
    })
    // Создание контейнера и других элементов
    const audioContainer = document.createElement('div')
    audioContainer.classList.add('custom-audio__container', 'flex', 'align-items-center');

    const playPausa = document.createElement('div')
    playPausa.classList.add('play-pause')

    playPausa.addEventListener('click', () => {

      // Запустить это аудио
      if (audio.paused) {
        audio.play();
        playPausa.classList.add('pause');
      }
      else if (audio.play) {
        audio.pause();
        playPausa.classList.remove('pause');
      }
      return false
    })

    const times = document.createElement('div')
    times.classList.add('times', 'flex')

    const currentTime = document.createElement('div')
    currentTime.classList.add('currentTime')
    currentTime.textContent = '00:00'

    const span = document.createElement('span')
    span.textContent = '/'

    const durationTime = document.createElement('div')
    durationTime.classList.add('durationTime')
    durationTime.textContent = toTime(audio.duration);

    audio.addEventListener('loadedmetadata', () => {
      durationTime.textContent = toTime1(audio.duration);
    })

    times.append(currentTime, span, durationTime)

    const progressBar = document.createElement('div')
    progressBar.classList.add('progress-bar')

    const currentProgress = document.createElement('div')
    currentProgress.classList.add('currentProgress')

    const currentProgressBall = document.createElement('div')
    currentProgressBall.classList.add('currentProgress-ball')

    currentProgress.append(currentProgressBall)
    progressBar.append(currentProgress)

    const timePlus = document.createElement('div')
    timePlus.classList.add('time-plus')
    timePlus.addEventListener('click', speedUp)

    const timeMinus = document.createElement('div')
    timeMinus.classList.add('time-minus')
    timeMinus.addEventListener('click', slowDown)

    // Функции для audio

    function speedUp() {
      audio.play();
      playPausa.classList.add('pause');
      // Перемтока на 30сек вперед
      audio.currentTime += 10;
    }

    function slowDown() {
      audio.play();
      // Перемтока на 10сек назад
      audio.currentTime -= 10;
    }

    // Секунды преобразование минута:секунда
    function toTime1(seconds = 0) {
      var date = new Date(null);
      date.setSeconds(seconds);
      return date.toISOString().slice(-10, -5);
    }
    // Запасная функция
    function toTime(time = 0) {
      let seconds = Math.floor(time % 60);
      if (seconds < 10) {
        seconds = `0` + seconds;
      }
      let minute = Math.floor(time / 60)
      return `${minute}:${seconds}`
    }
      // Прогресс бар
  function progressUpdate() {
    currentProgress.style.width = (audio.currentTime / audio.duration * 100) + "%";

    // Заполняем текстовую надпись текущим значением
    currentTime.textContent = toTime1(audio.currentTime);
    // displayStatus.innerHTML = (Math.round(audio.currentTime) / 100);
  }
  audio.addEventListener('timeupdate', progressUpdate)


      // Мануальная перемотка аудио
  function audioChangeTime(e) {
    var mouseX = Math.floor(e.pageX - progressBar.offsetLeft);
    var progress = mouseX / (progressBar.offsetWidth / 100);
    audio.currentTime = audio.duration * (progress / 100);
  }
  progressBar.addEventListener('click', audioChangeTime);

  audioContainer.append(playPausa, times, progressBar, timeMinus, timePlus)
  audio.after(audioContainer)
})
  })

// Одно играющее аудио на странице
function stopOtherAudio1(currentAudio) {
  allAudio.forEach((e) =>{
    if (e !== currentAudio) {
      e.pause()
    }
  })
}
let allAudio = Array.from(document.getElementsByTagName('audio'))
allAudio.forEach((e) => {
  e.addEventListener('play', ()=>{
    stopOtherAudio1(e)
  console.log('stop!')})
})

// Инициализация карусели
  $(document).ready(function(){
    $(".owl-carousel").owlCarousel(
      {
        items: 3,
        margin: 10,
        loop: true,
        nav: false,
        dots: true,
        aoutoplay: true,
        autoplayTimeout: 5000,
        responsive : {
          0:{
            items:1
          },
          768:{
            items:2
          },
          1180:{
            items:3
          }
        }
      }
    );
  });

// Функции для сквозного видео RITUAL
const ritual = document.querySelector('.ritual');
const ritualVideo = document.querySelector('.ritual__video');
const ritualClose = document.querySelector('.ritual__close');
const ritualMute = document.querySelector('.ritual__mute');
const ritualControls = document.querySelector('.ritual__controls');
let initialWidth = '130px';
let popedWidth = '300px';

ritual.addEventListener('click', (e) => {
  if (e.target === ritualClose || e.target ===ritualMute) {
    return
  }
  ritual.classList.remove('ritual_hover');
  if (ritualVideo.muted) {
  ritualVideo.currentTime = 0;}
  if (!ritualVideo.paused && ritual.style.maxWidth === popedWidth) {
    ritualVideo.pause();
  }
  else ritualVideo.play();
  ritual.style.maxWidth = popedWidth;
  ritualVideo.muted = false;
})

ritualClose.addEventListener('click', () => {
  if (ritual.classList.contains('ritual_hover') || ritual.style.maxWidth === initialWidth) {
    ritual.remove()
  }
  ritual.style.maxWidth = initialWidth;
  ritualVideo.muted = true;
})


ritualMute.addEventListener('click', () => {
  if (!ritualVideo.muted) {
  ritualVideo.muted = true;
  ritualMute.classList.add('ritual__unmute')}
  else {
    ritualVideo.muted = false;
    ritualMute.classList.remove('ritual__unmute')
};
})

// Функция для внезапного сообщения с боку
const sideMessage = document.getElementById('side-message')
const sideMessageDescr = document.getElementById('side-message__descr')

if (getLocal('sideMessages') === null) {
  setTimeout(() => {
    setLocal(1, 'sideMessages')
  }, 1000)}
if (getLocal('sideMessages') === 1) {
  sideMessageDescr.textContent = 'Александр из Москвы только что отправил поздравление девушке Арине!';
  sideMessage.style.animationDelay = '10s';
  setTimeout(()=>{
    setLocal(2, 'sideMessages');
  }, 1000)
}
if (getLocal('sideMessages') === 2) {
  sideMessageDescr.textContent = 'Михаил из Екатеринбурга только что отправил поздравление подруге Милене!';
  sideMessage.style.animationDelay = '20s';
  setTimeout(()=>{
    setLocal(3, 'sideMessages');
  }, 1000)
}

if (getLocal('sideMessages') === 3) {
  sideMessage.remove()
}



// работа с LocalStorage
// Фукнция записи дела в localStorage
function setLocal(inData, listName) {
  localStorage.setItem(listName, JSON.stringify(inData))
}

// Функция для возврата данных из localStorage
function getLocal(listName) {
  return JSON.parse(localStorage.getItem(listName));
}

