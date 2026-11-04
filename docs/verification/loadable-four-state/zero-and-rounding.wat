(module (memory 1 1)
 (func (export "main") (result i32 f32 f64 f32 f64 f32 f64 v128 v128 f64)
  i32.const 32 i32.load
  f32.const -0.5 f32.nearest
  f64.const 1.5 f64.nearest
  f32.const -0.25 f32.ceil
  f64.const -0.25 f64.floor
  f32.const 1.875 f32.trunc
  f64.const 0.25 f64.ceil
  v128.const f32x4 -0.5 1.5 -0.25 2.75 f32x4.nearest
  v128.const f64x2 -0.25 2.75 f64x2.floor
  f64.const nan:0x1 f64.trunc))
