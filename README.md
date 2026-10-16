# EasyEDA 3D Parts (and other 3D parts)

Ready-made 3D models, footprints and symbols for parts that EasyEDA Pro and KiCad do not ship, so anyone can drop them into a custom PCB. Each part has its own folder under [`parts/`](parts/), with the files for EasyEDA Pro, KiCad and generic VRML / OBJ.

## Parts
| Part | What you get |
|---|---|
| [`BluePill-GD32F103C8T6`](parts/BluePill-GD32F103C8T6/README.md) | Blue Pill (STM32F103C8T6 / GD32F103C8T6) plug-in module: 3D model with and without header pins (solder-in, pins go through the PCB), 40-pad footprint, 40-pin symbol, EasyEDA Pro device export, KiCad files, pin picture |

## Rules every part follows
- A README with a "facts and where they come from" section and a "still unverified" section. Nothing is claimed from memory.
- Footprint, symbol and 3D model share one pin numbering.
- Generated from one script in [`tools/`](tools/) so a changed measurement is a re-run, not a redraw.
- Solder-in parts have a 3D offset so the pin tails show below the PCB.

## Adding a new part
1. Make the files under `parts/<Part-Name>/` (3d, easyeda, kicad, extras, README).
2. Add a row to the table above.
3. Commit and push, one commit per part or per change (`git add -A && git commit && git push`).

## Licence
CC BY 4.0, see [`LICENSE.md`](LICENSE.md).
