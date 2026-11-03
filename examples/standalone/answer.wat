(module
  (memory 1 1)
  (global $bias (mut i32) (i32.const 7))
  (data (i32.const 16) "\23\00\00\00")
  (func $add (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add)
  (func (export "main") (result i32)
    i32.const 16
    i32.load
    global.get $bias
    call $add
    i32.const 0
    global.set $bias))
