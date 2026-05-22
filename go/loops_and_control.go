package main

import "fmt"


func main(){
	printRem(6, 2)
	
}

func printRem(numerator int, denominator int) int {
	rem := numerator / denominator
	fmt.Println(rem)
	return rem
}