from knowledge_base.engine import Rule


def load_all_rules(expert):
    """Loads the knowledge base into the expert system."""

    # ==========================================
    # PHASE 1: TIER ABSTRACTION
    # ==========================================
    expert.add_rule(Rule("R1", lambda f: f.get("Budget", 0) < 600,
                         lambda f: f.update({"Tier": "Entry"}),
                         "A budget under $600 restricts the build to entry-level architecture.", cf=1.0))

    expert.add_rule(Rule("R2", lambda f: 600 <= f.get("Budget", 0) < 1000,
                         lambda f: f.update({"Tier": "Mid-Range"}),
                         "A budget between $600 and $1000 determines a Mid-Range system architecture.", cf=1.0))

    expert.add_rule(Rule("R3", lambda f: 1000 <= f.get("Budget", 0) < 1800,
                         lambda f: f.update({"Tier": "High-End"}),
                         "A budget between $1000 and $1800 allows for High-End components.", cf=1.0))

    expert.add_rule(Rule("R4", lambda f: f.get("Budget", 0) >= 1800,
                         lambda f: f.update({"Tier": "Enthusiast"}),
                         "A budget over $1800 unlocks Enthusiast-tier 4K performance.", cf=1.0))

    # ==========================================
    # PHASE 2: CPU SELECTION & TDP
    # ==========================================
    expert.add_rule(Rule("R5", lambda f: f.get("Tier") == "Entry" and f.get("Preference") == "AMD",
                         lambda f: f.update({"CPU": "Ryzen 5 4500", "CPU_TDP": 65}),
                         "The Ryzen 5 4500 is selected for entry-level AMD setups.", cf=0.90))

    expert.add_rule(Rule("R6", lambda f: f.get("Tier") == "Entry" and f.get("Preference") != "AMD",
                         lambda f: f.update({"CPU": "Core i3-12100F", "CPU_TDP": 58}),
                         "The Core i3-12100F is the optimal budget processor for Intel/No Preference builds.", cf=0.95))

    expert.add_rule(Rule("R7", lambda f: f.get("Tier") == "Mid-Range" and f.get("Preference") == "AMD",
                         lambda f: f.update({"CPU": "Ryzen 5 5600", "CPU_TDP": 65}),
                         "The Ryzen 5 5600 provides peak price-to-performance for mid-range AMD builds.", cf=0.98))

    expert.add_rule(Rule("R8", lambda f: f.get("Tier") == "Mid-Range" and f.get("Preference") != "AMD",
                         lambda f: f.update({"CPU": "Core i5-12400F", "CPU_TDP": 65}),
                         "The Core i5-12400F offers robust 6-core performance for mid-range Intel builds.", cf=0.95))

    expert.add_rule(Rule("R9", lambda f: f.get("Tier") == "High-End" and f.get("Preference") == "AMD",
                         lambda f: f.update({"CPU": "Ryzen 7 7700X", "CPU_TDP": 105}),
                         "The Ryzen 7 7700X provides excellent multi-core scaling for high-end systems.", cf=0.90))

    expert.add_rule(Rule("R10", lambda f: f.get("Tier") == "High-End" and f.get("Preference") != "AMD",
                         lambda f: f.update({"CPU": "Core i5-13600K", "CPU_TDP": 181}),
                         "The i5-13600K is a high-end powerhouse for 1440p gaming.", cf=0.95))

    expert.add_rule(Rule("R11", lambda f: f.get("Tier") == "Enthusiast" and f.get("Preference") == "AMD",
                         lambda f: f.update({"CPU": "Ryzen 7 7800X3D", "CPU_TDP": 120}),
                         "The 7800X3D utilizes 3D V-Cache to deliver the fastest gaming performance available.",
                         cf=0.99))

    expert.add_rule(Rule("R12", lambda f: f.get("Tier") == "Enthusiast" and f.get("Preference") != "AMD",
                         lambda f: f.update({"CPU": "Core i9-14900K", "CPU_TDP": 253}),
                         "The i9-14900K is selected for uncompromised enthusiast performance.", cf=0.95))

    # ==========================================
    # PHASE 3: GPU SELECTION (CHAINED TO CPU)
    # ==========================================
    expert.add_rule(Rule("R13", lambda f: f.get("CPU") == "Ryzen 5 4500" or f.get("CPU") == "Core i3-12100F",
                         lambda f: f.update({"GPU": "Radeon RX 6600", "GPU_TDP": 132}),
                         "The RX 6600 pairs well with entry CPUs to maximize budget frame rates.", cf=0.92))

    expert.add_rule(Rule("R14", lambda f: f.get("CPU") == "Ryzen 5 5600" or f.get("CPU") == "Core i5-12400F",
                         lambda f: f.update({"GPU": "Radeon RX 6600 XT", "GPU_TDP": 160}),
                         "The RX 6600 XT pairs seamlessly with mid-range CPUs to prevent bottlenecks at 1080p.",
                         cf=0.95))

    expert.add_rule(Rule("R15", lambda f: f.get("Tier") == "High-End" and f.get("Preference") == "AMD",
                         lambda f: f.update({"GPU": "Radeon RX 7800 XT", "GPU_TDP": 263}),
                         "The 7800 XT dominates 1440p rasterization in high-end AMD systems.", cf=0.90))

    expert.add_rule(Rule("R16", lambda f: f.get("Tier") == "High-End" and f.get("Preference") != "AMD",
                         lambda f: f.update({"GPU": "GeForce RTX 4070 Super", "GPU_TDP": 220}),
                         "The RTX 4070 Super is selected for high-end ray tracing and DLSS support.", cf=0.93))

    expert.add_rule(Rule("R17", lambda f: f.get("Tier") == "Enthusiast" and f.get("Preference") == "AMD",
                         lambda f: f.update({"GPU": "Radeon RX 7900 XTX", "GPU_TDP": 355}),
                         "The 7900 XTX provides flagship AMD graphics performance for 4K rendering.", cf=0.96))

    expert.add_rule(Rule("R18", lambda f: f.get("Tier") == "Enthusiast" and f.get("Preference") != "AMD",
                         lambda f: f.update({"GPU": "GeForce RTX 4090", "GPU_TDP": 450}),
                         "The RTX 4090 is the undisputed tier leader for enthusiast 4K gaming.", cf=1.0))

    # ==========================================
    # PHASE 4: MOTHERBOARD & RAM CHAINING
    # ==========================================
    expert.add_rule(Rule("R19", lambda f: f.get("CPU") in ["Ryzen 5 4500", "Ryzen 5 5600"],
                         lambda f: f.update({"Socket": "AM4", "RAM_Type": "DDR4"}),
                         "Selected CPU requires the AM4 Socket and DDR4 memory architecture.", cf=1.0))

    expert.add_rule(Rule("R20", lambda f: f.get("CPU") in ["Ryzen 7 7700X", "Ryzen 7 7800X3D"],
                         lambda f: f.update({"Socket": "AM5", "RAM_Type": "DDR5"}),
                         "Selected CPU requires the next-generation AM5 Socket and DDR5 memory.", cf=1.0))

    expert.add_rule(Rule("R21", lambda f: "Core" in str(f.get("CPU", "")),
                         lambda f: f.update({"Socket": "LGA1700"}),
                         "Selected Intel CPU utilizes the LGA1700 Socket.", cf=1.0))

    expert.add_rule(Rule("R22", lambda f: f.get("Socket") == "LGA1700" and f.get("Tier") in ["Entry", "Mid-Range"],
                         lambda f: f.update({"RAM_Type": "DDR4"}),
                         "DDR4 memory is selected to keep Intel LGA1700 builds within budget constraints.", cf=0.90))

    expert.add_rule(Rule("R23", lambda f: f.get("Socket") == "LGA1700" and f.get("Tier") in ["High-End", "Enthusiast"],
                         lambda f: f.update({"RAM_Type": "DDR5"}),
                         "DDR5 memory is selected to maximize high-end Intel performance.", cf=0.98))

    expert.add_rule(Rule("R24", lambda f: f.get("Socket") == "AM4",
                         lambda f: f.update({"Motherboard": "B550 ATX"}),
                         "A B550 motherboard is assigned for AM4 stability and PCIe 4.0 support.", cf=0.95))

    expert.add_rule(Rule("R25", lambda f: f.get("Socket") == "AM5",
                         lambda f: f.update({"Motherboard": "B650 ATX"}),
                         "A B650 motherboard is assigned for AM5 architecture.", cf=0.90))

    expert.add_rule(Rule("R26", lambda f: f.get("Socket") == "LGA1700" and f.get("Tier") in ["High-End", "Enthusiast"],
                         lambda f: f.update({"Motherboard": "Z790 ATX"}),
                         "A Z790 motherboard is required to support Intel CPU overclocking.", cf=0.98))

    expert.add_rule(
        Rule("R27", lambda f: f.get("Socket") == "LGA1700" and f.get("Tier") not in ["High-End", "Enthusiast"],
             lambda f: f.update({"Motherboard": "B760 ATX"}),
             "A B760 motherboard provides solid baseline features for locked Intel processors.", cf=0.95))

    # ==========================================
    # PHASE 5: POWER SUPPLY (MATH INFERENCE)
    # ==========================================
    expert.add_rule(Rule("R28", lambda f: "CPU_TDP" in f and "GPU_TDP" in f,
                         lambda f: f.update({"Total_System_TDP": f["CPU_TDP"] + f["GPU_TDP"] + 100}),
                         "Calculated total system wattage (CPU + GPU + 100W buffer for fans/storage).", cf=1.0))

    expert.add_rule(Rule("R29", lambda f: f.get("Total_System_TDP", 0) > 0 and f.get("Total_System_TDP", 0) < 400,
                         lambda f: f.update({"Power_Supply": "550W 80+ Bronze"}),
                         "Assigned a 550W PSU to safely cover sub-400W system draw.", cf=0.95))

    expert.add_rule(Rule("R30", lambda f: f.get("Total_System_TDP", 0) >= 400 and f.get("Total_System_TDP", 0) < 600,
                         lambda f: f.update({"Power_Supply": "750W 80+ Gold"}),
                         "Assigned a 750W Gold PSU for mid-range power efficiency and headroom.", cf=0.98))

    expert.add_rule(Rule("R31", lambda f: f.get("Total_System_TDP", 0) >= 600,
                         lambda f: f.update({"Power_Supply": "1000W 80+ Gold"}),
                         "Assigned a 1000W PSU to handle enthusiast-level transient power spikes.", cf=0.95))

    # ==========================================
    # PHASE 6: CONFLICT RESOLUTION (Priority 10)
    # ==========================================
    expert.add_rule(Rule("R32_Conflict",
                         lambda f: f.get("Budget", 0) < 800 and f.get("Target_Resolution") in ["1440p", "4K"],
                         lambda f: f.update({"Target_Resolution": "1080p", "Conflict": True}),
                         "CONFLICT OVERRIDE: Budget cannot physically render higher resolutions reliably. Resolution downgraded to 1080p.",
                         priority=10, cf=0.99))

    expert.add_rule(Rule("R33_Conflict",
                         lambda f: f.get("Size") == "Small" and f.get("CPU") == "Core i9-14900K",
                         lambda f: f.update({"CPU": "Ryzen 7 7800X3D", "Conflict": True}),
                         "CONFLICT OVERRIDE: The i9 generates excessive heat for an ITX case. Swapped to the highly efficient 7800X3D.",
                         priority=10, cf=0.95))

    # ==========================================
    # PHASE 7: STORAGE ARCHITECTURE
    # ==========================================
    expert.add_rule(Rule("R34", lambda f: f.get("Tier") == "Entry",
                         lambda f: f.update({"Storage": "500GB NVMe Gen 3 SSD"}),
                         "A 500GB Gen 3 NVMe provides essential, budget-friendly fast storage for OS and core games.",
                         cf=0.85))

    expert.add_rule(Rule("R35", lambda f: f.get("Tier") == "Mid-Range",
                         lambda f: f.update({"Storage": "1TB NVMe Gen 4 SSD"}),
                         "A 1TB Gen 4 NVMe leverages the B550/B760 motherboard bandwidth for faster load times.",
                         cf=0.95))

    expert.add_rule(Rule("R36", lambda f: f.get("Tier") == "High-End",
                         lambda f: f.update({"Storage": "2TB NVMe Gen 4 SSD"}),
                         "A 2TB Gen 4 drive is standard for high-end builds to hold massive modern AAA game libraries.",
                         cf=0.98))

    expert.add_rule(Rule("R37", lambda f: f.get("Tier") == "Enthusiast",
                         lambda f: f.update({"Storage": "4TB NVMe Gen 4 SSD (or 2x 2TB)"}),
                         "Enthusiast architectures require massive, high-speed arrays for uncompromised 4K asset loading.",
                         cf=0.90))

    # ==========================================
    # PHASE 8: MEMORY CAPACITY & SPEED
    # ==========================================
    expert.add_rule(Rule("R38", lambda f: f.get("Tier") == "Entry" and f.get("RAM_Type") == "DDR4",
                         lambda f: f.update({"Memory_Kit": "16GB (2x8GB) 3200MHz"}),
                         "16GB of 3200MHz DDR4 is the baseline requirement to avoid stuttering in modern entry-level titles.",
                         cf=0.95))

    expert.add_rule(Rule("R39", lambda f: f.get("Tier") == "Mid-Range" and f.get("RAM_Type") == "DDR4",
                         lambda f: f.update({"Memory_Kit": "16GB (2x8GB) 3600MHz"}),
                         "3600MHz DDR4 is the sweet spot for maximizing the infinity fabric performance of mid-range Ryzen and Intel CPUs.",
                         cf=0.90))

    expert.add_rule(Rule("R40", lambda f: f.get("Tier") == "High-End" and f.get("RAM_Type") == "DDR5",
                         lambda f: f.update({"Memory_Kit": "32GB (2x16GB) 6000MHz CL30"}),
                         "32GB of low-latency 6000MHz DDR5 ensures high-refresh-rate 1440p gaming remains bottleneck-free.",
                         cf=0.98))

    expert.add_rule(Rule("R41", lambda f: f.get("Tier") == "Enthusiast" and f.get("RAM_Type") == "DDR5",
                         lambda f: f.update({"Memory_Kit": "64GB (2x32GB) 6000MHz+ CL30"}),
                         "64GB of premium DDR5 memory handles extreme 4K gaming and heavy background multitasking seamlessly.",
                         cf=0.90))

    # ==========================================
    # PHASE 9: THERMAL COOLING SOLUTIONS
    # ==========================================
    expert.add_rule(Rule("R42", lambda f: f.get("CPU_TDP", 0) > 0 and f.get("CPU_TDP", 0) <= 65,
                         lambda f: f.update({"CPU_Cooler": "Included Stock Cooler or $20 Air Tower"}),
                         "CPUs at or below 65W TDP generate minimal heat; a basic air cooler is entirely sufficient.",
                         cf=0.99))

    expert.add_rule(Rule("R43", lambda f: f.get("CPU_TDP", 0) > 65 and f.get("CPU_TDP", 0) <= 120,
                         lambda f: f.update({"CPU_Cooler": "High-Performance Dual Tower Air Cooler"}),
                         "CPUs in the 100W+ range require robust dual-tower air cooling to maintain boost clocks under load.",
                         cf=0.95))

    expert.add_rule(Rule("R44", lambda f: f.get("CPU_TDP", 0) > 120,
                         lambda f: f.update({"CPU_Cooler": "360mm AIO Liquid Cooler"}),
                         "High-wattage processors require premium liquid cooling to dissipate extreme heat and prevent thermal throttling.",
                         cf=0.98))

    # ==========================================
    # PHASE 10: ADVANCED CONFLICT RESOLUTIONS
    # ==========================================
    expert.add_rule(Rule("R45_Conflict",
                         lambda f: f.get("Tier") == "Enthusiast" and f.get("Target_Resolution") == "1080p",
                         lambda f: f.update({"Target_Resolution": "1440p", "Conflict": True}),
                         "CONFLICT OVERRIDE: Pairing an Enthusiast budget with a 1080p monitor creates a massive GPU bottleneck. Recommended resolution upgraded to 1440p minimum.",
                         priority=10, cf=0.85))

    expert.add_rule(Rule("R46_Conflict",
                         lambda f: f.get("Size") == "Small" and f.get("Tier") == "Enthusiast",
                         lambda f: f.update({"Size": "Standard Tower", "Conflict": True}),
                         "CONFLICT OVERRIDE: Enthusiast tier GPUs (like the RTX 4090) and 360mm Liquid Coolers physically do not fit in Small Form Factor cases. Form factor changed to Standard Tower.",
                         priority=10, cf=0.99))

    expert.add_rule(Rule("R47_Conflict",
                         lambda f: f.get("CPU") == "Core i3-12100F" and f.get("Target_Resolution") == "4K",
                         lambda f: f.update({"CPU": "Core i5-13600K", "Conflict": True}),
                         "CONFLICT OVERRIDE: A budget i3 CPU will severely bottleneck 4K GPU rendering pipelines. CPU upgraded to i5 to stabilize 1% low frame rates.",
                         priority=10, cf=0.90))

    expert.add_rule(Rule("R48_Conflict",
                         lambda f: f.get("Size") == "Small" and "ATX" in f.get("Motherboard", ""),
                         lambda f: f.update({"Motherboard": f["Motherboard"].replace("ATX", "Mini-ITX")}),
                         "CONFLICT RESOLUTION: Standard ATX motherboards physically do not fit in Small Form Factor cases. Form factor automatically adjusted to Mini-ITX.",
                         priority=9, cf=1.0))

    # ==========================================
    # PHASE 11: LIFESTYLE & WORKLOAD INFERENCE
    # ==========================================
    expert.add_rule(Rule("R49", lambda f: f.get("Upgrade_Path") == "High" and f.get("Preference") == "AMD",
                         lambda f: f.update({"Socket": "AM5", "RAM_Type": "DDR5"}),
                         "User requested a long-term upgrade path. Forced AMD architecture to the supported AM5 socket.",
                         cf=0.95))

    expert.add_rule(Rule("R50_Conflict", lambda f: f.get("Upgrade_Path") == "High" and f.get("Budget", 0) < 800,
                         lambda f: f.update({"Upgrade_Path": "Low", "Conflict": True}),
                         "CONFLICT OVERRIDE: A sub-$800 budget cannot afford the premium for next-gen AM5/DDR5 platforms. Prioritizing immediate performance on older architecture.",
                         priority=10, cf=0.85))

    expert.add_rule(Rule("R51", lambda f: f.get("Workload") == "Heavy Editing",
                         lambda f: f.update({"Memory_Capacity": "64GB"}),
                         "Heavy 4K editing workloads strictly require 64GB of memory to prevent system paging.",
                         cf=0.99))

    expert.add_rule(Rule("R52", lambda f: f.get("Workload") == "Streaming",
                         lambda f: f.update({"Memory_Capacity": "32GB"}),
                         "Assigned 32GB of memory to handle OBS streaming overhead while gaming without stuttering.",
                         cf=0.90))

    expert.add_rule(Rule("R53", lambda f: f.get("Library_Size") == "Massive (Keep everything installed)",
                         lambda f: f.update({"Storage": "2TB NVMe Gen 4 SSD"}),
                         "Assigned 2TB of fast storage to accommodate a continuously installed library of massive AAA games.",
                         cf=0.85))