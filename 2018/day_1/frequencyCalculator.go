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

    var frequency int64 = 0

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        adjustment, err := strconv.ParseInt(scanner.Text(), 10, 64)
        if err != nil {
            log.Print("Bad freq adjustment found")
            continue
        }
        frequency += adjustment
    }
    fmt.Print(frequency)
}

