#!/usr/bin/env python3
"""Check the actual C++ clock scheduler against independently enumerated edges."""
import json
from pathlib import Path
import shutil
import subprocess

from check_sdram_async_system import CLOCKS
from prepare_standalone import ROOT, digest


def main():
    directory = ROOT/'build/sdram-clock-driver'; directory.mkdir(parents=True, exist_ok=True)
    output = ROOT/'reports/sdram-clock-driver.json'; output.parent.mkdir(exist_ok=True)
    output.unlink(missing_ok=True)
    compiler = Path(shutil.which('g++')).resolve(); compiler_hash = digest(compiler)
    source = ROOT/'tests/sdram_async/loadable.cpp'
    text = source.read_text(); marker = '#define Vwasmetal_loadable AsyncSdramSystemModel'
    if text.count(marker) != 1:
        raise ValueError('review scheduler extraction boundary')
    prefix = text.split(marker)[0]
    fake = directory/'Vwasmetal_loadable.h'
    fake.write_text('''#pragma once
#include <cstdint>
#include <iostream>
struct ClockContext { uint64_t time=0; void timeInc(uint64_t delta) { time+=delta; } };
class Vwasmetal_loadable {
    ClockContext context_; bool old_cpu_=0, old_memory_=0;
public:
    uint8_t clk=0,memory_clk=0;
    virtual ~Vwasmetal_loadable() = default;
    ClockContext* contextp() { return &context_; }
    void final() {}
    void eval() {
        if(clk!=old_cpu_ || memory_clk!=old_memory_) {
            std::cout<<context_.time<<" "<<unsigned(clk)<<" "<<unsigned(memory_clk)<<"\\n";
            old_cpu_=clk;old_memory_=memory_clk;
        }
    }
};
''')
    main = '\nint main() { AsyncSdramSystemModel model; model.eval(); for(int i=0;i<200;i++) { model.clk=0;model.eval();model.clk=1;model.eval();model.clk=0;model.eval(); } }\n'
    mutations = {'early CPU edge': ('clk=previous_cpu_;', '/* missing restoration */'),
        'lost simultaneous edge': ('if(next_memory_==end)', 'if(false)'),
        'wrong memory period': ('next_memory_+=MEMORY_HALF_PERIOD;', 'next_memory_+=MEMORY_HALF_PERIOD+1;')}
    checks = []
    for name, clock in CLOCKS.items():
        header = directory/'clock_parameters.hpp'
        header.write_text('#pragma once\n#include <cstdint>\n'+
            f'constexpr uint64_t CPU_HALF_PERIOD={clock["cpu_half_period"]};\n'+
            f'constexpr uint64_t MEMORY_HALF_PERIOD={clock["memory_half_period"]};\n'+
            f'constexpr uint64_t MEMORY_PHASE={clock["memory_phase"]};\n'+
            'constexpr const char* CLOCK_COVERAGE='+json.dumps(str(directory/'counts.jsonl'))+';\n')
        end = 400*clock['cpu_half_period']
        cpu = set(range(clock['cpu_half_period'], end+1, clock['cpu_half_period']))
        memory = set(range(clock['memory_phase'], end+1, clock['memory_half_period']))
        cpu_level = memory_level = 0; expected = []
        for when in sorted(cpu|memory):
            if when in cpu:
                cpu_level ^= 1
            if when in memory:
                memory_level ^= 1
            expected.append([when, cpu_level, memory_level])
        for mutation in [None, *mutations]:
            body = prefix
            if mutation:
                before, after = mutations[mutation]
                if body.count(before) != 1:
                    raise ValueError('review scheduler mutation anchor')
                body = body.replace(before, after)
            case = name+('-'+mutation.replace(' ', '-') if mutation else '-positive')
            path = directory/(case+'.cpp'); path.write_text(body+main)
            binary = directory/case
            subprocess.run([str(compiler), '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-I'+str(directory),
                str(path), '-o', str(binary)], cwd=ROOT, check=True, capture_output=True, text=True)
            run = subprocess.run([str(binary)], cwd=ROOT, capture_output=True, text=True, timeout=10)
            run.check_returncode()
            actual = [list(map(int, line.split())) for line in run.stdout.splitlines()]
            same = actual == expected
            if same != (mutation is None):
                raise ValueError('clock edge oracle did not distinguish '+case)
            checks.append({'clock': name, 'mutation': mutation, 'exact_edge_match': same,
                'reference_events': len(expected), 'observed_events': len(actual),
                'generated_source_sha256': digest(path), 'binary_sha256': digest(binary)})
    if source.read_text() != text:
        raise ValueError('clock driver changed during verification')
    if digest(compiler) != compiler_hash:
        raise ValueError('clock driver compiler changed during verification')
    report = {'status': 'passed', 'scope': 'Actual C++ scheduler with a recording stand-in for eval; exact independent clock-event oracle, not CPU or DRAM correctness',
        'inputs': {str(path.relative_to(ROOT)): digest(path) for path in
            [source, Path(__file__).resolve(), ROOT/'tools/check_sdram_async_system.py', ROOT/'tools/prepare_standalone.py']},
        'checks': checks, 'compiler': {'path': str(compiler), 'sha256': compiler_hash},
        'physical_hardware_tested': False}
    output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS both exact clock traces and all six clock-scheduler mutations')


if __name__ == '__main__':
    main()
