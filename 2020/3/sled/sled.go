// Package sled provides sledding fun like in Christmas Vacation
package sled

import (
	"bufio"
	"os"
	"strings"
)

const (
	// byte that represents tress on the map
	tree string = "#"

	// byte that represents open spaces on the map
	open string = "."

	// file where the map is stored
	mapInputFile string = "input.txt"
)

// TreeMap represents a map of trees to be navigated.
type TreeMap struct {
	Layout [][]string

	// Convenience fields to store the height and width of the map
	// instead of calculating from the Layout every time they are needed
	Height int
	Width  int
}

// Location represents the X and Y coordinates of the Sled
type Location struct {
	X int
	Y int
}

// GameState represents the current TreeMap and location of the sled
type GameState struct {
	Map             *TreeMap
	CurrentLocation *Location
}

// NewGameState creates a new GameState based on the given TreeMap. This constructor
// assumes that the sled will always start in the upper left corner of the map at (0,0)
func NewGameState() *GameState {
	sl := new(Location)
	sl.X = 0
	sl.Y = 0

	m := newTreeMap()

	return &GameState{Map: m, CurrentLocation: sl}
}

// moveSled moves the sled's location in the current gamestate
func (gs *GameState) moveSled(deltaX, deltaY int) {
	gs.CurrentLocation.X += deltaX
	gs.CurrentLocation.Y += deltaY

	// check to see if the sled has gone "off" the width
	// of the map. This means the sled needs to wrap around
	// to the beginning to simulate the repetitive nature of
	// the environment
	if gs.CurrentLocation.X >= gs.Map.Width {
		gs.CurrentLocation.X -= gs.Map.Width
	}
}

// isCurrentLocationATree tests if the sled is currently on a tree
func (gs *GameState) isCurrentLocationATree() bool {
	return gs.Map.Layout[gs.CurrentLocation.Y][gs.CurrentLocation.X] == tree
}

func openMapFile() *bufio.Scanner {
	file, err := os.Open(mapInputFile)
	if err != nil {
		panic(err)
	}

	return bufio.NewScanner(file)
}

func newTreeMap() *TreeMap {
	scanner := openMapFile()
	var row string
	tm := new(TreeMap)
	for scanner.Scan() {
		row = scanner.Text()
		tm.Layout = append(tm.Layout, strings.Split(row, ""))
	}
	tm.Height = len(tm.Layout)
	tm.Width = len(tm.Layout[0])

	return tm
}

// CountTrees gives the number of trees that would be encountered
// when traveling on a slope of x, y
func (gs *GameState) CountTrees(x, y int) int {
	// reset the state's location
	gs.CurrentLocation.Y = 0
	gs.CurrentLocation.X = 0

	treesHit := 0

	// Loop while the sled is still on the map
	for {
		gs.moveSled(x, y)
		if gs.CurrentLocation.Y > gs.Map.Height-1 {
			break
		}
		if gs.isCurrentLocationATree() {
			treesHit++
		}
	}
	return treesHit
}
