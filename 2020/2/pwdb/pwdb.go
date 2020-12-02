// Package pwdb provides tools to interact with the North Pole
// Toboggan Rental Shop's password database
package pwdb

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

const databaseFile string = "input.txt"

// PasswordPolicy represents a password policy found in the
// rental shop's password database
type PasswordPolicy struct {
	Min    int
	Max    int
	Letter string
}

// Row represents a row in the rental shop's password database
type Row struct {
	Password string
	Policy   PasswordPolicy
}

// NewPasswordPolicy creates a passwordPolicy from a string representation assumed
// to be found in the database (``1-3 a: abcde``).
func NewPasswordPolicy(policy string) PasswordPolicy {
	var p PasswordPolicy

	// splitting on space results in the occurrence requirements being in
	// policyParts[0] and the enforced letter being in policyParts[1]
	policyParts := strings.Split(policy, " ")

	p.Letter = policyParts[1]

	enforcementLimits := strings.Split(policyParts[0], "-")
	p.Min, _ = strconv.Atoi(enforcementLimits[0])
	p.Max, _ = strconv.Atoi(enforcementLimits[1])
	return p
}

// NewRow creates a row struct from a string representation assumed to be found
// in the database (``2-9 c: ccccccccc``)
func NewRow(databaseRow string) Row {
	var r Row
	rowParts := strings.Split(databaseRow, ":")
	r.Policy = NewPasswordPolicy(rowParts[0])
	r.Password = strings.TrimSpace(rowParts[1])
	return r
}

// IsValid checks to see if the password database row contains a valid password
// according to the stored policy.
func (r Row) IsValid() bool {
	count := strings.Count(r.Password, r.Policy.Letter)
	return r.Policy.Min <= count && count <= r.Policy.Max
}

// IsOfficiallyValid checks to see if the password database row contains a valid
// password according to the stored policy using the Official Toboggan Corporate
// Policy.
func (r Row) IsOfficiallyValid() bool {
	lowMatch := r.Password[r.Policy.Min-1] == r.Policy.Letter[0]
	highMatch := r.Password[r.Policy.Max-1] == r.Policy.Letter[0]

	return (lowMatch || highMatch) && lowMatch != highMatch
}

// SelectStar reads all rows from the database and loads them into memory
func SelectStar() []Row {
	file, err := os.Open(databaseFile)
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	rows := make([]Row, 0, 50)
	for scanner.Scan() {
		rows = append(rows, NewRow(scanner.Text()))
	}
	return rows
}

func openDatabaseFile() *bufio.Scanner {
	file, err := os.Open(databaseFile)
	if err != nil {
		log.Fatal(err)
	}

	return bufio.NewScanner(file)
}

// SelectCountValidRows returns a count of rows containing valid passwords
func SelectCountValidRows() int {
	scanner := openDatabaseFile()
	rows := 0
	for scanner.Scan() {
		row := NewRow(scanner.Text())
		if row.IsValid() {
			rows++
		}
	}
	return rows
}

//SelectCountOfficiallyValidRows returns the rows containing OFFICIALLY valid passwords
func SelectCountOfficiallyValidRows() int {
	scanner := openDatabaseFile()
	rows := 0
	for scanner.Scan() {
		row := NewRow(scanner.Text())
		if row.IsOfficiallyValid() {
			rows++
		}
	}
	return rows
}
