document.addEventListener('DOMContentLoaded', () => {
    // Initialize Swiper (Vertical)
    const swiper = new Swiper('.swiper', {
        direction: 'vertical',
        slidesPerView: 1,
        spaceBetween: 0,
        mousewheel: true,
        keyboard: {
            enabled: true,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        speed: 800,
        effect: 'slide',
        on: {
            init: function () {
                animateSlide(this.slides[this.activeIndex]);
                updateCounter(this.activeIndex + 1, this.slides.length);
            },
            slideChangeTransitionStart: function () {
                // Hide elements in the previous active slide to re-animate them later
                const previousSlide = this.slides[this.previousIndex];
                if(previousSlide) {
                    gsap.set(previousSlide.querySelectorAll('.anim-elem'), { opacity: 0, y: 30 });
                    gsap.set(previousSlide.querySelectorAll('.anim-img'), { opacity: 0, scale: 0.8 });
                }
            },
            slideChangeTransitionEnd: function () {
                animateSlide(this.slides[this.activeIndex]);
                updateCounter(this.activeIndex + 1, this.slides.length);
            }
        }
    });

    // Function to animate elements in the active slide using GSAP
    function animateSlide(slide) {
        if (!slide) return;
        
        const tl = gsap.timeline();
        
        // Ensure initial state
        gsap.set(slide.querySelectorAll('.anim-elem'), { opacity: 0, y: 30 });
        gsap.set(slide.querySelectorAll('.anim-img'), { opacity: 0, scale: 0.8 });
        
        // Animate text elements (title, subtitle, list items, cards)
        tl.to(slide.querySelectorAll('.anim-elem'), {
            opacity: 1,
            y: 0,
            duration: 0.6,
            stagger: 0.1,
            ease: 'power3.out'
        });

        // Animate images
        tl.to(slide.querySelectorAll('.anim-img'), {
            opacity: 1,
            scale: 1,
            duration: 0.6,
            ease: 'back.out(1.2)'
        }, "-=0.4");
    }

    // Function to update the slide counter
    function updateCounter(current, total) {
        const counterEl = document.querySelector('.current-slide');
        const totalEl = document.querySelector('.total-slides');
        if(counterEl && totalEl) {
            counterEl.textContent = current;
            totalEl.textContent = total;
        }
        
        // Hide scroll indicator on the last slide
        const scrollIndicator = document.querySelector('.scroll-indicator');
        if(scrollIndicator) {
            if(current === total) {
                scrollIndicator.style.display = 'none';
            } else {
                scrollIndicator.style.display = 'flex';
            }
        }
    }
});
