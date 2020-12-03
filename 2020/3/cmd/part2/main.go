package main

import (
	"fmt"

	"github.com/cshoe/advent-of-code/2020/3/sled"
)

func main() {
	gs := sled.NewGameState()

	slopes := [5][2]int{
		{1, 1},
		{3, 1},
		{5, 1},
		{7, 1},
		{1, 2},
	}

	var product, treesHit int
	for i, slope := range slopes {
		treesHit = gs.CountTrees(slope[0], slope[1])
		if i == 0 {
			product = treesHit
		} else {
			product = product * treesHit
		}
	}
	fmt.Println(product)

}
