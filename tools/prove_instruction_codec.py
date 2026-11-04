#!/usr/bin/env python3
"""Prove lossless instruction storage for all binary inputs, with no opcode assumptions."""
import json
from pathlib import Path
import subprocess
from prepare_standalone import ROOT,digest


def main():
    directory=ROOT/'build/formal-instruction-codec';directory.mkdir(parents=True,exist_ok=True)
    encoder=ROOT/'soc/loader/wasmetal_instruction_encode.sv'
    decoder=ROOT/'soc/loader/wasmetal_instruction_decode.sv'
    original=ROOT/'tests/rtl/instruction_codec_proof.sv'
    inputs=[encoder,decoder,original,Path(__file__).resolve(),ROOT/'tools/upstream.lock.json',
            ROOT/'tools/prepare_standalone.py']
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs};proofs={}
    for name,negative in [('positive',False),('corrupted-opcode',True)]:
        source=original.read_text()
        if negative:
            needle='d(stored,restored)'
            if source.count(needle)!=1:raise ValueError('missing corruption point')
            source=source.replace(needle,"d(stored ^ 194'd1,restored)")
        harness=directory/(name+'.sv');harness.write_text(source)
        script=directory/(name+'.ys')
        script.write_text(f'read_verilog -sv {encoder} {decoder} {harness}\n'
            'prep -top codec_proof -flatten\nsat -verify -prove ok 1 -show-inputs -show-outputs\n')
        logfile=directory/(name+'.log')
        with logfile.open('w') as log:
            result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/yosys'),'-Q','-T','-s',str(script)],
                cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=120)
        expected='proof did fail' if negative else 'SUCCESS!'
        if (result.returncode!=0)!=negative or expected not in logfile.read_text():
            raise ValueError('codec proof did not reach its expected outcome: '+name)
        proofs[name]={'expected_outcome':'rejected' if negative else 'proven',
                     'log_sha256':digest(logfile),'script_sha256':digest(script)}
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):
        raise ValueError('instruction codec inputs changed during proof')
    report={'status':'passed','scope':'combinational binary proof; no opcode-specific assumptions or memory/loader integration',
        'expanded_bits':288,'stored_bits':194,'properties':[
            'encodable if and only if decoding the encoded row reproduces all 288 input bits',
            'all 32 opcode bits are preserved even for a rejected row',
            'every 194-bit stored word decodes to an encodable expanded row',
            'decoding then re-encoding and decoding preserves the expanded row'],
        'proofs':proofs,'negative_control_rejected':True,'inputs':hashes,
        'physical_hardware_tested':False}
    target=ROOT/'reports/instruction-codec-proof.json';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS all-input instruction codec proofs and corrupted-opcode negative control')


if __name__=='__main__':main()
