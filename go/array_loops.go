package main

import "fmt"
func main(){
	var intArr [3] int32
	intArr[1] = 123
	fmt.Println(intArr[0])
	fmt.Println(intArr[0:3])
	fmt.Println(&intArr[0])

}