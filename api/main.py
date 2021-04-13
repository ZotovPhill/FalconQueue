import falcon

import views

app = falcon.API()

app.add_route('/', views.HelloWorldResource())
app.add_route('/weather', views.OpenMapWeatherResource())
app.add_route('/weather/{task_id}', views.CheckWeatherResult())
