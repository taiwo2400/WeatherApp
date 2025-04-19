import structlog


# Configure structlog for JSON logging
def configure_structlog():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(10),  # INFO level
    )


# Create a reusable logger
def get_logger():
    return structlog.get_logger()
