# Genesys 2 DDR3 controller configuration

`mig.prj` is derived from Digilent's Genesys 2 Rev. H board file
`new/board_files/genesys2/H/mig.prj` in
[Digilent/vivado-boards](https://github.com/Digilent/vivado-boards) at commit
`d8d43ed9f3f7e367ee3de82782ed601d88305677`
(original SHA-256 `3ebd0a6d04613e2ba1f7fda692479d1212ca97f30714d48f30ae41d6507685ef`, MIT License, see `LICENSE`).

WasMetal changes only these fields:

| Field | Digilent | WasMetal | Reason |
| --- | --- | --- | --- |
| `ModuleName` | `design_1_mig_7series_0_0` | `wasmetal_genesys2_mig` | Stable module name for the top level |
| `SystemClock` | `Differential` | `No Buffer` | The top's `IBUFDS` already buffers the 200 MHz clock for the CPU divider |
| `C0_S_AXI_DATA_WIDTH` | 256 | 128 | Matches the verified 128-bit WasMetal AXI adapter |
| `C0_S_AXI_ID_WIDTH` | 3 | 4 | Matches the adapter's default ID width |

Memory device (MT41J256M16, 32-bit, 1,800 MT/s, 4:1 PHY), pinout and timing
are Digilent's unchanged values.
