hr_leaderboard:

for deployment/development:
- leave mlb endpoint as gd2, and all other config settings the same 
- make the container:
     - `make && make build && make run && docker logs -f hr_leaderboard`
     or if making not for the first time:
     - `make clean && make build && make run && docker logs -f hr_leaderboard`
     
sending requests:
requests require the following parameters:
start_date = 'year-month-date'
end_date = 'year-month-date'
num_leaders = integer # of top leaders to return

requests are sent in JSON format thru POST, for example:

```
{
    "start_date": "2019-06-01",
    "end_date": "2019-07-01",
    "num_leaders": "10"
}
```

If built to default, the endpoint will be `localhost:7777/v1/retrieve`
