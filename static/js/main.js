document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.getElementById("mobile-menu-button");
    const mobileMenu = document.getElementById("mobile-menu");

    const openIcon = document.getElementById("menu-open-icon");
    const closeIcon = document.getElementById("menu-close-icon");

    const mobileLinks = document.querySelectorAll(".mobile-nav-link");


    if (!menuButton || !mobileMenu) {
        return;
    }


    function openMenu() {
        mobileMenu.classList.remove("hidden");

        openIcon.classList.add("hidden");
        closeIcon.classList.remove("hidden");

        menuButton.setAttribute("aria-expanded", "true");
        menuButton.setAttribute("aria-label", "Close navigation menu");
    }


    function closeMenu() {
        mobileMenu.classList.add("hidden");

        openIcon.classList.remove("hidden");
        closeIcon.classList.add("hidden");

        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "Open navigation menu");
    }


    menuButton.addEventListener("click", () => {
        const isOpen =
            menuButton.getAttribute("aria-expanded") === "true";

        if (isOpen) {
            closeMenu();
        } else {
            openMenu();
        }
    });


    mobileLinks.forEach((link) => {
        link.addEventListener("click", () => {
            closeMenu();
        });
    });


    window.addEventListener("resize", () => {
        if (window.innerWidth >= 1024) {
            closeMenu();
        }
    });
});

// payment method


document.addEventListener("DOMContentLoaded", () => {

    const paymentMethod = document.getElementById(
        "id_payment_method"
    );

    const paymentInstructions = document.getElementById(
        "payment-instructions"
    );

    const instructionBank = document.getElementById(
        "instruction-bank"
    );

    const instructionBkash = document.getElementById(
        "instruction-bkash"
    );

    const instructionNagad = document.getElementById(
        "instruction-nagad"
    );

    const instructionCash = document.getElementById(
        "instruction-cash"
    );

    const instructionOther = document.getElementById(
        "instruction-other"
    );


    if (!paymentMethod || !paymentInstructions) {
        return;
    }


    const instructionBoxes = [
        instructionBank,
        instructionBkash,
        instructionNagad,
        instructionCash,
        instructionOther,
    ];


    function resetInstructions() {

        instructionBoxes.forEach((box) => {

            if (box) {
                box.classList.add("hidden");
            }

        });

    }


    function updatePaymentInstructions() {

        resetInstructions();

        const selectedMethod = paymentMethod.value;

        if (!selectedMethod) {

            paymentInstructions.classList.add("hidden");

            return;
        }


        paymentInstructions.classList.remove("hidden");


        if (selectedMethod === "bank") {
            instructionBank?.classList.remove("hidden");
        }

        else if (selectedMethod === "bkash") {
            instructionBkash?.classList.remove("hidden");
        }

        else if (selectedMethod === "nagad") {
            instructionNagad?.classList.remove("hidden");
        }

        else if (selectedMethod === "cash") {
            instructionCash?.classList.remove("hidden");
        }

        else if (selectedMethod === "other") {
            instructionOther?.classList.remove("hidden");
        }
    }


    paymentMethod.addEventListener(
        "change",
        updatePaymentInstructions
    );


    updatePaymentInstructions();

});



/* =========================================================
   ASOK HERO IMAGE CAROUSEL
========================================================= */

document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.getElementById("hero-carousel");

    if (!carousel) {
        return;
    }

    const slides = carousel.querySelectorAll(".hero-slide");
    const dots = carousel.querySelectorAll(".hero-dot");

    const previousButton = document.getElementById(
        "hero-carousel-prev"
    );

    const nextButton = document.getElementById(
        "hero-carousel-next"
    );

    if (slides.length <= 1) {
        return;
    }

    let currentSlide = 0;
    let autoPlay;


    function showSlide(index) {

        if (index >= slides.length) {
            index = 0;
        }

        if (index < 0) {
            index = slides.length - 1;
        }

        slides.forEach((slide, slideIndex) => {

            if (slideIndex === index) {
                slide.classList.remove("hidden");
                slide.classList.add("block");
            } else {
                slide.classList.remove("block");
                slide.classList.add("hidden");
            }

        });


        dots.forEach((dot, dotIndex) => {

            if (dotIndex === index) {

                dot.classList.remove(
                    "w-2",
                    "bg-white/50"
                );

                dot.classList.add(
                    "w-7",
                    "bg-emerald-400"
                );

            } else {

                dot.classList.remove(
                    "w-7",
                    "bg-emerald-400"
                );

                dot.classList.add(
                    "w-2",
                    "bg-white/50"
                );

            }

        });


        currentSlide = index;
    }


    function nextSlide() {
        showSlide(currentSlide + 1);
    }


    function previousSlide() {
        showSlide(currentSlide - 1);
    }


    function startAutoPlay() {

        stopAutoPlay();

        autoPlay = setInterval(() => {
            nextSlide();
        }, 5000);

    }


    function stopAutoPlay() {

        if (autoPlay) {
            clearInterval(autoPlay);
        }

    }


    if (nextButton) {

        nextButton.addEventListener("click", function () {

            nextSlide();
            startAutoPlay();

        });

    }


    if (previousButton) {

        previousButton.addEventListener("click", function () {

            previousSlide();
            startAutoPlay();

        });

    }


    dots.forEach((dot, index) => {

        dot.addEventListener("click", function () {

            showSlide(index);
            startAutoPlay();

        });

    });


    carousel.addEventListener(
        "mouseenter",
        stopAutoPlay
    );


    carousel.addEventListener(
        "mouseleave",
        startAutoPlay
    );


    carousel.addEventListener(
        "focusin",
        stopAutoPlay
    );


    carousel.addEventListener(
        "focusout",
        startAutoPlay
    );


    showSlide(0);
    startAutoPlay();

});