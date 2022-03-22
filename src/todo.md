# features:
- [X] make pointer `*int` as in rust instead of `int*` as in c, because that's how i can use type as an expression (`int*` =
  deref int or ptr to int type)
- [X] `as` binary operator
- better statement recognition
- [X] codegen_cpp split into files
- [X] linter split into files
- [X] merge Type and BarType
- better way of codegen assign
- [X] assign codegen
- think about how copy constructor in structure should work
- overriding functions
- own tokenizer
- import
- declare

# other
- cmd run
- address operator 
- sizeof function
- read/write specifier
- macro call without `()`

# future
- agnostic design
  - nasm codegen 
  - llvm codegen
- tests
- barman
- even better error handling 
  - test this too
- benchmarks