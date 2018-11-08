# Twitter Auth
Simple Flask app for authenticating Twitter users. Saves credentials to a file

## Installation

```bash
# clone repo
mkdir ~/python-projects && cd $_
git clone https://github.com/elhardoum/twitter-auth && cd twitter-auth

# env setup
virtualenv -p python3 env

# activate env
source env/bin/activate

# install dependencies
pip install -r requirements # or just: `pip install flask tweepy` as those are the 2 deps required
```

## Usage

Open the `config.py` and put your app consumer key and secret there. There are other settings which are optional.

You can run the app with this command:

```bash
env FLASK_APP=server.py FLASK_ENV=development flask run --port {desired_port} --host {your_machine_ip}
```

Make sure to replace `{desired_port}` with a random valid port number, e.g `4322`

And replace `{your_machine_ip}` with your IP, you can find the IP quickly with `hostname -I` or `curl icanhazip.com`

## Producation

To run the app forever, you need to have the command run in a detached state (in the background). There are so many ways, let's do `nohup`:

```
nohup env FLASK_APP=server.py FLASK_ENV=development flask run --port {desired_port} --host {your_machine_ip} &> /tmp/flask.log&
```

Now watch `/tmp/flask.log` for the logs.

Once you know your app URL, you can whitelist it in the Twitter app settings, as a callback URL.

Next, direct your users to the endpoint `/authenticate` (`http://{ip}:{port}/authenticate`) to authenticate.
