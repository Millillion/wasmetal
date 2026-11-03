;; Two 64-element i32 vectors: a[n]=n-32, b[n]=(3*n % 11)-5.
(module
  (memory 1 1)
  (data (i32.const 0) "\e0\ff\ff\ff\e1\ff\ff\ff\e2\ff\ff\ff\e3\ff\ff\ff\e4\ff\ff\ff\e5\ff\ff\ff\e6\ff\ff\ff\e7\ff\ff\ff\e8\ff\ff\ff\e9\ff\ff\ff\ea\ff\ff\ff\eb\ff\ff\ff\ec\ff\ff\ff\ed\ff\ff\ff\ee\ff\ff\ff\ef\ff\ff\ff\f0\ff\ff\ff\f1\ff\ff\ff\f2\ff\ff\ff\f3\ff\ff\ff\f4\ff\ff\ff\f5\ff\ff\ff\f6\ff\ff\ff\f7\ff\ff\ff\f8\ff\ff\ff\f9\ff\ff\ff\fa\ff\ff\ff\fb\ff\ff\ff\fc\ff\ff\ff\fd\ff\ff\ff\fe\ff\ff\ff\ff\ff\ff\ff\00\00\00\00\01\00\00\00\02\00\00\00\03\00\00\00\04\00\00\00\05\00\00\00\06\00\00\00\07\00\00\00\08\00\00\00\09\00\00\00\0a\00\00\00\0b\00\00\00\0c\00\00\00\0d\00\00\00\0e\00\00\00\0f\00\00\00\10\00\00\00\11\00\00\00\12\00\00\00\13\00\00\00\14\00\00\00\15\00\00\00\16\00\00\00\17\00\00\00\18\00\00\00\19\00\00\00\1a\00\00\00\1b\00\00\00\1c\00\00\00\1d\00\00\00\1e\00\00\00\1f\00\00\00\fb\ff\ff\ff\fe\ff\ff\ff\01\00\00\00\04\00\00\00\fc\ff\ff\ff\ff\ff\ff\ff\02\00\00\00\05\00\00\00\fd\ff\ff\ff\00\00\00\00\03\00\00\00\fb\ff\ff\ff\fe\ff\ff\ff\01\00\00\00\04\00\00\00\fc\ff\ff\ff\ff\ff\ff\ff\02\00\00\00\05\00\00\00\fd\ff\ff\ff\00\00\00\00\03\00\00\00\fb\ff\ff\ff\fe\ff\ff\ff\01\00\00\00\04\00\00\00\fc\ff\ff\ff\ff\ff\ff\ff\02\00\00\00\05\00\00\00\fd\ff\ff\ff\00\00\00\00\03\00\00\00\fb\ff\ff\ff\fe\ff\ff\ff\01\00\00\00\04\00\00\00\fc\ff\ff\ff\ff\ff\ff\ff\02\00\00\00\05\00\00\00\fd\ff\ff\ff\00\00\00\00\03\00\00\00\fb\ff\ff\ff\fe\ff\ff\ff\01\00\00\00\04\00\00\00\fc\ff\ff\ff\ff\ff\ff\ff\02\00\00\00\05\00\00\00\fd\ff\ff\ff\00\00\00\00\03\00\00\00\fb\ff\ff\ff\fe\ff\ff\ff\01\00\00\00\04\00\00\00\fc\ff\ff\ff\ff\ff\ff\ff\02\00\00\00\05\00\00\00\fd\ff\ff\ff")
  (func (export "main") (param $passes i32) (result i32)
    (local $pass i32) (local $p i32) (local $sum v128)
    block $done loop $again
      local.get $pass local.get $passes i32.ge_u br_if $done
      i32.const 0 local.set $p
      loop $vector
        local.get $sum
        local.get $p v128.load
        local.get $p i32.const 256 i32.add v128.load
        i32x4.mul i32x4.add local.set $sum
        local.get $p i32.const 16 i32.add local.tee $p
        i32.const 256 i32.lt_u br_if $vector
      end
      local.get $pass i32.const 1 i32.add local.set $pass
      br $again
    end end
    local.get $sum i32x4.extract_lane 0
    local.get $sum i32x4.extract_lane 1 i32.add
    local.get $sum i32x4.extract_lane 2 i32.add
    local.get $sum i32x4.extract_lane 3 i32.add))

