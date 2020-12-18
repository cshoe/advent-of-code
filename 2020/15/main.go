package main

import (
	"fmt"
)

type gameState struct {
	spokenNumbers map[int][]int

	lastTurn int

	lastSpoken int
}

func newGameState(startingNumbers []int) *gameState {
	spokenNumbers := make(map[int][]int)

	for idx, num := range startingNumbers {
		turnsSpoken := make([]int, 1, 2)
		turnsSpoken[0] = idx + 1
		spokenNumbers[num] = turnsSpoken
	}

	lastTurn := len(startingNumbers)
	lastSpoken := startingNumbers[len(startingNumbers)-1]

	return &gameState{spokenNumbers: spokenNumbers, lastTurn: lastTurn, lastSpoken: lastSpoken}
}

func (gs *gameState) play() {
	lastTurn := gs.lastTurn
	lastSpoken := gs.lastSpoken
	currentTurn := lastTurn + 1

	var toSpeak int

	if val, ok := gs.spokenNumbers[lastSpoken]; ok {
		if len(val) == 1 {
			toSpeak = 0
		} else if len(val) == 2 {
			toSpeak = val[1] - val[0]
		}
	}

	if turnsSpoken, ok := gs.spokenNumbers[toSpeak]; !ok {
		// that number has never been spoken
		turnsSpoken := make([]int, 1, 2)
		turnsSpoken[0] = currentTurn
		gs.spokenNumbers[toSpeak] = turnsSpoken
	} else {
		if len(turnsSpoken) == 1 {
			gs.spokenNumbers[toSpeak] = append(turnsSpoken, currentTurn)
		} else if len(turnsSpoken) == 2 {
			turnsSpoken[0] = turnsSpoken[1]
			turnsSpoken[1] = currentTurn
		}
	}
	gs.lastTurn++
	gs.lastSpoken = toSpeak
}

func runGame(input []int, iterations int) {
	gs := newGameState(input)
	for i := 0; i < iterations-len(input); i++ {
		if gs.lastTurn%1000000 == 0 {
			fmt.Printf("Turn %d: %d\n", gs.lastTurn, gs.lastSpoken)
		}
		gs.play()
	}
	fmt.Printf("Turn %d: %d\n", gs.lastTurn, gs.lastSpoken)
}

func part1() {
	runGame([]int{8, 11, 0, 19, 1, 2}, 2020)
}

func part2() {
	runGame([]int{8, 11, 0, 19, 1, 2}, 30000000)
}

func main() {
	part1()
	part2()
}
