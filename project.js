document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("recommendation-form");
    const recommendationsContainer = document.getElementById("recommendations-container");
    const recommendationsList = document.getElementById("recommendations-list");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // Prevent form from refreshing the page
        const userId = document.getElementById("user-id").value;

        try {
            const response = await fetch("/recommend", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ user_id: userId })
            });

            const result = await response.json();

            if (result.recommendations) {
                recommendationsList.innerHTML = ""; // Clear previous results
                result.recommendations.forEach(movie => {
                    const li = document.createElement("li");
                    li.textContent = movie;
                    recommendationsList.appendChild(li);
                });
            } else if (result.error) {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            alert("An error occurred while fetching recommendations.");
            console.error(error);
        }
    });
});
