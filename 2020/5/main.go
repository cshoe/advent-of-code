package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const (
	inputFile string = "input.txt"
)

func calculateSeatID(s string) int {
	s = strings.ReplaceAll(s, "F", "0")
	s = strings.ReplaceAll(s, "B", "1")
	s = strings.ReplaceAll(s, "R", "1")
	s = strings.ReplaceAll(s, "L", "0")
	i, err := strconv.ParseInt(s, 2, 0)
	if err != nil {
		panic(err)
	}
	return int(i)
}

func getSeatIDs() []int {
	ids := make([]int, 0, 900)
	file, err := os.Open(inputFile)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		ids = append(ids, calculateSeatID(scanner.Text()))
	}
	return ids
}

func getMaxAndMin(ids []int) (int, int) {
	if len(ids) == 0 {
		panic("Empty or nil slice found")
	}
	max, min := ids[0], ids[0]
	for _, id := range ids[1:] {
		if id > max {
			max = id
		}

		if id < min {
			min = id
		}
	}
	return max, min
}

func sumRange(max, min int) int {
	sum := 0
	for i := min; i <= max; i++ {
		sum += i
	}
	return sum
}

func main() {
	ids := getSeatIDs()
	max, min := getMaxAndMin(ids)
	fmt.Printf("Max seat ID is: %d\n\n", max)

	seatID := sumRange(max, min)
	for _, id := range ids {
		seatID -= id
	}

	fmt.Printf("Your seat is: %d\n\n", seatID)
}
