package example_grader

import (
	"example.com/example"
	"testing"
)

func TestNegate(t *testing.T) {
	if example.Negate(true) {
		t.Errorf("Expected false, was true")
	}
}


// func TestNegateTwo(t *testing.T) {
// 	if example.Negate(true) {
// 		t.Errorf("Expected false, was true")
// 	}
// }
