document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".crop-form[action*='recommend']");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    clearMessages(form);
    let valid = true;
    form.querySelectorAll("[required]").forEach((field) => {
      if (!field.value.trim()) {
        valid = false;
        markInvalid(field, validationMessage("required"));
      }
    });

    const area = form.querySelector("[name='land_area']");
    if (area && area.value) {
      const value = Number(area.value);
      if (!Number.isFinite(value) || value <= 0 || value > 10000) {
        valid = false;
        markInvalid(area, validationMessage("area"));
      }
    }

    if (!valid) {
      event.preventDefault();
      return;
    }

    const loading = form.querySelector(".loading");
    if (loading) loading.classList.add("is-active");
  });
});

function markInvalid(field, message) {
  field.classList.add("field-error");
  const note = document.createElement("span");
  note.className = "input-message";
  note.textContent = message;
  field.insertAdjacentElement("afterend", note);
}

function clearMessages(form) {
  form.querySelectorAll(".field-error").forEach((field) => field.classList.remove("field-error"));
  form.querySelectorAll(".input-message").forEach((message) => message.remove());
}

function validationMessage(key) {
  const language = localStorage.getItem("smartCropLanguage") || "en";
  const messages = {
    en: {
      required: "This field is required.",
      area: "Enter an area between 0.01 and 10,000 acres.",
    },
    ta: {
      required: "இந்த புலம் அவசியம்.",
      area: "0.01 முதல் 10,000 ஏக்கர் வரை நிலப்பரப்பை உள்ளிடவும்.",
    },
  };
  return messages[language]?.[key] || messages.en[key];
}
