document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("training-form");
    const goalSelect = document.getElementById("goal");
    const tipsSection = document.getElementById("customized-tips");

    const trainingTips = {
        obedience: [
            "Obedience training is about consistency.",
            "Use positive reinforcement and ensure sessions are short and engaging."
        ],
        behavioral: [
            "Behavioral training focuses on correcting unwanted habits.",
            "Reward good behavior and redirect negative actions."
        ],
        agility: [
            "Agility training requires patience and energy.",
            "Start with simple obstacles and gradually increase difficulty."
        ],
        "potty-training": [
            "Take your pet outside frequently, especially after meals.",
            "Praise them for going to the correct spot."
        ],
        "leash-walking": [
            "Teach leash walking by stopping when your pet pulls.",
            "Reward them when they stay beside you."
        ],
        socialization: [
            "Expose your pet to various environments and people.",
            "Reward calm behavior and avoid overwhelming situations."
        ],
        "trick-training": [
            "Teach fun tricks like 'sit' and 'shake' using treats and a clicker.",
            "Keep sessions exciting and reward success."
        ],
        "puppy-training": [
            "Focus on basic commands, potty training, and socialization.",
            "Use positive reinforcement and patience."
        ]
    };

    form.addEventListener("submit", (e) => {
        e.preventDefault(); // Prevent page reload

        const selectedGoal = goalSelect.value;
        const tipsMessage = trainingTips[selectedGoal];

        // Clear the previous content
        const tipsContainer = tipsSection.querySelector("p");
        tipsContainer.innerHTML = ""; // Clear any previous tips

        if (tipsMessage) {
            // Generate tips as points
            const ul = document.createElement("ul");
            tipsMessage.forEach(tip => {
                const li = document.createElement("li");
                li.textContent = tip;
                ul.appendChild(li);
            });
            tipsContainer.appendChild(ul);
        } else {
            tipsContainer.textContent = "No tips available for this training goal.";
        }

        // Add a slight highlight effect when the text updates
        tipsSection.classList.add("highlight");
        setTimeout(() => {
            tipsSection.classList.remove("highlight");
        }, 1000);
    });
});
