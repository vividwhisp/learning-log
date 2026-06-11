package main
import "fmt"

type gasEngine struct{
	mpg int
	gallons int
	// ownerInfo owner //we can just do  "owner" and don't specify ownerInfo too
	// int // we can also just say the type without giving it a name
}

// type owner struct{
// 	name string
// }

type electricEngine struct {
	mpkwh int
	kwh int
}

func ( e gasEngine) milesLeft() int {
	return e.gallons * e.mpg
}
func ( e electricEngine) milesLeft() int{
	return e.kwh * e.mpkwh
}

func canMakeIt(e engine, miles int){
	if miles <= e.milesLeft(){
		fmt.Println("You can make it there")
	}else{
		fmt.Println("You cannot make it there")
	}
}

type engine interface{
	milesLeft() int
}

// func main(){
// 	var gal electricEngine = electricEngine{25, 15} //we can also ommit the field names: gasEngine{15 ,100}
// 	canMakeIt(gal, 200)
// }