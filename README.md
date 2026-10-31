# WasMetal

A project to build a bare metal physical implementation of WebAssembly. That's right, a WebAssembly CPU. Inspired in part by [this amazing talk](https://www.destroyallsoftware.com/talks/the-birth-and-death-of-javascript).

WasMetal is being revived under [Millillion](https://github.com/Millillion) in 2026. Its SystemVerilog execution core passes all 259 files in the pinned official WebAssembly Core 3.0 test suite, using a software loading and validation front end. See the [verification evidence](docs/verification/core-3.0-current.json), [RTL architecture](docs/RTL.md) and [FPGA bring-up guide](docs/FPGA.md) for the execution boundary, resource limits and hardware build.

## GUI Microarchitecture Simulator

The [historical demo](https://wasm-metal-demo.netlify.com) uses the original hosting address; its availability has not been verified for the revival.

```bash
git clone https://github.com/Millillion/wasmetal.git
cd wasmetal
npm install
npm start
```

Go to [http://localhost:5000](http://localhost:5000) in your web browser.

## RTL Microarchitecture Simulator

The clocked SystemVerilog core runs in Verilator. The test harness converts the
pinned official Wasm core test suite and compares its expectations with RTL
execution results and traps. Unsupported cases fail the run.

```sh
python3 tools/bootstrap.py
make lint
make test-all
```

See [docs/RTL.md](docs/RTL.md). The original roadmap below is historical; the
WebAssembly specification and its official tests define the implementation target.

## Loading Microarchitecture Implementation to FPGA

A host-backed ULX3S 85F reference system includes a UART loader/step interface,
board constraints, synthesis, placement/routing and bitstream build tools. The
whole serial interface and CPU are tested together in simulation. Its storage
profile is smaller than the full conformance simulator's. See the
[FPGA guide](docs/FPGA.md); physical-board testing remains a separate step.

## Roadmap

- [ ] Understand the WebAssembly [ISA](https://en.wikipedia.org/wiki/Instruction_set_architecture)
- [ ] Implement the [mircoarchitecture](https://en.wikipedia.org/wiki/Microarchitecture) in HTML/CSS/JavaScript
  * This will be a GUI simulator of the microarchitecture
  * This simulator will become the specification for the microarchitecture
  * It will allow us to quickly experiment with hardware configurations
  * It will allow us to iterate and learn how the microarchitecture should work
- [ ] Implement the microarchitecture as an [RTL design](https://en.wikipedia.org/wiki/Register-transfer_level#RTL_description) in an [HDL](https://en.wikipedia.org/wiki/Hardware_description_language)
- [ ] Simulate the RTL design
- [ ] Test the implementation on an [FPGA](https://en.wikipedia.org/wiki/Field-programmable_gate_array)
- [ ] Design the [ASIC](https://en.wikipedia.org/wiki/Application-specific_integrated_circuit)

## Why is this a good idea?

* [Maybe it's not](https://twitter.com/lastmjs/status/928682791511789568), but who cares
* The world is moving to WebAssembly
* Some of the biggest and potentially most world-changing projects are implementing their virtual machines as WebAssembly virtual machines (DFINITY, Ethereum)
* The bytecode is being designed as a compilation target for low-level languages first
* The bytecode is meant to execute at near-native speeds on a variety of underlying ISAs
* Java processors already offer potential benefits, even being compilation targets for a high-level language
* Cutting out the translation from WebAssembly to the underlying ISAs could provide efficiency benefits
* We could get rid of WebAssembly virtual machines entirely, and replace them with WebAssembly physical machines
* If [all SIM cards are Java processors](https://twitter.com/hedgeberg/status/935380806549286912), imagine what WebAssembly processors could do. I'm betting that WebAssembly is a better bytecode than Java bytecode for what Java bytecode is doing with microcontrollers, so WebAssembly could take over all spaces that Java processors currently have

## Prior art

* https://en.wikipedia.org/wiki/Jazelle
* https://stackoverflow.com/questions/1153076/does-android-castrate-the-arms-jazelle-technology
* https://en.wikipedia.org/wiki/Lisp_machine
* https://en.wikipedia.org/wiki/Java_processor
* https://en.wikipedia.org/wiki/High-level_language_computer_architecture
