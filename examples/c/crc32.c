// SPDX-License-Identifier: MIT
// Freestanding C: no imports, libc, allocator or operating system.
#include <stdint.h>

static volatile uint8_t payload[1024];

uint32_t checksum(uint32_t length) {
    if (length > sizeof(payload)) return UINT32_MAX;
    for (uint32_t index = 0; index < length; ++index)
        payload[index] = (uint8_t)index;
    uint32_t crc = UINT32_MAX;
    for (uint32_t index = 0; index < length; ++index) {
        crc ^= payload[index];
        for (unsigned bit = 0; bit < 8; ++bit)
            crc = (crc >> 1) ^ (UINT32_C(0xedb88320) & (UINT32_C(0) - (crc & UINT32_C(1))));
    }
    return ~crc;
}
