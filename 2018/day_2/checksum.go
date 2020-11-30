package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "strings"
)


func main() {
    file, err := os.Open("./input")
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    var twoCount, threeCount int = 0, 0

    for scanner.Scan() {
        hasTwo, hasThree := false, false
        id := scanner.Text()
        uniques := make([]string, 0)
        seenRunes := make(map[rune]bool)

        for _, x := range id {
            if seenRunes[x] == true {
                continue
            } else {
                seenRunes[x] = true
                uniques = append(uniques, string(x))
            }
        }
        for _, x := range uniques {
            count := strings.Count(id, x)
            if hasTwo == false && count == 2 {
                hasTwo = true
                twoCount += 1
            }
            if hasThree == false && count == 3 {
                hasThree = true
                threeCount += 1
            }
            if hasThree && hasTwo {
                break
            }
        }
    }

    fmt.Print(twoCount * threeCount)
}

