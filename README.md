# lattice-serve

The serving layer of the Lattice fraud platform that wraps a trained model behind low-latency API. 

Live Demo: lattice-serve.onrender.com
Health: lattice-serve.onrender.com/health
# Architecture
![Lattice Serve Architecture](images/lattice-serve.png)

# Quickstart 


# API

# Design Notes

Serving is decoupled from the model. The service is built and tested against a deterministic stub ratherthan a real fraud model so that the serving infrastructure can be  developed and proven independently of any specific model. The real Graph and Baseline models drop in later by swapping the `load_model()` call, with no changes to the serving layer. 

Service owns shape, model owns meaning. The service validates only that a request is structurally well-formed and rejects malformed calls with a 422 code. Whether the input is actually valid for given model is the model's responsibility, whithc keeps the serving layer model-agnostic and unchanged when models are swapped. 

Health reports readiness, not just reachability. `/health` returns whether the model is actually loaded and ready to serve, not merely that the API responds. This lets orchestration tools route or restart based on real readiness, and surfaces the running model version at the same time. 

Observability: aggregate metrics + per-event logs. The service exposes Prometheus metrics following the RED method (Rate, Errors, and Duration). Because these 3 answer the question "is the service healthy right now". Duration is tracked as histogram rather than average, since an average hides tail latency (e.g. one 5 second request disappears among ninenty-nine fast ones), whereas percentiles like p95/p99 surface the slow cases taht actually hurt users. Metrics cover the aggregate picture; structured JSON logs complement them by capturing individual events for debugging a specific request.

Logs capture shape. Per-prediction logs record the feature count, not raw feature values, so that potentiall sensitive input never lands in logs. 

Tests assert properties: The `/predic` test checks that the score falls in [0,1] range rather than asserting an exact number. Testing the invariant keeps the suite passing when the real model replaces the stub. 
