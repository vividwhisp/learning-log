package main

import "fmt"
func printRem(numerator int, denominator int) int {
	rem := numerator / denominator
	fmt.Println(rem)
	return rem
}