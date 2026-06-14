package main

// import(
// 	"fmt"
// 	"time"
// 	"sync"
// )
// var wg = sync.WaitGroup{}
// var dbData = []string{"id1", "id2", "id3", "id4", "id5"}

// func main(){
// 	t0 := time.Now()
// 	for i:=0; i<len(dbData); i++{
// 		wg.Add(1)
// 		go dbcall(i)

// 	}
// 	wg.Wait()
// 	fmt.Printf("\n Total execution time: %v",time.Since(t0))

// }

// func dbcall(i int){
// 	var delay float32 = 2000
// 	time.Sleep(time.Duration(delay)*time.Millisecond)
// 	fmt.Println("The result from the database is: ",dbData[i])
// 	wg.Done()
// }