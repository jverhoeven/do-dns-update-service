'''
Created on Jun 28, 2015

Accepts an /update/ call with a domain name and will update the first A record for the
Digital Ocean DNS record if available. If it does not exist, none will be created.
The rationale for not automatically creating one is to prevent abuse.

Requires an environment variable named 'ENV_DO_ACCESS_TOKEN' that contains
the access token for digital ocaen (must have write access to the account)

Log level can also be set via environment variable 'ENV_LOG_LEVEL'

If the application is fronted by an NGINX or similar webserver, the header
X-Real-IP should be forwarded to allow the app to determine the source ip address. 

#!/usr/local/bin/python
@author: Jan Verhoeven
'''
from bottle import Bottle, run, request, abort
from digitalocean import Manager
import logging
import os
from IPy import IP


logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s  %(message)s')
logger = logging.getLogger("do-dns-update-service")
logger.setLevel(os.environ.get("ENV_LOG_LEVEL", logging.DEBUG))

app = Bottle()

@app.route('/update/<domain_name>')
def update(domain_name):
    do_access_token = os.environ.get("ENV_DO_ACCESS_TOKEN")
    if do_access_token is None:
        logger.error("No Digital Ocean access token is set as environment variable. Cannot serve request")
        abort(code=500, text="Config error. See log.")
        
    try:
        manager = Manager(token=do_access_token)
        source_ip = request.remote_addr
        if IP(source_ip).iptype() is not "PUBLIC":
            source_ip = request.headers.get("X-Real-IP")
        if not source_ip or IP(source_ip).iptype() is not "PUBLIC":
            logger.debug("Could not resolve source ip address")
            return "Could not resolve source ip address"
    
        logger.info("Received request from {0}".format(source_ip))
        existing_records = manager.get_domain(domain_name).get_records()
        record_to_update = None
        for record in existing_records:
            if record.type=='A' and record.name=='@':
                record_to_update = record
                # Stop on first A record found
                break;
        if record_to_update:
            if record_to_update.data != source_ip:
                record_to_update.data = source_ip
                #record_to_update.save()
                logger.info("Record updated to {0}".format(source_ip))
                return "Record for {0} updated to {1}".format(record_to_update.name, source_ip)
            else:
                logger.info("Record has not changed")
                return "Record has not changed"
        else:
            logger.info("Record could not be found")
            return "Record could not be found"
    except Exception as e:
        logger.exception(e)
        abort(code=500, text="Unknown error on server. Check logs")

if __name__=='__main__':
    # Only ran when in debug gmode. Normally the app should be run by gunicorn
    run(app, host="localhost", port=8000, debug=True)
