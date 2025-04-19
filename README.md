# Thronglets Simulation

A biologically-inspired AI simulation exploring emergent behavior in a virtual environment, inspired by *Black Mirror* Season 7, Episode 4: "Plaything" (2025). Creatures called **Thronglets** evolve, socialize, and adapt to environmental challenges like fire and rockfalls over hundreds of generations.

## 📦 Features

- **Dynamic Evolution:** Mutation-driven genetic evolution across generations
- **Social Relationships:** Thronglets form relationships, build groups, and develop social structures
- **Environmental Hazards:** Fire and rock events threaten survival
- **Grid-based Movement:** Real-time movement and interaction over a 2D grid
- **Emergent Behavior:** Watch intelligence and cooperation evolve under pressure
- **Data Logging:** JSON-based logs of all generations, including config snapshots
- **HTML Viewer:** View simulation history in an interactive HTML5 canvas

---

## 🧠 Algorithms and Mechanics

### Genetic Evolution
Each Thronglet has traits like `hp`, `speed`, `detection_range`, and `avoidance_speed`. Survivors pass their genes to offspring with a configurable `mutation_chance`.

### Relationship Dynamics
Thronglets detect nearby peers using `detection_range`. Repeated interaction strengthens or weakens relationship scores (0–10). Strong bonds lead to group formation.

### Group Formation
If a Thronglet has high scores (≥7) with neighbors, they form a **group**. Groups are tracked and visualized with IDs.

### Movement and Avoidance
Thronglets attempt to avoid recent "danger" areas—where other Thronglets died or where fire/rocks appeared.

### Environment Events
- **Fire Events:** Radius-based random events that reduce HP
- **Rock Events:** Radius-based impacts that instantly kill

---

## ⚙️ Configuration
Set simulation parameters in `config.json`:

```json
{
  "grid_width":100,
  "grid_height":100,
  "generations":200,
  "max_population":0,
  "population_size":200,
  "ticks_per_generation":30,
  "fire_event_chance":0.5,
  "rock_event_chance":0.2,
  "fire_event_radius":2,
  "rock_event_radius":1,
  "fire_event_max_damage":20,
  "mutation_chance":0.1,
  "logs_directory":"logs"
}
```

---

## 🕹️ Viewer
Run the simulation and open `viewer.html` in a browser. Load the `logs.zip` to visualize the simulation. Features include:

- Playback slider and animation
- Canvas-based cell grid
- Hover for Thronglet stats
- Fire/Rock visualization
- Group and relationship displays

---

## 🚀 Run the Simulation
Run from terminal:

```bash
python simulation.py
```

Zip logs are automatically created. Open them in the viewer.

---

## 📁 Log Output
Each generation is saved in `logs/` as `generation_X.json`.
Other files include:

- `final_state.json`: End-of-sim snapshot
- `final_config.json`: Final config used
- `fires.json`, `rocks.json`: Event coordinates per generation

---

## 📜 License
This project is open for research and educational purposes. Created by humans. Inspired by fiction.

MIT License

Copyright (c) 2025 triple7inc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 💡 Inspiration
"Thronglets" is a nod to *Black Mirror* S07E04 "Plaything" (2025), where emergent life simulations reveal unpredictable intelligence. We asked: what if evolution ran faster?
