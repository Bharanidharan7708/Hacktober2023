1
consistency of names and structure 
 Clinet ID -> Inside URL -> timestamp_fol -> 3 folders -> 3 files

2.
If one time web scrapping, old fun is enough.
Change the milvus struct with filename as primary key
Modify the insert into milvus fun according to the new column created

3.
process and dum openai fun add a new var -> filename
Add the new var when calling process and dumb fun from upload_url, upload_file

4.
Identify the subsequent runs of url, from second, third, and ...
Check the content of every url link, compare it with previous run
If the value is not present in previous run, then simply insert
If the value is present, then compare 
	If same:
		skip inserting
	else:
		drop the rows from milvus collection for the same filename
		Insert the data from the recent file


5
Add index_tree for URL, status tables in rdb 
