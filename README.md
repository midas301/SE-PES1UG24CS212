# Zombie Escape

Top-down wave survival shooter — WASD to move, click to shoot zombies.

## Getting Started

This game uses **pygame**. Install it before running:

```bash
pip install pygame-ce
python game.py
```

> **Note:** If you are on Python 3.12 or newer, use `pygame-ce` (Community Edition) instead of `pygame`. It is a drop-in replacement with the same API.


## Controls

| Key | Action |
|-----|--------|
| W/A/S/D | Move |
| Left Click | Shoot toward cursor |
| R | Restart |

## Before changing the code

Play several waves and observe how zombies spawn, move, and are killed. Trace the shooting logic from click event through `Player` to bullet collision. Understand wave progression and how score and kill counters interact before making any modifications.

## Task 1 — Health System

Give the player 3 HP. One zombie touch subtracts 1 HP; the game ends only when HP reaches 0. Add a brief invincibility window after each hit to prevent instant death. Show HP in the HUD.

**Done when:** the player survives multiple zombie touches, the invincibility window is visible, and the game over screen appears only at 0 HP.

## Task 2 — Ammo System

Limit the player to 12 bullets per clip. Prevent shooting when empty and trigger a reload that takes 2 seconds before ammo is restored. Display ammo count in the HUD.

**Done when:** shooting is blocked at 0 ammo, a reload timer counts down correctly, and ammo is restored only after the full reload duration.

## Task 3 — Explosive Barrel

Place 4 barrels on the map. A bullet hitting a barrel triggers an explosion that destroys all zombies within a fixed radius. Remove the barrel after it explodes.

**Done when:** barrels are visible on the map, a bullet collision triggers the explosion effect, nearby zombies are removed, and the barrel disappears.

## Task 4 — Zombie Types

Add a Fast Zombie (higher speed, 1 HP, smaller) and a Tank Zombie (lower speed, 6 HP, larger). Mix both types into wave spawning alongside the standard zombie.

**Done when:** both subtypes spawn correctly in waves, their distinct stats are reflected in combat, and wave progression still functions.

## Required testing

Survive several waves, take hits to verify the health and invincibility system, empty and reload a clip, shoot a barrel next to a group of zombies, verify both new zombie types spawn and behave correctly, and confirm game over triggers only at 0 HP. Test restarting after game over.

## LLM usage

You may use an LLM during the lab. The goal is to use it as a coding assistant while retaining responsibility for understanding and testing the result.

- Inspect the existing code before asking for changes.
- Ask for explanations when you do not understand a proposed change.
- Test generated code against the stated behaviour and edge cases.
- Keep your complete LLM chat history for submission.
- Do not replace the whole project with an unrelated implementation.

## Submission checklist

- [ ] Tasks 1–4 completed and tested.
- [ ] Health system with invincibility frames works correctly.
- [ ] Ammo limit and reload mechanic work correctly.
- [ ] Barrels explode and remove nearby zombies.
- [ ] Fast and Tank zombie types spawn and behave as specified.
- [ ] No unnecessary external dependencies added beyond pygame.
- [ ] Code remains understandable and modular.
- [ ] Complete LLM chat-history link included.

## Submission

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes
- [ ] A 10-second video of gameplay **after** your changes, showing the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
