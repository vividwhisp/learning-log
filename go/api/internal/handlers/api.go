package handlers

import (
	"github.com/go-chi/chi"
	chimiddle "github.com/go-chi/chi/middleware"
	"learning-log/go/internal/middleware"
)

func Handler(r *chi.Mux){
	r.Use(chimiddle.StripSlashes)
	r.Use(middleware.Cors)
	r.Route("/account",func(router chi.Router){
		router.Use(middleware.Authorization)
		router.Get("/coins",GetCoinBalance)
	})
}
