package example

// import "fmt"

//==================================================
// This compiles
//==================================================
func NegateCorrect(x bool) bool {
	//y := 5/0
	return !x
}

//==================================================
// This panics
//==================================================

//cannot use !x (type bool) as type int in return argument
func Negate(x bool) bool {
	panic("hello")
	return !x
}
