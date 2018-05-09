# i_Newspaper_RODS

This project uses batched Apache PySpark queries on Legion to run queries over the Times
Digital Archive. It is assumed that all queries are grouped by year, so that the results of
different years can be concatenated together without any processing.

While iRODS is in the name of the project, this is historical 

##### Architecture Motivation

The goal of this branch, where the compute is not done as a single PySpark run, but
rather as a larger number of smaller, single node, PySpark executions has multiple
reasons for it:

  * Support for partial failure, with an easy way to resubmit the failed task. 
  * Better chances of running on a larger number of machines. At the moment Legion
    does not give a way of saying how many actual machines are required. As these 
    tasks are generally considered to be IO bound - in the time spent fetching each
    individual file from the remote - having more nodes involved in the process should
    increase the execution speed (due to having more bandwidth available).
 * Allows work to be done even if only one machine is currently available. 


# Local Machine Requirements

  * Apache Spark
  * Python 2.7

# Executing

### Testing Locally

Any query can be tested on your local machine, using a tiny subset of the total 
file archive. This is achieved using: 

```
fab setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=5 test
```

### Running on HPC Resources

In theory this project can be run on either Legion or Grace. However, testing has only been done on 
Legion. Also, the rsd-modules modules (which include Spark which this project requires) have not yet
been set up on Grace. However, once that has all been set up, the same commands should work for grace
if the command `legion` is substituted for `grace`, with the same parameters. 

You can run the program to run with:
`fab setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=0,years_per_chunk=5 legion:username=<YOUR_UCL_USER_ID> prepare sub`

You can see the status of your jobs with: `fab legion:username=<YOUR_UCL_USER_ID> stat`

**Note** that the `prepare` and `sub` tasks must be run as part of the same `fab`
invocation because they create a folder with the current time and date on legion to
store all the data.
