# Digital Ocean DNS Update Service
##Introduction
This docker hosts a small python Bottle service that updates the Digital Ocean DNS record for a given domain based on callers source ip address.

This docker may be for you if you host your DNS via Digital ocean and have servers with a dynamic IP at home and are fed up with all these not-really free services such as no-ip and dyndns.

##Configuration

Environment var | Description
-------------|---------------
ENV\_DO\_ACCESS\_TOKEN | The access token to get to the digital ocean account for changing the DNS entry. As such the token must give write access to the account.
ENV\_LOG\_LEVEL | The log level used by the application. By default DEBUG is used.

##Proxy
If the application is fronted by an NGINX or similar webserver, the header
X-Real-IP should be forwarded to allow the app to determine the source ip address. 

##Example usage

On your server, start:
	
	docker run -d -p 8000:8000 -e ENV_DO_ACCESS_TOKEN=1234 jverhoeven/do-dns-update-service 

On your machine with a dynamic DNS, add this to a cron job:

	curl http://<dns-update-server:port>/update/www.example.com

to update you domain www.example.com to your current source ip address.