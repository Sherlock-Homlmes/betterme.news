# create .env file from example.env file if there are not exist .env file
if [ ! -f ./server/.env ]; then
    echo "Generate server .env file"
    cp server/example.env server/.env
fi
if [ ! -f ./admin_server/.env ]; then
    echo "Generate admin server .env file"
    cp admin_server/example.env admin_server/.env
fi
