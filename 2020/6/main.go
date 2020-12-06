package main

import (
	"bufio"
	"fmt"
	"os"
)

const (
	inputFile string = "input.txt"
)

func ParseFile() int {
	file, err := os.Open(inputFile)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var row string
	sum := 0
	for scanner.Scan() {
		var entry string
		people := 0
		for row = scanner.Text(); len(row) != 0; row = scanner.Text() {
			people++
			entry = entry + row
			scanner.Scan()
		}
		//sum += countUniqueChars(entry)
		sum += getCompliance(entry, people)
	}
	return sum
}

func getCompliance(s string, cnt int) int {
	uniques := make(map[int32]int)
	for _, char := range s {
		if _, ok := uniques[char]; !ok {
			uniques[char] = 1
		} else {
			uniques[char]++
		}
	}

	fmt.Println(uniques)
	complianceCnt := 0
	for _, v := range uniques {
		if v == cnt {
			complianceCnt++
		}
	}
	return complianceCnt
}

func countUniqueChars(s string) int {
	uniques := make(map[int32]int)
	for _, char := range s {
		if _, ok := uniques[char]; !ok {
			uniques[char] = 0
		}
	}
	return len(uniques)
}

func main() {
	fmt.Println(ParseFile())
}
