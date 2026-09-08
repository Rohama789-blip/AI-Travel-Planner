const form = document.getElementById("travel-form");
const chips = document.querySelectorAll(".chip");
const loadingEl = document.getElementById("loading");
const placeholderEl = document.getElementById("placeholder");
const resultSingle = document.getElementById("result-single");
const resultCompare = document.getElementById("result-compare");
const itineraryText = document.getElementById("itinerary-text");
const techniqueBadge = document.getElementById("technique-badge");
const compareBtn = document.getElementById("compare-btn");

let selectedInterests = [];

chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    chip.classList.toggle("selected");
    const value = chip.dataset.value;
    if (chip.classList.contains("selected")) {
      selectedInterests.push(value);
    } else {
      selectedInterests = selectedInterests.filter((v) => v !== value);
    }
  });
});

function getFormData() {
  return {
    name: document.getElementById("name").value,
    destination: document.getElementById("destination").value,
    days: parseInt(document.getElementById("days").value, 10),
    budget: parseFloat(document.getElementById("budget").value),
    interests: selectedInterests,
    travel_style: document.getElementById("travel_style").value,
  };
}

function showLoading() {
  placeholderEl.classList.add("hidden");
  resultSingle.classList.add("hidden");
  resultCompare.classList.add("hidden");
  loadingEl.classList.remove("hidden");
}

function hideLoading() {
  loadingEl.classList.add("hidden");
}

const TECHNIQUE_LABELS = {
  zero_shot: "Zero-Shot",
  few_shot: "Few-Shot",
  structured_reasoning: "Structured Reasoning",
};

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const technique = document.querySelector('input[name="technique"]:checked').value;
  const payload = { ...getFormData(), technique };

  if (payload.interests.length === 0) {
    alert("Please select at least one interest.");
    return;
  }

  showLoading();

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    hideLoading();
    techniqueBadge.textContent = TECHNIQUE_LABELS[data.technique] || data.technique;
    itineraryText.textContent = data.itinerary;
    resultSingle.classList.remove("hidden");
    resultCompare.classList.add("hidden");
  } catch (err) {
    hideLoading();
    placeholderEl.textContent = "Something went wrong: " + err.message;
    placeholderEl.classList.remove("hidden");
  }
});

compareBtn.addEventListener("click", async () => {
  const payload = { ...getFormData(), technique: "zero_shot" }; // technique field required but unused by /generate-all

  if (!payload.name || !payload.destination || !payload.days || !payload.budget) {
    alert("Please fill in the traveler details first.");
    return;
  }
  if (payload.interests.length === 0) {
    alert("Please select at least one interest.");
    return;
  }

  showLoading();

  try {
    const res = await fetch("/generate-all", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    hideLoading();
    resultCompare.innerHTML = "";
    Object.entries(data.results).forEach(([technique, text]) => {
      const col = document.createElement("div");
      col.className = "compare-col";
      col.innerHTML = `<h3>${TECHNIQUE_LABELS[technique] || technique}</h3><pre></pre>`;
      col.querySelector("pre").textContent = text;
      resultCompare.appendChild(col);
    });
    resultCompare.classList.remove("hidden");
    resultSingle.classList.add("hidden");
  } catch (err) {
    hideLoading();
    placeholderEl.textContent = "Something went wrong: " + err.message;
    placeholderEl.classList.remove("hidden");
  }
});
