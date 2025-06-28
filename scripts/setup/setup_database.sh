#!/bin/bash

# Database setup script for Hotel Management Toolbox

echo "🗄️ Setting up PostgreSQL database..."

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found. Please create one first."
    exit 1
fi

# Create user and database
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d postgres -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$PASSWORD';" 2>/dev/null || echo "User $POSTGRES_USER already exists"
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d postgres -c "CREATE DATABASE $POSTGRES_DATABASE;" 2>/dev/null || echo "Database $POSTGRES_DATABASE already exists"
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DATABASE TO $POSTGRES_USER;"

echo "📋 Dropping existing schema..."
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DATABASE -f scripts/setup/db/00_drop_tables.sql

echo "📋 Creating schema..."
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DATABASE -f scripts/setup/db/01_schema.sql

echo "📝 Inserting seed data..."
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DATABASE -f scripts/setup/db/02_seed_data.sql

echo "✅ Database setup complete!"
echo "   Database: $POSTGRES_DATABASE"
echo "   User: $POSTGRES_USER"
echo "   Host: $POSTGRES_HOST:$POSTGRES_PORT" 