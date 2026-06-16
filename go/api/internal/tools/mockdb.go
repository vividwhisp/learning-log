package tools

import(
	"time"

)

type mockDB struct{

}
var mockLoginDetails = map[string]LoginDetails{
	"raj" : {
		AuthToken: "123QWE",
		Username: "raj",
	},
	"alex" : {
		AuthToken: "123ABC",
		Username: "alex",
	},
	"neel" : {
		AuthToken: "123RTY",
		Username: "neel",
	},
}

var mockCoinDetails = map[string]CoinDetails{
	"raj" : {
		Coins: 100,
		Username: "raj",
	},
	"alex" : {
		Coins: 200,
		Username: "alex",
	},
	"neel" : {
		Coins: 300,
		Username: "neel",
	},
}

func (d *mockDB) GetUserLoginDetails(username string) *LoginDetails{
	time.Sleep(time.Second*1)

	var clientData = LoginDetails{}
	clientData, ok := mockLoginDetails[username]

	if !ok{
		return nil
	}
	return &clientData
}

func (d *mockDB) GetUserCoins(username string) *CoinDetails{
	time.Sleep(time.Second*1)

	var clientData = CoinDetails{}
	clientData, ok := mockCoinDetails[username]
	if !ok {
		return nil
	}
	return &clientData
}

func (d *mockDB) SetupDatabase() error{
	return  nil
}