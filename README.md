<img src="assets/takto/hero.webp" alt="TAKTO ONE, an open-source hand exoskeleton, in its Snow and Onyx colourways. Designed and built by Sebastian Molano." width="100%">

## Sebastian Molano

Robotics engineer. I design, build and program wearable robots end to end: mechanism, boards,
firmware, control loop, and the software on the other side of the wire. I came from design,
so the device has to feel right in the hand, not only close its loop.

M.Sc. Biomedical Engineering, Hochschule Anhalt · Germany ·
[LinkedIn](https://www.linkedin.com/in/sm29) · [sebastian.molano.29@gmail.com](mailto:sebastian.molano.29@gmail.com)

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/capabilities-dark-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/capabilities-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/capabilities-light-mobile.svg">
  <img alt="What I build, in five layers: mechanism, electronics, firmware, control and software, joined by one data path from a finger joint to the 3D twin." src="assets/capabilities-light.svg" width="100%">
</picture>

**The whole thing.** Sketch, CAD, boards, firmware, live twin in the browser. One pair of
hands, no handoffs.

**Measured, not claimed.** Every rate has its own number. Bench results are called bench
results.

**Built to be built.** Everything ships as source: parts you can print, boards you can order,
code that runs with no hardware attached.

---

### TAKTO ONE

<a href="https://github.com/molanocortes/takto-one"><img src="assets/takto/turntable.webp" alt="TAKTO ONE turning through one full revolution" width="100%"></a>

**Open-source hand exoskeleton. My master's thesis.** Twelve joints read at the joint, eight
tendons driven from the forearm, the control loop on the device. Designed, built and
programmed by one person.

The repository is everything needed to build one: CAD, two KiCad boards, Teensy firmware,
bridge and console, AR layer, phone app, BOM, illustrated build guide. The whole stack runs
in simulation before you print a part.

**[Explore the repository →](https://github.com/molanocortes/takto-one)**

<sub>Bench status: four fingers built and instrumented, twelve encoders live, motor-driven finger motion demonstrated. Force rendering and assistance not yet characterised.</sub>

---

### Released on their own

Pulled out of the work above because they stand on their own.

**[dynamixel-on-device](https://github.com/molanocortes/dynamixel-on-device)** <sub>C++ · AGPL-3.0</sub><br>
Dynamixel Protocol 2.0 on the microcontroller, no host PC. Fast Sync Read, no heap,
unit-testable without hardware.

**[bno085-multi](https://github.com/molanocortes/bno085-multi)** <sub>C · MIT</sub><br>
Several BNO085 IMUs on one MCU at full rate. The stock driver is single-instance by
construction; this one is reentrant.

**[consent-scoped-agent-negotiation](https://github.com/molanocortes/consent-scoped-agent-negotiation)** <sub>Python · MIT</sub><br>
Two AI agents settle a bounded decision without seeing each other's private data. Signed
consent, a wire format with nowhere for an injection to live, an offline adversarial suite.

**[latex-safe-build](https://github.com/molanocortes/latex-safe-build)** <sub>Shell · MIT</sub><br>
LaTeX builds in an isolated copy. A build can never corrupt its own source tree.

**[multi-volume-controller](https://github.com/molanocortes/multi-volume-controller)** <sub>Swift · AGPL-3.0</sub><br>
Per-app volume mixer for macOS on Core Audio process taps. No driver, no admin rights.

**[penumbra-screen-dimmer](https://github.com/molanocortes/penumbra-screen-dimmer)** <sub>Python · MIT</sub><br>
Dims a Mac below the hardware minimum. Click-through, every Space, every full-screen app.

<!-- Portfolio: add a sebastianmolano.com link to the header line once it is deployed. -->
