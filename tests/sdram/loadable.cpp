// SPDX-License-Identifier: MIT
// Preserve the existing pin-level upload oracle and flush device coverage.
#include "Vwasmetal_loadable.h"
class SdramSystemModel final : public Vwasmetal_loadable {
public:
    ~SdramSystemModel() override { final(); }
};
#define Vwasmetal_loadable SdramSystemModel
#include "../standalone/loadable.cpp"
#undef Vwasmetal_loadable
