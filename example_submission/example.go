package example

import "fmt"

//==================================================
// This compiles
//==================================================
func NegateCorrect(x bool) string {
	x := 5 / 0
	return !x
}
