# API for a Language Model Service

This repository provides a simple text summarization REST API service using the t5-small model and Transformers library to handle summarization.

## Setup

The code is intended to be deployed as a Docker container and can be built and run locally using the following commands:

```shell
$ docker build . -t lms
$ docker run -it --rm -p 8000:8000 lms
```

Once the container starts, documentation, including a simple interface to execute the API, can be found at http://localhost:8000/docs.

## Usage

The documentation provides details on how to use the service. 

It can be invoked from the command line

```shell
$ curl -X 'POST' \
  'http://localhost:9000/api/v1/summarize' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "A vector database is a tool most commonly used for storing text data in a way that enables querying based on similarity or semantic meaning. This technology is used to decrease hallucinations (where the AI model makes something up) by referencing data the model isn’t trained on, significantly improving the accuracy and quality of the LLM’s response. Use cases for vector databases also include reading documents, recommending similar products, or remembering past conversations.",
  "max_length": 250,
  "min_length": 30
}'
```

which will produce the following output:

```json
{
    "summary":"A vector database is a tool most commonly used for storing text data in a way that enables querying based on similarity or semantic meaning. This technology is used to decrease hallucinations (where the AI model makes something up) by referencing data the model isn’t trained on.",
    "original_length":480,
    "summary_length":280
}
```

## Deployment

The API service is stateless, so it can be scaled simply by adding more instances.

It is intended to be deployed in a cloud environment that can provide autoscaling of container workloads in response to demand, such as AWS ECS or Managed Kubernetes.

According to the principles of good design and the separation of concerns, the API service does not handle authentication, authorization, or rate limiting.

These essential functions must be provided elsewhere in the stack, for instance by an API Gateway service.

## Design

The service is implemented using Python and the FastAPI framework.

The model is preloaded on startup rather than when the first API call is received to ensure a predictable response time.

Once a model is loaded, it is cached to avoid the overhead of reloading it on subsequent calls.

## Environment Variables

| Name         | Default Value            | Description     |
|--------------|------------------|-------------------|
| MODEL_NAME | t5-small | The name of a model that can be loaded by the Transformers library |
| MAX_CACHED_INSTANCES | 1 | The number of cached model instances |


## Security

In accordance with best practices, the Docker container is built using a 2-stage process, with only essential files copied to the final image to reduce the attack surface. The Docker process also runs as a non-root user.

However, the service downloads model images on startup over the public Internet. These images could be compromised. The service should be updated to read model images from a controlled source.

## Reflection

I considered adding a streaming API to make it more responsive, but this would not have improved overall performance.

The current simple cache approach does not allow for new models to be added. A better approach would be to store the model in a local object store, with the location available through a configuration API that is periodically checked. When changes are detected, existing model instances are discarded (allowing those currently processing user requests to complete) and replaced with new versions instantiated with the new model files.
