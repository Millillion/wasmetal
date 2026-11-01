# FPGA selection for WasMetal

Research checked on **31 October 2026, America/New_York** (1 November UTC). Prices are USD snapshots before shipping, tax and any applicable tariffs. The recommendation considers a first FPGA purchase, sustained CPU development, open tools, community support and use in a US home engineering workspace.

**The Digilent Genesys 2 is the best technical fit for the next WasMetal development platform.** Its combination of programmable logic, directly attached DDR3, existing open CPU projects and approachable board interfaces is more useful here than the specialized interfaces on many much more expensive kits. Digilent lists it at $1,183; the checked US DigiKey listing was $1,244.01 with 112 units in stock. Purchase the exact **410-300 / XC7K325T-2FFG900C** kit through an authorized distributor. Stock and the final price need checking at checkout. [Digilent product](https://digilent.com/shop/genesys-2-amd-kintex-7-fpga-development-board/?setCurrencyId=1), [DigiKey listing](https://www.digikey.com/en/products/detail/digilent-inc/410-300/5730862).

**Home-use compliance remains a purchase condition.** The public documents reviewed do not establish FCC Class B compliance for Genesys 2 or the other leading candidates. Digilent expressly disclaims EMC testing for its development kits. A development kit can have a lawful evaluation route without consumer certification, but that route has conditions. Obtain the exact board's US regulatory basis and permitted home R&D conditions from the supplier before ordering; see the questions below. This is a conditional technical recommendation, not a finding that every requested purchasing criterion has been satisfied.

The **AMD ZCU104** is the strongest alternative when an onboard Arm/Linux host is desirable. **ULX3S 85F** remains valuable for the existing completely open build flow and inexpensive physical bring-up. **VCU118** becomes relevant if measured designs grow into large multicore or speculative CPU research. The useful initial spending range is approximately **$1,200–$1,700**, subject to retail prices and accessories; spending much more does not automatically accelerate WasMetal development.

## What the current design actually needs

The existing [RTL description](RTL.md), [FPGA guide](FPGA.md), [conformance record](verification/core-3.0-current.json) and [routed-board record](verification/fpga-routing.json) provide the starting point:

| Current property | Evidence and implication |
|---|---|
| Compatibility target | Pinned WebAssembly Core 3.0; all 259 pinned official suites pass the current RTL/software harness. Finite tests do not prove every possible program correct. |
| ECP5 logic | 58,892 / 83,640 logic cells, **70.4%**, for the routed host-backed ULX3S system. |
| ECP5 embedded memory | 98 / 208 18-Kbit RAM blocks. |
| ECP5 multiplication resources | 27 / 156 DSP18 blocks. |
| Timing | The core meets its 1 MHz constraint; the routed report gives 3.24 MHz maximum. This is a property of this implementation and its half-cycle paths, not an ECP5 family speed limit. |
| Execution architecture | Shared floating-point arithmetic and serialized integer SIMD reduce area. Supporting a vector instruction does not require executing every lane simultaneously. |
| Storage | 8,192 128-bit value slots, 2,048 labels, 512 frames, 256 descriptors per class and 1,048,576 external heap slots. The external heap is not all FPGA block RAM. |
| System boundary | The host supplies expanded instructions, metadata and backing memory. Autonomous boot, a local DRAM controller and reclaiming garbage collection remain future work. |
| Physical status | Routed bitstream and simulation evidence exist; no physical FPGA has been tested. |

The premise that implementing the rest of Wasm necessarily requires a giant FPGA is misleading. Much of the instruction execution already exists. The substantial next work is turning that engine into a useful independent computer and improving its performance.

WebAssembly 3.0 includes memory64, multiple memories, GC, typed function references, tail calls, exceptions and relaxed SIMD. Memory64 describes address capabilities; it does not require physically installing the entire 64-bit address space. Future proposals also have distinct maturity levels: the current proposals repository lists Threads at phase 4, Stack Switching at phase 3 and FP16 at phase 2. Proposal status should be pinned alongside the specification instead of treating every proposal as an adopted CPU requirement. [WebAssembly 3.0 announcement](https://webassembly.org/news/2025-09-17-wasm-3.0/), [proposal status](https://github.com/WebAssembly/proposals/blob/main/README.md), [finished proposals](https://github.com/WebAssembly/proposals/blob/main/finished-proposals.md).

WASI and the Component Model additionally involve software interfaces, loading and runtime services. They are not a simple list of gates to add to a CPU. Similarly, a reclaiming collector needs an explicit hardware/software design; implementing GC instructions and object allocation alone does not supply one.

### A measured Xilinx resource estimate

An isolated Yosys 0.33 experiment mapped the unchanged current core to Xilinx 7-series primitives using the existing FPGA capacity profile. The [machine-readable result](research/xc7-resource-estimate.json) records source hashes, tool identity, cell counts, warnings and limitations. The [exact recipe](research/xc7-resource-estimate.ys) is retained.

| Core-only estimate | Count | Fraction of Genesys 2 device capacity |
|---|---:|---:|
| LUT1–LUT6 primitives | 47,801 | **23.5%** of 203,800 LUT sites |
| Flip-flops | 5,265 | 1.3% of 407,600 |
| DSP48E1 | 30 | 3.6% of 840 |
| RAMB18E1 / RAMB36E1 | 60 / 19 | 49 equivalent 36-Kbit blocks; 11.0% of 445 |
| Carry / dedicated multiplexers | 2,063 CARRY4; 3,987 MUXF7; 1,356 MUXF8 | Packing and placement still matter |

The run completed with zero structural-check problems. It is **not a Vivado utilization report, a working board port, a timing result or functional verification of the Xilinx mapping**. It excludes board logic, clock and I/O buffers, DDR control, caches and autonomous execution. The log includes HardFloat default-parameter parsing warnings and temporary-array expansion warnings, recorded in the result. Those are not a substitute for checking the mapped design's behavior.

The same LUT count is about 35.5% of a Nexys Video A200T and 75.4% of an Arty A7 A100T. These are indicative core-only capacity comparisons, not routed occupancy. They support buying more room than an A100T for the main development board. The Genesys 2 figure leaves a useful engineering margin, but it does not guarantee that four complete CPUs, arbitrary future features or any particular clock frequency will fit.

To repeat the exploratory estimate after installing the repository's pinned tools:

```sh
python3 tools/bootstrap.py --fpga-tools
mkdir -p build/fpga-research
.cache/tools/usr/bin/yosys -Q -T -s docs/research/xc7-resource-estimate.ys > build/fpga-research/core-xc7.log 2>&1
```

This command generates an exploratory core netlist, not a supported Xilinx board image. Source/device counts come from the recorded run and AMD's [7-series overview](https://docs.amd.com/v/u/en-US/ds180_7Series_Overview).

### Where future area will go

| Development direction | Main resource pressure | Buying implication |
|---|---|---|
| Local instruction/data memory, loader and boot | DRAM controller, interconnect, buffers, some logic and block RAM | Real board RAM and working reference designs matter immediately. |
| Better clock frequency | Pipeline registers, control changes, placement and timing discipline | A larger or newer FPGA alone cannot repair a long combinational path. |
| Caches and a stack cache | Embedded RAM, tags and control | Reserve RAM blocks and routing room; external DDR does not replace low-latency on-chip storage. |
| Parallel SIMD and floating point | DSPs, LUTs and memory bandwidth | Add parallel lanes when benchmarks justify their cost. |
| Reclaiming GC and richer runtime | Heap bandwidth, metadata and hardware/software coordination | More DRAM helps workloads; implementation policy determines additional logic. |
| Threads and atomics | Ordering logic, synchronization and runtime services | Hardware multicores and coherent caches are performance choices, not an automatic one-core-per-thread requirement. |
| Multicore, speculation or out-of-order execution | Large increases in logic, RAM ports, interconnect and verification complexity | Reassess capacity using actual synthesized configurations; this is where research-scale boards become useful. |

As an engineering planning rule, target roughly 50–60% logic utilization for the first complete local-memory system if possible, leaving room for debug and changes. This is a conservative development preference, not a vendor rule or guarantee of timing closure. Do not allocate a made-up fixed percentage to every future Wasm feature.

## Board comparison

LUT4, LUT6, Altera logic elements/ALMs and Efinix logic elements are different architectures. Marketing “logic cells” are not a universal unit. The table uses actual LUT counts where available and labels the ECP5 separately. Even equal LUT6 counts do not imply equal speed, routing, RAM architecture or DSP capabilities.

| Board | Listed price | FPGA fabric | Board DRAM | Assessment for WasMetal |
|---|---:|---:|---|---|
| [ULX3S 85F](https://www.crowdsupply.com/radiona/ulx3s) | $275 | 83,640 LUT4-class cells | 32 MB SDRAM | Best inexpensive companion for the existing open flow; current system already uses 70.4% of logic. |
| [Arty A7-100T](https://digilent.com/shop/arty-a7-100t-artix-7-fpga-development-board/?setCurrencyId=1) | $322 | 63,400 LUT6 | 256 MB DDR3L | Good educational ecosystem; insufficient comfortable growth margin for the main board. |
| [Nexys Video](https://digilent.com/shop/nexys-video-amd-artix-7-fpga-trainer-board-for-multimedia-applications/?setCurrencyId=1) | $577 | 134,600 LUT6 | 512 MB DDR3 | Strong lower-cost alternative; more room than Arty, less than Genesys 2. |
| [Genesys 2](https://digilent.com/shop/genesys-2-amd-kintex-7-fpga-development-board/?setCurrencyId=1) | $1,183; checked DigiKey $1,244.01 | 203,800 LUT6 | 1 GB DDR3, 32-bit | Preferred dedicated CPU platform. |
| [ZCU104](https://www.amd.com/en/products/adaptive-socs-and-fpgas/evaluation-boards/zcu104.html) | $1,678 | 230,400 LUT6, plus hard Arm processors | 2 GB DDR4 on processor side; separate PL SODIMM socket | Preferred alternative for a self-contained Linux host plus WasMetal engine. |
| [KC705](https://www.amd.com/en/products/adaptive-socs-and-fpgas/evaluation-boards/ek-k7-kc705-g.html) | $2,995 | 203,800 LUT6 | 1 GB DDR3 | Same FPGA capacity as Genesys 2; premium buys a different reference platform and interfaces. |
| [Opal Kelly XEM8370-KU11P](https://www.opalkelly.com/products/fpga-integration/XEM8370) | $4,399.95, before accessories | 298,560 LUT6 | 4 GiB DDR4 | Strong fast USB-host integration; greater tool/accessory cost and a less direct CPU-board path. |
| [KCU105](https://www.amd.com/en/products/adaptive-socs-and-fpgas/evaluation-boards/kcu105.html) | $6,495 | 242,400 LUT6 | 2 GB DDR4 | Expensive for a modest general logic increase; buy for specific UltraScale/interface requirements. |
| [KCU116](https://www.amd.com/en/products/adaptive-socs-and-fpgas/evaluation-boards/ek-u1-kcu116-g.html) | $6,495 | 216,960 LUT6 | 1 GB DDR4 | Newer fabric, DSPs and UltraRAM; weak value if general CPU logic capacity is the purpose. |
| [VCU118](https://www.amd.com/en/products/adaptive-socs-and-fpgas/evaluation-boards/vcu118.html) | $14,995 | 1,182,240 LUT6 | Two 2.5 GB physical, 80-bit DDR4 banks | Genuine research-capacity jump; defer until a large measured design needs it. |

AMD device resources are in [DS890, tables 7, 9, 15 and 23](https://docs.amd.com/v/u/en-US/ds890-ultrascale-overview). Board memory details are in the [ZCU104 guide](https://docs.amd.com/api/khub/documents/g76en4BfB6qIp2gHDRkQxg/content), [KCU105 guide](https://docs.amd.com/v/u/en-US/ug917-kcu105-eval-bd), [KCU116 guide](https://docs.amd.com/v/u/en-US/ug1239-kcu116-eval-bd) and [VCU118 guide](https://docs.amd.com/v/u/en-US/ug1224-vcu118-eval-bd). VCU118's physical memory width/capacity must not be confused with usable payload capacity under a particular controller/ECC configuration. Manufacturer list prices are not guaranteed distributor checkout prices.

### Why Genesys 2 leads

Its 1 GB DDR3 connects directly to programmable logic. That suits building WasMetal's own memory subsystem. USB JTAG, UART, Ethernet, SD, Pmod and FMC expansion support practical development and later peripherals without starting with PCIe host integration. Its 840 DSPs and 445 36-Kbit RAM blocks offer much more room than the present core consumes. [Board specification](https://digilent.com/shop/genesys-2-amd-kintex-7-fpga-development-board/?setCurrencyId=1), [device resources](https://docs.amd.com/v/u/en-US/ds180_7Series_Overview).

The strongest community evidence is existing CPU development work:

- **CVA6** documents Genesys 2 FPGA builds and Linux boot, including DDR3 and SD setup. Its tutorial notes limitations, including nonfunctional Ethernet in that described setup; these examples are reusable engineering references, not a promise that every peripheral works unchanged. [CVA6 FPGA tutorial](https://github.com/openhwfoundation/cva6/blob/main/tutorials/fpga.md).
- **LiteX** provides a Genesys 2 target using LiteDRAM's 7-series DDR PHY. This offers an open system-integration reference around a proprietary FPGA backend. [LiteX board target](https://github.com/litex-hub/litex-boards/blob/master/litex_boards/targets/digilent_genesys2.py).
- **Chipyard** has board-specific Genesys 2 instructions, including DDR backing memory and a UART bring-up path. It also documents Nexys Video, ZCU104 and VCU118, so these are credible alternatives within an established CPU research ecosystem. [Genesys 2 instructions](https://chipyard.readthedocs.io/en/stable/prototyping/genesys2/), [supported platforms](https://chipyard.readthedocs.io/en/stable/prototyping/).

These projects use other CPU architectures. Their existence demonstrates useful board infrastructure, not that WasMetal has already been ported or will reach their clock rates. There is no credible universal popularity ranking that makes one board “universally loved.” For this project, usable CPU, DRAM and debugging examples deserve more weight than review stars or retro-gaming popularity.

The age of Kintex-7 is a real tradeoff, but not an immediate obsolescence finding. AMD's February 2026 lifecycle announcement extends 7-series silicon availability through 2040 and UltraScale+ through at least 2045, subject to its stated conditions. That is a silicon supply horizon, not a guarantee of Genesys 2 board availability or unchanged software licensing. Digilent's current company FAQ states a one-year manufacturing-defect warranty and routes purchases through distributors. [AMD lifecycle announcement](https://www.amd.com/en/blogs/2024/amd-supports-new-long-lifecycle-fpga-designs-thro.html), [Digilent purchasing and warranty FAQ](https://digilent.com/shop/company/).

Higher price does not imply a longer warranty: AMD's standard terms give development/evaluation boards and kits a 90-day warranty, with exclusions and potentially different written agreements. Confirm the actual seller's terms. No comparative failure-rate evidence establishes one finalist as inherently more reliable; documentation, known reference designs, cooling and warranty support are the practical robustness indicators used here. [AMD terms of sale](https://www.amd.com/en/legal/terms-of-sale.html).

### When ZCU104 is better

ZCU104 combines programmable logic with hard Arm application processors. They can eventually run Linux, load programs, manage storage and communicate with the WasMetal core over an AXI bus. That can make a useful standalone development appliance while WasMetal itself still executes in RTL.

Its 230,400 LUTs are only about 13% more than Genesys 2, but it also provides 1,728 DSPs, 11.0 Mbit block RAM and 27 Mbit UltraRAM. UltraRAM is a different memory primitive with its own widths, latency and placement constraints; it cannot simply be added to the block-RAM number and assumed interchangeable. [Device overview, table 23](https://docs.amd.com/v/u/en-US/ds890-ultrascale-overview).

The included 2 GB DDR4 is attached to the Arm processing system. Programmable logic can use the system interconnect, which requires integration. The separate DDR4 SODIMM socket connects to programmable logic, but **the official kit ships without that SODIMM**. Using a direct PL memory controller requires a compatible module and its own integration. These are separate options, not 2 GB plus free additional populated RAM. [ZCU104 user guide, pages 24 and 29](https://docs.amd.com/api/khub/documents/g76en4BfB6qIp2gHDRkQxg/content).

Choose ZCU104 if the built-in host, newer fabric and UltraRAM are deliberate priorities. Genesys 2 keeps the first system focused on the CPU and its directly attached memory. Both require a new board port. AMD's listed ZCU104 lead time was eight weeks; authorized distributor stock can differ. Its documented Class A EMC status also needs the home-use clarification below.

### Why spending more stops helping initially

The $6,495 KCU105 offers about 19% more LUTs than Genesys 2; KCU116 offers about 6% more. Their additional DSP, memory and high-speed I/O capabilities can be valuable, but those are not the current bottleneck. KC705 has the same K325T logic capacity as Genesys 2. Choosing these kits needs a specific interface, bandwidth or reference-design requirement.

Opal Kelly's XEM8370 provides approximately 47% more LUTs, 4 GiB DDR4 and a convenient USB/FrontPanel environment. The listed breakout board adds $399.95, with power and cooling accessories separate. It becomes attractive if fast host transfers are central to the project. FrontPanel and the vendor implementation flow introduce dependencies, and KU11P requires a paid Vivado tier under the current device table. [XEM8370 product](https://www.opalkelly.com/products/fpga-integration/XEM8370), [Vivado device coverage](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vivado/vivado-buy.html).

VCU118 provides roughly 5.8 times Genesys 2's LUT capacity. That is a real change of scale for large cores, multiple cores or accelerators. It also brings larger implementation jobs, power/cooling requirements and paid tool coverage. It does not make an unpipelined CPU fast or its verification complete. Its user guide describes Class A EMC, so spending $14,995 does not establish residential Class B suitability. [VCU118 product](https://www.amd.com/en/products/adaptive-socs-and-fpgas/evaluation-boards/vcu118.html), [user guide](https://docs.amd.com/v/u/en-US/ug1224-vcu118-eval-bd).

Upgrade when the complete design demonstrably runs out of logic, embedded RAM, memory bandwidth or a required interface after reasonable optimization. Until then, spend on a comfortable development computer, suitable bench equipment, debug access and engineering time. A second $275 ULX3S can preserve an open-flow reference and provide a smaller regression target alongside the main board; it is optional, not necessary to begin.

## Other families considered

| Candidate | What makes it relevant | Why it does not displace the shortlist |
|---|---|---|
| [Digilent Genesys ZU-5EV](https://digilent.com/shop/genesys-zu-zynq-ultrascale-mpsoc-development-board/?setCurrencyId=1) | Modern Zynq SoC platform; $2,095 shown for the 5EV variant. | ZU5EV has 117,120 LUTs, substantially fewer than Genesys 2 or ZCU104. A newer family name does not automatically mean more CPU fabric; compare the exact variant using DS890. |
| [Terasic DE25-Standard](https://www.terasic.com.tw/cgi-bin/page/archive.pl?CategoryNo=123&Language=English&No=1354) | $586 list price; Agilex 5 with 138K marketed logic elements, 1 GB DDR4 and 64 MB SDRAM; manufacturer advertises a free Quartus Pro license. | A serious modern lower-cost alternative. Its LE count is not 138K LUT6; WasMetal needs an Altera mapping estimate and a different board/DRAM flow before a capacity claim. |
| [Arrow AXE5 Eagle](https://www.altera.com/partners/offering/po-1632/axe-5-eagle-dev-kit?q=2043453176) | Modern Agilex 5 SoC and LPDDR4. | Current production and engineering-sample parts differ; compare the exact SKU, tool entitlement and reference designs, not an old larger-ES headline. The existing CPU ecosystem evidence favors the shortlist. |
| [Efinix Titanium Ti375 kit](https://www.efinixinc.com/shop/ti375.php) | Substantial newer fabric and memory; an interesting architectural alternative. | Efinity is a separate proprietary implementation flow. Published logic-element counts cannot be treated as Xilinx LUT6 counts; equivalent WasMetal synthesis and board integration remain necessary. |
| [Microchip PolarFire SoC Icicle](https://onlinedocs.microchip.com/oxy/GUID-41204B2E-6175-4401-895B-19ED7CD240F4-en-US-1/GUID-9D602E81-E6F1-4C09-AE69-14C8A4BD3F34.html) | Hard RISC-V host processors, Linux and FPGA fabric; production kit documentation provides Libero Silver licensing instructions. | Open RISC-V ISA does not make the FPGA tools open. This is another distinct integration flow; buy the production SKU rather than assuming old ES listings are equivalent. |
| [Tang Mega 138K Pro](https://en.wiki.sipeed.com/hardware/en/tang/tang-mega-138k/mega-138k-pro.html) | Large Gowin hobbyist board with 1 GB DDR3 and open documentation. | Exact device revision, supported tool features, support and regulatory documents matter. The vendor's current documentation distinguishes device B/C memory capabilities. Country of manufacture alone is not an export-law determination. |
| [OrangeCrab](https://orangecrab-fpga.github.io/orangecrab-hardware/docs/r0.2.1/) and [ULX4M](https://www.crowdsupply.com/intergalaktik/ulx4m) | Open ECP5 hardware with different form factors and larger external memory options. | The 85F variants retain essentially the same logic ceiling as ULX3S. ULX4M's checked Crowd Supply page remained “Coming Soon”; do not base an immediate purchase on a campaign announcement. |
| [NewAE CW340/CW341](https://opentitan.org/book/doc/contributing/fpga/get_a_board.html) | OpenTitan-supported security development platform using Kintex UltraScale KU095. | Valuable for security and side-channel research, with different board priorities. OpenTitan compatibility alone does not establish the best memory, cost or compliance fit for WasMetal. |
| Used accelerator/mining cards or custom carrier modules | Can offer a large amount of fabric. | Host PCIe, cooling, power, documentation, tool entitlements, board revision and warranty must all be established. They add avoidable uncertainty for a first board. |

Altera's current licensing documentation allows free Pro licenses for Agilex 5 E-series and Agilex 3. It would be incorrect to reject all newer Altera boards on an assumption that every Quartus Pro target needs a paid license. [Altera licensing guidance](https://docs.altera.com/r/docs/683472/25.3/altera-fpga-software-installation-and-licensing/evaluating-the-quartus-prime-software).

## Open source and long-term tool access

There are four separate questions: is the CPU RTL open; are the board design files openly licensed; are the synthesis/place-and-route/bitstream tools open; and can the system be used without a proprietary host SDK? An open ISA or published schematic does not settle the other three.

ULX3S is particularly strong for open hardware and the Yosys/nextpnr/Project Trellis flow already used by WasMetal. Genesys 2 is a pragmatic choice for larger designs using Vivado, with open CPU and system components around it. The project can continue using open simulation tools while the physical implementation backend is proprietary.

OpenXC7 is useful work to follow, but its Xilinx path should not be represented as a fully validated replacement for Vivado on this design. The current nextpnr documentation marks the Xilinx 7-series backend experimental. The earlier nextpnr-xilinx repository points to a successor and describes a Vivado dependency for UltraScale+ bitstream generation. Current nextpnr also lists Gowin Aurora V support, so an old blanket claim that Gowin has no open tool support would be inaccurate. Exact device and feature coverage still matters. [Current nextpnr](https://github.com/openXC7/nextpnr), [earlier Xilinx backend notes](https://github.com/openXC7/nextpnr-xilinx).

### Vivado terms changed in 2026

The current table covers Genesys 2, Nexys Video, ZCU104 and KCU116 in **Basic**, free with annual renewal and Linux/Windows support. KU040, KU11P and VU9P need **Core or higher**. Basic limits XSIM to 50K design instances without UVM, and debug to one ILA with five probes of at most 1,024 bits each. Existing Verilator-based RTL testing remains useful independently. [AMD current editions and device coverage](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vivado/vivado-buy.html).

| Node-locked license | Listed price | Time basis |
|---|---:|---|
| Basic | $0 | Annual renewal |
| Core | $1,200 | Annual subscription |
| Pro | $2,400 | Annual subscription |
| Enterprise | $4,395 | Perpetual covered versions; one year of updates |

At unchanged rates, five years of Core subscription would be $6,000; this is arithmetic, not a quote or a necessary expense for Genesys 2. Enterprise's perpetual rights apply to covered versions, not every future release. More expensive tools become justified when their device coverage or debugging/features are needed. [AMD pricing](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vivado/vivado-buy.html).

Digilent's Genesys 2 page still describes the older Standard/Enterprise arrangement and an included voucher. Confirm the precise entitlement supplied with the shipping kit. AMD's current FAQ says UltraScale/UltraScale+ development-kit vouchers are one-year Core subscriptions, and explains the 2026.1 license checkout and renewal changes. Older tool versions and older licenses have different rules; a new Basic license is not a universal entitlement to every historical Vivado release. Preserve installers, entitlement records and reproducible tool environments. [AMD licensing FAQ](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/licensing-faq.html).

## FCC, home use and export controls

### What the available compliance documents establish

| Board/document | What it establishes | What it does not establish |
|---|---|---|
| [Digilent development-kit EMC disclaimer](https://files.digilent.com/resources/documents/EMC_DISCLAIMER_DIGILENT_DEVELOPMENT_AND_EVALUATION_KITS.pdf) | Development/evaluation use restrictions; engineering/lab context; kits are not EMC tested and are not rated for household or commercial use as products. | FCC Class B emissions compliance or blanket permission for every home setup. The document principally addresses EMC/product use, not a complete US authorization record. |
| [Genesys 2 CE/UKCA declaration](https://www.mouser.com/catalog/additional/Digilent_Inc_Declaration_of_Conformity_Genesys_2.pdf) | Restricted-substance/RoHS conformity. | An EMC test report or FCC authorization. |
| [ZCU104 guide](https://docs.amd.com/api/khub/documents/g76en4BfB6qIp2gHDRkQxg/content), [KC705 guide](https://docs.amd.com/api/khub/documents/g0YC14NTyJ_D9ZQTSmzzWg/content) | Class A EMC statements and domestic-interference cautions. | FCC residential Class B compliance; the cited passages describe European EMC requirements. |
| [Opal Kelly EMC whitepaper](https://docs.opalkelly.com/resources/whitepapers/pre-compliance-emc-testing-with-opal-kelly-fpga-development-modules/) | Useful measurements and integration guidance; testing described is pre-compliance. | Certification of every module, arbitrary FPGA design or assembled end product. |
| [Kria KV260 regulatory section](https://docs.amd.com/r/en-US/ds986-kv260-starter-kit/FCC-Class-A-Products) | A statement explicitly scoped to the production K26 SOM. | Coverage of the non-production SOM supplied on the starter kit or proof of whole-kit Class B compliance. |
| ULX3S public product material | Open board documentation and an integrated ESP32 module. | A verified full-board Class B record. Radio-module approval does not establish emissions compliance of the complete CPU system. |

FCC Class A addresses commercial environments; Class B limits address residential protection. A Class A warning does not itself mean all home operation is prohibited, but it does mean residential compliance cannot be assumed and interference may require corrective measures. Neither a CE logo, a US seller, the absence/presence of an FCC ID, nor the chip manufacturer's name answers the entire question. Some equipment uses a Supplier's Declaration of Conformity rather than an FCC certification ID. [47 CFR 15.105 user information](https://www.law.cornell.edu/cfr/text/47/15.105), [47 CFR 2.803 authorization routes](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-2/subpart-I/section-2.803).

The current **47 CFR 2.803(d)(2)(iv)** permits qualifying evaluation-kit sales to product developers, software developers and system integrators with specified notices, labeling and conditions. Operation is separately governed by **2.805**; it is not an exemption from interference limits. This provides a possible legal path for development hardware without consumer certification. Whether the exact board and intended home R&D setup meet that path still needs specific supplier documentation. [Evaluation-kit marketing conditions](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-2/subpart-I/section-2.803), [operation before authorization](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-2/subpart-I/section-2.805).

Clocks, switching activity, attached cables, power supplies and enclosures affect emissions. An enclosure is an engineering measure, not automatic certification. Open-source status also does not change the FCC limits. If documented residential Class B compliance is an absolute purchasing requirement, **none of the leading candidates is verified to satisfy it by this research**; do not silently substitute an untested kit or a Class A statement.

### Export classification and ordinary domestic development

Digilent identifies Genesys 2 as **ECCN 5A992.c**. Preserve that exact-SKU classification and invoice with the purchase. It is useful manufacturer evidence, not a universal permission for every export, destination, recipient or end use. [Genesys 2 export classification](https://digilent.com/shop/genesys-2-amd-kintex-7-fpga-development-board/?setCurrencyId=1).

EAR jurisdiction and an export-license requirement are different questions. Domestic purchase for ordinary civilian development, later shipping abroad, sharing controlled nonpublic technology, and selling a future chip are also different activities. BIS explains that being subject to the EAR does not itself mean a license is required, while end-user and end-use controls can impose restrictions. Published software/information has specific treatment with exceptions; the purchased board's classification does not automatically classify WasMetal RTL, bitstreams or a future ASIC. [BIS EAR part 734](https://www.bis.gov/regulations/ear/734), [part 744 end-use/end-user controls](https://www.bis.gov/regulations/ear/744).

For this purchase, prefer a manufacturer or authorized US distributor, the production SKU, documented warranty and a stated ECCN. Reassess the actual transaction if exporting, reexporting or transferring controlled technology later. Do not infer legality or illegality from a vendor's nationality, or assume “open source” overrides sanctions. Formal transaction clearance would require the actual parties, destinations and end use; no blanket legal clearance is asserted here.

### Questions to resolve with the supplier before purchase

The following is a ready-to-send inquiry for the **Genesys 2, SKU 410-300**, with board revision specified in the reply:

> I am considering this kit for civilian FPGA/CPU development in a US home engineering workspace. Please provide the applicable US FCC authorization or evaluation-kit basis, required notices and operating conditions for the exact board revision you would ship. Is there a Class B report or Supplier's Declaration of Conformity? If sold under the evaluation-kit provisions, does your intended-use policy permit this home R&D environment, and what setup restrictions apply? Please also confirm the current ECCN, production status, warranty, included power supply, and exact Vivado voucher edition, expiration/renewal terms and device restrictions.

These questions seek concrete product records; they do not presume Class B certification is mandatory for every lawful development use. If the supplier cannot support the intended environment, reassess the board or development environment before purchase. No inquiry has been sent on the user's behalf.

## Development path after selecting the board

1. **Verify the purchased board using its vendor diagnostics.** Establish JTAG, UART, clocks, DRAM tests and temperature behavior before bringing up the CPU. Confirm the correct board revision and constraints.
2. **Create a minimal WasMetal board port.** Preserve the core's generic RTL, isolate vendor RAM/clock/I/O wrappers, constrain both clock edges and retain the existing UART protocol initially. Run the official RTL suite, appropriate mapped-circuit checks and static timing before claiming a supported bitstream.
3. **Run selected conformance tests on physical hardware, then broaden the hardware corpus.** Check stalls, resets, errors and memory boundaries. Simulated passes and hardware passes must remain separate records.
4. **Add the local memory subsystem and autonomous execution.** Bring up DDR independently, add interconnect/buffers and a boot/loading path, then move instructions and data onto the board. Define the boundary between a software loader/runtime and the Wasm CPU explicitly.
5. **Measure real workloads.** Collect instruction/cycle counts, memory stalls, frequency, utilization and power. Use those results to decide on pipelines, caches, parallel SIMD, collector design and additional cores.
6. **Revisit capacity when measurements justify it.** Synthesize complete candidate configurations before buying a larger board. An FPGA purchase is a development tool choice, not a final microarchitecture commitment.
7. **Prepare separately for an ASIC.** Replace FPGA-specific memories and clocking with process-compatible macros, add manufacturing test, complete physical implementation/signoff, and plan packaging and board bring-up. FPGA success substantially helps functional development but does not establish ASIC timing, power or manufacturability.

The immediate choice is therefore **Genesys 2, conditional on the home-use regulatory clarification**, with **ZCU104** preferred if its onboard host is a deliberate system requirement. Keep ULX3S as the currently routed reference. Do not change the repository's supported-board claim until the replacement target has its own implementation and verification evidence.
