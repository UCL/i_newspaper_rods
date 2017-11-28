# i_Newspaper_RODS

This project uses batched Apache PySpark queries on Legion to run queries over the Times
Digital Archive. It is assumed that all queries are grouped by year, so that the results of
different years can be concatenated together without any processing.

While iRODS is in the name of the project, there is actualy little in the code that ties
it to the iRODS system. All iRODS interaction is limited to a single fabric tasks, and
does not happen at runtime. Data is fetched by HTTP (from WOS), however, this could be
easily changed. The majority of work in this version of the code has gone into parsing
and manipulating the Issue and Article XML.

##### Architecture Motivation

The goal of this branch, where the compute is not done as a single PySpark run, but
rather as a larger number of smaller, single node, PySpark executions has mutliple
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
  * iCommands (kanki if you're on OS X , see below)

# Executing

### Testing Locally

Any query can be tested on your local machine, using a tiny subset of the total 
file archive. This is acheived using: 

 * On OS X: `fab --set DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=5 test`
 * Otherwise: `fab setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=5 test`

Note that the `DYLD_LIBRARY_PATH` must be provided explicitly on OS X as 
it cannot be passed to sub shells automatically due to System Integrity Protection (SIP).

### Running on HPC Resources

In theory this project can be run on either Legion or Grace. However, testing has only been done on 
Legion. Also, the rsd-modules modules (which include Spark which this project requires) have not yet
been set up on Grace. However, once that has all been set up, the same commands should work for grace
if the command `legion` is substituted for `grace`, with the same parameters. 

You can run the program to run with:
`fab --set DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=0,years_per_chunk=5 legion:username=<YOUR_UCL_USER_ID> prepare sub`

You can see the status of your jobs with: `fab legion:username=<YOUR_UCL_USER_ID> stat`

**Note** that the `prepare` and `sub` tasks must be run as part of the same `fab`
invocation because they create a folder with the current time and date on legion to
store all the data.

# Installing iRODS iCommands locally on OS X Sierra

While it looks like you can install iCommands with
`brew install irods`, in actual fact that version is too old to be
usable with the UCL iRods system.

The correct thing to install is [Kanki](https://github.com/ilarik/kanki-irodsclient).
You have to install the most recent version (not the stable one) to work with the newer
version of OS X.

While it is hidden in the documentation a bit, you have to remember the following steps:

Create `~/.irods/irods_environment.json` with the following contents (this combines both
the instructions for UCL and Kanki).

```json
{
    "irods_host": "arthur.rd.ucl.ac.uk",
    "irods_port": 1247,
    "irods_default_resource": "wos",
    "irods_zone_name": "rdZone",
    "irods_home": "/rdZone/live",
    "irods_authentication_scheme": "PAM",
    "irods_default_hash_scheme": "SHA256",
    "irods_user_name": "YOUR_UCL_USER_ID",
    "irods_plugins_home": "/Applications/iRODS.app/Contents/PlugIns/irods/"
}
```

You also must add the following lines to your `~/.bash_profile`

```bash
# iRods iCommands setup
export PATH=/Applications/iRODS.app/Contents/PlugIns/irods/icommands:$PATH
# This is not a real export due to SIP on OS X 
export DYLD_LIBRARY_PATH=/Applications/iRODS.app/Contents/Frameworks:$DYLD_LIBRARY_PATH
```

After having done both steps run (where you will be prompted for your password):

```bash
iinit
```

