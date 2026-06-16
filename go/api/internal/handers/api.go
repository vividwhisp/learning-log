package handers

import (
	"github.com/avukadin/goapi/internal/handlers"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	chimiddle "github.com/go-chi/chi/middleware"
)

func Handler(r *chi.Mux){
	r.Use(chimiddle.StripSlashes)
	r.Route("/account",func(router chi.Router){
		router.Use(middleware.Authorization)
		router.Get("/coins",GetCoinBalance)
	})
}
