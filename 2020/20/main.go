package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"
)

var neighbors = map[string][2]int{
	"top":    [2]int{0, -1},
	"right":  [2]int{1, 0},
	"bottom": [2]int{0, 1},
	"left":   [2]int{-1, 0},
}

type tile struct {
	id     int
	top    string
	right  string
	bottom string
	left   string
}

type board struct {
	tiles  [][]*tile
	length int
}

func newBoard(t []*tile) *board {
	length := int(math.Sqrt(float64(len(t))))
	tiles := make([][]*tile, 0, length-1)

	for i := 0; i < len(t); i += length {
		fmt.Println(i)
		row := make([]*tile, 0, length-1)

		for j := i; j < i+length; j++ {
			fmt.Printf("j: %d\n", j)
			row = append(row, t[j])
		}

		tiles = append(tiles, row)
	}

	b := board{
		tiles:  tiles,
		length: length,
	}
	return &b
}

func (b *board) getCorners() []int {
	return []int{
		b.tiles[0][0].id,
		b.tiles[0][b.length-1].id,
		b.tiles[b.length-1][0].id,
		b.tiles[b.length-1][b.length-1].id,
	}
}

func (b *board) checkEdges() bool {
	for ydx, row := range b.tiles {
		for xdx, tile := range row {
			for k, v := range neighbors {

				checkX := xdx + v[0]
				checkY := ydx + v[1]
				if checkX < 0 || checkY < 0 {
					continue
				}

				if checkX >= b.length || checkY >= b.length {
					continue
				}
				fmt.Printf("checkX: %d -- checkY: %d\n", checkX, checkY)

				switch k {
				case "top": // top neighbor
					if b.tiles[checkY][checkX].bottom != tile.top {
						fmt.Println("top neighbor doesn't match")
						return false
					}

				case "right":
					if b.tiles[checkY][checkX].left != tile.right {
						fmt.Println("right neighbor doesn't match")
						return false
					}
				case "bottom":
					if b.tiles[checkY][checkX].top != tile.bottom {
						fmt.Println("bottom neighbor doesn't match")
						return false
					}
				case "left":
					if b.tiles[checkY][checkX].right != tile.left {
						fmt.Println("left neighbor doesn't match")
						return false
					}
				}
			}
		}
	}
	return true
}

func reverse(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}

func newTile(lines []string) *tile {
	splits := strings.Split(lines[0], " ")
	id, err := strconv.Atoi(strings.Replace(splits[1], ":", "", -1))
	if err != nil {
		panic(err)
	}

	top := lines[1]
	bottom := lines[len(lines)-1]

	left := make([]byte, len(lines[0]))
	for _, row := range lines[1:] {
		left = append(left, row[0])
	}

	right := make([]byte, len(lines[0]))
	for _, row := range lines[1:] {
		right = append(right, row[len(row)-1])
	}

	t := tile{
		id:     id,
		top:    top,
		bottom: bottom,
		left:   string(left),
		right:  string(right),
	}
	return &t
}

func (t *tile) rotate() {
	oldBottom := t.bottom

	t.bottom = reverse(t.right)
	t.right = t.top
	t.top = reverse(t.left)
	t.left = oldBottom
}

func parseFile(filename string) []byte {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return data
}

func buildTiles(bs []byte) []*tile {
	tiles := make([]*tile, 0, 145)
	for _, tileString := range strings.Split(string(bs), "\n\n") {
		tiles = append(tiles, newTile(strings.Split(tileString, "\n")))
	}
	return tiles
}

func main() {
	filename := os.Args[1]
	file := parseFile(filename)
	tiles := buildTiles(file)
	//fmt.Println(tiles)

	board := newBoard(tiles)
	fmt.Printf("%v\n", board)
	fmt.Println(board.tiles[0][0].top)
	fmt.Println(board.tiles[0][0].right)
	fmt.Println(board.tiles[0][0].bottom)
	fmt.Println(board.tiles[0][0].left)

	fmt.Println()
	fmt.Println()
	fmt.Println()
	fmt.Println()
	board.tiles[0][0].rotate()

	fmt.Println(board.tiles[0][0].top)
	fmt.Println(board.tiles[0][0].right)
	fmt.Println(board.tiles[0][0].bottom)
	fmt.Println(board.tiles[0][0].left)

	fmt.Println(board.getCorners())

	fmt.Println(board.checkEdges())
}
