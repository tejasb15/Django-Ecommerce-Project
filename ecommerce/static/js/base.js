
// Form Valdiation 
var forms = document.querySelectorAll('.needs-validation')
Array.prototype.slice.call(forms)
    .forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })



// Spinner
var spinner = function () {
    setTimeout(function () {
        if ($('#spinner').length > 0) {
            $('#spinner').removeClass('show');
        }
    }, 1);
};
spinner();

// Back to top button
$(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
});
$('.back-to-top').click(function () {
    $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
    return false;
});

// Vendor carousel
$(document).ready(function () {
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 2
            },
            576: {
                items: 3
            },
            768: {
                items: 4
            },
            992: {
                items: 5
            },
            1200: {
                items: 6
            }
        }
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('floatingPassword');
    const passwordToggle = document.getElementById('passwordToggle');


    // Show the eye icon button when password input field is focused
    passwordInput.addEventListener('focus', function () {
        passwordToggle.style.display = 'block';
    });

    passwordInput.addEventListener("blur", function () {
        passwordToggle.style.display = '';
    });


    // Toggle password visibility when eye icon button is clicked
    passwordToggle.addEventListener('click', function () {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            this.innerHTML = '<i class="bi bi-eye-slash"></i>';
        } else {
            passwordInput.type = 'password';
            this.innerHTML = '<i class="bi bi-eye"></i>';
        }
    });
});

