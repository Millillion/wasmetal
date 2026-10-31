# Berkeley HardFloat Release 1

Source: https://www.jhauser.us/arithmetic/HardFloat-1.zip

Archive SHA-256: `6b3757c9fbfa2230c6a2b84605e39372cb589dd7500e979c4f0b8ecc8a03b14b`

Copyright and BSD license are retained in `COPYING.txt` and the source headers.
WasMetal uses the supplied RISC-V specialization. Wasm-specific NaN, signed-zero,
trapping-conversion and saturation behavior is implemented in WasMetal wrappers.

Compatibility change: removed the redundant `wire sqrtOpOut;` declaration in
`divSqrtRecFN_small.v`; the ANSI module port already declares the net. Verilator
5.020 rejects the duplicate declaration. No arithmetic logic was changed.

`rtl/vendor.vlt` scopes legacy naming and expression-width lint waivers to these
vendor files. WasMetal wrapper width and combinational-loop warnings remain fatal.
