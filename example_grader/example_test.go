package example_grader

import (
	"example.com/example"
	"testing"
)

func TestCorrect(t *testing.T) {
	if example.NegateCorrect(true) {
		t.Errorf("Expected false, was true")
	}


}

func TestNegate(t *testing.T) {
	panic("Hi, Moma! I am panicking.")
	if example.Negate(true) {
		t.Errorf("Expected false, was true")
	}
}
