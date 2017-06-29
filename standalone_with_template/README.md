Overview
--------
This example extends the example [standalone_basic](./standalone_basic) with custom html output.

### Running Locally

```
git clone https://github.com/snowch/bokeh-cloud-foundry.git
cd bokeh-cloud-foundry/standalone_with_template
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python bokeh_server.py
```

### Running on Cloud Foundry (e.g. Bluemix)

```
git clone https://github.com/snowch/bokeh-cloud-foundry.git
cd bokeh-cloud-foundry/standalone_with_template
cf login ...
# edit manifest.yml to provide unique route and set ALLOW_WEBSOCKET_ORIGIN
cf push
```
