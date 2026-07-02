# Tel-Spartan Gears — Baseball Trebuchet Arena

A 3D physics simulation of a robotic trebuchet that launches baseballs at a target board with 12 holes. Features an evolutionary AI that learns to hit all targets, a validation system to verify reliability, and a head-to-head competition mode.

## Quick Start

```bash
python server.py
```

Then open [http://localhost:8765](http://localhost:8765) (training), [http://localhost:8765/validate.html](http://localhost:8765/validate.html) (validation), or [http://localhost:8765/competition.html](http://localhost:8765/competition.html) (competition).

Or double-click `start.bat` (training), `start_validate.bat` (validation), or `start_competition.bat` (competition).

## Keyboard Shortcuts

### Training Arena (`index.html`)

| Key | Action |
|---|---|
| **W** | Drive forward (increase posZ) |
| **S** | Drive backward (decrease posZ) |
| **A** | Rotate heading left |
| **D** | Rotate heading right |
| **↑ / ↓ / ← / →** | Arrow key equivalents for W/A/S/D |
| **Space** | Fire trebuchet |
| **R** | Reset simulation |
| **Shift+T** | Top camera view |
| **Shift+S** | Side camera view |

### Validation Arena (`validate.html`)

| Key | Action |
|---|---|
| **W** | Drive forward (increase posZ) |
| **S** | Drive backward (decrease posZ) |
| **A** | Rotate heading left |
| **D** | Rotate heading right |
| **↑ / ↓ / ← / →** | Arrow key equivalents for W/A/S/D |
| **Space** | Fire trebuchet |
| **R** | Reset simulation |
| **Shift+T** | Top camera view |
| **Shift+S** | Side camera view |

### Competition Arena (`competition.html`)

| Key | Action |
|---|---|
| **W / ↑** | Drive robot forward |
| **S / ↓** | Drive robot backward |
| **A / ←** | Rotate heading left |
| **D / →** | Rotate heading right |
| **Space** | Start match (WAITING) / Fire player robot (match) |
| **R** | Full reset |
| **Shift+T** | Top camera view |
| **Shift+S** | Side camera view |
| **1** | Default camera view |

## Training Arena (`index.html`)

Manual and AI-powered training sim. The robot arm fires a baseball at a 3m × 3.4m board 7.5m away with 12 holes (9 standard + 3 bonus).

### GUI Controls

| Folder | Parameters |
|---|---|
| **Position & Heading** | Pos X (-1.8–1.8m), Pos Z (0.5–4.5m), Heading (±180°) |
| **Mechanism** | Pivot Height, Lever Load, Lever CW lengths, Motor Torque (5–200 Nm) |
| **Projectile & Release** | Release Angle (30–100°) |
| **Robot Mass** | Arm Mass (1–15kg), Base Mass (1–15kg), max 30kg total |

### AI Training

| Button | Action |
|---|---|
| **AI ⚡** | Start/Resume or Stop the evolutionary AI |
| **▶ Fresh Start** | Begin a new run from scratch |
| **↻ Resume Saved** | Continue from previous training data |
| **■ STOP** | Stop AI, apply best params to sim |
| **💾 Export CSV** | Download all trial data |
| **📂 Import CSV** | Restore training memory from a previous export |
| **📨 Suggest to AI** | Seed current settings into the AI population |
| **🗑 Wipe Data** | Clear all accumulated training data |

### AI Strategy

- **Progressive per-target training** — trains on one hole at a time (center out, easiest to hardest)
- **Population**: 6 individuals, 2 elites, 8 trials per individual
- **Mutation**: Directional mutation biased by where the ball missed (dz, dx, dy)
- **KNN acceleration**: Uses all past trials to guide mutation toward high-performing regions
- **Param avoidance**: Learns which parameter regions produce poor results and avoids them
- **Fitness**: `simAcc × 0.55 + physicsScore × 0.2 + trajectoryAcc × 0.25 + proximityBonus − avoidance penalty + KNN bonus`

### Diagnostics

| Feature | Description |
|---|---|
| **📊 Show Chart** | 2D top-down scatter plot of all landing positions |
| **🛤 3D Trajectories** | Interactive 3D viewer of past 500 ball trajectories |
| Status bar | Real-time: generation, individual, trials, predicted range, best fitness, avg trajectory error, proximity, per-target hit counts |

## Validation Arena (`validate.html`)

Automated testing of parameter sets to find configurations that **reliably** hit each target.

### Validation Levels (half-life decay)

| Level | Trials per target |
|---|---|
| 0 | 100 → 95% required |
| 1 | 50 |
| 2 | 25 |
| 3 | 12 |
| 4 | 6 |
| 5 | 3 |

### Workflow

1. **Load from Memory** — imports trained sets from the training arena (localStorage)
2. **Import CSV** — or load sets from a CSV file
3. **Start** — runs each parameter set against every target, applying small trial noise
4. **Advance** — when all targets pass, level increases (fewer trials needed)
5. **Pass** — a target validated at all 6 levels is considered reliably solved

### Hit Detection

Hits use a physics-based deflection model:

| Result | Condition | Visual |
|---|---|---|
| **Clean** | Ball center fully within `r_hole − r_ball` | Green glow |
| **Deflect in** | Edge collision, velocity carries ball through | Orange glow |
| **Bounce out** | Edge collision, ball deflects away | Red flash |

Proximity (0–1) is tracked per trial and displayed in results.

## Competition Arena (`competition.html`)

Head-to-head 1v1 match simulation between the player's robot (blue) and a rival AI robot (red), each with 27 baseballs per half.

### Match Structure

| Phase | Duration | Description |
|---|---|---|
| **WAITING** | 5s countdown | Robots in starting boxes, configure position |
| **FIRST_HALF** | 3:00 | AI-driven navigation to launch position |
| **SECOND_HALF** | 3:00 | 1v1 match — both robots fire autonomously (WASD manual override available) |
| **ENDED** | — | Final scores displayed |

### Rules

- Each robot starts with **27 balls** in the first half, **refilled to 27** at the start of the second half
- **Designated Target Bonus**: A random target (t9/t10/t11) glows red for 60s at the start of each half — hitting it scores 2× points
- Players can drive manually during both halves using **WASD / Arrow keys** (overrides AI navigation)
- **Space** fires the player robot once positioned
- First half: AI only (both robots navigate and fire autonomously)
- Second half: Full 1v1 with both robots firing; player can manually reposition with WASD

### Player Robot Controls

| Control | Action |
|---|---|
| **WASD / Arrows** | Drive robot forward/backward/rotate |
| **Space** | Start match / Fire at target |
| **R** | Full reset to WAITING |
| **T / S / 1** | Camera views (Top, Side, Default) |
| **GUI** | Position, heading, mechanism, mass sliders |

### Scoring

- **Standard hit**: 1 point
- **Bonus target hit** (within first 60s of half): 2 points
- Match winner determined by total points after both halves

## Physics Model

- **Engine**: [Cannon-es](https://github.com/pmndrs/cannon-es) physics + [Three.js](https://threejs.org) rendering
- **Arm**: Motor-driven hinge constraint with configurable torque
- **Projectile**: 0.035m radius baseball (0.03kg)
- **Trajectory prediction**: Energy-based analytical model shared between training and validation
- **Motor cap**: ω capped at 30 rad/s (physical motor limit)

## Project Structure

```
sim/
├── index.html              Training arena
├── validate.html           Validation arena
├── competition.html        Head-to-head competition arena
├── server.py               Python HTTP server (port 8765)
├── start.bat               Launch training
├── start_validate.bat      Launch validation
├── models/                 3D GLB models (robot arm, base)
├── .gitignore
└── README.md
```

## Requirements

- Python 3.x (for the server)
- A modern browser (Chrome, Firefox, Edge)
