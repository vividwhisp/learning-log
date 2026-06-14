package main

import (
	"fmt"
	"math/rand"
	"time"
)

//channels + goroutines

// func main(){
// 	var c = make( chan int, 5 )
// 	go process(c)
// 	for i:= range c{
// 		fmt.Println(i)
// 		time.Sleep(time.Second*1)
// 	}

// }

// func process(c chan int){
// 	defer close(c)
// 	for i:=0; i<5; i++{
// 		c <- i
// 	}
// 	fmt.Println("Exiting Process")

// }

var MAX_CHICKEN_PRICE float32 = 5

func main(){
	var chickenChannel = make(chan string)
	var chickenPrice float32 
	var websites = []string{"walmart.com","costco.com","wholefoods.com"}
	for i:= range websites{
		go checkChickenPrices(websites[i],chickenChannel)
	}
	sendMessage(chickenChannel, chickenPrice)
}

func checkChickenPrices(website string, chickenChannel chan string){
	for{
		time.Sleep(time.Second*1)
		var chickenPrice = rand.Float32()*20
		if chickenPrice<=MAX_CHICKEN_PRICE{
			chickenChannel <- website
			fmt.Println(chickenPrice)
			break
		}
	}
}

func sendMessage(chickenChannel chan string, chickenPrice float32){
	fmt.Printf("\nFound a deal on chievk at %s  at %v dollars",<-chickenChannel, chickenPrice)
}