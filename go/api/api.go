package api

import (
	"encoding/json"
	"net/http"
)

//coins balance params
type CoinBalanceParams struct{
	Username string
}

//coin Balance response
type CoinBalanceResponse struct{
	//Success code
	Code int

	//accpunt balance
	Balance int64
}

type Error struct{
	//Erro Code
	Code int

	//Error Message
	Message string
}