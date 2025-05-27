# Style guide

## Naming

The convention for naming goes as follows:

| Type           | Casing           | Example       |
|----------------|------------------|---------------|
| Modules        | Lower snake case | my_module     |
| Functions      | Lower snake case | my_function   |
| Variables      | Lower snake case | my_variable   |
| Packages       | Upper Camel case | MyPackageName |
| Constants      | Upper snake case | MY_CONSTANT   |
| Structs, Enums | Upper camel case | MyStruct      |

## Testing

### Organization

Generally, it's preferred to have separate `module_test.move` files. These should be placed under the `tests` folder.

### Functions

Test functions that are to be reused by other functions should be `#[test_only]` and `public`.

Test functions should *never* be `entry`.

## Scripts

### Organization

Move scripts should be in the `scripts` folder. Ideally, they should be in a separate package, to not involve confusion
in compilation with the regular modules.