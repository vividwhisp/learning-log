package main

import "fmt"

func main(){
	 intArr := [...]int32{1,2,3}
	fmt.Println(intArr)	

	var intSlice []int32 = []int32{4,5,6}
	fmt.Println(intSlice)
	intSlice = append(intSlice,7)
	fmt.Println(intSlice)

	var myMap map[string]uint8 = make(map[string]uint8)
	fmt.Println(myMap)

	var myMap2  = map[string]uint8{"Raj":20,"Shiva":24}
	fmt.Println(myMap2["Raj"])

	var age, ok = myMap2["R"]
	if ok{
		fmt.Printf("Age is %v\n",age)
	}else{
		fmt.Println(ok)
	}

	for name,age := range myMap2{
		fmt.Printf("Name: %v age: %v\n",name ,age)
	}
	for i, v := range intArr{
		fmt.Printf("Index: %v, Value: %v\n",i,v)
	}
	for i:=0; i<=10; i++{
		fmt.Println(i)
	}
}