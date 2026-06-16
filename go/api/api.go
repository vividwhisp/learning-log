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

func writeError(w http.ResponseWriter, message string, code int){
	resp := Error{
		Code: code,
		Message: message,
	}
	w.Header().Set("Content-Type","application/json")
	w.WriteHeader(code)

	json.NewEncoder(w).Encode(resp)
}

var(
	RequestErrorHandler = func( w http.ResponseWriter, err error){
		writeError(w, err.Error(),http.StatusBadRequest)
	}
	InternalErrorhandler = func( w http.ResponseWriter){
		writeError(w, "An Unexpected Error Occured. ",http.StatusInternalServerError)
	}
)