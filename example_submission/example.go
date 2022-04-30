package example

// // doesn't compile
// func Negate(x bool) int {
// 	return !x
// }

// second doesn't compile
func Negate(x bool) string {
	return !x
}

// // compiles
// func Negate(x bool) bool {
// 	return !x
// }
