// ===============================
// Animated Counter
// ===============================

const counters = document.querySelectorAll(".card h2");

counters.forEach(counter => {

    const target = Number(counter.innerText);

    let count = 0;

    const speed = Math.max(1, Math.ceil(target / 50));

    function updateCounter() {

        if (count < target) {

            count += speed;

            if (count > target)
                count = target;

            counter.innerText = count;

            requestAnimationFrame(updateCounter);

        }

    }

    updateCounter();

});


// ===============================
// Fade In Animation
// ===============================

window.addEventListener("load", () => {

    document.querySelectorAll(".card").forEach((card, index) => {

        card.style.opacity = "0";

        card.style.transform = "translateY(40px)";

        setTimeout(() => {

            card.style.transition = "0.6s ease";

            card.style.opacity = "1";

            card.style.transform = "translateY(0)";

        }, index * 150);

    });

});


// ===============================
// Active Sidebar
// ===============================

const menuItems = document.querySelectorAll(".sidebar ul li");

menuItems.forEach(item => {

    item.addEventListener("click", () => {

        menuItems.forEach(i => i.classList.remove("active"));

        item.classList.add("active");

    });

});


// ===============================
// Chart
// ===============================

const ctx = document.getElementById("statusChart");

if (ctx) {

    new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: [

                "Open",

                "Evaluation",

                "Completed"

            ],

            datasets: [

                {

                    data: [8, 5, 2],

                    backgroundColor: [

                        "#3B82F6",

                        "#06B6D4",

                        "#10B981"

                    ],

                    borderWidth: 0

                }

            ]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: "white",

                        font: {

                            size: 14

                        }

                    }

                }

            }

        }

    });

}