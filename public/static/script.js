const contactForm = document.querySelector("#contactForm");

const matrixCanvas = document.querySelector("#matrixRain");
const matrixContext = matrixCanvas?.getContext("2d");

if (matrixCanvas && matrixContext) {
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    if (!reducedMotion.matches) {
        const symbols = "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        const streams = [];
        let fontSize = 14;
        let columnGap = 27;
        let animationFrame = 0;
        let lastFrame = 0;
        let running = false;

        const resizeCanvas = () => {
            const pixelRatio = Math.min(window.devicePixelRatio || 1, 1.5);
            const width = window.innerWidth;
            const height = window.innerHeight;
            matrixCanvas.width = Math.floor(width * pixelRatio);
            matrixCanvas.height = Math.floor(height * pixelRatio);
            matrixContext.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
            fontSize = width < 480 ? 12 : 14;
            columnGap = fontSize * 1.1;
            matrixContext.font = `${fontSize}px monospace`;
            streams.length = 0;

            const columns = Math.ceil(width / columnGap);
            for (let column = 0; column < columns; column += 1) {
                streams.push({
                    x: column * columnGap,
                    y: Math.random() * (height / fontSize),
                    speed: 0.4 + Math.random() * 0.8,
                    trail: 9 + Math.floor(Math.random() * 11),
                });
            }
        };

        const drawMatrix = (timestamp) => {
            if (!running) return;
            animationFrame = window.requestAnimationFrame(drawMatrix);
            if (timestamp - lastFrame < 35) return;
            lastFrame = timestamp;

            const width = window.innerWidth;
            const height = window.innerHeight;
            matrixContext.fillStyle = "rgba(2, 0, 5, 0.13)";
            matrixContext.fillRect(0, 0, width, height);
            matrixContext.font = `${fontSize}px monospace`;
            matrixContext.textAlign = "center";
            matrixContext.shadowColor = "#ff2a6d";

            for (const stream of streams) {
                const head = Math.floor(stream.y);
                for (let trail = 0; trail < stream.trail; trail += 1) {
                    const row = head - trail;
                    const y = row * fontSize;
                    if (y < 0 || y > height + fontSize) continue;

                    const character = symbols[Math.floor(Math.random() * symbols.length)];
                    if (trail === 0) {
                        matrixContext.fillStyle = "#fff0f6";
                        matrixContext.shadowBlur = 12;
                    } else {
                        const opacity = Math.max(0.08, 0.82 - trail / stream.trail);
                        matrixContext.fillStyle = `rgba(255, ${Math.floor(35 + opacity * 45)}, ${Math.floor(95 + opacity * 90)}, ${opacity})`;
                        matrixContext.shadowBlur = trail < 3 ? 7 : 0;
                    }
                    matrixContext.fillText(character, stream.x, y);
                }

                stream.y += stream.speed;
                if (stream.y * fontSize - stream.trail * fontSize > height && Math.random() > 0.975) {
                    stream.y = -Math.random() * 12;
                    stream.speed = 0.35 + Math.random() * 0.85;
                }
            }

            matrixContext.shadowBlur = 0;
        };

        const startMatrix = () => {
            if (running || document.hidden) return;
            running = true;
            lastFrame = 0;
            animationFrame = window.requestAnimationFrame(drawMatrix);
        };

        const stopMatrix = () => {
            running = false;
            window.cancelAnimationFrame(animationFrame);
        };

        resizeCanvas();
        window.addEventListener("resize", resizeCanvas, { passive: true });
        document.addEventListener("visibilitychange", () => {
            if (document.hidden) stopMatrix();
            else startMatrix();
        });
        reducedMotion.addEventListener("change", () => {
            if (reducedMotion.matches) stopMatrix();
            else startMatrix();
        });
        window.addEventListener("pagehide", stopMatrix, { once: true });
        startMatrix();
    }
}

if (contactForm) {
    const submitButton = contactForm.querySelector('button[type="submit"]');
    const submitLabel = submitButton.querySelector("span");
    const spinner = submitButton.querySelector(".loading-spinner");
    const formMessage = contactForm.querySelector("#formMessage");

    contactForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (!contactForm.reportValidity()) return;

        submitButton.disabled = true;
        submitLabel.hidden = true;
        spinner.classList.remove("hidden");
        formMessage.className = "form-message";
        formMessage.textContent = "";

        try {
            const response = await fetch(contactForm.action, {
                method: "POST",
                body: new FormData(contactForm),
                headers: { Accept: "application/json" },
            });
            const result = await response.json();

            formMessage.textContent = result.message;
            formMessage.classList.add("is-visible");

            if (!response.ok) {
                formMessage.setAttribute("role", "alert");
                return;
            }

            formMessage.setAttribute("role", "status");
            contactForm.reset();
        } catch {
            formMessage.textContent =
                "Não foi possível conectar ao servidor. Tente novamente ou use o WhatsApp.";
            formMessage.classList.add("is-visible");
            formMessage.setAttribute("role", "alert");
        } finally {
            submitButton.disabled = false;
            submitLabel.hidden = false;
            spinner.classList.add("hidden");
        }
    });
}
