$(document).ready(function() {
    // Initialize Fancybox
    $('[data-fancybox]').fancybox({
        youtube: {
            controls: 0,
            showinfo: 0
        },
        vimeo: {
            color: 'f00'
        }
    });

    // Carousel functionality
    let currentIndex = 0;
    const images = $('.carousel img');
    const imageCount = images.length;

    function showNextImage() {
        images.eq(currentIndex).removeClass('active');
        currentIndex = (currentIndex + 1) % imageCount;
        images.eq(currentIndex).addClass('active');
    }

    // Show the first image initially
    images.eq(currentIndex).addClass('active');

    // Set interval for automatic changing of images
    setInterval(showNextImage, 3000);
});

const texts = [
    "Think Blue Go Green",
    "Connecting Miles",
    "Connecting Lives"
];

const typingText = document.querySelector('.typing-text');
let currentTextIndex = 0;
let currentCharIndex = 0;
let isTyping = true;

function typeText() {
    if (isTyping) {
        typingText.textContent = texts[currentTextIndex].substring(0, currentCharIndex + 1);
        currentCharIndex++;
        if (currentCharIndex > texts[currentTextIndex].length) {
            isTyping = false;
            setTimeout(() => eraseText(), 1000);
        }
    }
}

function eraseText() {
    if (!isTyping) {
        typingText.textContent = texts[currentTextIndex].substring(0, currentCharIndex - 1);
        currentCharIndex--;
        if (currentCharIndex <= 0) {
            isTyping = true;
            currentTextIndex = (currentTextIndex + 1) % texts.length;
            setTimeout(() => typeText(), 500);
        } else {
            setTimeout(() => eraseText(), 50);
        }
    }
}

setInterval(typeText, 200);

document.addEventListener('DOMContentLoaded', function() {
    var dropdowns = document.querySelectorAll('.custom-dropdown');

    dropdowns.forEach(function(dropdown) {
        var selected = dropdown.querySelector('.dropdown-selected');
        var items = dropdown.querySelector('.dropdown-items');

        selected.addEventListener('click', function() {
            items.style.display = items.style.display === 'block' ? 'none' : 'block';
        });

        items.querySelectorAll('div').forEach(function(item) {
            item.addEventListener('click', function() {
                selected.textContent = item.textContent;
                items.style.display = 'none';
            });
        });
    });

    document.addEventListener('click', function(event) {
        dropdowns.forEach(function(dropdown) {
            if (!dropdown.contains(event.target)) {
                dropdown.querySelector('.dropdown-items').style.display = 'none';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var interchangeButton = document.querySelector('.interchange-button');
    var locationSelect = document.querySelector('select[name="location"]');
    var destinationSelect = document.querySelector('select[name="destination"]');

    interchangeButton.addEventListener('click', function() {
        var tempValue = locationSelect.value;
        locationSelect.value = destinationSelect.value;
        destinationSelect.value = tempValue;
    });
});

document.addEventListener('DOMContentLoaded', function() {
function addTime(departureTime, travelTime) {
    let [depHours, depMinutes] = departureTime.split(':').map(Number);

    let [travHours = 0, travMinutes = 0] = travelTime.split(':').map(Number);

    let arrivalHours = depHours + travHours;
    let arrivalMinutes = depMinutes + travMinutes;

    if (arrivalMinutes >= 60) {
        arrivalHours += Math.floor(arrivalMinutes / 60);
        arrivalMinutes = arrivalMinutes % 60;
    }

    arrivalHours = String(arrivalHours).padStart(2, '0');
    arrivalMinutes = String(arrivalMinutes).padStart(2, '0');

    return `${arrivalHours}:${arrivalMinutes}`;
}

document.querySelectorAll('.arrival').forEach(function(arrivalCell) {
    let departureTime = arrivalCell.previousElementSibling.textContent.trim();
    let travelTime = arrivalCell.getAttribute('data-travel-time') || '0:00';
    if (departureTime) {
        let arrivalTime = addTime(departureTime, travelTime);
        arrivalCell.textContent = arrivalTime;
    }
});
});

document.addEventListener('DOMContentLoaded', function() {
    var terminalsContainer = document.querySelector('.terminals-main-container');

    terminalsContainer.addEventListener('wheel', function(e) {
        if (e.deltaY !== 0) {
            e.preventDefault();

            var scrollAmount = e.deltaY * 3; 

            terminalsContainer.scrollLeft += scrollAmount;
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var terminalsContainer = document.querySelector('.tourspots-main-container');

    terminalsContainer.addEventListener('wheel', function(e) {
        if (e.deltaY !== 0) {
            e.preventDefault();

            var scrollAmount = e.deltaY; 

            terminalsContainer.scrollLeft += scrollAmount;
        }
    });
});


