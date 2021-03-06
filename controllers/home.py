# Import Required Libraries
import cherrypy
from controllers.base import BaseController
from models import Config, Parsing


class HomeController(BaseController):
    # CherryPy load the Index Page (Setup)
    @cherrypy.expose
    def index(self):
        config = Config.readconfig()
        # Check if there is a config.
        if config != 0:
            # Else redirect the User to the Dashboard
            raise cherrypy.HTTPRedirect("Home/dash")
        else:
            # If True Return the template
            return self.render_template('home/index.html')


    # CherryPy load the Dashboard Page
    @cherrypy.expose
    def dash(self, **params):
        config = Config.readconfig()
        # Attempts to read the config.
        if config == 0:
            # Else it uses the Arguements to create a config.
            # organises make config data
            data = {str(key):str(value) for key,value in params.items()}
            url = []
            for i, v in data.items():
                url.append(v)

            # makes config
            Config.mkconfig(url)
        else:
            # If True it saves the data to a variable
            URLS = config["URLS"]
            refresh = config["refresh"]

        # Runs the script in the Parsing Model. Parses the XML Files from URL
        parse = Parsing.system()
        refresh = config["refresh"]


        # Returns the template with Parsed XML Data and The Refresh Integer from the Config.
        return self.render_template('home/dash.html', template_vars={'data': parse, 'refresh': refresh})

    # CherryPy load the Settings Page
    @cherrypy.expose
    def settings(self):
        # get config data
        config = Config.readconfig()
        URLS = config["URLS"]
        refresh = config["refresh"]
        times = config["time"]

        # Return the template
        return self.render_template('home/settings.html', template_vars={'refresh': refresh, 'urls': URLS, 'time': times})

    # CherryPy load the Confimed Settings Page
    @cherrypy.expose
    def confirmed(self, **params):
        url = []
        # setup update config data
        for k, v in params.items():
            if k != "refresh" and k != "time":
                url.append(v)
            elif k == "refresh":
                refresh = v
            elif k == "time":
                time = v

        # update config
        Config.updateconfig(url, refresh, time)

        # redirect to dashboard
        raise cherrypy.HTTPRedirect("dash")
