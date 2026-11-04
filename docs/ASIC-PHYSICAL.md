# Experimental ASIC physical tools

WasMetal has a reproducible tool-input check for an experimental SKY130HD
physical flow. It verifies the inputs needed for placement, clock trees and
routing. It does not establish a completed physical implementation.

```sh
python3 tools/asic_physical_tools.py
```

The command targets Ubuntu 24.04 on x86-64. It keeps OpenROAD and two additional
runtime packages in the project's private cache. Other OpenROAD runtime
dependencies must already be available on the host; missing libraries cause a
failure. CI installs those prerequisites on its disposable runner. The local
verification did not install system packages.

The [lock](../tools/asic_physical.lock.json) pins OpenROAD
`26Q2-1164-g08f67ee5ec`, its Ubuntu package, the two extra runtime packages and
seven physical platform files. OpenROAD comes from the download service linked
by the [official installation documentation](https://openroad.readthedocs.io/en/latest/user/Build.html).
Its [source revision](https://github.com/Precision-Innovations/OpenROAD/tree/08f67ee5ecd14db5a42be8c610bbfd1ccf079299)
is recorded. The platform files use the same OpenROAD-flow-scripts revision as
the [standard-cell functional reference](ASIC-STANDARD-CELLS.md).

The checker verifies package sizes and SHA256 values, every extracted file and
symlink, the executable hash and reported version. It rejects extra files in
the private package directories and checks physical-source byte counts,
SHA256 values and Git blob identities. Fresh extraction is verified in a
temporary directory before becoming the active cache. Source and resolved
shared-library identities are checked again before a successful report.

The [local report](verification/asic-physical-tools.json) covers 11,632 package
files, seven physical platform inputs and 133 resolved shared libraries. The
[archive](verification/asic-physical-tools/index.json) retains the source locks,
physical inputs, license notices and verification logs. Binary packages are
identified by their hashes and download URLs; they are not redistributed in
the archive. A failed check removes the previous output report.

The OpenROAD package hash was pinned from its first HTTPS download. This is
neither a vendor-signature attestation nor proof that rebuilding its source
produces that binary. Host runtime libraries are fingerprinted, rather than
assumed identical across computers. The tool-input CI job is separate from
functional and physical circuit verification.

These platform inputs do not select the final CPU's fabrication process.
A physical block still needs constrained timing, routing checks, functional
equivalence after physical changes and appropriate process-corner analysis.
SRAM macros, pads, manufacturing test, full-chip verification and foundry
signoff remain further work.
