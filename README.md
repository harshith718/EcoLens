EcoLens

EcoLens is an ecological simulation engine designed to model species interactions, population dynamics, and environmental pressures over time. It enables users to simulate predator–prey systems, carrying capacity limits, food availability, and adaptive population responses in a simplified virtual ecosystem.

This project is part of your 6-project computational evolution portfolio and stands as the ecological-dynamics module of the suite.

🧩 Features

Simulates multi-species interactions (predator–prey, resource competition)

Models population growth using logistic, exponential, or custom rules

Environment-driven variation (food levels, habitat constraints)

Tracks population curves for every generation

Generates visual plots (population over time, resource availability curves)

Extensible modular code (ecosystem engine, species definitions, plotting utilities)

📁 Project Structure
ecolens/
│
├── code/
│   ├── ecolens_engine.py         # Core simulation engine
│   ├── species.py                # Species definitions and interactions
│   ├── environment.py            # Environmental parameters (food, resources)
│   ├── run_ecolens.py            # Main script to run the full simulation
│   └── helper_functions.py       # Utility functions used by the engine
│
├── graphs/
│   ├── population_curve.png      # Population size over generations
│   ├── predator_prey_plot.png    # Interaction dynamics graph
│   └── resources_over_time.png   # Environmental resource trend
│
└── logs/
    ├── ecolens_log.json          # All generations recorded
    └── best_population.txt       # Summary of strongest stable configuration

🚀 How to Run
1️⃣ Install requirements

If required:

pip install matplotlib numpy

2️⃣ Run the simulation
python run_ecolens.py

3️⃣ Outputs generated

Graphs in the graphs/ folder

Simulation logs in the logs/ folder

Printed summary in terminal

🔬 Example Output (Explained)

Population Curve → shows how predator and prey populations rise and fall

Predator-Prey Plot → cycle dynamics (Lotka-Volterra–like patterns)

Resource Plot → food/resource levels changing with consumption

🧠 Concepts Modeled

Logistic population growth

Predator–prey feedback loops

Resource depletion & regeneration

Survival pressure

Stability vs collapse of ecosystems

📌 Use Cases

EcoLens is especially useful for:

Understanding ecological stability

Simulating interventions (increase food, remove predators, etc.)

Studying how small changes affect entire ecosystems

Visualizing population dynamics for research or teaching

📜 License

This project is part of a personal research portfolio and is free to use for educational and non-commercial purposes.
