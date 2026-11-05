#include "Vcarry_ports.h"
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("expected one oracle trace");
        std::ifstream trace(argv[1]);
        std::array<uint8_t, 1024> expected{};
        for (auto& value : expected) {
            std::string a, b;
            if (!(trace >> a >> b) || a.size() != 8 || a != b || a.find_first_not_of("01") != std::string::npos)
                throw std::runtime_error("invalid binary carry oracle");
            value = static_cast<uint8_t>(std::stoul(a, nullptr, 2));
        }
        std::string extra;
        if (trace >> extra) throw std::runtime_error("extra carry oracle data");
        auto dut = std::make_unique<Vcarry_ports>();
        unsigned checks = 0;
        auto check = [&] {
            dut->eval();
            if (dut->observed != expected[dut->pins])
                throw std::runtime_error("CARRY_ORACLE_MISMATCH pins="+std::to_string(dut->pins));
            ++checks;
        };
        for (unsigned value = 0; value < expected.size(); ++value) {
            dut->pins = static_cast<uint16_t>(value);
            check();
        }
        for (unsigned value = 0; value < expected.size(); ++value) {
            for (unsigned bit = 0; bit < 10; ++bit) {
                const unsigned mask = 1U << bit;
                dut->pins = static_cast<uint16_t>((dut->pins & ~mask) | (value & mask));
                check();
            }
        }
        dut->final();
        std::cout << "PASS " << checks << " CARRY4 C++ input transitions\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
