package tools

import (
	"database/sql"
	_ "embed"
	"os"

	_ "github.com/lib/pq"
	log "github.com/sirupsen/logrus"
)

//go:embed init.sql
var initSQL string

type postgresDB struct {
	db *sql.DB
}

func (d *postgresDB) GetUserLoginDetails(username string) *LoginDetails {
	row := d.db.QueryRow("SELECT username, auth_token FROM users WHERE username = $1", username)

	var details LoginDetails
	err := row.Scan(&details.Username, &details.AuthToken)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil
		}
		log.Error(err)
		return nil
	}
	return &details
}

func (d *postgresDB) GetUserCoins(username string) *CoinDetails {
	row := d.db.QueryRow("SELECT username, balance FROM coins WHERE username = $1", username)

	var details CoinDetails
	err := row.Scan(&details.Username, &details.Coins)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil
		}
		log.Error(err)
		return nil
	}
	return &details
}

func (d *postgresDB) SetupDatabase() error {
	connStr := os.Getenv("DATABASE_URL")
	if connStr == "" {
		connStr = "postgres://postgres:mysecretpassword@localhost:5432/learninglog?sslmode=disable"
	}

	var err error
	d.db, err = sql.Open("postgres", connStr)
	if err != nil {
		return err
	}

	if err = d.db.Ping(); err != nil {
		return err
	}

	_, err = d.db.Exec(initSQL)
	if err != nil {
		return err
	}

	log.Info("PostgreSQL database setup complete")
	return nil
}
