package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

type loc struct {
	instruction string
	arg         int
}

var locParser = regexp.MustCompile(`(acc|jmp|nop) ([+-]{1}\d+)`)

func newLoc(line string) *loc {
	l := new(loc)
	matches := locParser.FindStringSubmatch(line)
	if len(matches) < 3 {
		panic("Syntax error")
	}
	arg, err := strconv.Atoi(matches[2])
	if err != nil {
		panic("Bad arg")
	}
	l.instruction = matches[1]
	l.arg = arg
	return l
}

type machine struct {
	pointer int
	acc     int
	code    []*loc
}

func newMachine(filename string) *machine {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	lines := make([]*loc, 0)
	for scanner.Scan() {
		lines = append(lines, newLoc(scanner.Text()))
	}
	m := new(machine)
	m.pointer = 0
	m.acc = 0
	m.code = lines
	return m
}

// execute runs the machine from it's current state and returns
// the value of the accumulator when a loop is detected
func (m *machine) execute() (int, error) {
	stack := make(map[int]int, 0)
	for {
		if m.pointer >= len(m.code) {
			return m.acc, nil
		}
		if _, ok := stack[m.pointer]; !ok {
			stack[m.pointer] = 0
		} else {
			return 0, errors.New("Loop detected")
		}
		l := m.code[m.pointer]
		switch inst := l.instruction; inst {
		case "nop":
			m.doNop(l)
		case "jmp":
			m.doJmp(l)
		case "acc":
			m.doAcc(l)
		}
	}
}

func (m *machine) doNop(l *loc) {
	m.pointer++
}

func (m *machine) doJmp(l *loc) {
	m.pointer += l.arg
}

func (m *machine) doAcc(l *loc) {
	m.acc += l.arg
	m.pointer++
}

func main() {
	m := newMachine("input.txt")
	var orig string
	for i, line := range m.code {
		if line.instruction != "acc" {
			switch line.instruction {
			case "jmp":
				orig = "jmp"
				line.instruction = "nop"
			case "nop":
				orig = "nop"
				line.instruction = "jmp"
			}
			acc, err := m.execute()
			if err == nil {
				fmt.Println(acc)
				return
			}
			m.code[i].instruction = orig
			m.pointer = 0
			m.acc = 0
		}
	}
	fmt.Printf("uh oh %d", m.acc)
}
