# PLATO-V---CDC-IST-II-Terminal-

A repo documenting the CDC IST-II terminal, modern peripherals, documentation, and reverse engineering.

Reference manuals are in [`documentation/`](documentation/), primarily the *CDC IST-II Hardware Maintenance Manual* (82100083, 1979) and *CDC PLATO Terminal Communications* (1977).

Switch convention used throughout: **ON = closed (switch up)** , **OFF = open (switch down)**. In tables below, **1** = ON and **0** = OFF unless noted. **X** = don't care.

## Switch banks overview

| Bank | Location | Positions | Function |
|------|----------|-----------|----------|
| **S5** | C-13 | 8 | Default PLATO load file; default ASCII baud rate |
| **S2** | G-11 | 10 | Communications interface and terminal configuration |
| **ROM** | *(controller board)* | 4 | ROM socket presence (ROMs 1–4) |
| **Front panel** | Operator panel | 6 rockers + controls/LEDs | Diagnostics, mode, brightness, comms status |

---

## Current switch configuration

As found on this terminal (documented 2026-09-06). **ON** = switch up/closed, **OFF** = switch down/open.

### ROM presence (4-position)

| Pos | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|
| **State** | OFF | OFF | OFF | OFF |

All positions OFF → **no ROMs indicated as present** in sockets 1–4. Verify against actual chips installed; positions should match physical ROM population.

### S5 at C-13 (8-position)

| Pos | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-----|---|---|---|---|---|---|---|---|
| **State** | OFF | ON | ON | ON | ON | ON | ON | ON |

| Setting | Decoded value | Notes |
|---------|---------------|-------|
| Default PLATO load file (pos 1–4) | **Ambiguous** | Pos 2 & 4 agree (ON); pos 1 & 3 disagree (OFF / ON). Closest match is **load file 1** (requires 1 & 3 OFF, 2 & 4 ON) — pos 3 may be out of agreement with its redundant pair. |
| Default ASCII baud rate (pos 6–8) | **75 bps** | All three ON |
| Pos 5 | *(unused)* | ON |

### S2 at G-11 (10-position)

| Pos | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-----|---|---|---|---|---|---|---|---|---|---|
| **State** | ON | ON | ON | OFF | ON | ON | ON | OFF | ON | ON |

| Pos | Decoded setting |
|-----|-----------------|
| 1 | DTR **constant** |
| 2 | **RS-232** interface |
| 3–5 | PLATO transmit rate **75 bps** (3=ON, 4=OFF, 5=ON) |
| 6 | Internal PLATO modem **present** |
| 7 | **Primary** transmit channel |
| 8 | Diagnostic loop **off** |
| 9 | Touch panel **present** |
| 10 | **32K** program memory |

> For direct RS-232 host connection at 1200 bps, S2 positions 3–5 would normally be set for 1200 bps (4=ON, 5=OFF) rather than the current 75 bps. The current S2/S5 settings are consistent with a reverse-channel or modem-based site configuration rather than a direct 1200 bps PLATO host link.

---

## Front panel

Controls, indicators, and switches on the operator panel (figure 2-1 in the 1979 manual).

### Controls

| Control | Type | Function |
|---------|------|----------|
| **Power ON/OFF** | Rocker switch | Main power and circuit breaker. Allow ~45 s after power-on for CRT warmup. |
| **Brightness** | Knob | Adjusts display brightness. Avoid setting too high — reduces focus and shortens CRT life. |
| **RESET** | Push button | Momentary press: re-initializes logic, checksums controlware blocks, auto-reloads any blocks in error. Hold **> 3 seconds**: full logic init, runs resident diagnostics (per rocker switch settings), and autoloads controlware from the PLATO system. |
| **DATA / TALK** | Slide switch | *(Internal modem units only.)* **TALK** routes the phone line to the handset; **DATA** routes it to the internal modem. Set to **DATA** after dial-up connection; set to **TALK** to disconnect. |

### Status LEDs

Six red LEDs on the front panel, left to right as observed on this unit:

| LED | Label | Function |
|-----|-------|----------|
| | **ERR** | Lit when the controller detects an error condition. See maintenance manual section 6 for error codes. |
| | **XMT** | Monitors transmitted data at the shift register output. **Lit** = space (logical 0); **off** = mark (logical 1). |
| | **RCV** | Monitors received data (after carrier detect / DSR gating). **Lit** = space (logical 0); **off** = mark (logical 1). |
| | **RTS** | Request to Send. Normally **lit** when not in test mode. |
| | **DGR** | Likely **DSR** (Data Set Ready) — follows the DSR signal from the PLATO interface connector or internal modem. Lit when modem/interface is ready. |
| | **DTR** | Data Terminal Ready. Normally **lit** when the terminal is powered on. |

All six LEDs can be forced on by pressing and holding **RESET**.

### Rocker switches (behind protective door)

Six rocker switches behind the protective door on the operator panel.

#### Documented functions (1979 manual)

| Switch | ON / up position | OFF / down position | Notes |
|--------|------------------|---------------------|-------|
| **SOFT / LOUD** | Soft (low alarm volume) | Loud (high alarm volume) | |
| **LOOP / EXIT** | Loop — repeat resident diagnostics | Exit — run diagnostics once, then exit | Only active when TEST/SKIP = TEST |
| **KB-TP / SKIP** | KB-TP — run keyboard/touchpanel test | SKIP — bypass KB/TP test | Only active when TEST/SKIP = TEST |
| **TEST / SKIP** | TEST — run resident diagnostics | SKIP — bypass diagnostics, proceed to controlware autoload | Use with LOOP/EXIT |
| *(2 switches)* | *Unassigned in 1979 manual* | *Do not affect operation* | |

Normal operating position: **TEST/SKIP = SKIP**, **LOOP/EXIT = EXIT**, **KB-TP/SKIP = SKIP**.

#### Observed panel labels (physical unit)

Some IST-II units label additional switches not described in the 1979 manual. Labels observed on this terminal:

| Label pair | Likely function | Notes |
|------------|-----------------|-------|
| PLATO / ASCII | Network mode selection | Selects PLATO communication vs ASCII serial channel |
| ODD / EVEN | Parity | Serial channel even/odd parity (when parity enabled) |
| HALF / FULL | Duplex or word format | Possibly half- vs full-duplex or related serial option |
| 7 / *(none)* | Data bits | Possibly 7-bit vs 8-bit serial word length |
| LOUD / SOFT | Alarm volume | Same as documented SOFT/LOUD |
| SKIP / KB-TP | Diagnostic KB/TP test | Same as documented KB-TP/SKIP |
| SKIP / TEST | Diagnostic enable | Same as documented TEST/SKIP |
| HOST / LOCAL | Host vs local operation | Function not in 1979 manual |
| INT / EXT | Internal vs external clock/interface | May relate to clock or modem source |
| NORM / SEL | Normal vs select mode | Function not in 1979 manual |

> The 1979 manual states that several front-panel switches were unassigned; field or later-revision units may wire additional functions. Verify behavior against resident diagnostics before relying on undocumented positions.

---

## Switch bank S2 at G-11

10-position switch **S2** at card location **G-11** on the controller board. Access requires removing the terminal hood.

| Pos | Function | OFF (open) | ON (closed) |
|-----|----------|------------|-------------|
| **1** | ASCII/PLATO communications DTR | Switched | Constant |
| **2** | ASCII/PLATO communications interface | Long line | RS-232 |
| **3–5** | Transmission rate to PLATO network | See table below | |
| **6** | Internal PLATO network modem present | No | Yes |
| **7** | ASCII/PLATO transmit channel | Secondary | Primary |
| **8** | Loop on diagnostic tests | No | Yes |
| **9** | Touch panel present | No | Yes |
| **10** | Bytes of program memory | 16K | 32K |

**S2-7** (primary vs secondary channel) requires **S2-2 = ON** (RS-232 enabled).

### S2-3 / S2-4 / S2-5 — PLATO network transmit rate

Positions **3, 4, 5** select the terminal-to-host transmission rate on the PLATO communication network.

| Pos 3 | Pos 4 | Pos 5 | Rate |
|-------|-------|-------|------|
| 1 | X | 1 | 75 bps |
| 0 | X | 1 | 120 bps |
| X | 1 | 0 | **1200 bps** |
| X | 0 | 0 | External clock input (RJ1-15) |

Direct-connected terminals normally use **1200 bps** (positions 4=ON, 5=OFF). Two-wire reverse-channel site installations often used **120 bps** — confirm with site configuration.

### Recommended direct-connect RS-232 settings

| Switch | Setting |
|--------|---------|
| S2-1 | ON (DTR constant) |
| S2-2 | ON (RS-232) |
| S2-3/4/5 | 1200 bps |
| S2-6 | OFF or ON depending on internal modem installed |
| S2-7 | ON (primary channel) |

> The 1979 hardware manual labels some S2 positions differently (e.g. S2-1 as CTS, S2-6 as serial parity, S2-8 as stop bits). The table above reflects the silkscreen on this unit at G-11.

---

## ROM presence switches

4-position switch on the controller board; one position per ROM socket **ROM 1** through **ROM 4**.

| Position | ROM | OFF (open) | ON (closed) |
|----------|-----|------------|-------------|
| **1** | ROM 1 | Not present | Present |
| **2** | ROM 2 | Not present | Present |
| **3** | ROM 3 | Not present | Present |
| **4** | ROM 4 | Not present | Present |

Set each position to match which ROM chips are physically installed in the corresponding socket.

---

## Switch bank S5 at C-13

8-position switch **S5** at location **C-13** on the controller board. Positions are numbered 1–8.

### Positions 1–4 — default PLATO load file number

Positions **1 and 3** must agree; positions **2 and 4** must agree (redundant pairs).

| Load file # | Pos 1 & 3 | Pos 2 & 4 |
|-------------|-----------|-----------|
| 0 | ON | ON |
| 1 | OFF | ON |
| 2 | ON | OFF |
| 3 | OFF | OFF |

### Positions 6–8 — default ASCII communication data rate

Position **5** is unused. Positions **6, 7, 8** select the default baud rate for the ASCII (serial) communication network.

| Rate | Pos 6 | Pos 7 | Pos 8 |
|------|-------|-------|-------|
| 75 bps | ON | ON | ON |
| 150 bps | ON | ON | OFF |
| 300 bps | ON | OFF | ON |
| 600 bps | ON | OFF | OFF |
| 1200 bps | OFF | ON | ON |
| 2400 bps | OFF | ON | OFF |
| 4800 bps | OFF | OFF | ON |
| External clock input | OFF | OFF | OFF |

---

## Serial channel baud rates (software-selected)

The serial channel (RJ3) supports baud rates selected by program control via the Load Serial Control output, not by a DIP switch:

| Data lines 5/6/7 | Rate |
|------------------|------|
| 000 | 150 bps |
| 001 | 300 bps |
| 010 | 600 bps |
| 011 | 1200 bps |
| 100 | 2400 bps |
| 101 | 4800 bps |
| 110 | 9600 bps |
| 111 | 19200 bps |

Word length (5–8 data bits), parity (even/odd), and stop bits are set under program control via the Load Serial Control output and front-panel mode switches.

---

## PLATO communication interface summary

| Direction | Format | Rate |
|-----------|--------|------|
| Host → terminal (receive) | 21-bit isochronous words | 1200 bps nominal |
| Terminal → host (transmit) | 12-bit async words | 75 / 120 / 1200 bps (S2-3/4/5) |

Interface options: direct RS-232-C (≤ 50 ft) or long line driver (≤ 10,000 ft), selected by **S2-2**.
