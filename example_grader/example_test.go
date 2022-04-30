package example_grader

import (
	"example.com/example"
	"testing"
)

func SecondNegate(t *testing.T) {
	if example.Negate(true) {
		t.Errorf("Expected false, was true")
	}
}
