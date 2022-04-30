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
// func Negate(x bool) int {
// 	return !x
// }

// // cannot use !x (type bool) as type int in return argument
// func Negate(x bool) string {
// 	return !x
// }

// cannot use !x (type bool) as type int in return argument
func Negate(x bool) byte {
	return !x
}
