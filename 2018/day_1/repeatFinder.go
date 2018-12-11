package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "strconv"
)


func main() {
    file, err := os.Open("./input")
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    seenFrequencies := make(map[int64]bool)
    var frequency int64 = 0
    keepLooking := true

    for keepLooking {
        scanner := bufio.NewScanner(file)
        for scanner.Scan() {
            adjustment, err := strconv.ParseInt(scanner.Text(), 10, 64)
            if err != nil {
                log.Print("Bad freq adjustment found")
                continue
            }
            frequency += adjustment
            _, ok := seenFrequencies[frequency]
            if ok {
                keepLooking = false
                break
            }
            seenFrequencies[frequency] = true
        }
        file.Seek(0, 0)
    }
    fmt.Print(frequency)
}

