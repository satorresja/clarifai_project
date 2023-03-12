#pip install clarifai-grpc
import os
YOUR_CLARIFAI_API_KEY = os.environ.get("YOUR_CLARIFAI_API_KEY")
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

YOUR_APPLICATION_ID = "my-first-application"
SAMPLE_URL = "https://www.zooplus.es/magazine/wp-content/uploads/2019/07/border-collie-.jpeg"

# This is how you authenticate.
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)

request = service_pb2.PostModelOutputsRequest(
    # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
    model_id="general-image-recognition", #"general-image-recognition",
    user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
    inputs=[
        resources_pb2.Input(
            data=resources_pb2.Data(image=resources_pb2.Image(url=SAMPLE_URL))
        )
    ],
)
response = stub.PostModelOutputs(request, metadata=metadata)
if response.status.code != status_code_pb2.SUCCESS:
    print(response)
    raise Exception(f"Request failed, status code: {response.status}")

concept_name = []
concept_value = []
for concept in response.outputs[0].data.concepts:
    #print("%12s: %.2f" % (concept.name, concept.value))
    concept_name.append(concept.name)
    concept_value.append(concept.value)

lista_formateada = [list(x) for x in zip(concept_name, concept_value)]
print(lista_formateada)