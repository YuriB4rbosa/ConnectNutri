// Mobile menu toggle
(function () {
  const mobileMenuBtn = document.querySelector(".mobile-menu-btn");
  const nav = document.querySelector(".nav");

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener("click", () => {
      mobileMenuBtn.classList.toggle("active");
      nav.classList.toggle("nav--active");
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
        // Close mobile menu if open
        if (nav && nav.classList.contains("nav--active")) {
          nav.classList.remove("nav--active");
          if (mobileMenuBtn) mobileMenuBtn.classList.remove("active");
        }
      }
    });
  });
})();

// Form submission handler with AJAX
(function () {
  const form = document.getElementById("appointmentForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const submitBtn = document.getElementById("submitBtn");
      const btnText = submitBtn.querySelector(".btn__text");
      const btnLoading = submitBtn.querySelector(".btn__loading");

      // Show loading state
      btnText.style.display = "none";
      btnLoading.style.display = "inline";
      submitBtn.disabled = true;

      // Get form data
      const formData = new FormData(form);

      try {
        // Send data to server
        const response = await fetch(form.action, {
          method: "POST",
          body: formData,
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const result = await response.json();

        if (result.success) {
          // 1. Pegar dados
          const nome = formData.get("nome");
          const whatsapp = formData.get("whatsapp");
          const objetivo = formData.get("objetivo");

          // 2. Montar mensagem
          const message = `Olá Taynara! Me chamo ${nome} e gostaria de agendar uma consulta.\n\n*Objetivo:* ${objetivo}\n*WhatsApp:* ${whatsapp}\n\nVamos conversar?`;
          const encodedMessage = encodeURIComponent(message);
          const whatsappUrl = `https://wa.me/5561993324869?text=${encodedMessage}`;

          // 3. Resetar formulário
          form.reset();

          // 4. LÓGICA HÍBRIDA (PC vs CELULAR)
          const isMobile = /iPhone|iPad|iPod|Android/i.test(
            navigator.userAgent,
          );

          if (isMobile) {
            // No celular, redireciona na mesma aba para forçar a abertura do App
            window.location.assign(whatsappUrl);
          } else {
            // No PC, abre em uma nova aba para não fechar o seu site
            window.open(whatsappUrl, "_blank");
          }
        } else {
          alert("❌ Erro: " + result.message);
        }
      } catch (error) {
        console.error("Error:", error);
        alert("❌ Erro ao enviar formulário. Tente novamente.");
      } finally {
        // Reset button
        btnText.style.display = "inline";
        btnLoading.style.display = "none";
        submitBtn.disabled = false;
      }
    });
  }
})();

// Add scroll effect to header
(function () {
  const header = document.querySelector(".header");

  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 100) {
      header.style.background = "rgba(255, 255, 255, 0.98)";
      header.style.boxShadow = "var(--shadow-md)";
    } else {
      header.style.background = "rgba(255, 255, 255, 0.98)";
      header.style.boxShadow = "var(--shadow-sm)";
    }
  });
})();
