package main
import "fmt"

type gasEngine struct{
	mpg uint8
	gallons uint8
	// ownerInfo owner //we can just do  "owner" and don't specify ownerInfo too
	// int // we can also just say the type without giving it a name
}

// type owner struct{
// 	name string
// }

func ( e gasEngine) milesLeft() uint8 {
	return e.gallons * e.mpg
}

func main(){
	var gal gasEngine = gasEngine{ 15,  100} //we can also ommit the field names: gasEngine{15 ,100}
	fmt.Printf("Miles left : %v", gal.milesLeft())
}