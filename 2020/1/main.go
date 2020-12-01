package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
)

const (
	targetAmount int    = 2020
	inputFile    string = "input.txt"
)

func findTargetEntries(entries []int) ([2]int, error) {

	// Loop through every possible iteration looking for two entires that add to
	// targetAmount
	var firstEntry, secondEntry, i, j int
	for i, firstEntry = range entries {
		for j, secondEntry = range entries {
			// Don't test an entry against itself
			if i == j {
				continue
			}

			if firstEntry+secondEntry == targetAmount {
				return [2]int{firstEntry, secondEntry}, nil
			}
		}
	}

	return [2]int{}, errors.New("Target amount not found")
}

func findThreeTargetEntries(entries []int) ([3]int, error) {
	// Loop through every possible iteration looking for three entires that add to
	// targetAmount
	var firstEntry, secondEntry, thirdEntry, i, j, k int
	for i, firstEntry = range entries {
		for j, secondEntry = range entries {
			for k, thirdEntry = range entries {
				// skip iterations that reuse and entry
				if i == j || j == k || i == k {
					continue
				}

				if firstEntry+secondEntry+thirdEntry == targetAmount {
					return [3]int{firstEntry, secondEntry, thirdEntry}, nil
				}
			}
		}
	}

	return [3]int{}, errors.New("Target amount not found")

}

// Read entries from input.txt in the same directory
func getEntries() ([]int, error) {
	var entries []int

	file, err := os.Open(inputFile)
	if err != nil {
		return nil, err
	}

	scanner := bufio.NewScanner(file)

	var inputEntry string
	var convertedEntry int
	var convertErr error

	for scanner.Scan() {
		inputEntry = scanner.Text()
		convertedEntry, convertErr = strconv.Atoi(inputEntry)
		if convertErr != nil {
			return nil, err
		}
		entries = append(entries, convertedEntry)
	}
	return entries, nil
}

func part1() {
	entries, err := getEntries()
	if err != nil {
		fmt.Println(err)
		return
	}
	targetEntries, err := findTargetEntries(entries)
	fmt.Printf("Part 1 product of entries is: %d\n", targetEntries[0]*targetEntries[1])
}

func part2() {
	entries, err := getEntries()
	if err != nil {
		fmt.Println(err)
		return
	}
	targetEntries, err := findThreeTargetEntries(entries)
	fmt.Printf("Part 2 product of entries is: %d\n", targetEntries[0]*targetEntries[1]*targetEntries[2])
}

func main() {
	part1()
	part2()
}
