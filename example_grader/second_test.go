package example_grader

import (
	"example.com/example"
	"testing"
)

func TestSecondNegate(t *testing.T) {
	if example.Negate(true) {
		t.Errorf("Expected false, was true")
	}
}

// func TestSecondNegateTA(t *testing.T) {
// 	if example.Negate(true) {
// 		t.Errorf("Expected false, was true")
// 	}
// }

