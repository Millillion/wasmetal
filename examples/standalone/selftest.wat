;; Exercises every backing-memory kind and several independent execution units.
(module
  (type $unary (func (param i32) (result i32)))
  (type $cell (struct (field (mut i32))))
  (type $cells (array (mut i32)))
  (memory $empty 0 0)
  (memory $ram 1 1)
  (table 4 8 funcref)
  (global $bias (mut i32) (i32.const 1))
  (global $initial (ref $cell) (struct.new $cell (i32.const 39)))
  (tag $event (param i32))
  (data (memory $ram) (i32.const 16) "\23\00\00\00")
  (data $blob "\11\22\33\44")
  (elem (i32.const 0) $inc $double)
  (elem $elements func $double)
  (func $inc (type $unary) local.get 0 i32.const 1 i32.add)
  (func $double (type $unary) local.get 0 i32.const 2 i32.mul)
  (func $tail (type $unary)
    local.get 0
    if (result i32)
      local.get 0 i32.const 1 i32.sub return_call $tail
    else
      i32.const 99
    end)
  (func $initialize
    global.get $bias i32.const 6 i32.add global.set $bias)
  (start $initialize)
  (func $catch (result i32)
    (block $caught (result i32)
      (try_table (result i32) (catch $event $caught)
        i32.const 42 throw $event)))
  (func (export "main") (result i32 i32 i32 i32 f32 f64 v128 i32 i32 i32 i32 i32)
    ;; Exercise data/element ROMs and bulk writes before reading the results.
    i32.const 32 i32.const 0 i32.const 4 memory.init $ram $blob
    i32.const 33 i32.const 32 i32.const 3 memory.copy $ram $ram
    i32.const 40 i32.const 165 i32.const 3 memory.fill $ram
    i32.const 2 i32.const 0 i32.const 1 table.init $elements
    ;; A fresh allocation must not overwrite the object allocated during boot.
    i32.const 1 struct.new $cell drop
    i32.const 16 i32.load $ram global.get $bias i32.add
    i32.const 21 i32.const 2 call_indirect (type $unary)
    i32.const 1 ref.func $inc call_ref $unary
    global.get $initial struct.get $cell 0
    f32.const 1.5 f32.const 2.25 f32.add
    f64.const 9 f64.sqrt
    v128.const i16x8 1 2 3 4 5 6 7 8
    v128.const i16x8 10 20 30 40 50 60 70 80
    i16x8.add
    call $catch
    i32.const 32 i32.load $ram
    i32.const 41 i32.load16_u $ram
    i32.const 10 i32.const 20 i32.const 30 array.new_fixed $cells 3
    i32.const 1 array.get $cells
    i32.const 100 call $tail))
