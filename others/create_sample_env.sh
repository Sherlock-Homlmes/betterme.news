# create .env file from example.env file if there are not exist .env file
if [ ! -f ./server/.env ]; then
    echo "Generate server .env file"
    cp server/example.env server/.env
fi
