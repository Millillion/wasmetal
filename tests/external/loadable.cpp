// SPDX-License-Identifier: MIT
// Reuse the pin-level uploader unchanged, while flushing simulation-only bus
// coverage from the HDL's final block when the model is destroyed.
#include "Vwasmetal_loadable.h"
class AxiSystemModel final : public Vwasmetal_loadable {
public:
    ~AxiSystemModel() override { final(); }
};
#define Vwasmetal_loadable AxiSystemModel
#include "../standalone/loadable.cpp"
#undef Vwasmetal_loadable
