package example

//==================================================
// This compiles
//==================================================
// func Negate(x bool) bool {
// 	return !x
// }

//==================================================
// This doesn't compile
//==================================================

// cannot use !x (type bool) as type int in return argument
func Negate(x bool) int {
	return !x
}

// // cannot use !x (type bool) as type int in return argument
// func Negate(x bool) string {
// 	return !x
// }

//==================================================
// This panics
//==================================================

// cannot use !x (type bool) as type int in return argument
// func Negate(x bool) bool {
// 	panic("hello")
// 	return !x
// }

// Output:
// ['Submitted 01/21/22 20:56:47 +0000\n', '## Grade: 0.00%',
// '  * 0 points of a possible 10',
// '  * Passed   0 / 0  tests     (0 failed)',
// '    * // Passed  0 / 0 subtests  (0 failed)',
// '## Correctness Tests']

// Output:
// ['Submitted 01/21/22 20:56:47 +0000\n', '## Grade: 100.00%',
// '  * 10 points of a possible 10',
//  '  * Passed   1 / 1  tests     (0 failed)',
// '    * Passed  0 / 0 subtests  (0 failed)',
//  '## Correctness Tests', '### 1. Negate', '                               -- test passed --']
