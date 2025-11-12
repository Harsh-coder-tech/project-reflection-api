const API_BASE = "https://project-reflection-api.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
  loadQuestions();
  loadResponses();
});

async function loadQuestions() {
  const container = document.getElementById("questions");
  container.innerHTML = "<p>Loading questions...</p>";

  try {
    const res = await fetch(`${API_BASE}/questions`);
    const questions = await res.json();
    container.innerHTML = "";

    questions.forEach(q => {
      const div = document.createElement("div");
      div.className = "question";
      div.innerHTML = `
        <strong>${sanitize(q.question)}</strong>
        <textarea id="answer-${q.id}" placeholder="Write your answer here..."></textarea>
        <button onclick="submitAnswer(${q.id}, this)">Submit</button>
      `;
      container.appendChild(div);
    });
  } catch (error) {
    container.innerHTML = "<p>Failed to load questions.</p>";
    console.error(error);
  }
}

async function submitAnswer(id, button) {
  const textarea = document.getElementById(`answer-${id}`);
  const your_answer = textarea.value.trim();
  const username = prompt("Enter your name:")?.trim();

  if (!your_answer || !username) {
    alert("Please enter both your name and answer.");
    return;
  }

  button.disabled = true;
  button.textContent = "Submitting...";

  try {
    const res = await fetch(`${API_BASE}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question_id: id,
        your_answer,
        username
      })
    });

    const data = await res.json();

    if (res.ok) {
      showResponse(data.response);
      textarea.value = "";
      alert("Response submitted successfully!");
    } else {
      alert(data.error || "Submission failed.");
    }
  } catch (error) {
    alert("Submission failed due to a network error.");
    console.error(error);
  } finally {
    button.disabled = false;
    button.textContent = "Submit";
  }
}

function showResponse(response) {
  const container = document.getElementById("responses");
  const div = document.createElement("div");
  div.className = "response";
  div.innerHTML = `
    <strong>User:</strong> ${sanitize(response.user)}<br/>
    <strong>Q:</strong> ${sanitize(response.question)}<br/>
    <strong>Your Answer:</strong> ${sanitize(response.your_answer)}
  `;
  container.appendChild(div);
}

async function loadResponses() {
  const container = document.getElementById("responses");
  container.innerHTML = "<p>Loading responses...</p>";

  try {
    const res = await fetch(`${API_BASE}/responses`);
    const responses = await res.json();
    container.innerHTML = "";

    responses.forEach(r => showResponse(r));
  } catch (error) {
    container.innerHTML = "<p>Failed to load responses.</p>";
    console.error(error);
  }
}

function sanitize(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
