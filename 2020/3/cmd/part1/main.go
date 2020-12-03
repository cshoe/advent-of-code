package main

import (
	"fmt"

	"github.com/cshoe/advent-of-code/2020/3/sled"
)

func main() {
	gs := sled.NewGameState()
	fmt.Println(gs.CountTrees(3, 1))
}
