package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const (
	inputFile string = "whole_input.txt"
)

func parseFile() []string {
	file, err := os.Open(inputFile)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	lines := make([]string, 0, 30)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines
}

func getDownStreams(lines []string, target string) map[string]int {
	matches := make([]string, 0, 10)
	uniques := make(map[string]int)
	for _, l := range lines {
		parts := strings.Split(l, " bags contain ")
		if len(parts) < 2 {
			panic("Malformed parts")
		}

		if strings.Contains(parts[1], target) {
			matches = append(matches, parts[0])
			if _, ok := uniques[parts[0]]; !ok {
				uniques[parts[0]] = 0
			}
		}
	}
	if len(uniques) > 0 {
		for k1 := range uniques {
			for k2 := range getDownStreams(lines, k1) {
				if _, ok := uniques[k2]; !ok {
					uniques[k2] = 0
				}
			}
		}
	}
	return uniques
}

var recordMatcher = regexp.MustCompile(`(\d) (\w* \w*) bag[s]?`)

func getBagWeight(lines []string, target string) int {
	totalWeight := 0
	var bagDesc string
	for _, l := range lines {
		if strings.Index(l, target) == 0 {
			bagDesc = l
			break
		}
	}
	matches := recordMatcher.FindAllStringSubmatch(bagDesc, -1)
	for _, match := range matches {
		i, err := strconv.Atoi(match[1])
		if err != nil {
			panic(fmt.Sprintf("Bad count found: %s", match[1]))
		}
		totalWeight += i + (i * getBagWeight(lines, match[2]))
	}
	return totalWeight
}

func main() {
	lines := parseFile()
	fmt.Printf("%d bag colors will eventually contain a 'shiny gold' bag\n", len(getDownStreams(lines, "shiny gold")))
	fmt.Printf("A 'shiny gold' bag has %d bags inside.\n", getBagWeight(lines, "shiny gold"))
}
