from django.http import HttpResponse
from spyne.server.wsgi import WsgiApplication
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.service import ServiceBase
from spyne.model.primitive import Integer
from spyne.model.complex import Iterable
from spyne.decorator import rpc


# Definisikan service SOAP
class CalculatorService(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def add(ctx, a, b):
        return a + b


# Konfigurasi aplikasi Spyne
soap_app = Application(
    [CalculatorService],
    tns="calculator.soap",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(soap_app)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def soap_service_view(request):
    environ = request.META.copy()
    environ["PATH_INFO"] = request.path
    environ["QUERY_STRING"] = request.META.get("QUERY_STRING", "")
    environ["wsgi.input"] = request

    response = HttpResponse()

    def start_response(status, headers):
        response.status_code = int(status.split(" ")[0])
        for header, value in headers:
            response[header] = value

    try:
        response.content = b"".join(wsgi_app(environ, start_response))
    except Exception as e:
        response.status_code = 500
        response.content = str(e).encode()

    return response

