// Package passports provides convenient functionality
// for hacking passport systems
package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const (
	inputFile string = "../input.txt"
)

type valueValidator func(string) bool
type valueFinder func(regexp.Regexp) string

func ParseFile(fn valueValidator) int {
	file, err := os.Open(inputFile)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var row string
	validCnt := 0
	for scanner.Scan() {
		var entry string
		for row = scanner.Text(); len(row) != 0; row = scanner.Text() {
			entry = entry + " " + row
			scanner.Scan()
		}
		if fn(entry) {
			validCnt++
		}
	}
	return validCnt
}

type field struct {
	name string
	//finder    valueFinder
	validator valueValidator
}

func (f *field) findValue(s string) (string, error) {
	r := regexp.MustCompile(fmt.Sprintf(`%s:(?P<val>\S*)`, f.name))
	matches := r.FindStringSubmatch(s)
	if len(matches) < 2 {
		return "", errors.New("No matchfound")
	}
	return matches[1], nil
}

func (f *field) isValid(s string) bool {
	value, err := f.findValue(s)
	if err != nil || len(value) == 0 {
		//fmt.Println("missing")
		return false
	}
	//if !f.validator(value) {
	//fmt.Println("invalid: " + value)
	//}
	return f.validator(value)
}

var hgtFinder = regexp.MustCompile(`(?P<number>\d{2,3})(?P<unit>cm|in)`)

var requiredFields = [...]field{
	{"byr", validateInt(1920, 2002)},
	{"iyr", validateInt(2010, 2020)},
	{"eyr", validateInt(2020, 2030)},
	{"byr", validateInt(1920, 2002)},
	{"hgt", validateHgt},
	{"hcl", validateStr(regexp.MustCompile(`^#([a-f]|[0-9]){6}$`))},
	{"ecl", validateStr(regexp.MustCompile(`^(amb|blu|brn|gry|grn|hzl|oth)$`))},
	{"pid", validateStr(regexp.MustCompile(`^\d{9}$`))},
}

func validateHgt(s string) bool {
	matches := hgtFinder.FindStringSubmatch(s)
	if len(matches) < 3 {
		return false
	}
	switch matches[2] {
	case "in":
		return validateInt(59, 76)(matches[1])
	case "cm":
		return validateInt(150, 193)(matches[1])
	}
	return false
}

func validateInt(low, high int) func(string) bool {
	return func(val string) bool {
		i, err := strconv.Atoi(val)
		if err != nil {
			return false
		}
		return low <= i && i <= high
	}
}

func validateStr(r *regexp.Regexp) func(string) bool {
	return func(val string) bool {
		return r.MatchString(val)
	}
}

func containsRequiredFields(p string) bool {
	if len(p) < 32 {
		return false
	}
	for _, field := range requiredFields {
		if !strings.Contains(p, field.name+":") {
			return false
		}
	}
	return true
}

func containsValidRequiredFields(p string) bool {
	if len(p) < 64 {
		return false
	}
	for _, field := range requiredFields {
		if !field.isValid(p) {
			//fmt.Println(field)
			//fmt.Println(p)
			return false
		}
	}
	return true
}

func main() {
	fmt.Println(ParseFile(containsRequiredFields))
	fmt.Println(ParseFile(containsValidRequiredFields))
}
