package example

import ("fmt")
//==================================================
// This compiles
//==================================================
func NegateCorrect(x bool) string {
	return !x
}

//==================================================
// This panics
//==================================================

// cannot use !x (type bool) as type int in return argument
func Negate(x bool) int {
	// panic("hello")
	return !x
}