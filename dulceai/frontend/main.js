// DulceAI - Main JavaScript con animaciones GSAP

// Registrar el plugin ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// Variables globales
let tl = gsap.timeline();

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeNavigation();
    initializeMobileMenu();
    initializeProductCards();
    initializeContactForm();
    initializeScrollAnimations();
});

// Función principal de inicialización de animaciones
function initializeAnimations() {
    // Animación de entrada del hero
    tl.from('.hero-title', {
        duration: 1.2,
        y: 100,
        opacity: 0,
        ease: 'power3.out'
    })
    .from('.hero-subtitle', {
        duration: 1,
        y: 50,
        opacity: 0,
        ease: 'power2.out'
    }, '-=0.8')
    .from('.hero-image-container', {
        duration: 1.5,
        scale: 0.8,
        opacity: 0,
        ease: 'back.out(1.7)'
    }, '-=0.6')
    .from('.explore-btn', {
        duration: 1,
        y: 30,
        opacity: 0,
        ease: 'power2.out'
    }, '-=0.4');

    // Animación de pulsación para el botón explorar
    gsap.to('.explore-btn', {
        scale: 1.05,
        duration: 2,
        ease: 'power2.inOut',
        yoyo: true,
        repeat: -1
    });
}

// Función para inicializar la navegación
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                // Animación suave de scroll
                gsap.to(window, {
                    duration: 1,
                    scrollTo: {
                        y: targetSection,
                        offsetY: 80
                    },
                    ease: 'power2.inOut'
                });
            }
        });
    });
}

// Función para inicializar el menú móvil
function initializeMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            const isHidden = mobileMenu.classList.contains('hidden');
            
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
                gsap.fromTo(mobileMenu, 
                    { 
                        opacity: 0, 
                        y: -20,
                        scale: 0.95
                    },
                    { 
                        opacity: 1, 
                        y: 0,
                        scale: 1,
                        duration: 0.3,
                        ease: 'power2.out'
                    }
                );
            } else {
                gsap.to(mobileMenu, {
                    opacity: 0,
                    y: -20,
                    scale: 0.95,
                    duration: 0.3,
                    ease: 'power2.in',
                    onComplete: () => mobileMenu.classList.add('hidden')
                });
            }
        });
    }
    
    // Cerrar menú móvil al hacer clic en un enlace
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
            gsap.to(mobileMenu, {
                opacity: 0,
                y: -20,
                scale: 0.95,
                duration: 0.3,
                ease: 'power2.in',
                onComplete: () => mobileMenu.classList.add('hidden')
            });
        });
    });
}

// Función para inicializar las tarjetas de productos
function initializeProductCards() {
    const productCards = document.querySelectorAll('.product-card');
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    // Animación de hover para las tarjetas
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            gsap.to(this, {
                duration: 0.3,
                y: -10,
                scale: 1.02,
                ease: 'power2.out'
            });
            
            gsap.to(this.querySelector('.product-image'), {
                duration: 0.3,
                scale: 1.1,
                ease: 'power2.out'
            });
        });
        
        card.addEventListener('mouseleave', function() {
            gsap.to(this, {
                duration: 0.3,
                y: 0,
                scale: 1,
                ease: 'power2.out'
            });
            
            gsap.to(this.querySelector('.product-image'), {
                duration: 0.3,
                scale: 1,
                ease: 'power2.out'
            });
        });
    });
    
    // Animación para botones de agregar al carrito
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Animación de click
            gsap.to(this, {
                duration: 0.1,
                scale: 0.95,
                yoyo: true,
                repeat: 1,
                ease: 'power2.inOut'
            });
            
            // Simular agregado al carrito
            this.classList.add('clicked');
            this.textContent = 'Agregado ✓';
            
            // Mostrar notificación
            showNotification('¡Producto agregado al carrito!', 'success');
            
            // Resetear después de 2 segundos
            setTimeout(() => {
                this.classList.remove('clicked');
                this.textContent = 'Agregar al carrito';
            }, 2000);
        });
    });
}

// Función para inicializar el formulario de contacto
function initializeContactForm() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Animación de envío
            const submitButton = this.querySelector('button[type="submit"]');
            gsap.to(submitButton, {
                duration: 0.2,
                scale: 0.95,
                yoyo: true,
                repeat: 1,
                ease: 'power2.inOut'
            });
            
            // Simular envío
            setTimeout(() => {
                showNotification('¡Mensaje enviado correctamente!', 'success');
                this.reset();
            }, 500);
        });
        
        // Animación de focus para inputs
        const inputs = contactForm.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                gsap.to(this, {
                    duration: 0.3,
                    scale: 1.02,
                    ease: 'power2.out'
                });
            });
            
            input.addEventListener('blur', function() {
                gsap.to(this, {
                    duration: 0.3,
                    scale: 1,
                    ease: 'power2.out'
                });
            });
        });
    }
}

// Función para inicializar animaciones de scroll
function initializeScrollAnimations() {
    // Animación para la sección de productos
    gsap.fromTo('.productos-title', {
        opacity: 0,
        y: 50
    }, {
        opacity: 1,
        y: 0,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '.productos-title',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
    
    gsap.fromTo('.productos-subtitle', {
        opacity: 0,
        y: 30
    }, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '.productos-subtitle',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
    
    // Animación escalonada para las tarjetas de productos
    gsap.fromTo('.product-card', {
        opacity: 0,
        y: 50,
        scale: 0.9
    }, {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.8,
        ease: 'power2.out',
        stagger: 0.2,
        scrollTrigger: {
            trigger: '.product-card',
            start: 'top 85%',
            end: 'bottom 15%',
            toggleActions: 'play none none reverse'
        }
    });
    
    // Animación para la sección "Sobre Nosotros"
    gsap.fromTo('.sobre-title', {
        opacity: 0,
        x: -50
    }, {
        opacity: 1,
        x: 0,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '.sobre-title',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
    
    gsap.fromTo('.sobre-text', {
        opacity: 0,
        y: 30
    }, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: 'power2.out',
        stagger: 0.3,
        scrollTrigger: {
            trigger: '.sobre-text',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
    
    gsap.fromTo('.sobre-image', {
        opacity: 0,
        x: 50,
        scale: 0.9
    }, {
        opacity: 1,
        x: 0,
        scale: 1,
        duration: 1.2,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '.sobre-image',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
    
    // Animación para la sección de contacto
    gsap.fromTo('.contacto-title', {
        opacity: 0,
        y: 50
    }, {
        opacity: 1,
        y: 0,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '.contacto-title',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
    
    gsap.fromTo('.contacto-subtitle', {
        opacity: 0,
        y: 30
    }, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '.contacto-subtitle',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
    
    gsap.fromTo('#contact-form', {
        opacity: 0,
        y: 50,
        scale: 0.95
    }, {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '#contact-form',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <span class="text-lg">${type === 'success' ? '✓' : 'ℹ'}</span>
            <span>${message}</span>
        </div>
    `;
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Animación de entrada
    gsap.fromTo(notification, {
        x: 400,
        opacity: 0
    }, {
        x: 0,
        opacity: 1,
        duration: 0.5,
        ease: 'power2.out'
    });
    
    // Remover después de 3 segundos
    setTimeout(() => {
        gsap.to(notification, {
            x: 400,
            opacity: 0,
            duration: 0.3,
            ease: 'power2.in',
            onComplete: () => notification.remove()
        });
    }, 3000);
}

// Función para crear efecto de partículas (opcional)
function createParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    particlesContainer.style.position = 'fixed';
    particlesContainer.style.top = '0';
    particlesContainer.style.left = '0';
    particlesContainer.style.width = '100%';
    particlesContainer.style.height = '100%';
    particlesContainer.style.pointerEvents = 'none';
    particlesContainer.style.zIndex = '1';
    
    document.body.appendChild(particlesContainer);
    
    // Crear partículas
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 3 + 4) + 's';
        particlesContainer.appendChild(particle);
    }
}

// Función para inicializar efectos especiales
function initializeSpecialEffects() {
    // Crear efecto de partículas en el hero
    const heroSection = document.querySelector('#home');
    if (heroSection) {
        createParticles();
    }
}

// Función para manejar el scroll suave
function smoothScrollTo(target) {
    gsap.to(window, {
        duration: 1,
        scrollTo: {
            y: target,
            offsetY: 80
        },
        ease: 'power2.inOut'
    });
}

// Función para detectar dispositivos móviles
function isMobile() {
    return window.innerWidth <= 768;
}

// Función para optimizar animaciones en móviles
function optimizeForMobile() {
    if (isMobile()) {
        // Reducir duración de animaciones en móviles
        gsap.globalTimeline.timeScale(1.2);
        
        // Desactivar algunas animaciones complejas en móviles
        gsap.set('.particle', { display: 'none' });
    }
}

// Inicializar optimizaciones para móviles
window.addEventListener('resize', optimizeForMobile);
optimizeForMobile();

// Exportar funciones para uso global si es necesario
window.DulceAI = {
    showNotification,
    smoothScrollTo,
    isMobile
};



