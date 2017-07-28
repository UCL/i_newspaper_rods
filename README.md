# i_newspaper_rods
Working with iRods to analyse the Times Digital Archive

# Running

You can run the program to run with
 * Legion: `fab prepare sub(query=your_query)`
 * Grace: `fab grace prepare sub(query=your_query)`

You can see the status of your jobs with

* Legion: `fab stat`
* Grace: `fab grace stat`

And retreive the results of your query with

* Legion: `fab fetch`
* Grace: `fab grace fetch`


# Running iRODS iCommands locally on OS X Sierra

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
export DYLD_LIBRARY_PATH=/Applications/iRODS.app/Contents/Frameworks:$DYLD_LIBRARY_PATH
```

After having done both steps run (where you will be promted for your password):

```bash
iinit
```

