package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

// Find the min value in `array`. Return the value and it's index.
// All of the values in array are assumed to be positive integers.
func minAndIndex(array [3]int) (int, int) {
	min, index := 0, 0
	for i, val := range array {
		if i == 0 {
			min = val
			index = i
		} else {
			if val < min {
				min = val
				index = i
			}
		}
	}
	return min, index
}

func sum(array [3]int) int {
	result := 0
	for _, val := range array {
		result += val
	}
	return result
}

func part1() {
	readFile, err := os.Open("input.txt")
	defer readFile.Close()

	if err != nil {
		fmt.Println(err)
	}
	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	maxCalories, currentTotalCalories := 0, 0
	for fileScanner.Scan() {
		calsOnLine, err := strconv.Atoi(fileScanner.Text())
		if err != nil {
			if currentTotalCalories > maxCalories {
				maxCalories = currentTotalCalories
			}
			currentTotalCalories = 0
		} else {
			currentTotalCalories += calsOnLine
		}
	}

	fmt.Printf("Max number of calories is: %d\n", maxCalories)
}

func part2() {
	readFile, err := os.Open("input.txt")
	defer readFile.Close()

	if err != nil {
		fmt.Println(err)
	}
	fileScanner := bufio.NewScanner(readFile)
	fileScanner.Split(bufio.ScanLines)

	maxCalorieElves := [...]int{0, 0, 0}
	currentTotalCalories := 0
	for fileScanner.Scan() {
		calsOnLine, err := strconv.Atoi(fileScanner.Text())
		if err != nil {
			min, minIndex := minAndIndex(maxCalorieElves)
			if currentTotalCalories > min {
				maxCalorieElves[minIndex] = currentTotalCalories
			}
			currentTotalCalories = 0
		} else {
			currentTotalCalories += calsOnLine
		}
	}

	fmt.Printf("Total calories of top 3 elves: %d\n", sum(maxCalorieElves))
}

func main() {
	part1()
	part2()
}
