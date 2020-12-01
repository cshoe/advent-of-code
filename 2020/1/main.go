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

	// Loop through every possible iteration looking for targetAmount
	var firstEntry, secondEntry, i, j int
	for i, firstEntry = range entries {
		for j, secondEntry = range entries {
			// Don't try to an entry against itself
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

func main() {
	entries, err := getEntries()
	if err != nil {
		fmt.Println(err)
		return
	}

	targetEntries, err := findTargetEntries(entries)
	fmt.Printf("Product of entries is: %d\n", targetEntries[0]*targetEntries[1])
}
