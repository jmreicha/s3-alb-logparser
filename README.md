### Notes

To quickly get started, run the following command.

```
python3 setup.py develop
```

Example usage:

```
logparser getcodes --from_date 2017/08/01 --to_date 08/01/17
logparser geturls --code 400 --from_date 2017/08/01 --to_date 08/01/17
logparser getuas --code 400 --from_date 2017/08/01 --to_date 08/01/17
```

 - [x] Get CLI working - use click
 - [x] Get basic filter working to only download logs from certain date
   - [ ] Figure out how to parse the file name to get days and hours
 - [x] Read logs using boto based on date filter
 - [x] Get top N 404 filter working
 - [x] Get user-agent filter working
 - [ ] Get reports working
 - [x] Create diagram
 - [ ] Things to refactor
    - [x] Move date parsing into helper
