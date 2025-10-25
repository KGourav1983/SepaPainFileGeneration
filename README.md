# SepaPainFileGeneration
Sepa Pain File Generation Program

Commands to use 
0. From path sepa_agent run "docker-compose up --build" to create image
1. docker images
2. docker ps (shows only running container) : docker ps -a (shows all container) 
3. docker volume create sepa_agent_painfiles
docker volume ls
docker run --rm -v sepa_agent_painfiles:/data alpine ls /data
docker run -it --rm -v sepa_agent_painfiles:/data alpine sh # inside the container shell less /data/yourfile.xml

3. Start sepa_agent_backend container
docker run -d -p 8000:8000 --name sepa_agent-backend -v sepa_agent_painfiles:/app/painfiles sepa_agent-backend:latest

4. Start sepa_agent_frontend
docker run -d -p 5173:5173 --name sepa_agent-frontend sepa_agent-frontend:latest
 
-d → detached mode (run in background)
-p → map container port to host
-v → mount local folders for hot reload
--name → optional, so you can reference containers easily

Note : Make Port 8000 public after startup

5. docker stop sepa_agent-backend sepa_agent-frontend
6. docker stop $(docker ps -q)
7. docker rm $(docker ps -aq)

8. See on UI

https://spooky-crematorium-4jprj6v6j7px35x9p-8000.app.github.dev/
https://spooky-crematorium-4jprj6v6j7px35x9p-8000.app.github.dev/direct-debit/
https://spooky-crematorium-4jprj6v6j7px35x9p-8000.app.github.dev/generate-pain-file/

9. Curl Commands from Terminal
curl -X 'POST' \
  'http://127.0.0.1:8000/direct-debit/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "creditor_name": "DEF Doe",
        "creditor_iban": "GB29NWBK60161331926819",
        "debtor_name": "Jane Smith",
        "debtor_iban": "GB29NWBK60161331926820",
        "amount": 1500.00,
        "channel_initiated": "Online Banking",
        "account_number": "1234567890",
        "remittance_info": "Payment for Invoice #1234"
      }'
curl -X 'GET' 'http://127.0.0.1:8000/'
curl -X 'GET' 'http://127.0.0.1:8000/direct-debit/'
curl -i 'http://127.0.0.1:8000/direct-debit/'

curl http://127.0.0.1:8000/generate-pain-file/

10. Running program outside Image :
pip install fastapi uvicorn sqlalchemy pydantic

cd sepa_agent
npm create vite@latest frontend --template react

cd sepa_agent
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
cd frontend
npm run dev

11. SQL commands from Terminal
sqlite3 test.db
SELECT * FROM direct_debits;
INSERT INTO direct_debits (creditor_name, creditor_iban, debtor_name, debtor_iban, amount, channel_initiated, account_number, remittance_info)
VALUES ('John Doe', 'GB29NWBK60161331926819', 'Jane Smith', 'GB29NWBK60161331926820', 1500.00, 'Online Banking', '1234567890', 'Payment for Invoice #1234');
COMMIT;
