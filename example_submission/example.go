package example

// doesn't compile
func Negate(x bool) int {
	return !x
}

// // compiles
// func Negate(x bool) bool {
// 	return !x
// }
