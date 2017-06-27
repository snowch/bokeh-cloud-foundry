Overview
--------
This is a proof-of-concept for running bokeh server as a Cloud Foundry application based on the bokeh server example, [standalone_embed.py](https://github.com/bokeh/bokeh/blob/master/examples/howto/server_embed/standalone_embed.py)

### Running Locally

```
git clone https://github.com/snowch/bokeh-cloud-foundry.git
cd bokeh-cloud-foundry/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python bokeh_server.py
```

### Running on Cloud Foundry (e.g. Bluemix)

```
git clone https://github.com/snowch/bokeh-cloud-foundry.git
cd bokeh-cloud-foundry/
cf login ...
# edit manifest.yml to provide unique route and set ALLOW_WEBSOCKET_ORIGIN
cf push
```
