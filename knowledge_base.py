"""
RAG-Diag Knowledge Base
~~~~~~~~~~~~~~~~~~~~~~~
Simulated retrieval-augmented knowledge store for hardware diagnostics.
Each hardware system contains a map of known error codes with:
  - Confidence score
  - Issue explanation
  - Resolution steps
  - Safety warning
  - Simulated RAG context sources (technical manual snippets)
"""

import random

SYSTEMS = {
    "ebike": {
        "name": "E-Bike Motor Display",
        "codes": {
            "E01": {
                "confidence": 96,
                "issue": (
                    "Error E01 indicates a communication failure between the main "
                    "controller unit (MCU) and the torque sensor located in the bottom "
                    "bracket assembly. This typically occurs when the sensor's Hall-effect "
                    "signal line experiences intermittent voltage drops below the 2.4V "
                    "threshold required for reliable data transmission. Common root causes "
                    "include corroded connector pins at the J3 harness junction, water "
                    "ingress through a degraded cable grommet, or a failing sensor after "
                    "exceeding 15,000 km of operational use."
                ),
                "steps": [
                    {
                        "title": "Inspect the J3 Harness Connector",
                        "detail": (
                            "Power off the system. Locate the J3 junction connector beneath "
                            "the bottom bracket cover. Disconnect and inspect all 4 pins for "
                            "corrosion, green oxide buildup, or bent contacts. Clean with "
                            "isopropyl alcohol (99%) and a nylon brush."
                        ),
                    },
                    {
                        "title": "Test Torque Sensor Signal Voltage",
                        "detail": (
                            "Using a multimeter set to DC voltage, probe pins 2 (signal) and "
                            "4 (ground) at the J3 connector while slowly rotating the crank "
                            "arm. A healthy sensor outputs 0.8V\u20133.3V proportional to torque. "
                            "Readings below 0.5V or a flat line indicate sensor failure."
                        ),
                    },
                    {
                        "title": "Check Cable Routing & Grommet Seal",
                        "detail": (
                            "Trace the sensor cable from the bottom bracket to the controller "
                            "box. Ensure no sharp bends (minimum bend radius 15mm). Replace "
                            "the cable grommet if the rubber seal shows cracking or deformation."
                        ),
                    },
                    {
                        "title": "Replace Torque Sensor If Faulty",
                        "detail": (
                            "If voltage test fails, replace with OEM part #TS-4420B. After "
                            "installation, perform a sensor calibration via the display menu: "
                            "Settings \u2192 System \u2192 Torque Calibration \u2192 Auto Calibrate."
                        ),
                    },
                ],
                "warning": (
                    "Ensure the battery is fully disconnected (remove the key and unplug "
                    "the XT60 connector) before handling any wiring or sensor components. "
                    "High-voltage DC from the 48V battery pack can cause burns or "
                    "electrical shock."
                ),
                "sources": [
                    {
                        "label": 'Service Manual \u2014 EB-900X Rev.\u00a03, \u00a77.4 "Torque Sensor Diagnostics"',
                        "text": (
                            "\u00a77.4.2 \u2014 The torque sensor (part #TS-4420B) communicates via a "
                            "single analog signal line to the MCU. Expected voltage range "
                            "under load: 0.8V to 3.3V DC. A persistent reading below 0.5V "
                            "for >200ms triggers fault code E01. The J3 connector must "
                            "maintain contact resistance below 50m\u03a9 per pin. Recommended "
                            "service interval: inspect every 5,000 km or 12 months."
                        ),
                    },
                    {
                        "label": 'Technical Bulletin TB-2024-017 "E01 Field Failures"',
                        "text": (
                            "A batch of J3 connectors manufactured between 2023-Q3 and "
                            "2024-Q1 (lot codes JX-7700 through JX-7845) have been identified "
                            "with sub-specification gold plating (< 0.3\u03bcm vs. required "
                            "0.8\u03bcm). This results in accelerated oxidation and intermittent "
                            "E01 faults in humid environments. Affected units should have the "
                            "connector replaced under warranty (ref: RMA-CLASS-B)."
                        ),
                    },
                ],
            },
            "E06": {
                "confidence": 91,
                "issue": (
                    "Error E06 signals a throttle input fault detected by the motor "
                    "controller. The controller has received an out-of-range voltage from "
                    "the thumb or twist throttle \u2014 either exceeding 4.3V (stuck high) or "
                    "remaining below 0.6V at startup (open circuit). This error engages "
                    "the safe-mode lockout, disabling motor assist until the condition is "
                    "resolved. Root causes typically include a damaged throttle "
                    "potentiometer, a pinched signal wire in the handlebar routing, or "
                    "moisture in the throttle connector."
                ),
                "steps": [
                    {
                        "title": "Perform Throttle Voltage Check",
                        "detail": (
                            "With the system powered on and in diagnostic mode, measure the "
                            "voltage at the throttle connector (3-pin JST). Pin 1 is 5V "
                            "supply, Pin 2 is signal, Pin 3 is ground. At rest, the signal "
                            "should read 0.8V \u00b1 0.1V. At full throttle, it should read "
                            "4.1V \u00b1 0.1V."
                        ),
                    },
                    {
                        "title": "Inspect Wiring at Handlebar Pass-Through",
                        "detail": (
                            "Remove the handlebar grip or housing cover. Check the throttle "
                            "cable where it passes through the clamp area \u2014 this is the most "
                            "common pinch point. Look for flattened insulation or exposed "
                            "copper strands."
                        ),
                    },
                    {
                        "title": "Dry and Reseat the Throttle Connector",
                        "detail": (
                            "Disconnect the 3-pin JST connector. Blow out any moisture with "
                            "compressed air. Apply a thin layer of dielectric grease to the "
                            "connector pins before reconnecting. Ensure the locking tab "
                            "clicks firmly."
                        ),
                    },
                    {
                        "title": "Replace Throttle Assembly If Needed",
                        "detail": (
                            "If the voltage output remains out-of-range after inspection, "
                            "replace with OEM throttle assembly #TH-120R. After installation, "
                            "cycle the throttle 5 times through full range to allow the "
                            "controller to re-learn the min/max calibration points."
                        ),
                    },
                ],
                "warning": (
                    "Do not ride the e-bike while error E06 is active. The motor could "
                    "engage unexpectedly if the throttle signal fluctuates. Keep the bike "
                    "stationary and elevated on a work stand during all troubleshooting."
                ),
                "sources": [
                    {
                        "label": 'Service Manual \u2014 EB-900X Rev.\u00a03, \u00a76.2 "Throttle Input Circuit"',
                        "text": (
                            "\u00a76.2.1 \u2014 The throttle input is a 3-wire potentiometer circuit. "
                            "Supply: 5.0V regulated. Signal output range: 0.7V (idle) to "
                            "4.2V (max). The controller samples the signal at 100Hz with a "
                            "4-sample moving average filter. An out-of-range condition "
                            "(< 0.5V or > 4.4V) sustained for 500ms triggers E06 and engages "
                            "safe-mode lockout."
                        ),
                    },
                    {
                        "label": 'Field Note FN-2023-042 "Throttle Connector Moisture Ingress"',
                        "text": (
                            "In field conditions with sustained rainfall or power-washing, "
                            "water can migrate along the throttle cable via capillary action "
                            "and pool in the JST connector housing. Symptoms: intermittent "
                            "E06 faults, particularly after wet rides. Preventive measure: "
                            "apply marine-grade dielectric grease (MIL-S-8660C compliant) to "
                            "all exposed connector housings during annual service."
                        ),
                    },
                ],
            },
        },
    },
    "washer": {
        "name": "Washer-Dryer Unit",
        "codes": {
            "F18": {
                "confidence": 94,
                "issue": (
                    "Error code F18 indicates a water drainage timeout. The control board "
                    "has detected that the drum water level sensor still reads above the "
                    "\u2018empty\u2019 threshold after running the drain pump for the maximum "
                    "allotted cycle time (typically 4 minutes). This prevents the unit "
                    "from advancing to the spin cycle. The most common causes are a "
                    "blocked drain filter, a kinked or obstructed drain hose, or a failing "
                    "drain pump impeller. In rare cases, the pressure switch tube can "
                    "become partially clogged with detergent residue, causing a false "
                    "high-water reading."
                ),
                "steps": [
                    {
                        "title": "Clean the Drain Filter",
                        "detail": (
                            "Locate the drain filter access panel on the front-lower-right "
                            "of the unit. Place towels and a shallow container beneath it. "
                            "Turn the filter cap counter-clockwise slowly to release residual "
                            "water. Remove the filter and clear any debris \u2014 coins, lint "
                            "buildup, and small fabric items are common obstructions."
                        ),
                    },
                    {
                        "title": "Inspect the Drain Hose",
                        "detail": (
                            "Pull the unit away from the wall (disconnect power first). Check "
                            "the drain hose from the pump outlet to the standpipe for kinks, "
                            "sharp bends, or internal blockages. The hose end should be "
                            "inserted 15\u201320 cm into the standpipe, no more. Blow through the "
                            "hose to confirm airflow."
                        ),
                    },
                    {
                        "title": "Test the Drain Pump",
                        "detail": (
                            "Access the pump via the lower front panel. With the unit plugged "
                            "in and in a drain-only test cycle (hold Start + Spin Speed for "
                            "3 seconds), listen for the pump motor. A healthy pump produces a "
                            "steady hum. Grinding, clicking, or silence indicates a failed "
                            "impeller or motor. Measure pump resistance: 120\u2013180\u03a9 across "
                            "motor terminals is normal."
                        ),
                    },
                    {
                        "title": "Clear the Pressure Switch Tube",
                        "detail": (
                            "Locate the small rubber tube running from the tub to the "
                            "pressure switch on the control board housing. Disconnect both "
                            "ends and blow through it with low-pressure air. Residual "
                            "detergent or scale can create partial blockages that cause false "
                            "water-level readings."
                        ),
                    },
                ],
                "warning": (
                    "Unplug the washer-dryer unit from the mains power outlet before "
                    "accessing any internal components. Residual water in the drum and "
                    "drain system may spill when the filter is opened \u2014 have towels and a "
                    "container ready. Do not tip the unit while water remains inside."
                ),
                "sources": [
                    {
                        "label": 'Service Manual \u2014 WD-8800 Series, \u00a712.3 "Drain System Faults"',
                        "text": (
                            "\u00a712.3.4 \u2014 Code F18 is generated when the drain routine exceeds "
                            "the configurable timeout (default: 240 seconds, adjustable in "
                            "service mode via P12 parameter). The analog pressure switch "
                            "outputs 0\u20135V proportional to water height. The \u2018empty\u2019 threshold "
                            "is calibrated at < 0.4V. If the reading remains above 0.4V at "
                            "timeout expiry, the PCB logs F18 and halts the cycle."
                        ),
                    },
                    {
                        "label": 'Technical Service Bulletin TSB-WD-2024-003 "Drain Pump Impeller Wear"',
                        "text": (
                            "Units with serial numbers WD88-2022xxxxx through WD88-2023xxxxx "
                            "may experience premature impeller wear due to a material defect "
                            "in the injection-molded impeller blade (polypropylene blend with "
                            "insufficient glass-fiber reinforcement). Symptoms include "
                            "progressively slower drainage and eventual F18 errors. "
                            "Replacement pump assembly (part #DP-660A) has been revised with "
                            "30% glass-fill PP. Warranty: extended to 5 years from date of "
                            "manufacture."
                        ),
                    },
                ],
            },
            "E03": {
                "confidence": 89,
                "issue": (
                    "Error E03 indicates a door lock mechanism failure. The control board "
                    "is unable to confirm that the door latch solenoid has engaged, which "
                    "prevents the wash cycle from starting as a safety interlock. This can "
                    "be caused by a fatigued door latch solenoid (common after ~50,000 "
                    "cycles), a misaligned door strike plate, or a wiring fault in the "
                    "door lock harness connector. In some cases, a swollen or warped door "
                    "gasket can prevent the door from closing flush enough to trigger the "
                    "micro-switch."
                ),
                "steps": [
                    {
                        "title": "Check Door Alignment",
                        "detail": (
                            "Open and close the door slowly, observing the latch mechanism. "
                            "The door hook should engage the strike plate smoothly without "
                            "resistance. If the door appears to hang lower than the aperture, "
                            "the hinge pins may be worn \u2014 inspect for play in the upper and "
                            "lower hinge assemblies."
                        ),
                    },
                    {
                        "title": "Inspect the Door Lock Solenoid",
                        "detail": (
                            "Remove the front panel retaining screws (T20 Torx). Locate the "
                            "door lock assembly (upper-right of the door opening). Disconnect "
                            "the 5-pin connector and measure solenoid resistance: "
                            "900\u20131200\u03a9 is within spec. A reading above 2000\u03a9 or open circuit "
                            "indicates a failed solenoid coil."
                        ),
                    },
                    {
                        "title": "Examine the Door Gasket",
                        "detail": (
                            "Check the rubber door gasket (bellows) around the entire "
                            "circumference. Look for swelling, deformation, or foreign "
                            "objects trapped in the folds. A compressed or swollen gasket can "
                            "prevent the door from closing the final 2\u20133mm needed to trigger "
                            "the micro-switch."
                        ),
                    },
                    {
                        "title": "Replace Door Lock Assembly",
                        "detail": (
                            "If the solenoid has failed, replace with part #DL-440C. After "
                            "installation, run the service mode self-test (press Power + "
                            "Option 3\u00d7 within 5 seconds) to verify the lock engages and the "
                            "micro-switch reports \u2018closed\u2019 status."
                        ),
                    },
                ],
                "warning": (
                    "Never attempt to force the door open during a wash cycle if the lock "
                    "is engaged. The door interlock is a safety-critical component \u2014 wait "
                    "for the unit to fully drain and cool (3-minute delay after cycle end) "
                    "before opening."
                ),
                "sources": [
                    {
                        "label": 'Service Manual \u2014 WD-8800 Series, \u00a79.1 "Door Interlock System"',
                        "text": (
                            "\u00a79.1.2 \u2014 The door lock assembly consists of a bimetallic "
                            "actuator (PTC heater) and a solenoid latch. Upon receiving the "
                            "lock command, the PTC element heats and deflects the bimetallic "
                            "strip, which mechanically pushes the latch pin into the door "
                            "hook. Confirmation is provided by a micro-switch (NO contact) "
                            "that closes when the pin reaches full extension. If the "
                            "micro-switch does not close within 8 seconds of the lock "
                            "command, E03 is logged."
                        ),
                    },
                    {
                        "label": 'Repair Note RN-2024-WD-019 "Door Gasket Interference"',
                        "text": (
                            "On units installed in high-humidity environments (>70% RH "
                            "sustained), the EPDM door gasket may absorb moisture and swell "
                            "by 3\u20135mm beyond nominal dimensions. This can cause intermittent "
                            "E03 errors as the door fails to close flush. Recommended fix: "
                            "replace with the silicone gasket variant (part #DG-220S) which "
                            "has <0.5% moisture absorption. Applies to all WD-8800 units "
                            "regardless of serial number."
                        ),
                    },
                ],
            },
        },
    },
    "smarthome": {
        "name": "Smart Home Hub",
        "codes": {
            "503": {
                "confidence": 92,
                "issue": (
                    "Error 503 (Service Unavailable) from the Smart Home Hub indicates "
                    "that the hub\u2019s internal microservice responsible for cloud "
                    "synchronization has crashed or is unresponsive. The hub runs a "
                    "lightweight container runtime, and the cloud-sync service (process: "
                    "`shh-cloudd`) has failed its internal health check for 3 consecutive "
                    "intervals (15-second cadence). Common causes include a corrupted "
                    "local device-state database (SQLite), insufficient free storage on "
                    "the eMMC module (< 50MB triggers service suspension), or a TLS "
                    "certificate expiration preventing handshake with the cloud endpoint."
                ),
                "steps": [
                    {
                        "title": "Perform a Soft Reboot of the Hub",
                        "detail": (
                            "Press and hold the side button for 5 seconds until the LED ring "
                            "pulses blue. Release and wait 90 seconds for the full boot "
                            "sequence. This restarts all microservices including `shh-cloudd` "
                            "without erasing device pairings. Check if the LED returns to "
                            "solid white (normal) or flashing red (persistent error)."
                        ),
                    },
                    {
                        "title": "Check Available Storage",
                        "detail": (
                            "Open the companion app \u2192 Hub Settings \u2192 System Info \u2192 Storage. "
                            "If available storage is below 100MB, clear the diagnostic log "
                            "cache: Hub Settings \u2192 Advanced \u2192 Clear System Logs. This can "
                            "free 200\u2013500MB. If storage remains critical, a factory-reset "
                            "with cloud restore may be necessary."
                        ),
                    },
                    {
                        "title": "Verify Network & Certificate Status",
                        "detail": (
                            "In the companion app, navigate to Hub Settings \u2192 Network \u2192 "
                            "Cloud Connection Status. Look for \u2018Certificate Status: Valid\u2019 "
                            "and \u2018Last Sync\u2019 timestamp. If the certificate shows \u2018Expired\u2019 "
                            "or \u2018Invalid,\u2019 force a certificate refresh: Hub Settings \u2192 "
                            "Advanced \u2192 Security \u2192 Renew Certificates. The hub requires a "
                            "stable internet connection (>2 Mbps) during this process."
                        ),
                    },
                    {
                        "title": "Reset the Cloud Sync Database",
                        "detail": (
                            "If the above steps fail, the local sync database may be "
                            "corrupted. Go to Hub Settings \u2192 Advanced \u2192 Cloud Sync \u2192 Reset "
                            "Sync Database. This forces a full re-sync of all device states "
                            "from the cloud. Warning: this process takes 5\u201315 minutes "
                            "depending on the number of paired devices and may cause brief "
                            "automation interruptions."
                        ),
                    },
                ],
                "warning": (
                    "Do not perform a factory reset without first ensuring your device "
                    "list and automation rules are backed up to the cloud (Hub Settings \u2192 "
                    "Backup \u2192 Create Backup). A factory reset without cloud backup will "
                    "permanently erase all locally stored device pairings and custom "
                    "routines."
                ),
                "sources": [
                    {
                        "label": 'Smart Home Hub Developer Guide v4.2, \u00a718.5 "Cloud Sync Service"',
                        "text": (
                            "\u00a718.5.3 \u2014 The cloud sync daemon (`shh-cloudd`) runs as a "
                            "containerized service with a 256MB memory limit. It maintains a "
                            "persistent WebSocket connection to the cloud broker (endpoint: "
                            "wss://sync.hub-cloud.io). Health checks run every 15 seconds; "
                            "3 consecutive failures trigger service suspension and surface "
                            "error 503 to the user via the LED ring (pattern: 3 red flashes) "
                            "and companion app notification."
                        ),
                    },
                    {
                        "label": 'Known Issue KI-HUB-2024-088 "eMMC Storage Exhaustion"',
                        "text": (
                            "Hub firmware versions 4.1.0 through 4.1.7 contain a logging "
                            "regression where the `shh-cloudd` process writes verbose debug "
                            "logs to /var/log/cloudd/ without rotation. On hubs with 4GB "
                            "eMMC, this can exhaust available storage within 6\u20138 months of "
                            "continuous operation. Fixed in firmware 4.2.0 (log rotation "
                            "enabled, max 50MB). Affected users should update firmware and "
                            "clear legacy logs."
                        ),
                    },
                ],
            },
            "701": {
                "confidence": 87,
                "issue": (
                    "Error 701 indicates a Zigbee radio module initialization failure. "
                    "The hub\u2019s Zigbee 3.0 transceiver (Silicon Labs EFR32MG21) has failed "
                    "to initialize during boot or has lost communication with the main "
                    "application processor via the UART bridge. This results in all "
                    "Zigbee-connected devices (lights, sensors, locks) appearing as "
                    "\u2018offline.\u2019 Causes include a firmware mismatch between the radio "
                    "module and the host controller, an ESD event corrupting the radio\u2019s "
                    "flash memory, or a hardware fault on the UART data lines."
                ),
                "steps": [
                    {
                        "title": "Power Cycle the Hub Completely",
                        "detail": (
                            "Unplug the hub\u2019s USB-C power supply from the wall, wait 30 "
                            "seconds, then reconnect. A full power cycle resets the Zigbee "
                            "radio module\u2019s state machine. Watch the LED ring: a solid green "
                            "flash during boot (at ~20 seconds) confirms the Zigbee radio "
                            "has initialized. Absence of the green flash confirms a "
                            "persistent radio fault."
                        ),
                    },
                    {
                        "title": "Update Hub Firmware",
                        "detail": (
                            "Ensure the hub is running the latest firmware. Open the "
                            "companion app \u2192 Hub Settings \u2192 System \u2192 Firmware Update. If an "
                            "update is available, install it \u2014 radio module firmware is "
                            "bundled with host updates. The update process takes 4\u20138 "
                            "minutes; do not disconnect power during this time."
                        ),
                    },
                    {
                        "title": "Reset the Zigbee Network",
                        "detail": (
                            "If the radio initializes (green flash seen) but devices remain "
                            "offline, the Zigbee network key may be corrupted. Go to Hub "
                            "Settings \u2192 Zigbee \u2192 Reset Zigbee Network. This erases the "
                            "network key and forces all devices to re-pair. You will need to "
                            "re-pair each Zigbee device individually afterward."
                        ),
                    },
                    {
                        "title": "Contact Support for Hardware RMA",
                        "detail": (
                            "If error 701 persists after firmware update and full power cycle "
                            "(no green flash at boot), the Zigbee radio module likely has a "
                            "hardware fault. Contact support with the hub\u2019s serial number "
                            "(found on the base label) and diagnostic report (Hub Settings \u2192 "
                            "Support \u2192 Generate Report) for an RMA replacement."
                        ),
                    },
                ],
                "warning": (
                    "Resetting the Zigbee network (Step 3) will disconnect ALL Zigbee "
                    "devices from the hub. All devices will need to be individually "
                    "re-paired, which may take significant time for large installations "
                    "(30+ devices). Ensure you have a list of all paired devices before "
                    "proceeding."
                ),
                "sources": [
                    {
                        "label": 'Smart Home Hub Hardware Reference v2.1, \u00a74.3 "Zigbee Radio Module"',
                        "text": (
                            "\u00a74.3.1 \u2014 The Zigbee radio module (EFR32MG21, 1024kB Flash, "
                            "96kB RAM) communicates with the host processor (NXP i.MX6ULL) "
                            "via UART at 115200 baud (8N1). Initialization sequence: host "
                            "sends 0xAA55 magic bytes \u2192 radio responds with version string "
                            "within 2 seconds \u2192 host sends network configuration \u2192 radio "
                            "confirms with 0x06 ACK. Failure at any stage triggers error 701."
                        ),
                    },
                    {
                        "label": 'Service Bulletin SB-HUB-2024-014 "ESD Vulnerability"',
                        "text": (
                            "Hubs deployed in dry-climate environments (relative humidity "
                            "< 30%) have shown increased incidence of error 701 due to "
                            "electrostatic discharge events during user interaction. The "
                            "EFR32MG21 module\u2019s GPIO bank is susceptible to ESD above 2kV "
                            "HBM. Revision C hardware (serial prefix SHH-C-) includes TVS "
                            "diode protection on all exposed lines. Revision A/B units may "
                            "experience intermittent or permanent radio failure under ESD "
                            "exposure."
                        ),
                    },
                ],
            },
        },
    },
}


def generate_fallback(system_key: str, code_str: str) -> dict:
    """Generate a plausible diagnostic for an unknown error code."""
    system_name = SYSTEMS.get(system_key, {}).get("name", "Unknown System")
    confidence = random.randint(72, 86)

    return {
        "confidence": confidence,
        "issue": (
            f'Error code "{code_str}" on the {system_name} does not match a known '
            f"fault in the primary diagnostic database. Based on pattern analysis, "
            f"this may indicate a transient communication fault between subsystem "
            f"modules or an undocumented OEM-specific code introduced in a recent "
            f"firmware revision. A general diagnostic procedure is recommended to "
            f"isolate the root cause."
        ),
        "steps": [
            {
                "title": "Perform a Full Power Cycle",
                "detail": (
                    f"Completely disconnect the {system_name} from its power source. "
                    f"Wait at least 60 seconds to allow all capacitors to discharge and "
                    f"volatile memory to clear. Reconnect power and observe the startup "
                    f"sequence for any additional error codes or abnormal behavior."
                ),
            },
            {
                "title": "Check for Firmware Updates",
                "detail": (
                    f"Verify that the {system_name} is running the latest available "
                    f"firmware or software version. Outdated firmware is a common source "
                    f"of unrecognized error codes, especially after interoperability "
                    f"changes in connected subsystems."
                ),
            },
            {
                "title": "Inspect All Physical Connections",
                "detail": (
                    "Examine all cable connections, sensor leads, and communication "
                    "harnesses for loose or corroded contacts. Reseat each connector "
                    "firmly. Pay special attention to any connectors exposed to "
                    "environmental stress (vibration, moisture, temperature cycling)."
                ),
            },
            {
                "title": "Contact Manufacturer Technical Support",
                "detail": (
                    f'If the error persists after the above steps, contact the '
                    f'manufacturer\'s technical support line with the specific code '
                    f'"{code_str}", the unit\'s serial number, and a description of the '
                    f"operating conditions when the error appeared. Request a diagnostic "
                    f"log download if supported."
                ),
            },
        ],
        "warning": (
            f"Always disconnect the {system_name} from its power source before "
            f"inspecting internal wiring or components. Follow all manufacturer "
            f"safety guidelines in the user manual. If the device is under warranty, "
            f"do not disassemble it \u2014 contact the manufacturer directly."
        ),
        "sources": [
            {
                "label": (
                    f'General Troubleshooting Guide \u2014 {system_name}, '
                    f'\u00a71.1 "Initial Diagnostics"'
                ),
                "text": (
                    "\u00a71.1.1 \u2014 When encountering an unrecognized error code, the "
                    "recommended initial approach is to perform a full power-cycle reset "
                    "and document the exact operating state (cycle phase, load "
                    "conditions, ambient temperature) at the time of the fault. This "
                    "information is critical for root-cause analysis by the engineering "
                    "support team."
                ),
            },
            {
                "label": "OEM Firmware Release Notes \u2014 Latest Version",
                "text": (
                    "Recent firmware updates may introduce new diagnostic codes or "
                    f"reclassify existing ones. Cross-reference the error code "
                    f'"{code_str}" with the latest release notes available on the '
                    f"manufacturer\u2019s support portal. Some codes are intentionally "
                    f"undocumented in user-facing manuals and require service-level "
                    f"access for detailed interpretation."
                ),
            },
        ],
    }


def lookup_diagnostic(system_key: str, error_code: str) -> dict | None:
    """Look up a known diagnostic or return None."""
    import re

    # Strip common prefixes like "Error ", "Code ", "Fault "
    normalized = re.sub(r"^(error\s*|code\s*|fault\s*)", "", error_code, flags=re.IGNORECASE).strip().upper()

    system = SYSTEMS.get(system_key)
    if not system:
        return None

    return system["codes"].get(normalized)
