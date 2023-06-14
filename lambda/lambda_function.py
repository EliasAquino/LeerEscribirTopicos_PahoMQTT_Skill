# -*- coding: utf-8 -*-


import logging
import ask_sdk_core.utils as ask_utils
import paho.mqtt.client as mqtt

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bienvenido a la skill de prueba de cidesi MQTT"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

#-------------------------------------------------------------------------------------------------------------------------------------------------#
class ChTopicIntentHandler(AbstractRequestHandler):
    def on_connect(self, client, userdata, flags, rc):
        print("Conexión establecida con éxito al broker MQTT")

    def on_message(self, client, userdata, message):
        print("Mensaje recibido en el tópico " + message.topic + " con el siguiente contenido: " + message.payload.decode())

    def on_disconnect(self, client, userdata, rc):
        print("Desconectado del broker MQTT")
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> boolt
        return ask_utils.is_intent_name("ChTopic")(handler_input)
    
    def handle(self, handler_input):
        # Conf cliente MQTT
        num = handler_input.request_envelope.request.intent.slots['valor']
        num = str(num.value)
        client = mqtt.Client(client_id="my_client_T")  # Asigna un identificador único para el cliente
        client.on_connect = self.on_connect  # Define la función callback que se ejecuta cuando se establece la conexión
        client.on_message = self.on_message  # Define la función callback que se ejecuta cuando se recibe un mensaje
        client.on_disconnect = self.on_disconnect  # Define la función callback que se ejecuta cuando se desconecta del broker
        client.connect("test.mosquitto.org", 1883)  # Conecta al broker Mosquitto
        client.publish("test/prueba", f"{num}", 1, True)
        #client.disconnect()  
        # type: (HandlerInput) -> Response
        speak_output = "mqtt test exitoso, se actualizo el valor!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
        #final
#-------------------------------------------------------------------------------------------------------------------------------------------------#

class RdTopicIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.mqtt_client = mqtt.Client(client_id="my_client_dede")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.connect("test.mosquitto.org", 1883)
        self.mqtt_client.subscribe("test/prueba")
        self.mqtt_client.loop_start()
        self.msg_topico = None
    
    def on_connect(self, client, userdata, flags, rc):
        print("Conexión establecida con éxito al broker MQTT")

    def on_message(self, client, userdata, message):
        self.msg_topico = message.payload.decode()
        print("Mensaje recibido en el tópico test/prueba: " + self.msg_topico)

    def on_disconnect(self, client, userdata, rc):
        print("Desconectado del broker MQTT")

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RdTopicIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = f"Mensaje recibido en el tópico test/prueba con el siguiente contenido: {self.msg_topico}"
        #client.disconnect() 
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Puedes decirme a que valor quieres cambiar el topico"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Tenga un buen dia!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, No entendi lo que me pediste, puedes pedirme ayuda diciendo: Alexa ayuda"
        reprompt = "No he entendido lo que me has dicho, en que te puedo ayudar?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Haz activado la funcion de cambiar el valor del topico" + ChTopicIntent + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Lo siento, he tenido problemas para hacer lo que me pides. Por favor, inténtelo de nuevo."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ChTopicIntentHandler())
sb.add_request_handler(RdTopicIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()