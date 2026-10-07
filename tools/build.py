#!/usr/bin/env python3
"""Builds the Zaid Saifan Portfolio static site (GitHub Pages ready).

Run from anywhere:  python3 tools/build.py
Regenerates index.html and projects/*.html at the repo root. Edit content HERE, not in the generated HTML.
CSS lives in assets/css/site.css, JS in assets/js/site.js (not generated)."""
import math, os, html

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "Zaid Saifan"
EMAIL = "zaid.saifan06@gmail.com"
PHONE = "(905) 617-1304"
PHONE_TEL = "+19056171304"
LINKEDIN = "https://www.linkedin.com/in/zaid-saifan-0b369b356"
FONTS = ("https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@500;600;700;800"
         "&family=Red+Hat+Mono:wght@400;500;600&family=Red+Hat+Text:wght@400;500;600;700&display=swap")
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='12' fill='%231F3A5F'/%3E%3Ctext x='32' y='42' text-anchor='middle' "
           "font-family='monospace' font-weight='700' font-size='26' fill='%23F1F3F2'%3EZS%3C/text%3E%3C/svg%3E")

I = {
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
 "in": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.75h4v11H3v-11Zm6.5 0h3.8v1.6h.06c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.77 2.6 4.77 6v5.45h-4v-4.83c0-1.15-.02-2.63-1.6-2.63-1.6 0-1.85 1.25-1.85 2.55v4.91h-4v-11Z"/></svg>',
 "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "cap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
}

# ---------------------------------------------------------------- SVG diagrams
def box(x, y, w, h, title, sub=None, kind="dg-box"):
    s = f'<rect class="{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
    if sub:
        s += f'<text class="dg-t" x="{x+w/2}" y="{y+h/2-3}" text-anchor="middle">{title}</text>'
        s += f'<text class="dg-s" x="{x+w/2}" y="{y+h/2+13}" text-anchor="middle">{sub}</text>'
    else:
        s += f'<text class="dg-t" x="{x+w/2}" y="{y+h/2+4.5}" text-anchor="middle">{title}</text>'
    return s

def arrow_defs(i):
    return (f'<defs><marker id="ah{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 10 5 0 10z" style="fill:var(--copper)"/></marker></defs>')

def svg_golfcart():
    s = [f'<svg viewBox="0 0 680 290" role="img" aria-label="Power tree: 24 V battery splits into a fused 20 A motor branch and a fused 5 A logic branch stepped down to 12 V and 5 V">', arrow_defs("g")]
    s.append(box(16, 115, 132, 60, "24 V LiFePO₄", "100 Ah pack", "dg-box-cu"))
    s.append('<path class="dg-cu" d="M148 145 H190 V62 H222"/><path class="dg-cu" d="M190 145 V228 H222"/><circle class="dg-dot" cx="190" cy="145" r="4"/>')
    s.append(box(222, 37, 92, 50, "F1 · 20 A", "motor fuse", "dg-box-mask"))
    s.append(f'<path class="dg-cu" d="M314 62 H350" marker-end="url(#ahg)"/>')
    s.append(box(352, 37, 146, 50, "Motor driver", "bulk caps at input"))
    s.append(f'<path class="dg-cu" d="M498 62 H534" marker-end="url(#ahg)"/>')
    s.append(box(536, 37, 128, 50, "Brushed DC", "traction motor"))
    s.append(box(222, 203, 92, 50, "F2 · 5 A", "logic fuse", "dg-box-mask"))
    s.append(f'<path class="dg-line" d="M314 228 H350" marker-end="url(#ahg)"/>')
    s.append(box(352, 203, 96, 50, "Buck", "24 → 12 V"))
    s.append(f'<path class="dg-line" d="M448 228 H470" marker-end="url(#ahg)"/>')
    s.append(box(472, 203, 70, 50, "Buck", "12 → 5 V"))
    s.append(f'<path class="dg-line" d="M542 228 H560" marker-end="url(#ahg)"/>')
    s.append(box(562, 203, 102, 50, "Pi 5 +", "4× ESP32"))
    s.append('<text class="dg-cu-t" x="200" y="20">15–20 A continuous · 2 oz Cu · IPC-2221</text>')
    s.append('<text class="dg-cu-t" x="200" y="282">logic tier</text>')
    s.append('</svg>')
    return "".join(s)

def svg_rc():
    s = [f'<svg viewBox="0 0 680 260" role="img" aria-label="Control path from a PS5 controller through a Python interface and Arduino firmware to two rear motors and a steering servo">', arrow_defs("r")]
    s.append(box(14, 96, 110, 58, "PS5", "controller"))
    s.append('<path class="dg-cu" d="M124 125 H154" marker-end="url(#ahr)"/>')
    s.append(box(156, 96, 120, 58, "Python", "stick → command"))
    s.append('<path class="dg-cu" d="M276 125 H306" marker-end="url(#ahr)" stroke-dasharray="5 4"/>')
    s.append('<text class="dg-cu-t" x="291" y="112" text-anchor="middle">wireless</text>')
    s.append(box(308, 88, 128, 74, "Arduino", "C++ · PWM +", "dg-box-cu"))
    s.append('<text class="dg-s" x="372" y="153" text-anchor="middle">differential math</text>')
    s.append('<path class="dg-line" d="M436 110 H470 V62 H490" marker-end="url(#ahr)"/>')
    s.append('<path class="dg-line" d="M436 140 H470 V200 H490" marker-end="url(#ahr)"/>')
    s.append(box(492, 36, 82, 52, "L298N", "H-bridge"))
    s.append('<path class="dg-line" d="M574 52 H600" marker-end="url(#ahr)"/><path class="dg-line" d="M574 74 H600" marker-end="url(#ahr)"/>')
    s.append(box(602, 30, 64, 30, "M · L", None, "dg-box-mask"))
    s.append(box(602, 64, 64, 30, "M · R", None, "dg-box-mask"))
    s.append(box(492, 174, 174, 52, "Steering servo", "own supply rail", "dg-box-mask"))
    s.append('<text class="dg-cu-t" x="14" y="250">11.1 V 3S LiPo → dual buck converters</text>')
    s.append('</svg>')
    return "".join(s)

def svg_roboracer():
    s = [f'<svg viewBox="0 0 680 280" role="img" aria-label="Power distribution: battery feeds a custom board that separates protected actuator rails from an isolated logic rail">', arrow_defs("b")]
    s.append(box(14, 110, 110, 60, "Battery", "drive pack", "dg-box-cu"))
    s.append('<path class="dg-cu" d="M124 140 H160" marker-end="url(#ahb)"/>')
    s.append(box(162, 90, 140, 100, "Custom PDB", "Altium Designer", "dg-box-cu"))
    s.append('<path class="dg-cu" d="M302 115 H340 V58 H372" marker-end="url(#ahb)"/><path class="dg-cu" d="M340 115 V118 H372" marker-end="url(#ahb)"/>')
    s.append('<text class="dg-cu-t" x="372" y="22">protected actuator rails</text>')
    s.append(box(374, 32, 136, 50, "VESC", "motor controller"))
    s.append(box(374, 94, 136, 50, "Steering servos", "high torque"))
    s.append('<path class="dg-mask" d="M302 165 H340 V222 H372" marker-end="url(#ahb)"/>')
    s.append('<text class="dg-cu-t" x="372" y="190" style="fill:var(--mask)">isolated logic rail</text>')
    s.append(box(374, 198, 136, 50, "Onboard computer", "SLAM", "dg-box-mask"))
    s.append('<path class="dg-mask" d="M510 223 H540 V196 H556" marker-end="url(#ahb)"/><path class="dg-mask" d="M540 223 V250 H556" marker-end="url(#ahb)"/>')
    s.append(box(558, 176, 108, 40, "2D LiDAR", None, "dg-box-mask"))
    s.append(box(558, 230, 108, 40, "IMU", None, "dg-box-mask"))
    s.append('</svg>')
    return "".join(s)

def svg_fpga():
    codes = ["000", "001", "011", "010", "110", "111", "101", "100"]
    cx, cy, R = 200, 150, 110
    s = ['<svg viewBox="0 0 680 300" role="img" aria-label="Eight-state Moore machine with Gray-coded states arranged in a ring; gate input cost reduced from 83 to 63">', arrow_defs("f")]
    pts = []
    for i in range(8):
        a = -math.pi / 2 + i * 2 * math.pi / 8
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    for i in range(8):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 8]
        dx, dy = x2 - x1, y2 - y1; d = math.hypot(dx, dy)
        sx, sy = x1 + dx / d * 27, y1 + dy / d * 27
        ex, ey = x2 - dx / d * 29, y2 - dy / d * 29
        s.append(f'<path class="dg-cu" d="M{sx:.1f} {sy:.1f} L{ex:.1f} {ey:.1f}" marker-end="url(#ahf)"/>')
    for i, (x, y) in enumerate(pts):
        k = "dg-box-cu" if i == 7 else "dg-box"
        s.append(f'<circle class="{k}" cx="{x:.1f}" cy="{y:.1f}" r="25"/>')
        s.append(f'<text class="dg-s" x="{x:.1f}" y="{y-4:.1f}" text-anchor="middle">S{i}</text>')
        s.append(f'<text class="dg-t" x="{x:.1f}" y="{y+12:.1f}" text-anchor="middle" style="font-family:var(--f-mono);font-size:12px">{codes[i]}</text>')
    s.append('<text class="dg-s" x="200" y="154" text-anchor="middle">one bit flips</text>')
    s.append('<text class="dg-s" x="200" y="168" text-anchor="middle">per transition</text>')
    # cost bars
    bx = 400
    s.append('<text class="dg-cu-t" x="400" y="70">GATE INPUT COST</text>')
    s.append(f'<rect x="{bx}" y="88" width="{83*3}" height="34" rx="4" style="fill:var(--line)"/>')
    s.append(f'<text class="dg-t" x="{bx+10}" y="110">Binary · 83</text>')
    s.append(f'<rect x="{bx}" y="136" width="{63*3}" height="34" rx="4" style="fill:var(--copper)"/>')
    s.append(f'<text class="dg-t" x="{bx+10}" y="158" style="fill:var(--paper)">Gray · 63</text>')
    s.append(f'<text class="dg-t" x="{bx}" y="210" style="font-size:30px;font-weight:800;fill:var(--copper)">−24%</text>')
    s.append(f'<text class="dg-s" x="{bx}" y="232">same behaviour, less hardware</text>')
    s.append('</svg>')
    return "".join(s)

def svg_funcgen():
    W = 680
    s = ['<svg viewBox="0 0 680 300" role="img" aria-label="Three-stage signal chain producing square, triangle and sine waves at 4.4 kHz and 10 V">', arrow_defs("w")]
    stages = [("Oscillator", "TL082 core"), ("Integrator", "square → triangle"), ("Shaper", "triangle → sine")]
    xs = [20, 250, 480]
    for (t, sub), x in zip(stages, xs):
        s.append(box(x, 24, 180, 52, t, sub, "dg-box-cu" if x == 20 else "dg-box"))
    s.append('<path class="dg-cu" d="M200 50 H248" marker-end="url(#ahw)"/><path class="dg-cu" d="M430 50 H478" marker-end="url(#ahw)"/>')
    # waveforms under each
    y0, A = 190, 52
    def path(fn, x0):
        pts = []
        for i in range(0, 181):
            t = i / 180 * 2  # two periods
            pts.append(f"{x0+i:.1f},{y0 - A*fn(t):.1f}")
        return "M" + " L".join(pts)
    sq = lambda t: 1 if (t % 1) < .5 else -1
    tri = lambda t: 4 * abs((t % 1) - .5) - 1
    sn = lambda t: math.sin(2 * math.pi * t)
    for fn, x, lab in [(sq, 20, "Square"), (tri, 250, "Triangle"), (sn, 480, "Sine")]:
        s.append(f'<line class="dg-grid" x1="{x}" y1="{y0}" x2="{x+180}" y2="{y0}"/>')
        s.append(f'<path class="dg-cu" d="{path(fn, x)}"/>')
        s.append(f'<text class="dg-t" x="{x}" y="{y0+A+40}">{lab}</text>')
    s.append('<text class="dg-cu-t" x="660" y="290" text-anchor="end">4.4 kHz · 10 V</text>')
    s.append('</svg>')
    return "".join(s)

# ---------------------------------------------------------------- Projects
P = [
 dict(
  slug="hospital-delivery-robot",
  title="Hospital Autonomous Secure Delivery Robot",
  short="Hospital Delivery Robot",
  eyebrow="Western University · Team design project",
  lede="A delivery robot for moving supplies between hospital departments. It drives itself down a corridor, stops before it hits anything, and only opens its cargo box for an authorized RFID card.",
  card="Custom Altium PCB shield that ties 5 sensors and 4 actuator systems into one Arduino control loop, with an RFID-locked cargo box and a 20 cm obstacle stop.",
  role="Electrical architecture, PCB shield, control integration",
  tags=["Altium Designer", "Arduino C++", "PCB assembly", "RFID", "Power rails"],
  thumb=("img", "hospital-robot.webp", "The assembled hospital delivery robot with its custom PCB shield and RFID-locked cargo box"),
  specs=[("Team", "Section 3, Team 6"), ("Controller", "Arduino Uno + custom shield"),
         ("Sensors", "HC-SR04 ultrasonic, RC522 RFID, HC-05 Bluetooth, DHT11 temp/humidity"),
         ("Actuators", "2 DC motors via L298N, servo latch, 16×2 LCD"),
         ("Power", "11.1 V LiPo → 5.1 V logic + 7.9 V motor rails"), ("Runtime", "45 min continuous"),
         ("Tools", "Altium Designer, Arduino IDE, multimeter")],
  hero=("img", "hospital-pcb-3d.webp", "3D render of the custom shield in Altium. Every header is labelled on the silkscreen."),
  results=[("45 min", "continuous runtime on one 11.1 V LiPo"), ("100%", "integration tests passed"), ("< 20 cm", "verified obstacle-stop distance")],
  sections=[
   ("The problem", "Brief", """<p>Hospitals move medication, samples and supplies between departments all day. The work is repetitive and time-sensitive, and it carries a chain-of-custody requirement: the cargo can only go to the right person.</p>
<p>Our brief was a vehicle that drives a corridor on its own, refuses to run into anything, and will not release its cargo without authorization.</p>"""),
   ("Off the breadboard, onto a custom shield", "PCB design", """<p>I designed the electrical architecture as a single-layer <strong>Altium PCB shield</strong> that stacks directly onto an Arduino Uno. Every subsystem gets its own labelled header: 5 V power, RFID, ultrasonic, motor driver, Bluetooth, temperature sensor, servo and LCD, plus an onboard push button with a 10 kΩ pull-down.</p>
<p>Labelling every connector on the silkscreen meant the harness could only go together one way, which removed a whole class of wiring mistakes during integration.</p>"""),
   ("Two rails from one battery", "Power", """<ul>
<li>One <strong>11.1 V LiPo</strong> feeds two buck converters: a <strong>5.1 V logic rail</strong> and a <strong>7.9 V motor rail</strong>.</li>
<li>Keeping the rails separate holds motor switching noise off the sensors and the I²C bus.</li>
<li>Stable ultrasonic readings are what made the obstacle stop safe to rely on.</li></ul>"""),
   ("Sensing and actuation", "Control loop", """<p>Five sensors and four actuator systems run in one microcontroller control loop:</p>
<ul>
<li><strong>HC-SR04 ultrasonic</strong> measures range ahead and stops the robot inside 20 cm.</li>
<li><strong>RC522 RFID</strong> reader unlocks the cargo compartment only for an authorized tag.</li>
<li><strong>HC-05 Bluetooth</strong> carries commands and telemetry.</li>
<li><strong>DHT11</strong> logs temperature and humidity inside the cargo box in transit.</li>
<li>A <strong>16×2 LCD</strong> shows status, two DC motors run through an <strong>L298N</strong>, and a <strong>servo</strong> drives the latch.</li></ul>"""),
   ("Build and debug", "Integration", """<p>I specified the components, drew the schematics and kept the full bill of materials. I then hand-soldered and assembled the shield, and used a multimeter to trace each wiring and integration fault back to its root cause until every subsystem test passed.</p>"""),
  ],
  gallery=[("hospital-pcb-layout.webp", "Altium PCB layout: top copper, pads and silkscreen labels for each subsystem header", True),
           ("hospital-pcb-3d.webp", "3D render of the shield with the push button, 10 kΩ resistor and headers populated", False),
           ("hospital-wiring.webp", "Full system wiring plan: Arduino Uno, sensors, RFID, LCD, L298N, buck converters and LiPo", False),
           ("hospital-robot.webp", "The assembled robot, with the shield wired to every subsystem", False)],
 ),
 dict(
  slug="golf-cart-power-and-throttle",
  title="Autonomous Golf Cart: Power Distribution & Throttle Control",
  short="Golf Cart Power & Throttle",
  eyebrow="Western Engineering AutoPilot · Oct 2025 – present",
  lede="A student team is turning a full-scale golf cart into an autonomous vehicle. I work on throttle and motor control, and co-designed the board that carries motor current and hands out clean logic rails.",
  card="PWM throttle control through a high-current ESC, and a 2-layer, 2 oz copper power distribution board that carries 15–20 A from a 24 V LiFePO₄ pack.",
  role="Throttle & motor control; power distribution board co-design",
  tags=["Altium Designer", "PWM", "ESC", "IPC-2221", "24 V LiFePO₄"],
  thumb=("img", "pdb-3d.webp", "3D render of the golf cart power distribution board in Altium"),
  specs=[("Team", "Western Engineering AutoPilot"), ("Source", "24 V, 100 Ah LiFePO₄"), ("Board", "2-layer, 2 oz copper"),
         ("Current", "15–20 A continuous"), ("Rails", "24 V motor · 12 V · 5 V"), ("Loads", "DC motor drive, Raspberry Pi 5, 4× ESP32"),
         ("Protection", "20 A motor fuse, 5 A logic fuse"), ("Tools", "Altium Designer, microcontroller, bench supply")],
  hero=("img", "pdb-3d.webp", "3D render of the WEAP golf cart PDB in Altium: battery input, two fused branches, the 24 → 12 V buck connector, bulk capacitor C1 and the Pololu motor-driver output."),
  results=[("15–20 A", "continuous current target"), ("3", "power tiers: 24 V, 12 V, 5 V"), ("2 oz", "copper on both layers")],
  sections=[
   ("The brief", "Context", """<p>Everything downstream of the cart's 24 V traction pack, the motor drive, a single-board computer, four microcontrollers and their sensors, was being wired point to point. On a vehicle that drives itself, loose high-current wiring is a safety problem first.</p>
<p>The fix was one board that carries motor-level current and supplies clean rails to the compute stack.</p>"""),
   ("Throttle control", "My subsystem", """<ul>
<li>Programmed a microcontroller to generate <strong>PWM throttle commands</strong> for a high-current ESC, automating acceleration on the full-scale cart.</li>
<li>Wired, bench-tested and debugged the system for <strong>repeatable speed regulation</strong> before it went on the vehicle.</li></ul>"""),
   ("Power architecture", "Three tiers", """<ul>
<li>The 24 V rail runs straight to the motor driver through its own fuse and bulk capacitance, keeping the highest-current path short.</li>
<li>A 24 → 12 V buck feeds everything that is not the drive motor.</li>
<li>A 12 → 5 V stage supplies a Raspberry Pi 5 and four ESP32 controllers.</li>
<li>Voltage, current and thermal margin were checked on every rail, not just the input.</li></ul>
<figure class="figure"><div class="media">""" + svg_golfcart() + """</div><figcaption><b>Diagram</b><span>Power tree. The motor branch stays short and is fused separately from the stepped-down logic tier.</span></figcaption></figure>"""),
   ("On the board", "Schematic", """<ul>
<li><strong>Battery Connect</strong> brings the 24 V pack onto the board through a screw-terminal block.</li>
<li><strong>Fuse 1</strong> protects the branch that feeds the <strong>24 → 12 V buck converter</strong> for the logic tier.</li>
<li><strong>Fuse 2</strong> protects the motor branch, which passes a <strong>1000 µF bulk capacitor (C1)</strong> before the <strong>Pololu motor driver</strong> output.</li>
<li>All grounds return on one shared net, and every connector uses the same screw-terminal footprint, so the harness is simple to service.</li></ul>"""),
   ("Carrying the current", "Copper sizing", """<ul>
<li>Trace widths calculated to <strong>IPC-2221</strong> for a 15–20 A continuous target.</li>
<li><strong>2 oz copper</strong> on both layers, with polygon pours instead of discrete traces.</li>
<li><strong>Via stitching</strong> so both pours share the load and spread the heat.</li></ul>
<p>Heat dissipation was a placement constraint from the first layout pass.</p>"""),
   ("Protection", "Safety", """<p>A 5 A fuse on the logic branch and a 20 A fuse on the motor branch, coordinated with the driver's current limit so the fuse acts last. Bulk capacitance holds the motor rail up through current steps, and anti-spark connectors protect the contacts when the 100 Ah pack is connected. The board shipped with a full BOM and wiring documentation for design review.</p>"""),
  ],
  gallery=[("pdb-3d.webp", "3D render: wide copper traces with via stitching between the fuses, buck connector, C1 and the Pololu output. Silkscreen credits Zaid & Abdelrahman.", True),
           ("pdb-schematic.webp", "Schematic: battery input split into two fused branches, one to the 24 → 12 V buck converter and one through C1 to the Pololu motor driver.", False)],
  gallery_title="Board and schematic",
  note="<b>Next step:</b> current sensing on each branch, reported back to the compute stack, so the vehicle can see its own power draw.",
 ),
 dict(
  slug="roboracer-autonomous-race-car",
  title="Roboracer 1/10-Scale Autonomous Race Car",
  short="Roboracer Race Car",
  eyebrow="Dr. Zaki Research Lab, Western University · Sep 2026 – present",
  lede="Undergraduate research on a 1/10-scale autonomous racing platform: a custom power distribution board, LiDAR and IMU integration for SLAM, and printed mounts to bring the centre of gravity down.",
  card="Custom Altium power board that isolates the VESC and steering-servo rails from noise-sensitive logic, plus 2D LiDAR and IMU integration for real-time SLAM.",
  role="Undergraduate Research Assistant",
  tags=["Altium Designer", "LiDAR", "IMU", "SLAM", "ROS", "Onshape"],
  thumb=("svg", svg_roboracer, ""),
  specs=[("Lab", "Dr. Zaki Research Lab"), ("Platform", "1/10-scale autonomous vehicle"), ("Board", "Custom PDB, Altium Designer"),
         ("Actuators", "VESC motor controller, high-torque steering servos"), ("Sensing", "2D LiDAR + IMU for real-time SLAM"),
         ("Mechanical", "Onshape CAD, 3D-printed mounts"), ("Status", "In progress")],
  hero=("svg", svg_roboracer, "Power distribution concept: protected actuator rails kept apart from the logic rail that feeds the computer and sensors."),
  results=None,
  sections=[
   ("Power distribution", "Board design", """<p>I routed a custom power distribution board in <strong>Altium Designer</strong> that gives the VESC motor controller and the high-torque steering servos their own protected rails. The servos and drive motor pull sharp current spikes, so keeping them away from the logic rail protects the onboard computer and sensors from noise and brownouts.</p>"""),
   ("Sensing for SLAM", "Integration", """<p>I interfaced the onboard computer with a <strong>2D LiDAR</strong> and an <strong>IMU</strong> so the car can build a map and localize itself in real time.</p>"""),
   ("Mechanical", "Packaging", """<p>I modelled sensor mounts and enclosures in <strong>Onshape</strong> and 3D-printed them, placing heavy parts low to bring down the car's centre of gravity.</p>"""),
   ("Also in the lab: Clearpath Husky UGV", "Field robot", """<p>I help a PhD researcher wire and modify the electrical hardware on a Clearpath Husky ground robot used for outdoor mapping. That covers power and sensor connections, checked against the platform's wiring before field testing, and hands-on setup support for other researchers in the lab.</p>"""),
  ],
 ),
 dict(
  slug="wireless-rc-car",
  title="Wireless RC Car with Electronic Differential",
  short="Wireless RC Car",
  eyebrow="Western Engineering AutoPilot",
  lede="A custom RC car driven from a PS5 controller. Each rear wheel has its own motor, and the firmware sets their speeds from the steering angle so the car corners without the inside wheel slipping.",
  card="Electronic differential on two independent rear motors, servo steering, Arduino C++ firmware for wireless PS5 input, and a SolidWorks chassis.",
  role="Steering, chassis, electronic differential",
  tags=["Arduino C++", "Python", "SolidWorks", "L298N", "PWM"],
  thumb=("img", "rc-three-quarter.webp", "The finished wireless RC car with its printed front wing, rear wing and red-rimmed wheels"),
  specs=[("Team", "Western Engineering AutoPilot"), ("Input", "PS5 controller, wireless"), ("Code", "Arduino C++, Python interface"),
         ("Drive", "2 independent rear DC motors, L298N"), ("Steering", "Servo"), ("Power", "11.1 V 3S LiPo, dual buck converters"),
         ("CAD", "SolidWorks chassis"), ("Parts", "Tracked in an Excel BOM")],
  hero=("img", "rc-three-quarter-rear.webp", "The finished car: printed upper deck and rear wing over the drivetrain, with the steering linkage visible at the front."),
  results=None,
  sections=[
   ("Why an electronic differential", "Problem", """<p>A fixed rear axle forces both wheels to turn at the same speed. In a corner the inside wheel travels a shorter arc, so one wheel has to slip, which shows up as understeer and lost traction.</p>
<p>Giving each rear wheel its own motor lets the firmware set a speed offset from the steering input, so each wheel turns at the speed the corner asks for.</p>"""),
   ("Control path", "Firmware", """<ul>
<li>A PS5 controller pairs to a Python interface that turns stick positions into throttle and steering commands.</li>
<li>Commands go wirelessly to <strong>C++ firmware on the Arduino</strong>, which handles PWM timing and the differential math.</li>
<li>The loop is short, so the car responds without noticeable lag.</li></ul>
<figure class="figure"><div class="media">""" + svg_rc() + """</div><figcaption><b>Diagram</b><span>Control path from thumbstick to PWM. The Arduino owns PWM timing and the differential math.</span></figcaption></figure>"""),
   ("Power and motor hardware", "Electrical", """<ul>
<li>An <strong>11.1 V 3S LiPo</strong> powers the whole car, split by dual buck converters so logic and actuators never share a rail.</li>
<li>An <strong>L298N dual H-bridge</strong> drives both rear motors.</li>
<li>The steering servo has its own supply, so a stall cannot brown out the microcontroller mid-corner.</li>
<li>I designed the circuit and wiring layout and selected every part against a BOM.</li></ul>"""),
   ("Chassis", "Mechanical", """<p>I modelled the chassis in <strong>SolidWorks</strong> to package the steering servo, motors and electronics, then completed the mechanical assembly. The car was demonstrated live to club leadership, which tested control response, chassis integrity and firmware stability under real driving.</p>"""),
  ],
  videos=[("rc-driving.mp4", "rc-driving-poster.webp", "Driving test on carpet, controlled wirelessly from the PS5 controller.", "wide"),
          ("rc-steering.mp4", "rc-steering-poster.webp", "Bench test of the servo steering sweeping lock to lock.", "tall")],
  gallery=[("rc-three-quarter.webp", "Front three-quarter view: printed upper deck, front and rear wings", False),
           ("rc-side.webp", "Side profile: steering servo and gold linkage at the front, electronics bay between the axles", False),
           ("rc-front-low.webp", "Low front view of the steering knuckles and printed front frame", False),
           ("rc-front.webp", "Head-on view with the battery mounted on the deck", False),
           ("rc-electronics.webp", "Electronics bay during build: Arduino Uno, buck converter, L298N, HC-05 Bluetooth and both rear drive motors", False),
           ("rc-cad.webp", "SolidWorks assembly model of the chassis, drivetrain and wings", False)],
  gallery_title="Build photos and CAD",
 ),
 dict(
  slug="analog-function-generator",
  title="Analog Function Generator and PCB",
  short="Analog Function Generator",
  eyebrow="Western University · Electronic circuits",
  lede="A multi-stage op-amp function generator, taken from simulation to a hand-soldered board and measured against the model on an oscilloscope.",
  card="TL082 op-amp generator producing square, triangle and sine waves at 4.4 kHz and 10 V, simulated in Micro-Cap and built on an Altium PCB.",
  role="Simulation, schematic, layout, assembly, test",
  tags=["Micro-Cap", "Altium Designer", "Op-amps", "Oscilloscope"],
  thumb=("svg", svg_funcgen, ""),
  specs=[("Simulator", "Micro-Cap 12"), ("Op-amp", "TL082"), ("Outputs", "Square, triangle, sine"), ("Frequency", "4.4 kHz"),
         ("Amplitude", "10 V"), ("Board", "Custom Altium PCB, through-hole"), ("Test", "Oscilloscope vs. simulation")],
  hero=("svg", svg_funcgen, "Three outputs from one oscillator core. Chaining the stages locks all three to the same frequency."),
  results=[("4.4 kHz", "design frequency, met on hardware"), ("10 V", "output amplitude"), ("3", "waveforms from one core")],
  sections=[
   ("Topology", "Design", """<ul>
<li>A <strong>TL082</strong> oscillator core produces the square wave.</li>
<li>An integrator stage turns it into a triangle.</li>
<li>A shaping and amplification stage produces the sine.</li></ul>"""),
   ("Simulate first", "Micro-Cap", """<p>I tuned the circuit in <strong>Micro-Cap 12</strong> to 4.4 kHz at 10 V before ordering any boards. Simulation is cheap; a board revision is not.</p>"""),
   ("Board and bring-up", "Hardware", """<p>The PCB was routed in <strong>Altium Designer</strong>, populated with through-hole parts and hand-soldered. I captured each output on an oscilloscope and compared it against the simulated traces. The measured hardware matched the simulation on all three outputs at the design frequency and amplitude.</p>"""),
  ],
 ),
 dict(
  slug="fpga-sequence-detector",
  title="FPGA Sequence Detector and Logic Optimization",
  short="FPGA Sequence Detector",
  eyebrow="Western University · Digital logic",
  lede="An 8-state Moore machine that finds a 4-bit pattern in a serial stream, then an optimization pass that made it 24% cheaper in hardware.",
  card="8-state Moore FSM in Quartus Prime. A custom Gray-code state assignment and Karnaugh-map simplification cut gate input cost from 83 to 63.",
  role="FSM design, encoding, optimization, simulation",
  tags=["Quartus Prime", "FPGA", "Moore FSM", "K-maps"],
  thumb=("svg", svg_fpga, ""),
  specs=[("Tool", "Quartus Prime"), ("Elements", "D flip-flops"), ("States", "8, Moore"), ("Encoding", "Custom Gray code"),
         ("Gate input cost", "83 → 63"), ("Reduction", "24%")],
  hero=("svg", svg_fpga, "State ring with Gray-coded assignments, and the gate input cost before and after."),
  results=[("83 → 63", "gate input cost"), ("−24%", "hardware cost, same behaviour"), ("8", "Moore states")],
  sections=[
   ("The machine", "Design", """<p>A Moore machine with <strong>8 states</strong>, built from D flip-flops, that detects a 4-bit sequence anywhere in a continuous stream. When a partial match breaks, the machine falls back to the state for the suffix it has already seen instead of resetting to zero.</p>"""),
   ("Cheaper in gates", "Optimization", """<ul>
<li>A custom <strong>Gray-code</strong> state assignment changes only one state bit per transition, which reduces the terms each next-state equation has to cover.</li>
<li><strong>Karnaugh-map</strong> simplification took total gate input cost from 83 to 63, a 24% cut with no change in behaviour.</li></ul>"""),
   ("Verification", "Simulation", """<p>I checked timing and state transitions in Quartus Prime simulation, covering partial matches, broken matches and back-to-back detections as well as the normal case.</p>"""),
  ],
 ),
]

# ---------------------------------------------------------------- page chrome
def head(title, desc, root, artifact=False):
    meta = f"""<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{root}assets/css/site.css">"""
    if artifact:
        return f"<title>{html.escape(title)}</title>\n{meta}\n"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
{meta}
</head>
<body>
"""

def header(root, current=""):
    def cur(k): return ' aria-current="page"' if current == k else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{root}index.html"><span class="brand-mark">ZS</span><span>{NAME}</span></a>
    <nav class="nav" aria-label="Main">
      <a class="keep" href="{root}index.html#work"{cur('work')}>Projects</a>
      <a href="{root}index.html#experience">Experience</a>
      <a href="{root}index.html#skills">Skills</a>
      <a href="{root}index.html#contact">Contact</a>
      <a class="btn-sm" href="{root}assets/Zaid_Saifan_Resume.pdf" target="_blank" rel="noopener">Résumé</a>
    </nav>
  </div>
</header>
"""

def contact(root):
    return f"""<section class="section contact" id="contact">
  <div class="wrap contact-grid">
    <div>
      <p class="label">Contact</p>
      <h2 style="margin-top:.6rem">Let's build something.</h2>
      <p class="lead">I'm looking for 12–16 month co-op and internship terms starting May 2027 in power and electrical design, controls, robotics, embedded systems or hardware test.</p>
      <div class="btns" style="margin-top:2rem">
        <a class="btn" href="mailto:{EMAIL}">{I['mail']}Email me</a>
        <a class="btn btn--ghost" href="{LINKEDIN}" target="_blank" rel="noopener">{I['in']}LinkedIn</a>
      </div>
    </div>
    <ul class="contact-list">
      <li><span class="label">Email</span><span><a href="mailto:{EMAIL}">{EMAIL}</a><button class="copy" type="button" data-copy="{EMAIL}">Copy</button></span></li>
      <li><span class="label">Phone</span><span><a href="tel:{PHONE_TEL}">{PHONE}</a></span></li>
      <li><span class="label">LinkedIn</span><span><a href="{LINKEDIN}" target="_blank" rel="noopener">linkedin.com/in/zaid-saifan</a></span></li>
      <li><span class="label">Résumé</span><span><a href="{root}assets/Zaid_Saifan_Resume.pdf" target="_blank" rel="noopener">Zaid_Saifan_Resume.pdf</a></span></li>
      <li><span class="label">Based in</span><span>London, Ontario</span></li>
    </ul>
  </div>
</section>
<footer class="site-foot">
  <div class="wrap"><span>© <span id="year">2026</span> {NAME} · Electrical Engineering, Western University</span><a href="{root}index.html#top">Back to top ↑</a></div>
</footer>
<script src="{root}assets/js/site.js"></script>
"""

def media(thumb, root, eager=False):
    kind, a, b = thumb
    if kind == "img":
        return f'<img src="{root}assets/img/{a}" alt="{html.escape(b)}" loading="{"eager" if eager else "lazy"}">'
    return a()

def tags(ts): return '<ul class="tags">' + "".join(f"<li>{html.escape(t)}</li>" for t in ts) + "</ul>"

def proj_card(p, root, cls="proj"):
    return f"""<a class="{cls}" href="{root}projects/{p['slug']}.html">
  <div class="proj-media">{media(p['thumb'], root)}</div>
  <div class="proj-body">
    <p class="label label--copper">{html.escape(p['eyebrow'])}</p>
    <h3>{html.escape(p['title'])}</h3>
    <p>{p['card']}</p>
    {tags(p['tags'])}
    <span class="proj-more">Read the write-up <span aria-hidden="true">→</span></span>
  </div>
</a>"""

# ---------------------------------------------------------------- index
def build_index(artifact=False):
    root = ""
    t = "Zaid Saifan Portfolio"
    d = "Zaid Saifan, Electrical Engineering student at Western University: PCB and power distribution design, robotics, controls and embedded systems projects."
    out = [head(t, d, root, artifact), header(root, "")]
    out.append(f"""<main id="main">
<section class="hero" id="top">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <div class="hero-id">
        <div class="avatar" aria-hidden="true">ZS<img src="assets/img/zaid.jpg" alt=""></div>
        <span class="status">Open to co-op from May 2027</span>
      </div>
      <h1>Zaid<br>Saifan</h1>
      <p class="role">Electrical Engineering · Power, Controls &amp; Robotics</p>
      <p class="lede">I'm an electrical engineering student at Western University. I design power distribution boards, wire and debug robots, and write the control code that makes them move. Recently that has meant an autonomous golf cart, a 1/10-scale race car and building electrical design work in industry.</p>
      <div class="btns">
        <a class="btn" href="#work">See my projects</a>
        <a class="btn btn--ghost" href="assets/Zaid_Saifan_Resume.pdf" target="_blank" rel="noopener">{I['doc']}Résumé (PDF)</a>
        <a class="btn btn--ghost" href="{LINKEDIN}" target="_blank" rel="noopener">{I['in']}LinkedIn</a>
      </div>
      <div class="hero-meta">
        <span>{I['pin']}London, Ontario</span>
        <span>{I['cap']}B.E.Sc. Electrical, Western ’29</span>
        <span>{I['cal']}12–16 month terms</span>
      </div>
    </div>
    <figure class="drawing" style="margin:0">
      <div class="drawing-img"><img src="assets/img/hospital-pcb-layout.webp" alt="Altium PCB layout of the custom Arduino shield for the hospital delivery robot" width="645" height="473"></div>
      <div class="titleblock" aria-label="Drawing title block">
        <div><span>Title</span><b>Delivery robot shield</b></div>
        <div><span>Tool</span><b>Altium Designer</b></div>
        <div><span>Drawn</span><b>Z. Saifan</b></div>
        <div><span>Rev</span><b>A · 1 of 1</b></div>
      </div>
    </figure>
  </div>
</section>

<section class="facts" aria-label="At a glance">
  <div class="wrap">
    <div class="fact"><b>81.3%</b><span>Year 2 average · Dean's Honor List 2025–26</span></div>
    <div class="fact"><b>15–20 A</b><span>power board co-designed for an autonomous golf cart</span></div>
    <div class="fact"><b>140 h</b><span>building electrical design internship, Amman</span></div>
    <div class="fact"><b>6</b><span>documented hardware projects below</span></div>
  </div>
</section>

<section class="section" id="work">
  <div class="wrap">
    <div class="section-head">
      <div><p class="label">Selected work</p><h2>Projects</h2></div>
      <p>Each project has a full write-up with the design decisions, specs and results. Start with the delivery robot for the most complete build.</p>
    </div>
    <div class="projects">
      {proj_card(P[0], root, "proj proj--feature")}
      {proj_card(P[1], root)}
      <div class="proj-pair">
        {proj_card(P[2], root)}
        {proj_card(P[3], root)}
      </div>
      <div class="proj-pair">
        {proj_card(P[4], root)}
        {proj_card(P[5], root)}
      </div>
    </div>
  </div>
</section>

<section class="section" id="experience">
  <div class="wrap">
    <div class="section-head"><div><p class="label">Where I've worked</p><h2>Experience</h2></div></div>
    <div class="timeline">
      <article class="job">
        <div class="job-when">Sep 2026 – Present<br><span class="now">Current</span></div>
        <div>
          <h3>Undergraduate Research Assistant</h3>
          <p class="org">Dr. Zaki Research Lab, Western University</p>
          <p class="sub">Roboracer Autonomous Race Car <span>· 1/10-scale autonomous vehicle platform</span></p>
          <ul>
            <li>Routed a custom power distribution board in Altium Designer, isolating protected rails for the VESC motor controller and high-torque steering servos from noise-sensitive logic circuits.</li>
            <li>Interfaced the onboard computer with a 2D LiDAR and IMU for real-time SLAM, and 3D-printed Onshape-modelled sensor mounts and enclosures to lower the car's centre of gravity.</li>
          </ul>
          <p class="sub">Clearpath Husky UGV <span>· outdoor mapping research robot</span></p>
          <ul>
            <li>Helping a PhD researcher wire and modify the robot's electrical hardware, making power and sensor connections and checking them against the platform's wiring before field testing.</li>
          </ul>
        </div>
      </article>
      <article class="job">
        <div class="job-when">Jun 2026 – Jul 2026</div>
        <div>
          <h3>Electrical Engineering Intern</h3>
          <p class="org">Epsilon Engineers &amp; Architects · Amman, Jordan</p>
          <ul>
            <li>Performed load calculations, cable sizing and voltage-drop checks across 3–5 active projects over 140 hours, checking results against design criteria with senior engineers before single-line diagrams were issued.</li>
            <li>Drafted and revised 10+ electrical drawing sheets (power and lighting layouts, panel schedules) in AutoCAD and Revit, closing out engineer redlines to firm standards and local code.</li>
            <li>Routed conduit and cable tray in the Revit BIM model around HVAC and structural elements, resolving clashes with mechanical engineers and architects before construction.</li>
            <li>Assisted with low-voltage system layouts and prepared bills of quantities for electrical materials.</li>
          </ul>
        </div>
      </article>
      <article class="job">
        <div class="job-when">Oct 2025 – Present<br><span class="now">Current</span></div>
        <div>
          <h3>Build Team Member, Throttle &amp; Motor Control</h3>
          <p class="org">Western Engineering AutoPilot</p>
          <ul>
            <li>Built and bench-tested a PWM-based throttle control system that automates acceleration on a full-scale autonomous golf cart, interfacing a microcontroller with a high-current ESC for repeatable speed regulation.</li>
            <li>Contributed to a 2-layer power distribution board in Altium Designer, applying trace-width calculations, 2 oz copper and via stitching to carry 15–20 A to the drive and sensing systems within voltage and thermal margins.</li>
            <li>Built a wireless RC car with servo steering and an electronic differential on two independent rear motors.</li>
          </ul>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section" id="skills">
  <div class="wrap two-col">
    <div>
      <div class="section-head" style="margin-bottom:1.5rem"><div><p class="label">Education</p><h2>Western University</h2></div></div>
      <div class="edu">
        <div><h3>Bachelor of Engineering Science</h3><p style="color:var(--muted);margin-top:.3rem">Electrical Engineering · London, ON</p></div>
        <dl>
          <dt>Expected</dt><dd>April 2029</dd>
          <dt>Year 2 average</dt><dd>81.3%</dd>
          <dt>Cumulative</dt><dd>76.3%</dd>
          <dt>Availability</dt><dd>12–16 month co-op from May 2027</dd>
        </dl>
        <span class="badge">Dean's Honor List 2025–26</span>
        <div>
          <p class="label" style="margin-bottom:.6rem">Coursework</p>
          <ul class="chips">
            <li>Control Systems</li><li>Power Systems</li><li>Electric Machines</li><li>Electronic Circuits</li><li>Signal Processing</li><li>Digital Logic &amp; Microprocessors</li><li>Magnetic Circuits</li>
          </ul>
        </div>
      </div>
    </div>
    <div>
      <div class="section-head" style="margin-bottom:1.5rem"><div><p class="label">Toolkit</p><h2>Skills</h2></div></div>
      <div class="skills">
        <div class="skill-group"><h3>Power &amp; electrical design</h3><ul class="chips"><li>Load calculations</li><li>Cable sizing &amp; voltage drop</li><li>Single-line diagrams</li><li>Panel schedules</li><li>Lighting &amp; power layouts</li><li>Power distribution boards</li><li>Trace-width sizing</li></ul></div>
        <div class="skill-group"><h3>Controls, robotics &amp; embedded</h3><ul class="chips"><li>PWM motor control</li><li>ESCs &amp; servos</li><li>DC motor drives</li><li>Microcontrollers</li><li>LiDAR &amp; IMU</li><li>RFID &amp; ultrasonic sensors</li><li>ROS</li><li>FPGA</li></ul></div>
        <div class="skill-group"><h3>CAD &amp; EDA</h3><ul class="chips"><li>Altium Designer</li><li>AutoCAD</li><li>Revit</li><li>SolidWorks</li><li>Onshape</li><li>Micro-Cap</li><li>Quartus Prime</li><li>3D printing</li></ul></div>
        <div class="skill-group"><h3>Programming</h3><ul class="chips"><li>C/C++</li><li>Python</li><li>MATLAB</li><li>Java</li><li>Arduino</li><li>Excel</li></ul></div>
        <div class="skill-group"><h3>Build &amp; test</h3><ul class="chips"><li>Soldering &amp; PCB assembly</li><li>Wiring &amp; harnessing</li><li>Oscilloscopes</li><li>Multimeters</li><li>Function generators</li><li>Bench testing</li><li>Root-cause troubleshooting</li></ul></div>
      </div>
    </div>
  </div>
</section>
</main>
""")
    out.append(contact(root))
    if not artifact: out.append("</body>\n</html>\n")
    return "".join(out)

# ---------------------------------------------------------------- project pages
def build_project(i, artifact_links=False):
    p = P[i]; root = "../"
    prev, nxt = P[i - 1], P[(i + 1) % len(P)]
    out = [head(f"{p['title']} · {NAME}", p['lede'], root), header(root, "work")]
    specs = "".join(f'<div class="row"><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>' for k, v in p['specs'])
    kind, a, cap = p['hero']
    if kind == "img":
        hero_media = f'<button class="zoom" type="button" aria-label="Open image full size"><div class="media dark"><img src="{root}assets/img/{a}" alt="{html.escape(cap)}" loading="eager"></div></button>'
    else:
        hero_media = f'<div class="media">{a()}</div>'
    secs = ""
    for title, small, body in p['sections']:
        secs += f'<section><h2><small>{small}</small>{title}</h2>{body}</section>\n'
    if p.get('results'):
        res = "".join(f'<div class="result"><b>{v}</b><span>{l}</span></div>' for v, l in p['results'])
        secs += f'<section><h2><small>Validation</small>Results</h2><div class="results">{res}</div></section>\n'
    if p.get('note'):
        secs += f'<p class="note">{p["note"]}</p>\n'
    if p.get('videos'):
        v = ""
        for f, poster, vcap, shape in p["videos"]:
            v += f'''<figure class="figure vid-{shape}"><div class="media dark"><video controls muted playsinline preload="metadata" poster="{root}assets/video/{poster}"><source src="{root}assets/video/{f}" type="video/mp4">Your browser can't play this video.</video></div><figcaption><b>Video</b><span>{html.escape(vcap)}</span></figcaption></figure>'''
        secs += f'<section><h2><small>Demo</small>See it drive</h2><div class="videos">{v}</div></section>\n'
    if p.get('gallery'):
        g = ""
        for n, (f, c, _) in enumerate(p['gallery'], 1):
            g += f'''<figure class="figure"><button class="zoom" type="button" aria-label="Open figure {n} full size"><div class="media{' dark' if f.startswith('hospital') else ''}"><img src="{root}assets/img/{f}" alt="{html.escape(c)}" loading="lazy"></div></button><figcaption><b>Fig. {n}</b><span>{html.escape(c)}</span></figcaption></figure>'''
        secs += f'<section><h2><small>Figures</small>{p.get('gallery_title', 'Board, wiring and build')}</h2><p style="color:var(--muted)">Select any figure to open it full size.</p><div class="gallery">{g}</div></section>\n'
    out.append(f"""<main id="main">
<div class="wrap">
  <p class="crumbs"><a href="{root}index.html#work">Projects</a> / {html.escape(p['short'])}</p>
  <div class="ds-head">
    <div>
      <p class="label label--copper">{html.escape(p['eyebrow'])}</p>
      <h1>{html.escape(p['title'])}</h1>
      <p class="lede">{p['lede']}</p>
    </div>
    <div class="ds-role"><span class="label">My role</span><b>{html.escape(p['role'])}</b><div style="margin-top:.9rem">{tags(p['tags'])}</div></div>
  </div>
  <figure class="figure ds-hero">{hero_media}<figcaption><b>Fig. 0</b><span>{html.escape(cap)}</span></figcaption></figure>
  <div class="ds-body">
    <article class="prose">
{secs}    </article>
    <aside class="ds-aside">
      <div class="spec"><h2>Key specifications</h2><dl>{specs}</dl></div>
      <a class="btn btn--ghost" href="{root}assets/Zaid_Saifan_Resume.pdf" target="_blank" rel="noopener" style="justify-content:center">{I['doc']}View my résumé</a>
    </aside>
  </div>
  <nav class="pager" aria-label="More projects">
    <a href="{prev['slug']}.html"><span class="label">← Previous project</span><b>{html.escape(prev['short'])}</b></a>
    <a class="next" href="{nxt['slug']}.html"><span class="label">Next project →</span><b>{html.escape(nxt['short'])}</b></a>
  </nav>
</div>
</main>
""")
    out.append(contact(root))
    out.append("</body>\n</html>\n")
    return "".join(out)

if __name__ == "__main__":
    os.makedirs(f"{OUT}/projects", exist_ok=True)
    open(f"{OUT}/index.html", "w").write(build_index())
    for i, p in enumerate(P):
        open(f"{OUT}/projects/{p['slug']}.html", "w").write(build_project(i))
    print("built", len(P), "projects")
